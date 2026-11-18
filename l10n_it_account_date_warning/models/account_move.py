# Copyright 2026 Marco Colombo (<https://github/TheMule71)
# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    # warning icon for accounting date
    l10n_it_show_date_warning = fields.Boolean(
        string="Date Warning",
        compute="_compute_l10n_it_show_date_warning",
    )

    @api.depends("date", "invoice_date")
    def _compute_l10n_it_show_date_warning(self):
        for record in self:
            record.l10n_it_show_date_warning = bool(
                record.is_purchase_document(include_receipts=True)
                and record.date
                and record.invoice_date
                and record.date < record.invoice_date
            )
