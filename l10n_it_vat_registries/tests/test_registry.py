# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import io
from zipfile import ZipFile

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase

from odoo.addons.base.models.ir_qweb import QWebException


class TestRegistry(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.test_date = fields.Date.today()
        cls.journal = cls.env["account.journal"].search(
            [("type", "=", "sale")], limit=1
        )
        cls.ova = cls.env["account.account"].search(
            [("account_type", "=", "asset_current")],
            limit=1,
        )
        cls.tax = cls.env["account.tax"].create(
            {
                "name": "Tax 10.0",
                "amount": 10.0,
                "amount_type": "fixed",
            }
        )
        cls.tax_registry = cls.env["account.tax.registry"].create(
            {
                "name": "Sales",
                "layout_type": "customer",
                "journal_ids": [(6, 0, [cls.journal.id])],
            }
        )

        cls.invoice_line_account = (
            cls.env["account.account"]
            .search(
                [("account_type", "=", "expense")],
                limit=1,
            )
            .id
        )

        cls.invoice = cls.env["account.move"].create(
            {
                "partner_id": cls.env.ref("base.res_partner_2").id,
                "invoice_date": cls.test_date,
                "move_type": "out_invoice",
                "journal_id": cls.journal.id,
                "invoice_line_ids": [
                    (
                        0,
                        None,
                        {
                            "product_id": cls.env.ref("product.product_product_4").id,
                            "quantity": 1.0,
                            "price_unit": 100.0,
                            "name": "product that cost 100",
                            "account_id": cls.invoice_line_account,
                            "tax_ids": [(6, 0, [cls.tax.id])],
                        },
                    )
                ],
            }
        )
        cls.invoice.action_post()

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

        report_name = "l10n_it_vat_registries.report_registro_iva"
        domain = [
            ("report_type", "like", "qweb"),
            ("report_name", "in", [report_name]),
        ]
        report = self.env["ir.actions.report"].search(domain)
        data = res["context"]["report_action"]["data"]
        html = report._render_qweb_html(report_name, data["ids"], data)

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
        xlsx, _type = report._render_xlsx(report_name, data["ids"], data)

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

    def _create_out_invoice(self, tax_ids, line_name):
        invoice = self.env["account.move"].create(
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
                            "name": line_name,
                            "account_id": self.invoice_line_account,
                            "tax_ids": [(6, 0, tax_ids)],
                        },
                    )
                ],
            }
        )
        invoice.action_post()
        return invoice

    def _render_registro_html(self):
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

        report_name = "l10n_it_vat_registries.report_registro_iva"
        domain = [
            ("report_type", "like", "qweb"),
            ("report_name", "in", [report_name]),
        ]
        report = self.env["ir.actions.report"].search(domain)
        data = res["context"]["report_action"]["data"]
        return report._render_qweb_html(report_name, data["ids"], data)

    def test_invoice_with_excluded_tax(self):
        """Registry is printed when only one tax is not excluded."""
        included_tax = self.env["account.tax"].create(
            {
                "name": "Tax included",
                "amount": 10.0,
                "amount_type": "fixed",
            }
        )
        excluded_tax = self.env["account.tax"].create(
            {
                "name": "Tax excluded",
                "amount": 4.0,
                "amount_type": "fixed",
                "exclude_from_registries": True,
            }
        )
        self._create_out_invoice(
            [included_tax.id, excluded_tax.id], "product that cost 100"
        )

        html = self._render_registro_html()

        self.assertTrue(b"Tax included" in html[0])
        self.assertFalse(b"Tax excluded" in html[0])

    def test_invoice_with_multiple_taxes(self):
        """Registry raises when more than one tax is included."""
        tax_a = self.env["account.tax"].create(
            {
                "name": "Tax A",
                "amount": 10.0,
                "amount_type": "fixed",
            }
        )
        tax_b = self.env["account.tax"].create(
            {
                "name": "Tax B",
                "amount": 4.0,
                "amount_type": "fixed",
            }
        )
        self._create_out_invoice([tax_a.id, tax_b.id], "product that cost 100")

        with self.assertRaises(QWebException) as error:
            self._render_registro_html()
        self.assertIsInstance(error.exception.__cause__, UserError)

    def test_invoice_with_only_excluded_taxes(self):
        """Registry skips lines whose taxes are all excluded."""
        tax_a = self.env["account.tax"].create(
            {
                "name": "Excluded A",
                "amount": 10.0,
                "amount_type": "fixed",
                "exclude_from_registries": True,
            }
        )
        tax_b = self.env["account.tax"].create(
            {
                "name": "Excluded B",
                "amount": 4.0,
                "amount_type": "fixed",
                "exclude_from_registries": True,
            }
        )
        self._create_out_invoice([tax_a.id, tax_b.id], "product that cost 100")

        html = self._render_registro_html()

        self.assertTrue(b"Tax 10.0" in html[0])
        self.assertFalse(b"Excluded A" in html[0])
        self.assertFalse(b"Excluded B" in html[0])
