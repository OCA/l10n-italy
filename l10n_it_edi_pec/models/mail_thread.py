# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, models
from odoo.exceptions import UserError

from odoo.addons.l10n_it_edi_sdi.models.mail_thread import (
    FATTURAPA_IN_REGEX,
    METADATI_REGEX,
    RESPONSE_MAIL_REGEX,
)

_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.model
    def message_route(
        self, message, message_dict, model=None, thread_id=None, custom_values=None
    ):
        # Check if the email comes from the SDI PEC system
        if any(
            "@pec.fatturapa.it" in x
            for x in [
                message.get("Reply-To", ""),
                message.get("From", ""),
                message.get("Return-Path", ""),
            ]
        ):
            _logger.info(
                "Processing FatturaPA PEC with Message-Id: %s",
                message.get("Message-Id"),
            )
            attachments = message_dict.get("attachments", [])
            fatturapa_attachments = [
                x for x in attachments if FATTURAPA_IN_REGEX.match(x.fname)
            ]
            response_attachments = [
                x for x in attachments if RESPONSE_MAIL_REGEX.match(x.fname)
            ]
            metadati_attachments = [
                x for x in attachments if METADATI_REGEX.match(x.fname)
            ]
            company = self._l10n_it_edi_pec_get_company()
            # SDI delivers incoming invoices with both the invoice XML
            # and a Metadati (MT) file; require both to confirm this is
            # genuinely an incoming invoice delivery.
            if metadati_attachments and fatturapa_attachments:
                return self._l10n_it_edi_sdi_process_incoming_invoices(
                    message, fatturapa_attachments, company
                )
            if response_attachments:
                return self._l10n_it_edi_sdi_process_notifications(
                    message, response_attachments, company
                )
            _logger.warning(
                "SDI PEC email with no matching attachments: %s",
                message_dict.get("subject"),
            )
            return []

        # Check if this is a PEC delivery receipt (CONSEGNA/ACCETTAZIONE)
        # from a PEC server that is configured for e-invoicing
        fetchmail_server_id = self._context.get("default_fetchmail_server_id")
        if fetchmail_server_id:
            fetchmail_server = self.env["fetchmail.server"].browse(fetchmail_server_id)
            if fetchmail_server.is_l10n_it_edi_pec:
                move = self._l10n_it_edi_pec_find_move_by_subject(
                    message_dict.get("subject", "")
                )
                if move:
                    return self._l10n_it_edi_pec_process_delivery_receipt(
                        move, message_dict
                    )
                raise UserError(
                    _(
                        'PEC message "%(subject)s" has been read '
                        "but not processed, as not related to an "
                        "e-invoice.\n"
                        "Please check PEC mailbox %(fetchmail_name)s, "
                        "at server %(fetchmail_server)s, "
                        "with user %(fetchmail_user)s.",
                        subject=message_dict.get("subject"),
                        fetchmail_name=fetchmail_server.name,
                        fetchmail_server=fetchmail_server.server,
                        fetchmail_user=fetchmail_server.user,
                    )
                )

        return super().message_route(
            message,
            message_dict,
            model=model,
            thread_id=thread_id,
            custom_values=custom_values,
        )

    @api.model
    def _l10n_it_edi_pec_process_delivery_receipt(self, move, message_dict):
        """Process a PEC delivery/acceptance receipt (CONSEGNA/ACCETTAZIONE).

        These are from the PEC provider confirming email delivery,
        not from SdI. They are informational only (no state change).
        """
        move.with_context(no_new_invoice=True).sudo().message_post(
            body=message_dict.get("body", ""),
            subject=message_dict.get("subject", ""),
        )
        return []

    @api.model
    def _l10n_it_edi_pec_find_move_by_subject(self, subject):
        """Find a move from a PEC delivery receipt subject.

        PEC delivery receipts have subjects like:
        - "CONSEGNA: IT01234567890_12345.xml"
        - "ACCETTAZIONE: IT01234567890_12345.xml"
        """
        company = self._l10n_it_edi_pec_get_company()
        for prefix in ("CONSEGNA: ", "ACCETTAZIONE: "):
            if prefix in subject:
                filename = subject.split(prefix, 1)[1].strip()
                move = self._l10n_it_edi_sdi_find_move_by_attachment_name(
                    filename, company
                )
                if move:
                    return move
        return self.env["account.move"]

    @api.model
    def _l10n_it_edi_pec_get_company(self):
        """Get the company associated with the current PEC fetchmail server."""
        fetchmail_server_id = self._context.get("default_fetchmail_server_id")
        if fetchmail_server_id:
            companies = self.env["res.company"].search(
                [
                    ("l10n_it_edi_pec_fetch_server_id", "=", fetchmail_server_id),
                ],
                limit=1,
            )
            if companies:
                return companies
        return self.env.company
