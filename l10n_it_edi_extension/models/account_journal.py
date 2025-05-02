# Copyright 2025 Simone Rubino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from lxml import etree

from odoo import api, models

from odoo.addons.l10n_it_edi.tools.remove_signature import remove_signature

_logger = logging.getLogger(__name__)


class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.model
    def _l10n_it_edi_extension_e_invoice_parser(self):
        """Parser used to parse an e-invoice attachment."""
        # Expose the parser used by `l10n_it_edi`.
        return etree.XMLParser(
            recover=True,
            resolve_entities=False,
        )

    @api.model
    def _l10n_it_edi_extension_parse_e_invoice_content(self, content):
        """Parse the `content` of an e-invoice to a XML tree.

        Return None if the parsing fails.
        """
        parser = self._l10n_it_edi_extension_e_invoice_parser()
        try:
            parsed_xml = etree.fromstring(content, parser)
        except (etree.ParseError, ValueError):
            parsed_xml = None
        return parsed_xml

    @api.model
    def _l10n_it_edi_extension_parse_e_invoice(self, attachment):
        """Parse the e-invoice `attachment` to a XML tree, decoding it if needed."""
        parse_content = self._l10n_it_edi_extension_parse_e_invoice_content
        if (xml_tree := parse_content(attachment.raw)) is None:
            xml_tree = parse_content(remove_signature(attachment.raw))
        return xml_tree

    @api.model
    def _l10n_it_edi_extension_split_content(self, attachment):
        """
        Break down the content of `attachment`
        if contains multiple FatturaElettronicaBody.

        If `attachment` is an e-invoice that contains N FatturaElettronicaBody:

        <FatturaElettronica>
            <FatturaElettronicaHeader/>
            <FatturaElettronicaBody>
                // Content of 1st invoice
            </FatturaElettronicaBody>
            // ...
            <FatturaElettronicaBody>
                // Content of N-th invoice
            </FatturaElettronicaBody>
        </FatturaElettronica>

        return a list of N strings (bytes) with the same FatturaElettronicaHeader:

        <FatturaElettronica>
            <FatturaElettronicaHeader/>
            <FatturaElettronicaBody>
                // Content of N-th invoice
            </FatturaElettronicaBody>
        </FatturaElettronica>
        """
        attachment.ensure_one()

        if (
            xml_tree := self._l10n_it_edi_extension_parse_e_invoice(attachment)
        ) is not None:
            header = xml_tree.xpath("//FatturaElettronicaHeader")[0]
            bodies = xml_tree.xpath("//FatturaElettronicaBody")
            result = []
            for body in bodies:
                e_invoice_root = etree.Element("FatturaElettronica")
                e_invoice_root.insert(0, header)
                e_invoice_root.insert(1, body)
                result.append(etree.tostring(e_invoice_root))
        else:
            result = [attachment.raw]
        return result

    def _l10n_it_edi_extension_split_attachments(self, attachment_ids):
        """
        Split the attachments that contain multiple invoices
        in multiple attachments containing one invoice each.

        Do not touch the attachments that do not need splitting.

        Return the IDs of the splitted attachments and of the unaffected ones.
        """
        attachment_model = self.env["ir.attachment"]
        attachments = attachment_model.browse(attachment_ids)
        l10n_it_edi_format = next(
            filter(
                lambda fmt: fmt["format"] == "l10n_it_edi",
                attachment_model._get_edi_supported_formats(),
            )
        )
        l10n_it_edi_check, l10n_it_edi_decoder = (
            l10n_it_edi_format["check"],
            l10n_it_edi_format["decoder"],
        )

        e_invoice_attachments = attachment_model.browse()
        splitted_attachments_values = dict()
        other_attachments = attachment_model.browse()
        for attachment in attachments:
            if l10n_it_edi_check(attachment):
                parsed_xml_bodies = l10n_it_edi_decoder(attachment.name, attachment.raw)
                if len(parsed_xml_bodies) >= 2:
                    # In this e-invoice there are multiple invoices,
                    # extract the content of the splitted e-invoice
                    # containing only one FatturaElettronicaBody each
                    splitted_attachments_values[attachment] = {
                        "original_attachment": attachment,
                        "contents": self._l10n_it_edi_extension_split_content(
                            attachment
                        ),
                    }
                else:
                    e_invoice_attachments |= attachment
            else:
                other_attachments |= attachment

        if splitted_attachments_values:
            e_invoice_attachments |= attachment_model.create(
                [
                    {
                        "name": f"Partial {attachment.name}",
                        "raw": content,
                    }
                    for attachment, att_data in splitted_attachments_values.items()
                    for content in att_data["contents"]
                ]
            )

        return (e_invoice_attachments | other_attachments).ids

    def _create_document_from_attachment(self, attachment_ids):
        attachment_ids = self._l10n_it_edi_extension_split_attachments(attachment_ids)
        return super()._create_document_from_attachment(attachment_ids)
