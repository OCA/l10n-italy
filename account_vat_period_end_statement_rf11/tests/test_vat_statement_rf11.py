from odoo.tests import tagged

from odoo.addons.account_vat_period_end_statement.tests.common import TestVATStatementCommon

@tagged("post_install", "-at_install")
class TestVatStatementRF11(TestVATStatementCommon):
    def create_74ter_account_income(self):
        return self.account_model.create(
            {
                "name": "74ter Income Account",
                "code": "74TER",
            }
        )

    def create_74ter_taxes(self, account_74ter):
        tax_sale = self.tax_model.create(
            {
                "name": "22% 74ter (sale)",
                "amount_type": "percent",
                "amount": 0.0,
                "type_tax_use": "sale",
                "sequence": 1,
                "is_tax_74ter": True,
                "tax_74ter_amount": 22.0,
                "tax_74_ter_income_account_id": account_74ter.id,
            }
        )
        tax_purchase = self.tax_model.create(
            {
                "name": "22% 74ter (purchase)",
                "amount_type": "percent",
                "amount": 0.0,
                "type_tax_use": "purchase",
                "sequence": 1,
                "is_tax_74ter": True,
                "tax_74ter_amount": 22.0,
                "tax_74_ter_income_account_id": account_74ter.id
            }
        )
        return tax_sale, tax_purchase

    # def set_company_fiscal_position_rf11(self):
    #     fiscal_position = self.env["account.fiscal.position"].search(
    #         [("code", "=", "RF11")]
    #     )
    #     company_id = self.env.user.company_id
    #     company_id.write({"property_account_position_id": fiscal_position.id})

    def test_vat_statement_rf11(self):
        account_74ter = self.create_74ter_account_income()
        tax_sale, tax_purchase = self.create_74ter_taxes(account_74ter)

        out_invoice = self.invoice_model.create(
            {
                "invoice_date": self.recent_date,
                "journal_id": self.sale_journal.id,
                "partner_id": self.env.ref("base.res_partner_3").id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "service",
                            "price_unit": 3660,
                            "quantity": 1,
                            "tax_ids": [(6, 0, [tax_sale.id])],
                        },
                    )
                ],
            }
        )
        out_invoice.action_post()

        in_invoice = self.invoice_model.create(
            {
                "invoice_date": self.recent_date,
                "journal_id": self.purchase_journal.id,
                "partner_id": self.env.ref("base.res_partner_4").id,
                "move_type": "in_invoice",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "service",
                            "price_unit": 1220,
                            "quantity": 1,
                            "tax_ids": [(6, 0, [tax_purchase.id])],
                        },
                    )
                ],
            }
        )
        in_invoice.action_post()
        self.vat_statement = self.vat_statement_model.create(
            {
                "journal_id": self.general_journal.id,
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