# Copyright 2018 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import re

from lxml import etree

from odoo import api, fields, models
from odoo.fields import first

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

    @api.model
    def _search_attachment_out_by_notification(
        self,
        response_name,
        response_content,
    ):
        """Search Electronic Invoice referenced by this notification"""
        attachment_model = self.env["fatturapa.attachment.out"]
        attachment = attachment_model.browse()

        root = etree.fromstring(response_content)
        file_name = root.find("NomeFile")

        if file_name is not None:
            file_name = file_name.text
            unsigned_file_name = file_name.replace(".p7m", "")
            attachment = attachment_model.search(
                [
                    "|",
                    ("name", "=", file_name),
                    ("name", "=", unsigned_file_name),
                ]
            )
            if len(attachment) > 1:
                _logger.info("More than 1 out invoice found for incoming" "message")
                attachment = first(attachment)
        return attachment

    def _process_single_notification(
        self,
        attachment,
        notification_type,
        parsed_notification,
    ):
        """
        Update `attachment` based on the content of the notification.
        """
        id_sdi = parsed_notification.find("IdentificativoSdI")
        receipt_dt = parsed_notification.find("DataOraRicezione")
        message_id = parsed_notification.find("MessageId")

        id_sdi = id_sdi.text if id_sdi is not None else False
        receipt_dt = receipt_dt.text if receipt_dt is not None else False
        message_id = message_id.text if message_id is not None else False

        # 2A. Notifica di Scarto
        if notification_type == "NS":
            error_list = parsed_notification.find("ListaErrori")
            error_str = ""
            for error in error_list:
                error_str += "\n[%s] %s %s" % (
                    error.find("Codice").text
                    if error.find("Codice") is not None
                    else "",
                    error.find("Descrizione").text
                    if error.find("Descrizione") is not None
                    else "",
                    error.find("Suggerimento").text
                    if error.find("Suggerimento") is not None
                    else "",
                )
            return attachment.write(
                {
                    "state": "sender_error",
                    "last_sdi_response": "SdI ID: {}; "
                    "Message ID: {};"
                    "Receipt date: {}; "
                    "Error: {}".format(
                        id_sdi,
                        message_id,
                        receipt_dt,
                        error_str,
                    ),
                }
            )

        # 3A. Mancata consegna
        if notification_type == "MC":
            missed_delivery_note = parsed_notification.find("Descrizione").text
            return attachment.write(
                {
                    "state": "recipient_error",
                    "last_sdi_response": "SdI ID: {}; "
                    "Message ID: {}; Receipt date: {}; "
                    "Missed delivery note: {}".format(
                        id_sdi,
                        message_id,
                        receipt_dt,
                        missed_delivery_note,
                    ),
                }
            )

        # 3B. Ricevuta di Consegna
        if notification_type == "RC":
            delivery_dt = parsed_notification.find("DataOraConsegna").text
            return attachment.write(
                {
                    "state": "validated",
                    "delivered_date": fields.Datetime.now(),
                    "last_sdi_response": "SdI ID: {}; "
                    "Message ID: {}; "
                    "Receipt date: {}; "
                    "Delivery date: {}".format(
                        id_sdi,
                        message_id,
                        receipt_dt,
                        delivery_dt,
                    ),
                }
            )

        # 4A. Notifica Esito per PA
        if notification_type == "NE":
            esito_committente = parsed_notification.find("EsitoCommittente")
            if esito_committente is not None:
                # more than one esito?
                esito = esito_committente.find("Esito")
                if esito is not None:
                    if esito.text == "EC01":
                        state = "accepted"
                    elif esito.text == "EC02":
                        state = "rejected"
                    return attachment.write(
                        {
                            "state": state,
                            "last_sdi_response": "SdI ID: {}; "
                            "Message ID: {}; "
                            "Response: {}".format(
                                id_sdi,
                                message_id,
                                esito.text,
                            ),
                        }
                    )

        # 5. Decorrenza Termini per PA
        if notification_type == "DT":
            description = parsed_notification.find("Descrizione")
            if description is not None:
                return attachment.write(
                    {
                        "state": "validated",
                        "last_sdi_response": "SdI ID: {}; "
                        "Message ID: {}; "
                        "Receipt date: {}; "
                        "Description: {}".format(
                            id_sdi,
                            message_id,
                            receipt_dt,
                            description.text,
                        ),
                    }
                )

        # 6. Avvenuta Trasmissione per PA
        if notification_type == "AT":
            description = parsed_notification.find("Descrizione")
            if description is not None:
                return attachment.write(
                    {
                        "state": "accepted",
                        "last_sdi_response": "SdI ID: {}; "
                        "Message ID: {}; "
                        "Receipt date: {}; "
                        "Description: {}".format(
                            id_sdi,
                            message_id,
                            receipt_dt,
                            description.text,
                        ),
                    }
                )
        # Notification has not been managed
        return False

    @api.model
    def receive_notification(
        self,
        response_name_content_dict,
    ):
        """
        Find and update the Electronic Invoices referenced by SdI notifications.

        Note that updating the Electronic Invoices
        does not depend on the channel record.

        :param response_name_content_dict: Dictionary mapping
            file names to their content (bytes)
            for each SdI notification.
        :return: the updated Electronic Invoices (`fatturapa.attachment.out`).
        """
        attachments = self.env["fatturapa.attachment.out"].browse()
        for response_name, response_content in response_name_content_dict.items():
            if response_name.lower().endswith(".zip"):
                # not implemented, case of AT, todo
                continue

            message_type = response_name.split("_")[2]
            root = etree.fromstring(response_content)
            file_name = root.find("NomeFile")

            attachment = self._search_attachment_out_by_notification(
                response_name,
                response_content,
            )
            if not attachment:
                # Metadati
                if message_type == "MT":
                    # out invoice not found, so it is an incoming invoice
                    continue
                else:
                    _logger.info(
                        "Error: FatturaPA {} not found.".format(
                            file_name,
                        )
                    )
                    # TODO Send a mail warning
                    continue
            else:
                self._process_single_notification(
                    attachment,
                    message_type,
                    root,
                )
                attachments |= attachment
        return attachments

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
