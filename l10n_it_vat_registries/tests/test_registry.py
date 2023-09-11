# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests.common import TransactionCase


class TestRegistry(TransactionCase):
    def test_invoice_and_report(self):
        test_date = fields.Date.today()
        self.journal = self.env["account.journal"].search(
            [("type", "=", "sale")], limit=1
        )
        self.ova = self.env["account.account"].search(
            [("account_type", "=", "asset_current")],
            limit=1,
        )
        tax = self.env["account.tax"].create(
            {
                "name": "Tax 10.0",
                "amount": 10.0,
                "amount_type": "fixed",
            }
        )
        tax_registry = self.env["account.tax.registry"].create(
            {
                "name": "Sales",
                "layout_type": "customer",
                "journal_ids": [(6, 0, [self.journal.id])],
            }
        )
        invoice_line_account = (
            self.env["account.account"]
            .search(
                [("account_type", "=", "expense")],
                limit=1,
            )
            .id
        )

        invoice = self.env["account.move"].create(
            {
                "partner_id": self.env.ref("base.res_partner_2").id,
                "invoice_date": test_date,
                "move_type": "out_invoice",
                "journal_id": self.journal.id,
                "invoice_line_ids": [
                    (
                        0,
                        None,
                        {
                            "product_id": self.env.ref("product.product_product_4").id,
                            "quantity": 1.0,
                            "price_unit": 100.0,
                            "name": "product that cost 100",
                            "account_id": invoice_line_account,
                            "tax_ids": [(6, 0, [tax.id])],
                        },
                    )
                ],
            }
        )
        invoice.action_post()

        wizard = self.env["wizard.registro.iva"].create(
            {
                "from_date": test_date,
                "to_date": test_date,
                "tax_registry_id": tax_registry.id,
                "layout_type": "supplier",
                "fiscal_page_base": 0,
            }
        )
        wizard.on_change_tax_registry_id()
        res = wizard.print_registro()

        report_name = "l10n_it_vat_registries.report_registro_iva"
        domain = [
            ("report_type", "like", "qweb"),
            ("report_name", "in", [report_name]),
        ]
        report = self.env["ir.actions.report"].search(domain)
        data = res["context"]["report_action"]["data"]
        html = report._render_qweb_html(report_name, data["ids"], data)

        self.assertTrue(b"Tax 10.0" in html[0])

    def test_no_report_from_invoice(self):
        """Check that the report is not available from invoice context menu."""
        report_id = self.ref("l10n_it_vat_registries.action_report_registro_iva")

        bindings = self.env["ir.actions.actions"].get_bindings("account.move")
        report_actions = bindings.get("report")
        report_ids = map(lambda report_action: report_action.get("id"), report_actions)

        self.assertNotIn(report_id, report_ids)
