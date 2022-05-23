# Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
# Copyright 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018-2019 Lorenzo Battistini <https://github.com/eLBati>

import logging
import re

from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.base.models.ir_mail_server import MailDeliveryException

_logger = logging.getLogger(__name__)

RESPONSE_MAIL_REGEX = (
    "[A-Z]{2}[a-zA-Z0-9]{11,16}_[a-zA-Z0-9]{,5}_[A-Z]{2}_" "[a-zA-Z0-9]{,3}"
)


class FatturaPAAttachmentOut(models.Model):
    _inherit = "fatturapa.attachment.out"

    last_sdi_response = fields.Text(
        string="Last Response from Exchange System",
        default="No response yet",
        readonly=True,
    )
    sending_user = fields.Many2one("res.users", readonly=True)

    @api.model
    def _check_fetchmail(self):
        server = self.env["fetchmail.server"].search(
            [("is_fatturapa_pec", "=", True), ("state", "=", "done")]
        )
        if not server:
            raise UserError(_("No incoming PEC server found. Please configure it."))

    def send_via_pec(self):
        self._check_fetchmail()
        self.env.company.sdi_channel_id.check_first_pec_sending()
        states = self.mapped("state")
        if set(states) != {"ready"}:
            raise UserError(_("You can only send files in 'Ready to Send' state."))
        for att in self:
            if not att.datas or not att.name:
                raise UserError(_("File content and file name are mandatory"))
            mail_message = self.env["mail.message"].create(
                {
                    "model": self._name,
                    "res_id": att.id,
                    "subject": att.name,
                    "body": "XML file for FatturaPA {} sent to Exchange System to "
                    "the email address {}.".format(
                        att.name, self.env.company.email_exchange_system
                    ),
                    "attachment_ids": [(6, 0, att.ir_attachment_id.ids)],
                    "email_from": self.env.company.email_from_for_fatturaPA,
                    "reply_to": self.env.company.email_from_for_fatturaPA,
                    "mail_server_id": self.env.company.sdi_channel_id.pec_server_id.id,
                }
            )

            mail = self.env["mail.mail"].create(
                {
                    "mail_message_id": mail_message.id,
                    "body_html": mail_message.body,
                    "email_to": self.env.company.email_exchange_system,
                    "headers": {
                        "Return-Path": self.env.company.email_from_for_fatturaPA
                    },
                }
            )

            if mail:
                try:
                    mail.send(raise_exception=True)
                    att.state = "sent"
                    att.sending_date = fields.Datetime.now()
                    att.sending_user = self.env.user.id
                    self.env.company.sdi_channel_id.update_after_first_pec_sending()
                except MailDeliveryException as e:
                    att.state = "sender_error"
                    mail.body = str(e)

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
