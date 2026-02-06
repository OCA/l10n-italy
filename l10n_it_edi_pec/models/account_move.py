# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2025 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import logging
from email.message import EmailMessage

from odoo import models

from odoo.addons.account_edi_proxy_client.models.account_edi_proxy_user import (
    AccountEdiProxyError,
)

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    def _l10n_it_edi_upload(self, files):
        """Override to send files via PEC instead of IAP proxy.

        :param files: A list of dict {filename, xml (base64-encoded string),
                      destination_code}.
        :returns: A dict mapping each input filename to the upload result.
        """
        self.ensure_one()
        if not self.company_id.l10n_it_edi_use_pec:
            return super()._l10n_it_edi_upload(files)

        company = self.company_id
        pec_server = company.l10n_it_edi_pec_server_id
        sdi_email = company.l10n_it_edi_pec_email_exchange_system
        email_from = pec_server.l10n_it_edi_pec_email_from

        results = {}
        for file_data in files or []:
            filename = file_data["filename"]
            xml_bytes = base64.b64decode(file_data["xml"])
            try:
                msg = EmailMessage()
                msg["Subject"] = filename
                msg["From"] = email_from
                msg["To"] = sdi_email
                msg["Reply-To"] = email_from
                msg["Return-Path"] = email_from
                msg.set_content("")
                msg.add_attachment(
                    xml_bytes,
                    maintype="application",
                    subtype="xml",
                    filename=filename,
                )
                self.env["ir.mail_server"].send_email(msg, mail_server_id=pec_server.id)
                results[filename] = {
                    "id_transaction": f"pec_{self.id}_{filename}",
                }
            except Exception as e:
                raise AccountEdiProxyError("PEC", str(e)) from e
        return results

    def _l10n_it_edi_update_send_state(self):
        """Skip proxy polling for PEC moves.

        PEC notifications arrive asynchronously via email and are
        processed by the fetchmail cron through mail_thread.message_route.
        """
        non_pec = self.filtered(lambda m: not m.company_id.l10n_it_edi_use_pec)
        if non_pec:
            return super(AccountMove, non_pec)._l10n_it_edi_update_send_state()

    def _l10n_it_edi_transform_notification(self, parsed_notification):
        """Extend state_map to handle attestazioneTrasmissione (AT).

        AT means SdI accepted the invoice but could not deliver it to the
        recipient after repeated attempts. Maps to forward_failed.
        """
        result = super()._l10n_it_edi_transform_notification(parsed_notification)
        if parsed_notification.get("sdi_state") == "attestazioneTrasmissione":
            result["l10n_it_edi_state"] = "forward_failed"
            result["send_ack_to_edi_proxy"] = False
        return result

    def action_check_l10n_it_edi(self):
        """Override to trigger PEC fetch instead of proxy poll."""
        self.ensure_one()
        if not self.company_id.l10n_it_edi_use_pec:
            return super().action_check_l10n_it_edi()
        fetch_server = self.company_id.l10n_it_edi_pec_fetch_server_id
        if fetch_server and fetch_server.state == "done":
            fetch_server.fetch_mail()
