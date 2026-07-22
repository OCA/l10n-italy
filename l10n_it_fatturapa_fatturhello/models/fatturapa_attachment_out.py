# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class FatturaPAAttachmentOut(models.Model):
    _inherit = "fatturapa.attachment.out"

    fatturhello_protocol = fields.Char(
        readonly=True,
        help="Identifier assigned during upload to Fatturhello.",
    )
    state = fields.Selection(
        selection_add=[
            # Before the `sent` status
            ("sent_to_fatturhello", "Sent to Fatturhello"),
            ("sent",),
        ],
        ondelete={
            "sent_to_fatturhello": "set default",
        },
    )
    fatturhello_last_processed_status_datetime = fields.Datetime(
        string="Last processed Fatturhello status",
        help="All the status updates more recent than this date will be processed.\n"
        "If empty, all the status updates will be processed.",
    )

    def _fatturhello_adapt_file_name(self, file_name):
        """Fatturhello requires the file name to start with the country code (IT)."""
        company = self.env.company
        if file_name:
            country_code = company.country_id.code
            if country_code and not file_name.startswith(country_code):
                file_name = country_code + file_name
        return file_name

    @api.model
    def get_file_vat(self):
        file_vat = super().get_file_vat()
        company = self.env.company
        if company.sdi_channel_id.channel_type == "fatturhello":
            file_vat = self._fatturhello_adapt_file_name(file_vat)
        return file_vat

    def _is_sent_to_sdi(self):
        if self.state == "sent_to_fatturhello":
            is_sent_to_sdi = False
        else:
            is_sent_to_sdi = super()._is_sent_to_sdi()
        return is_sent_to_sdi

    def _fatturhello_get_e_invoice_identifier(self):
        """How the uploaded invoice can be identified for API calls."""
        self.ensure_one()
        return self.name

    @api.model
    def _fatturhello_get_noupdate_statuses(self):
        """E-Invoices in these statuses will not fetch updates from Fatturhello."""
        return (
            "rejected",
            "validated",
            "accepted",
        )
