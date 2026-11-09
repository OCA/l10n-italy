# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2025 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import logging

from markupsafe import Markup

from odoo import _, fields, models
from odoo.exceptions import UserError

from odoo.addons.account_edi_proxy_client.models.account_edi_proxy_user import (
    AccountEdiProxyError,
)

_logger = logging.getLogger(__name__)

# Prefix of the e-invoice files kept as history by a reset of the sending
HISTORY_PREFIX = "old_"


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
                msg = self.env["ir.mail_server"].build_email(
                    email_from=email_from,
                    email_to=sdi_email,
                    subject=filename,
                    body="",
                    reply_to=email_from,
                    attachments=[(filename, xml_bytes, "application/xml")],
                    headers={"Return-Path": email_from},
                )
                self.env["ir.mail_server"].send_email(msg, mail_server_id=pec_server.id)
                results[filename] = {
                    "id_transaction": f"pec_{self.id}_{filename}",
                }
            except Exception as e:
                raise AccountEdiProxyError("PEC", message=str(e)) from e
        return results

    def _l10n_it_edi_update_send_state(self):
        """Skip proxy polling for PEC moves.

        PEC notifications arrive asynchronously via email and are
        processed by the fetchmail cron through mail_thread.message_route.
        """
        non_pec = self.filtered(lambda m: not m.company_id.l10n_it_edi_use_pec)
        if non_pec:
            return super(AccountMove, non_pec)._l10n_it_edi_update_send_state()

    def action_check_l10n_it_edi(self):
        """Override to trigger PEC fetch instead of proxy poll."""
        self.ensure_one()
        if not self.company_id.l10n_it_edi_use_pec:
            return super().action_check_l10n_it_edi()
        fetch_server = self.company_id.l10n_it_edi_pec_fetch_server_id
        if fetch_server and fetch_server.state == "done":
            fetch_server.fetch_mail()

    def action_l10n_it_edi_pec_reset(self):
        """Allow sending again an e-invoice sent via PEC that got no answer.

        A move sent via PEC stays in "processing" until an SDI notification
        is processed, and core neither exports it again nor shows "Reset to
        draft". When the notification never arrives (for instance the file
        name was wrong), this resets the sending.

        The e-invoice XML and the PDF are not deleted: they are renamed
        old_<timestamp>_<name>, detached from their fields and attached to
        a chatter message, so that the next sending builds new ones.
        A late SDI notification about the old file still finds the move.
        """
        for move in self:
            if not (
                move.state == "posted"
                and move.company_id.l10n_it_edi_use_pec
                and move.l10n_it_edi_state == "processing"
            ):
                raise UserError(
                    _(
                        "%(move)s is not a posted move sent via PEC "
                        "and waiting for an SDI answer.",
                        move=move.display_name,
                    )
                )
            stamp = fields.Datetime.context_timestamp(
                move, fields.Datetime.now()
            ).strftime("%Y%m%d-%H%M")
            old_attachments = (
                move.l10n_it_edi_attachment_id | move.invoice_pdf_report_id
            )
            old_names = old_attachments.mapped("name")
            for attachment in old_attachments.sudo():
                attachment.write(
                    {
                        "res_field": False,
                        "name": f"{HISTORY_PREFIX}{stamp}_{attachment.name}",
                    }
                )
            old_transaction = move.l10n_it_edi_transaction
            move.write(
                {
                    "l10n_it_edi_state": False,
                    "l10n_it_edi_transaction": False,
                    "l10n_it_edi_header": False,
                }
            )
            move.invalidate_recordset(
                fnames=[
                    "l10n_it_edi_attachment_id",
                    "l10n_it_edi_attachment_file",
                    "invoice_pdf_report_id",
                    "invoice_pdf_report_file",
                ]
            )
            # no_new_invoice: do not decode the old XML into the move
            move.with_context(no_new_invoice=True).message_post(
                body=Markup("<p>%s</p>")
                % _(
                    "SDI sending reset (transaction %(transaction)s): "
                    "%(files)s kept here as history.",
                    transaction=old_transaction or "-",
                    files=", ".join(old_names) or "-",
                ),
                attachment_ids=old_attachments.ids,
            )
        return True
