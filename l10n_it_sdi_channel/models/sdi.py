# Copyright 2018 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import io
import logging
import re
import zipfile

from odoo import api, fields, models

FATTURAPA_IN_REGEX = (
    "^(IT[a-zA-Z0-9]{11,16}|"
    "(?!IT)[A-Z]{2}[a-zA-Z0-9]{2,28})"
    "_[a-zA-Z0-9]{1,5}"
    "\\.(xml|XML|Xml|zip|ZIP|Zip|p7m|P7M|P7m)"
    "(\\.(p7m|P7M|P7m))?$"
)

fatturapa_regex = re.compile(FATTURAPA_IN_REGEX)

_logger = logging.getLogger(__name__)


class SdiChannel(models.Model):
    _name = "sdi.channel"
    _description = "ES channel"

    name = fields.Char(required=True, translate=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    channel_type = fields.Selection(
        string="ES channel type",
        selection=[],
        required=True,
        help="Channels (Pec, Web, Sftp) could be provided by external modules.",
    )

    def send(self, attachment_out_ids):
        """
        Send `attachment_out_ids` to SdI.

        Each channel will define a method send_via_<channel_type>.

        The method will receive a recordset of
        Electronic Invoice (`fatturapa.attachment.out`)
        that have to be sent to SdI.

        The method will take care of updating the state
        of each Electronic Invoice that has managed to send.
        """
        self.ensure_one()
        channel_type = self.channel_type
        send_method_name = "send_via_" + channel_type
        send_method = getattr(self, send_method_name)
        return send_method(attachment_out_ids)

    @api.model
    def _prepare_attachment_in_values(
        self,
        file_name,
        file_content,
        **default_values,
    ):
        """
        Get values to create an Electronic Bill (`fatturapa.attachment.in`).

        If this bill is already contained in other Electronic Bills,
        no values are returned.
        """
        attachment_model = self.env["fatturapa.attachment.in"]

        # If a company is specified, attachments are searched
        # using the e-invoice user configured in that company.
        company_id = default_values.get("company_id")
        if company_id:
            company = self.env["res.company"].browse(company_id)
            e_invoice_user = company.e_invoice_user_id
            if e_invoice_user:
                attachment_model = attachment_model.sudo(e_invoice_user.id)
        existing_attachments = attachment_model.search(
            [
                ("name", "=", file_name),
            ]
        )
        if existing_attachments:
            _logger.info(
                "Electronic bill %s already processed"
                % existing_attachments.mapped("name")
            )
            attachment_values = dict()
        else:
            attachment_values = default_values
            attachment_values.update(
                {
                    "name": file_name,
                    "datas": base64.encodebytes(file_content),
                }
            )
        return attachment_values

    @api.model
    def _process_single_fe(
        self,
        file_name,
        file_content,
        **default_values,
    ):
        """
        Extract values from SdI file to create Electronic Bill(s).

        Note that processing a single SdI file
        might produce many Electronic Bills
        when the SdI file is an archive (.zip).
        """
        attachments_values = list()
        is_archive = file_name.lower().endswith(".zip")
        if is_archive:
            # Create one Electronic Bill for each file in the archive
            with zipfile.ZipFile(io.BytesIO(file_content)) as zip_file:
                for compressed_file_name in zip_file.namelist():
                    if fatturapa_regex.match(compressed_file_name):
                        compressed_file = zip_file.open(compressed_file_name)
                        compressed_file_content = compressed_file.read()
                        attachment_values = self._prepare_attachment_in_values(
                            compressed_file_name,
                            compressed_file_content,
                            **default_values,
                        )
                        if attachment_values:
                            attachments_values.append(attachment_values)
        else:
            attachment_values = self._prepare_attachment_in_values(
                file_name,
                file_content,
                **default_values,
            )
            if attachment_values:
                attachments_values.append(attachment_values)

        return attachments_values

    @api.model
    def receive_fe(
        self,
        file_name_content_dict,
        metadata_file_name_content_dict,
        **default_values,
    ):
        """
        Save Electronic Bills received from SdI.

        Note that saving the Electronic Bills
        does not depend on the channel record;
        if any channel-specific value has to be saved in the records,
        it can be added in `default_values`.

        :param file_name_content_dict: Dictionary mapping
            file names to their base64-encoded content for each Electronic Bill.
        :param metadata_file_name_content_dict: Dictionary mapping
            file names to their base64-encoded content for each Metadata file.
        :param default_values: Default values
            for the creation of Electronic Bill.
        :return: the created Electronic Bills (`fatturapa.attachment.in`).
        """
        all_attachments_values = list()
        for file_name, file_content in file_name_content_dict.items():
            attachments_values = self._process_single_fe(
                file_name,
                file_content,
                **default_values,
            )
            if attachments_values:
                all_attachments_values.extend(attachments_values)

        attachment_model = self.env["fatturapa.attachment.in"]
        # Attachments will be created in a specific company:
        # use the configured user to create them.
        company_id = default_values.get("company_id")
        if company_id:
            company = self.env["res.company"].browse(company_id)
            e_invoice_user = company.e_invoice_user_id
            if e_invoice_user:
                attachment_model = attachment_model.sudo(e_invoice_user.id)
        return attachment_model.create(all_attachments_values)
