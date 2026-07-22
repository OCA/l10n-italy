# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models

from ..models.connector import (
    SENT_FROM_FATTURHELLO_NOTIFICATION_TYPE,
)

LOGIN_DURATION = relativedelta(
    years=1,
)

_logger = logging.getLogger(__name__)


class SdIChannel(models.Model):
    _name = "sdi.channel"
    _inherit = [
        "sdi.channel",
        "mail.activity.mixin",
    ]

    channel_type = fields.Selection(
        selection_add=[
            ("fatturhello", "Fatturhello"),
        ],
        ondelete={
            "fatturhello": "cascade",
        },
    )
    fatturhello_base_url = fields.Char(
        name="Fatturhello base URL",
        default="https://app.b2beasy.it",
    )
    fatturhello_username = fields.Char(
        readonly=True,
        help="Username can only be set during login.",
    )
    fatturhello_login_authtoken = fields.Char(
        readonly=True,
        help="Token can only be set during login. Login again to update the token.",
    )
    fatturhello_login_authtoken_create_date = fields.Date(
        readonly=True,
    )

    def send_via_fatturhello(self, attachment_out_ids):
        """Send the e-invoices `attachment_out_ids` using Fatturhello."""
        self.ensure_one()
        connector = self.env["l10n_it_fatturapa_fatturhello.connector"]
        url = self.fatturhello_base_url
        session_token = connector.get_session_token(
            url,
            self.fatturhello_login_authtoken,
        )
        company_identifier = self.company_id.fatturhello_identifier
        for attachment in attachment_out_ids:
            connector.upload_e_invoice(
                url,
                session_token,
                company_identifier,
                attachment,
            )
        return True

    def _process_single_notification(
        self,
        attachment,
        notification_type,
        parsed_notification,
    ):
        if attachment.channel_type == "fatturhello":
            # Process the special Fatturhello notification.
            if notification_type == SENT_FROM_FATTURHELLO_NOTIFICATION_TYPE:
                result = attachment.write(
                    {
                        "state": "sent",
                    }
                )
            else:
                result = super()._process_single_notification(
                    attachment,
                    notification_type,
                    parsed_notification,
                )

            if result:
                receipt_datetime_node = parsed_notification.find("DataOraRicezione")
                receipt_datetime = fields.Datetime.from_string(
                    receipt_datetime_node.text
                )
                attachment.fatturhello_last_processed_status_datetime = receipt_datetime
        else:
            result = super()._process_single_notification(
                attachment,
                notification_type,
                parsed_notification,
            )
        return result

    def fatturhello_action_login(self):
        """Action to open the login wizard."""
        login_wizard = self.env["l10n_it_fatturapa_fatturhello.login"].with_context(
            active_id=self.id,
        )
        login_action = login_wizard.get_formview_action()
        login_action.update(
            {
                "name": "Login",
                "target": "new",
            }
        )
        return login_action

    def _fatturhello_update_credentials(self, credentials):
        """Store the credentials for authenticating API calls."""
        self.ensure_one()
        self.update(
            {
                "fatturhello_username": credentials["username"],
                "fatturhello_login_authtoken": credentials["authtoken"],
                "fatturhello_login_authtoken_create_date": fields.Date.today(),
            }
        )
        self.company_id.fatturhello_identifier = credentials["company_identifier"]
        self.activity_schedule(
            act_type_xmlid="mail.mail_activity_data_todo",
            summary=_("Renew login"),
            date_deadline=fields.Date.context_today(self) + LOGIN_DURATION,
        )
        return True

    @api.model
    def _fatturhello_import_e_bills_cron(self):
        """Method executed by CRON to import E-Bills."""
        connector = self.env["l10n_it_fatturapa_fatturhello.connector"]
        # Not using sudo so that we can do only
        # whatever the CRON's user can do
        companies = self.env.companies.filtered(
            lambda company: company.sdi_channel_type == "fatturhello"
        )
        for company in companies:
            channel = company.sdi_channel_id
            # Login
            url = channel.fatturhello_base_url
            session_token = connector.get_session_token(
                url,
                channel.fatturhello_login_authtoken,
            )

            # Retrieve the identifiers of the E-Bills to be downloaded
            company_identifier = company.fatturhello_identifier
            e_bills_identifiers = connector.get_e_bills_list(
                url,
                session_token,
                company_identifier,
                last_downloaded_e_bill_identifer=company.fatturhello_last_downloaded_e_bill_identifer,
            )
            if e_bills_identifiers:
                company.fatturhello_last_downloaded_e_bill_identifer = (
                    e_bills_identifiers[-1]
                )

                # Download each E-Bill's data
                file_name_content_dict = dict()
                for e_bill_identifier in e_bills_identifiers:
                    file_name, file_content = connector.download_file(
                        url,
                        session_token,
                        company_identifier,
                        e_bill_identifier,
                    )
                    file_name_content_dict[file_name] = file_content

                # Create E-Bills
                self.receive_fe(
                    file_name_content_dict,
                    dict(),
                    channel_id=channel.id,
                    company_id=company.id,
                )

    @api.model
    def _fatturhello_get_attachments_for_status_update(self, companies):
        """E-Invoices in `companies` to be updated with Fatturhello data.

        Grouped by Company.
        """
        noupdate_statuses = self.env[
            "fatturapa.attachment.out"
        ]._fatturhello_get_noupdate_statuses()
        e_invoices_data = self.env["fatturapa.attachment.out"].search_read(
            domain=[
                ("state", "not in", noupdate_statuses),
                ("company_id", "in", companies.ids),
            ],
            fields=[
                "id",
                "company_id",
            ],
            load=None,
        )
        attachments_by_company = dict()
        for e_invoice_data in e_invoices_data:
            company = self.env["res.company"].browse(e_invoice_data["company_id"])
            attachment = self.env["fatturapa.attachment.out"].browse(
                e_invoice_data["id"]
            )
            if company not in attachments_by_company:
                attachments_by_company[company] = attachment
            else:
                attachments_by_company[company] |= attachment
        return attachments_by_company

    @api.model
    def _fatturhello_update_e_invoices_status_cron(self):
        """Method executed by CRON to update the status of E-Invoices."""
        connector = self.env["l10n_it_fatturapa_fatturhello.connector"]
        # Not using sudo so that we can do only
        # whatever the CRON's user can do
        companies = self.env.companies.filtered(
            lambda company: company.sdi_channel_type == "fatturhello"
        )
        attachments_by_company_id = self._fatturhello_get_attachments_for_status_update(
            companies
        )
        sdi_response_name_content_dict = dict()
        for company, attachments in attachments_by_company_id.items():
            channel = company.sdi_channel_id
            # Login
            url = channel.fatturhello_base_url
            session_token = connector.get_session_token(
                url,
                channel.fatturhello_login_authtoken,
            )

            # Download each E-Invoice's status
            attachment_to_statuses_dict = {
                attachment: connector.get_e_invoice_status_list(
                    url,
                    session_token,
                    company.fatturhello_identifier,
                    attachment._fatturhello_get_e_invoice_identifier(),
                )
                for attachment in attachments
            }

            # Parse the Fatturhello status into a SdI message
            for attachment, statuses in attachment_to_statuses_dict.items():
                last_processed_status_datetime = (
                    attachment.fatturhello_last_processed_status_datetime
                )
                for status_index, status in enumerate(statuses):
                    status_datetime = status["Data"]
                    if (
                        not last_processed_status_datetime
                        or status_datetime > last_processed_status_datetime
                    ):
                        # Process only if more recent than the last one processed
                        name, content = connector._prepare_sdi_notification(
                            attachment.name,
                            status_index,
                            status,
                        )
                        sdi_response_name_content_dict[name] = content

        # Update attachments
        self.receive_notification(
            sdi_response_name_content_dict,
        )
