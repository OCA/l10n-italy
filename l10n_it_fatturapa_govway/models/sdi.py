import base64
from urllib.parse import urljoin

import requests

from odoo import _, fields, models
from odoo.exceptions import UserError


class SdiChannel(models.Model):
    _inherit = "sdi.channel"

    channel_type = fields.Selection(
        selection_add=[("govway", "GovWay")], ondelete={"govway": "cascade"}
    )
    govway_url = fields.Char(
        string="GovWay URL",
    )
    govway_user = fields.Char(string="GovWay User")
    govway_password = fields.Char(string="GovWay Password")

    # @api.constrains("fetch_pec_server_id")
    # def check_fetch_pec_server_id(self):
    #     pec_channels = self.filtered(lambda c: c.channel_type == "pec")
    #     for channel in pec_channels:
    #         domain = [
    #             ("fetch_pec_server_id", "=", channel.fetch_pec_server_id.id),
    #             ("id", "in", pec_channels.ids),
    #         ]
    #         elements = self.search(domain)
    #         if len(elements) > 1:
    #             raise exceptions.ValidationError(
    #                 _("The channel %s with pec server %s already exists")
    #                 % (channel.name, channel.fetch_pec_server_id.name)
    #             )
    #
    # @api.constrains("pec_server_id")
    # def check_pec_server_id(self):
    #     pec_channels = self.filtered(lambda c: c.channel_type == "pec")
    #     for channel in pec_channels:
    #         domain = [
    #             ("pec_server_id", "=", channel.pec_server_id.id),
    #             ("id", "in", pec_channels.ids),
    #         ]
    #         elements = self.search(domain)
    #         if len(elements) > 1:
    #             raise exceptions.ValidationError(
    #                 _("The channel %s with pec server %s already exists")
    #                 % (channel.name, channel.pec_server_id.name)
    #             )
    #
    # @api.constrains("email_exchange_system")
    # def check_email_validity(self):
    #     if self.env.context.get("skip_check_email_validity"):
    #         return
    #     pec_channels = self.filtered(lambda c: c.channel_type == "pec")
    #     for channel in pec_channels:
    #         if not extract_rfc2822_addresses(channel.email_exchange_system):
    #             raise exceptions.ValidationError(
    #                 _("Email %s is not valid") % channel.email_exchange_system
    #             )
    #
    # def check_first_pec_sending(self):
    #     if not self.first_invoice_sent:
    #         sdi_address = self.env["ir.config_parameter"].get_param(
    #             "sdi.pec.first.address",
    #         )
    #         self.email_exchange_system = sdi_address
    #     else:
    #         if not self.email_exchange_system:
    #             raise exceptions.UserError(
    #                 _(
    #                     "SDI PEC address not set. Please update it with the "
    #                     "address indicated by SDI after the first sending"
    #                 )
    #             )
    #
    # def update_after_first_pec_sending(self):
    #     if not self.first_invoice_sent:
    #         self.first_invoice_sent = True
    #         self.with_context(
    #             skip_check_email_validity=True
    #         ).email_exchange_system = False

    def send_via_govway(self, attachment_out_ids):
        if not self.govway_url:
            raise UserError(_("Missing GovWay URL"))
        for att in attachment_out_ids:
            if not att.datas or not att.name:
                raise UserError(_("File content and file name are mandatory"))
            company = att.company_id
            vat = company.vat.split("IT")[1]
            url = (
                "govway/sdi/out/xml2soap/Pretecno"
                "/CentroServiziFatturaPA/SdIRiceviFile/v1"
            )
            url = urljoin(self.govway_url, url)
            params = {
                "Versione": "FPR12",  # VersioneFatturaPA
                "TipoFile": "XML",  # P7M: application/pkcs7-mime
                "IdPaese": "IT",
                "IdCodice": vat,
            }
            try:
                response = requests.post(
                    url=url,
                    data=base64.b64decode(att.datas),
                    params=params,
                    timeout=60,
                    auth=(self.govway_user, self.govway_password),
                    headers={"Content-Type": "application/octet-stream"},
                )
                if not response.ok:
                    # response_data = json.loads(response.text)
                    # status = response_data.get("status")
                    # if status and status.get("error_code", False):
                    raise Exception(
                        _(
                            "Failed to fetch from CoinMarketCap with error code: "
                            "%s and error message: %s"
                        )
                        % (response.status_code, response.text)
                    )
            except Exception as e:
                raise UserError(
                    _("GovWay server not available for %s. Please configure it.")
                    % str(e)
                )
            return {"result": "ok"}  # response_data.get("data", {})
          mail_message = self.env["mail.message"].create(
                {
                    "model": att._name,
                    "res_id": att.id,
                    "subject": att.name,
                    "body": "XML file for FatturaPA {} sent to Exchange System to "
                    "the email address {}.".format(
                        att.name, company.email_exchange_system
                    ),
                    "attachment_ids": [(6, 0, att.ir_attachment_id.ids)],
                    "email_from": company.email_from_for_fatturaPA,
                    "reply_to": company.email_from_for_fatturaPA,
                    "mail_server_id": company.sdi_channel_id.pec_server_id.id,
                }
            )

            mail = self.env["mail.mail"].create(
                {
                    "mail_message_id": mail_message.id,
                    "body_html": mail_message.body,
                    "email_to": company.email_exchange_system,
                    "headers": {"Return-Path": company.email_from_for_fatturaPA},
                }
            )

            if mail:
                try:
                    mail.send(raise_exception=True)
                    att.state = "sent"
                    att.sending_date = fields.Datetime.now()
                    att.sending_user = user.id
                    company.sdi_channel_id.update_after_first_pec_sending()
                except MailDeliveryException as e:
                    att.state = "sender_error"
                    mail.body = str(e)
