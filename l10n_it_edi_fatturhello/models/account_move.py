# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo import api, fields, models

from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.addons.l10n_it_edi.models.account_move import WAITING_STATES
from odoo.addons.l10n_it_edi_sdi.models.mail_thread import NOTIFICATION_TYPE_MAP

NOTIFICATION_TYPE_MAP["FHSDI"] = "awaiting_outcome"


class AccountMove(models.Model):
    _inherit = "account.move"

    fatturhello_protocol = fields.Char(
        readonly=True,
        help="Identifier assigned during upload to Fatturhello.",
    )
    l10n_it_edi_state = fields.Selection(
        selection_add=[
            # Before the `being_sent` status
            ("sent_to_fatturhello", "Sent to Fatturhello"),
            ("being_sent",),
        ],
        ondelete={
            "sent_to_fatturhello": "set being_sent",
        },
    )
    fatturhello_last_processed_status_datetime = fields.Datetime(
        string="Last processed Fatturhello status",
        help="All the status updates more recent than this date will be processed.\n"
        "If empty, all the status updates will be processed.",
    )
    fatturhello_is_used = fields.Boolean(
        related="company_id.fatturhello_is_used",
    )

    def _fatturhello_adapt_file_name(self, file_name):
        """Fatturhello requires the file name to start with the country code (IT)."""
        company = self.env.company
        if file_name:
            country_code = company.country_id.code
            if country_code and not file_name.startswith(country_code):
                file_name = country_code + file_name
        return file_name

    def _l10n_it_edi_generate_filename(self):
        file_vat = super()._l10n_it_edi_generate_filename()
        company = self.company_id._l10n_it_get_edi_company()
        if company.fatturhello_is_used:
            file_vat = self._fatturhello_adapt_file_name(file_vat)
        return file_vat

    def _fatturhello_get_e_invoice_identifier(self):
        """How the uploaded invoice can be identified for API calls."""
        self.ensure_one()
        return self.l10n_it_edi_attachment_id.name

    def _fatturhello_check_l10n_it_edi_state(self):
        self.ensure_one()
        if self.l10n_it_edi_state == "sent_to_fatturhello":
            self._l10n_it_edi_update_send_state()

    def action_check_l10n_it_edi(self):
        if self.company_id.fatturhello_is_used:
            self._fatturhello_check_l10n_it_edi_state()
        return super().action_check_l10n_it_edi()

    @api.model
    def _fatturhello_import_e_bills_cron(self):
        """Method executed by CRON to import E-Bills."""
        connector = self.env["l10n_it_edi_fatturhello.connector"]
        # Not using sudo so that we can do only
        # whatever the CRON's user can do
        companies = self.env["res.company"].search(
            [
                ("fatturhello_is_used", "=", True),
            ]
        )
        for company in companies:
            # Login
            url = company.fatturhello_base_url
            session_token = connector.get_session_token(
                url,
                company.fatturhello_login_authtoken,
            )

            # Retrieve the identifiers of the E-Bills to be downloaded
            company_identifier = company.fatturhello_identifier
            e_bills_identifiers = connector.get_e_bills_list(
                url,
                session_token,
                company_identifier,
                last_downloaded_e_bill_identifer=company.fatturhello_last_downloaded_e_bill_identifer,
            )
            file_name_content_list = []
            if e_bills_identifiers:
                company.fatturhello_last_downloaded_e_bill_identifer = (
                    e_bills_identifiers[-1]
                )

                # Download each E-Bill's data
                file_name_content_list = list()
                for e_bill_identifier in e_bills_identifiers:
                    file_name, file_content = connector.download_file(
                        url,
                        session_token,
                        company_identifier,
                        e_bill_identifier,
                    )
                    file_name_content_list.append(
                        self.env["mail.thread"]._Attachment(file_name, file_content, {})
                    )

                # Create E-Bills
                self.env["mail.thread"]._l10n_it_edi_sdi_process_incoming_invoices(
                    dict(),
                    file_name_content_list,
                    company,
                )

    def _l10n_it_edi_download_invoices(self, proxy_user):
        # Fatturhello companies do not need a proxy user,
        # so this method shouldn't be called.
        # But if they had one, `super` would fail.
        if proxy_user.company_id.fatturhello_is_used:
            return True
        return super()._l10n_it_edi_download_invoices(proxy_user)

    def _fatturhello_get_moves_for_status_update(self):
        """Invoices in to be updated with Fatturhello data.

        Grouped by Company.
        If called on a recordset, the invoices returned are a subset of the recordset.
        """
        if self:
            companies = self.company_id.filtered("fatturhello_is_used")
        else:
            companies = self.env["res.company"].search(
                [
                    ("fatturhello_is_used", "=", True),
                ]
            )

        domain = [
            ("l10n_it_edi_state", "in", ("sent_to_fatturhello",) + WAITING_STATES),
            ("company_id", "in", companies.ids),
        ]
        if self:
            domain.append([("id", "in", self.ids)])

        invoices_data = self.env["account.move"].search_read(
            domain=domain,
            fields=[
                "id",
                "company_id",
            ],
            load=None,
        )
        invoices_by_company = dict()
        for invoice_data in invoices_data:
            company = self.env["res.company"].browse(invoice_data["company_id"])
            move = self.env["account.move"].browse(invoice_data["id"])
            if company not in invoices_by_company:
                invoices_by_company[company] = move
            else:
                invoices_by_company[company] |= move
        return invoices_by_company

    def _fatturhello_l10n_it_edi_update_send_state(self):
        """Update the status of E-Invoices in `self`, if needed.

        If `self` is an empty recordset (CRON),
        update all the invoices in the current companies.
        """
        connector = self.env["l10n_it_edi_fatturhello.connector"]
        moves_by_company_id = self._fatturhello_get_moves_for_status_update()
        for company, moves in moves_by_company_id.items():
            sdi_response_name_content_list = list()
            # Login
            url = company.fatturhello_base_url
            session_token = connector.get_session_token(
                url,
                company.fatturhello_login_authtoken,
            )

            # Download each E-Invoice's status
            move_to_statuses_dict = {
                move: connector.get_e_invoice_status_list(
                    url,
                    session_token,
                    company.fatturhello_identifier,
                    move._fatturhello_get_e_invoice_identifier(),
                )
                for move in moves
            }

            # Parse the Fatturhello status into a SdI message
            for move, statuses in move_to_statuses_dict.items():
                last_processed_status_datetime = (
                    move.fatturhello_last_processed_status_datetime
                )
                for status_index, status in enumerate(statuses):
                    status_datetime = status["Data"]
                    if (
                        not last_processed_status_datetime
                        or status_datetime > last_processed_status_datetime
                    ):
                        # Process only if more recent than the last one processed
                        name, content = connector._prepare_sdi_notification(
                            move._fatturhello_get_e_invoice_identifier(),
                            status_index,
                            status,
                        )
                        sdi_response_name_content_list.append(
                            self.env["mail.thread"]._Attachment(name, content, {})
                        )

            # Update moves
            self.env["mail.thread"]._l10n_it_edi_sdi_process_notifications(
                dict(), sdi_response_name_content_list, company=company
            )

    def _l10n_it_edi_update_send_state(self):
        fatturhello_moves = self.filtered(
            lambda move: move.company_id.fatturhello_is_used
        )
        fatturhello_moves._fatturhello_l10n_it_edi_update_send_state()

        other_moves = self - fatturhello_moves
        result = None
        if other_moves:
            result = super(AccountMove, other_moves)._l10n_it_edi_update_send_state()
        return result

    def cron_l10n_it_edi_download_and_update(self):
        self._fatturhello_import_e_bills_cron()
        self._fatturhello_l10n_it_edi_update_send_state()
        return super().cron_l10n_it_edi_download_and_update()

    def _fatturhello_l10n_it_edi_upload_single(self, file):
        """Send the e-invoices in `self` using Fatturhello."""
        self.ensure_one()
        connector = self.env["l10n_it_edi_fatturhello.connector"]
        url = self.company_id.fatturhello_base_url
        session_token = connector.get_session_token(
            url,
            self.company_id.fatturhello_login_authtoken,
        )
        company_identifier = self.company_id.fatturhello_identifier
        upload_result = connector.upload_e_invoice(
            url,
            session_token,
            company_identifier,
            self,
            file["filename"],
            file["xml"].encode(),
        )
        return {
            "message": "Sent to Fatturhello",
            "id_transaction": upload_result["protocollo"],
            "error": upload_result["error"],
        }

    def _l10n_it_edi_upload_single(self, file):
        if self.company_id.fatturhello_is_used:
            return self._fatturhello_l10n_it_edi_upload_single(file)
        return super()._l10n_it_edi_upload_single(file)

    def _fatturhello_l10n_it_edi_send(self, attachments_vals):
        # Extracted from super's `_l10n_it_edi_send`
        # because it does many proxy-related things
        # that we can't easily avoid/undo
        results = {}
        for move in self:
            attachment = attachments_vals[move]
            filename = attachment["name"]
            content = base64.b64encode(attachment["raw"]).decode()

            results[filename] = move._l10n_it_edi_upload(
                [
                    {
                        "filename": filename,
                        "xml": content,
                        "destination_code": move.commercial_partner_id.l10n_it_pa_index,
                    }
                ]
            )[filename]

            message = move.env._(
                "The e-invoice file %s was sent to Fatturhello.", filename
            )
            move.update(
                {
                    "l10n_it_edi_header": message,
                    "l10n_it_edi_state": "sent_to_fatturhello",
                }
            )

            header = nl2br(message)
            move.sudo().message_post(body=header)
        return results

    def _l10n_it_edi_send(self, attachments_vals):
        results = {}
        fatturhello_moves = self.filtered(
            lambda move: move.company_id.fatturhello_is_used
        )
        if fatturhello_moves:
            results.update(self._fatturhello_l10n_it_edi_send(attachments_vals))

        results.update(
            super(AccountMove, self - fatturhello_moves)._l10n_it_edi_send(
                attachments_vals
            )
        )
        return results

    def _fatturhello_l10n_it_edi_write_send_state(
        self, transformed_notification, message
    ):
        if receipt_datetime := transformed_notification.get("date"):
            self.fatturhello_last_processed_status_datetime = receipt_datetime

    def _l10n_it_edi_write_send_state(self, transformed_notification, message):
        result = super()._l10n_it_edi_write_send_state(
            transformed_notification, message
        )
        if self.company_id.fatturhello_is_used:
            self._fatturhello_l10n_it_edi_write_send_state(
                transformed_notification, message
            )
        return result
