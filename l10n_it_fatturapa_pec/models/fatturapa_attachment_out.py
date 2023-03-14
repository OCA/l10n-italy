# Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
# Copyright 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018-2019 Lorenzo Battistini <https://github.com/eLBati>

import logging
import re

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

RESPONSE_MAIL_REGEX = (
    "[A-Z]{2}[a-zA-Z0-9]{11,16}_[a-zA-Z0-9]{,5}_[A-Z]{2}_" "[a-zA-Z0-9]{,3}"
)


class FatturaPAAttachmentOut(models.Model):
    _inherit = "fatturapa.attachment.out"

    def _message_type_ns(
        self, root, id_sdi, message_id, receipt_dt, fatturapa_attachment_out
    ):
        error_list = root.find("ListaErrori")
        error_str = ""
        for error in error_list:
            error_str += "\n[%s] %s %s" % (
                error.find("Codice").text if error.find("Codice") is not None else "",
                error.find("Descrizione").text
                if error.find("Descrizione") is not None
                else "",
                error.find("Suggerimento").text
                if error.find("Suggerimento") is not None
                else "",
            )
        fatturapa_attachment_out.write(
            {
                "state": "sender_error",
                "last_sdi_response": "SdI ID: {}; "
                "Message ID: {}; Receipt date: {}; "
                "Error: {}".format(id_sdi, message_id, receipt_dt, error_str),
            }
        )

    def _message_type_mc(
        self, root, id_sdi, message_id, receipt_dt, fatturapa_attachment_out
    ):
        missed_delivery_note = root.find("Descrizione").text
        fatturapa_attachment_out.write(
            {
                "state": "recipient_error",
                "last_sdi_response": "SdI ID: {}; "
                "Message ID: {}; Receipt date: {}; "
                "Missed delivery note: {}".format(
                    id_sdi, message_id, receipt_dt, missed_delivery_note
                ),
            }
        )

    def _message_type_rc(
        self, root, id_sdi, message_id, receipt_dt, fatturapa_attachment_out
    ):
        delivery_dt = root.find("DataOraConsegna").text
        fatturapa_attachment_out.write(
            {
                "state": "validated",
                "delivered_date": fields.Datetime.now(),
                "last_sdi_response": "SdI ID: {}; "
                "Message ID: {}; Receipt date: {}; "
                "Delivery date: {}".format(id_sdi, message_id, receipt_dt, delivery_dt),
            }
        )

    def _message_type_ne(self, root, id_sdi, message_id, fatturapa_attachment_out):
        esito_committente = root.find("EsitoCommittente")
        if esito_committente is not None:
            # more than one esito?
            esito = esito_committente.find("Esito")
            state = ""
            if esito is not None:
                if esito.text == "EC01":
                    state = "accepted"
                elif esito.text == "EC02":
                    state = "rejected"
                fatturapa_attachment_out.write(
                    {
                        "state": state,
                        "last_sdi_response": "SdI ID: {}; "
                        "Message ID: {}; Response: {}; ".format(
                            id_sdi, message_id, esito.text
                        ),
                    }
                )

    def _message_type_dt(
        self, root, id_sdi, message_id, receipt_dt, fatturapa_attachment_out
    ):
        description = root.find("Descrizione")
        if description is not None:
            fatturapa_attachment_out.write(
                {
                    "state": "validated",
                    "last_sdi_response": "SdI ID: {}; "
                    "Message ID: {}; Receipt date: {}; "
                    "Description: {}".format(
                        id_sdi, message_id, receipt_dt, description.text
                    ),
                }
            )

    def _message_type_at(
        self, root, id_sdi, message_id, receipt_dt, fatturapa_attachment_out
    ):
        description = root.find("Descrizione")
        if description is not None:
            fatturapa_attachment_out.write(
                {
                    "state": "accepted",
                    "last_sdi_response": (
                        "SdI ID: {}; Message ID: {}; Receipt date: {};"
                        " Description: {}"
                    ).format(id_sdi, message_id, receipt_dt, description.text),
                }
            )

    def parse_pec_response(self, message_dict):
        message_dict["model"] = self._name
        message_dict["res_id"] = 0

        regex = re.compile(RESPONSE_MAIL_REGEX)
        notifications = [x for x in message_dict["attachments"] if regex.match(x.fname)]

        if not notifications:
            raise UserError(
                _(
                    'PEC message "%s" is coming from SDI but attachments do not '
                    "match SDI response format. Please check."
                )
                % (message_dict["subject"])
            )

        sdi_channel_model = self.env["sdi.channel"]
        attachments = sdi_channel_model.receive_notification(
            {
                notification.fname: notification.content
                for notification in notifications
            },
        )

        # Link the message to the last attachment updated
        message_dict["res_id"] = attachments[-1].id
        return message_dict
