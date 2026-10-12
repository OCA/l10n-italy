# Copyright 2024-2026 Innovyou srl <http://www.innovyou.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests import tagged

from odoo.addons.l10n_it_account_vat_period_end_settlement.tests.common import (
    TestVATStatementCommon,
)


@tagged("post_install", "-at_install")
class TestVatStatementRF11(TestVATStatementCommon):
    def _create_74ter_income_account(self):
        return self.env["account.account"].create(
            {
                "name": "74ter Income Account",
                "code": "74TER",
                "account_type": "income",
                "company_ids": [Command.set(self.company.ids)],
            }
        )

    def _create_74ter_taxes(self, income_account):
        country_id = self.company.account_fiscal_country_id.id
        # 74-ter taxes are 0% (VAT not shown in invoice, margin regime): the
        # Italian localization requires an exoneration code and a law reference.
        # N5 = "Regime del margine / IVA non esposta in fattura".
        tax_sale = self.env["account.tax"].create(
            {
                "name": "22% 74ter (sale)",
                "amount_type": "percent",
                "amount": 0.0,
                "type_tax_use": "sale",
                "country_id": country_id,
                "l10n_it_exempt_reason": "N5",
                "l10n_it_law_reference": "Art. 74-ter DPR 633/72",
                "is_tax_74ter": True,
                "tax_74ter_amount": 22.0,
                "tax_74_ter_income_account_id": income_account.id,
            }
        )
        tax_purchase = self.env["account.tax"].create(
            {
                "name": "22% 74ter (purchase)",
                "amount_type": "percent",
                "amount": 0.0,
                "type_tax_use": "purchase",
                "country_id": country_id,
                "l10n_it_exempt_reason": "N5",
                "l10n_it_law_reference": "Art. 74-ter DPR 633/72",
                "is_tax_74ter": True,
                "tax_74ter_amount": 22.0,
                "tax_74_ter_income_account_id": income_account.id,
            }
        )
        return tax_sale, tax_purchase

    def test_vat_statement_rf11(self):
        """Margin "base su base": sale base 3660 - purchase base 1220 = 2440
        gross margin -> net 2000, 74ter VAT 440 (22% extracted from 2440)."""
        self.env.user.company_id = self.company.id
        income_account = self._create_74ter_income_account()
        tax_sale, tax_purchase = self._create_74ter_taxes(income_account)

        out_invoice = self.env["account.move"].create(
            {
                "invoice_date": self.recent_date,
                "partner_id": self.italian_partner_a.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "service",
                            "price_unit": 3660,
                            "quantity": 1,
                            "tax_ids": [Command.set(tax_sale.ids)],
                        }
                    )
                ],
            }
        )
        out_invoice.action_post()

        in_invoice = self.env["account.move"].create(
            {
                "invoice_date": self.recent_date,
                "partner_id": self.italian_partner_a.id,
                "move_type": "in_invoice",
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "service",
                            "price_unit": 1220,
                            "quantity": 1,
                            "tax_ids": [Command.set(tax_purchase.ids)],
                        }
                    )
                ],
            }
        )
        in_invoice.action_post()

        self.vat_statement = self.env["account.vat.period.end.statement"].create(
            {
                "journal_id": self.company_data_2["default_journal_misc"].id,
                "authority_vat_account_id": self.vat_authority.id,
                "payment_term_id": self.account_payment_term.id,
            }
        )
        self.current_period.vat_statement_id = self.vat_statement
        self.vat_statement.compute_amounts()

        self.assertEqual(self.vat_statement.net_tax_74_ter, 2000)
        self.assertEqual(self.vat_statement.tax_74_ter_amount, 440)
        self.assertEqual(self.vat_statement.tax_74_ter_amount_previous, 0)
        self.assertEqual(self.vat_statement.tax_74_ter_amount_total, 440)
