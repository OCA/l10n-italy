#  Copyright 2019 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class IntrastatStatementPurchaseSection(models.AbstractModel):
    _inherit = "account.intrastat.statement.section"
    _name = "account.intrastat.statement.purchase.section"
    _description = "Fields and methods " "common to all Intrastat purchase sections"

    amount_currency = fields.Integer(string="Amount in Currency")

    @api.model
    def _prepare_statement_line(self, inv_intra_line, statement_id=None):
        res = super()._prepare_statement_line(inv_intra_line, statement_id)
        company_id = self.env.context.get("company_id", self.env.company)
        invoice_id = inv_intra_line.invoice_id

        # Amounts
        amount_currency = 0
        if (
            invoice_id.currency_id != invoice_id.company_id.currency_id
            and invoice_id.currency_id != self.env.ref("base.EUR")
        ):
            # Only for non-Euro countries
            dp_model = self.env["decimal.precision"]
            amount_currency = statement_id.round_min_amount(
                inv_intra_line.amount_currency,
                statement_id.company_id or company_id,
                dp_model.precision_get("Account"),
                truncate=True,
            )

        res.update(
            {
                "amount_currency": amount_currency,
            }
        )
        return res

    @api.model
    def get_section_type(self):
        return "purchase"

    @api.model
    def _default_transaction_nature_id(self):
        company_id = self.env.context.get("company_id", self.env.company)
        return company_id.intrastat_purchase_transaction_nature_id

    @api.model
    def _default_transaction_nature_b_id(self):
        company_id = self.env.context.get("company_id", self.env.user.company_id)
        return company_id.intrastat_purchase_transaction_nature_b_id
