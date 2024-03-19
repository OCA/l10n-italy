#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, models


class VatStatement(models.AbstractModel):
    _inherit = "report.account_vat_period_end_statement.vat_statement"

    @api.model
    def _get_report_values(self, docids, data=None):
        return super(
            VatStatement,
            self.with_context(
                use_l10n_it_vat_settlement_date=True,
            ),
        )._get_report_values(docids, data=data)
