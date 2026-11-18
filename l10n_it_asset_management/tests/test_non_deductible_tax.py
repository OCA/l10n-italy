# Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.fields import Command
from odoo.tests import Form

from .common import Common


class TestNonDeductibleTax(Common):
    def _invoice_line_vals(self, price_unit, account=None):
        return {
            "account_id": (account or self.asset_category_1.asset_account_id).id,
            "quantity": 1,
            "price_unit": price_unit,
            "tax_ids": [Command.set(self.tax_22_partial_60.ids)],
        }

    def _create_invoice(self, lines_vals, post=True):
        invoice = self.env["account.move"].create(
            {
                "move_type": "in_invoice",
                "invoice_date": fields.Date.today(),
                "partner_id": self.env.ref("base.partner_demo").id,
                "invoice_line_ids": [Command.create(vals) for vals in lines_vals],
            }
        )
        if post:
            invoice.action_post()
        return invoice

    def _asset_tax_lines(self, invoice):
        return invoice.line_ids.filtered(
            lambda line: line.display_type == "tax"
            and line.account_id == self.asset_category_1.asset_account_id
        )

    def _asset_base_lines(self, invoice):
        return invoice.invoice_line_ids.filtered(
            lambda line: line.account_id == self.asset_category_1.asset_account_id
        )

    def test_tax_line_for_each_asset_line(self):
        """Non deductible VAT on an asset account has a tax line for each line,
        the other tax lines are grouped as usual."""
        invoice = self._create_invoice(
            [self._invoice_line_vals(600) for _i in range(4)]
            + [self._invoice_line_vals(100, self.expense_account) for _i in range(2)]
        )
        base_lines = self._asset_base_lines(invoice)
        tax_lines = self._asset_tax_lines(invoice)
        self.assertEqual(len(tax_lines), 4)
        self.assertEqual(tax_lines.mapped("balance"), [52.8] * 4)
        self.assertEqual(
            set(tax_lines.mapped("l10n_it_asset_tax_key")),
            set(base_lines.mapped("l10n_it_asset_tax_key")),
        )
        self.assertEqual(len(set(base_lines.mapped("l10n_it_asset_tax_key"))), 4)
        deductible_line = invoice.line_ids.filtered(
            lambda line: line.account_id == self.tax_account
        )
        self.assertRecordValues(deductible_line, [{"balance": 343.2}])
        expense_tax_line = invoice.line_ids.filtered(
            lambda line: line.display_type == "tax"
            and line.account_id == self.expense_account
        )
        self.assertRecordValues(
            expense_tax_line, [{"balance": 17.6, "l10n_it_asset_tax_key": False}]
        )
        self.assertAlmostEqual(invoice.amount_tax, 2600 * 0.22)

    def test_tax_lines_updated_in_draft(self):
        """Changes to the lines of a draft invoice update their own tax line."""
        invoice = self._create_invoice(
            [self._invoice_line_vals(600) for _i in range(2)], post=False
        )
        with Form(invoice) as invoice_form:
            with invoice_form.invoice_line_ids.edit(1) as line_form:
                line_form.price_unit = 1000
            with invoice_form.invoice_line_ids.new() as line_form:
                line_form.name = "New asset"
                line_form.account_id = self.asset_category_1.asset_account_id
                line_form.price_unit = 500
                line_form.tax_ids.clear()
                line_form.tax_ids.add(self.tax_22_partial_60)
        tax_by_key = {
            line.l10n_it_asset_tax_key: line.balance
            for line in self._asset_tax_lines(invoice)
        }
        self.assertEqual(
            {
                line.price_unit: tax_by_key[line.l10n_it_asset_tax_key]
                for line in self._asset_base_lines(invoice)
            },
            {600: 52.8, 1000: 88.0, 500: 44.0},
        )

    def test_tax_lines_rounding(self):
        """The tax lines of each line sum up to the grouped tax."""
        for rounding_method in ("round_per_line", "round_globally"):
            self.env.company.tax_calculation_rounding_method = rounding_method
            invoice = self._create_invoice([self._invoice_line_vals(33.33)] * 3)
            grouped_invoice = self._create_invoice(
                [self._invoice_line_vals(33.33, self.expense_account)] * 3
            )
            grouped_tax_line = grouped_invoice.line_ids.filtered(
                lambda line: line.display_type == "tax"
                and line.account_id == self.expense_account
            )
            tax_lines = self._asset_tax_lines(invoice)
            self.assertEqual(len(tax_lines), 3)
            self.assertAlmostEqual(
                sum(tax_lines.mapped("balance")), grouped_tax_line.balance
            )
            self.assertAlmostEqual(invoice.amount_tax, grouped_invoice.amount_tax)

    def test_create_assets_from_invoice_lines(self):
        """Each asset gets the non deductible VAT of its own line."""
        invoice = self._create_invoice(
            [self._invoice_line_vals(600) for _i in range(3)]
            + [self._invoice_line_vals(1000)]
        )
        base_lines = self._asset_base_lines(invoice)
        assets = self.env["asset.asset"]
        for base_line in base_lines:
            # The wizard proposes every line not linked yet:
            # the user keeps only one line of the asset account
            wiz_vals = invoice.open_wizard_manage_asset()
            lines = self.env["account.move.line"].browse(
                wiz_vals["context"]["default_move_line_ids"][0][2]
            )
            wiz_vals["context"]["default_move_line_ids"] = [
                Command.set((lines - (base_lines - base_line)).ids)
            ]
            wiz = (
                self.env["wizard.account.move.manage.asset"]
                .with_context(**wiz_vals["context"])
                .create(
                    {
                        "management_type": "create",
                        "category_id": self.asset_category_1.id,
                        "name": base_line.name or "Asset",
                    }
                )
            )
            # The deductible VAT is not on the asset account
            wiz.move_line_ids = wiz.move_line_ids.filtered(
                lambda line: line.account_id == self.asset_category_1.asset_account_id
            )
            assets |= wiz.link_asset()
        self.assertEqual(
            assets.mapped("purchase_amount"), [652.8, 652.8, 652.8, 1088.0]
        )
        for tax_line in self._asset_tax_lines(invoice):
            self.assertEqual(len(tax_line.asset_accounting_info_ids), 1)
