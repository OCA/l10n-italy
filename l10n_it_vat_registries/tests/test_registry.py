# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import io
from zipfile import ZipFile

from odoo import fields
from odoo.tests.common import TransactionCase


class TestRegistry(TransactionCase):
    def setUp(self):
        super().setUp()

        self.test_date = fields.Date.today()
        self.journal = self.env["account.journal"].search(
            [("type", "=", "sale")], limit=1
        )
        self.ova = self.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_current_assets").id,
                )
            ],
            limit=1,
        )
        self.tax = self.env["account.tax"].create(
            {
                "name": "Tax 10.0",
                "amount": 10.0,
                "amount_type": "fixed",
            }
        )
        self.tax_registry = self.env["account.tax.registry"].create(
            {
                "name": "Sales",
                "layout_type": "customer",
                "journal_ids": [(6, 0, [self.journal.id])],
            }
        )

        self.invoice_line_account = (
            self.env["account.account"]
            .search(
                [
                    (
                        "user_type_id",
                        "=",
                        self.env.ref("account.data_account_type_expenses").id,
                    )
                ],
                limit=1,
            )
            .id
        )

        self.invoice = self.env["account.move"].create(
            {
                "partner_id": self.env.ref("base.res_partner_2").id,
                "invoice_date": self.test_date,
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
                            "account_id": self.invoice_line_account,
                            "tax_ids": [(6, 0, [self.tax.id])],
                        },
                    )
                ],
            }
        )
        self.invoice.action_post()

    def test_invoice_and_report(self):
        wizard = self.env["wizard.registro.iva"].create(
            {
                "from_date": self.test_date,
                "to_date": self.test_date,
                "tax_registry_id": self.tax_registry.id,
                "layout_type": "supplier",
                "fiscal_page_base": 0,
            }
        )
        wizard.on_change_tax_registry_id()
        res = wizard.print_registro()

        domain = [
            ("report_type", "like", "qweb"),
            ("report_name", "=", "l10n_it_vat_registries.report_registro_iva"),
        ]
        report = self.env["ir.actions.report"].search(domain)
        data = res["context"]["report_action"]["data"]
        html = report._render_qweb_html(data["ids"], data)

        self.assertTrue(b"Tax 10.0" in html[0])

        # XLSX
        res = wizard.print_registro_xlsx()

        report_name = "l10n_it_vat_registries.report_registro_iva_xlsx"
        domain = [
            ("report_type", "=", "xlsx"),
            ("report_name", "=", report_name),
        ]
        report = self.env["ir.actions.report"].search(domain)
        data = res["context"]["report_action"]["data"]
        xlsx, _type = report._render_xlsx(data["ids"], data)

        # basic reading of a file
        # we don't want to depend on other non-standard libraries such as openpyxl
        f = io.BytesIO(xlsx)
        with ZipFile(f, "r").open("xl/sharedStrings.xml", "r") as wf:
            self.assertTrue(self.invoice.partner_id.name.encode("utf8") in wf.read())

    def test_no_report_from_invoice(self):
        """Check that the report is not available from invoice context menu."""
        report_id = self.ref("l10n_it_vat_registries.action_report_registro_iva")

        bindings = self.env["ir.actions.actions"].get_bindings("account.move")
        report_actions = bindings.get("report")
        report_ids = map(lambda report_action: report_action.get("id"), report_actions)

        self.assertNotIn(report_id, report_ids)
