# Copyright 2021 Sergio Corato <https://github.com/sergiocorato>
# Copyright 2022 Simone Rubino - TAKOBI
# Copyright 2023 Nextev Srl <odoo@nextev.it>
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import date

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.fields import first
from odoo.tools.date_utils import relativedelta

from .test_assets_common import TestAssets


class TestAssetsManagement(TestAssets):
    def test_00_create_asset_depreciate_and_sale(self):
        today = fields.Date.today()
        first_depreciation_date = today.replace(month=12, day=31) + relativedelta(
            years=-1
        )
        second_depreciation_date = today.replace(month=12, day=31)
        asset = self._create_asset(today + relativedelta(years=-1))
        civ_type = self.env.ref("assets_management.ad_type_civilistico")
        depreciation_id = asset.depreciation_ids.filtered(
            lambda x: x.type_id == civ_type
        )
        self.assertAlmostEqual(depreciation_id.amount_depreciable, 1000)
        depreciation_id.percentage = 25.0
        depreciation_id.mode_id.line_ids.coefficient = 0.5
        self.assertEqual(
            asset.state, "non_depreciated", "Asset is not in non depreciated state!"
        )

        self._depreciate_asset(asset, first_depreciation_date)
        self._depreciate_asset(asset, second_depreciation_date)
        dep_lines = asset.depreciation_ids.line_ids
        self.assertTrue(dep_lines)
        self.assertEqual(len(dep_lines), 2)
        civ_dep_lines = dep_lines.filtered(
            lambda x: x.depreciation_id.type_id == civ_type
            and x.move_type == "depreciated"
        )
        self.assertAlmostEqual(sum(civ_dep_lines.mapped("amount")), 375)
        self.assertEqual(asset.state, "partially_depreciated")

        # create sale invoice and link to asset
        sale_invoice = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.env.ref("base.partner_demo").id,
                "journal_id": self.env["account.journal"]
                .search(
                    [
                        ("type", "=", "sale"),
                    ],
                    limit=1,
                )
                .id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": asset.category_id.asset_account_id.id,
                            "quantity": 1,
                            "price_unit": 600,
                        },
                    )
                ],
            }
        )
        sale_invoice.action_post()
        wiz_vals = sale_invoice.open_wizard_manage_asset()
        move_line_ids = wiz_vals["context"]["default_move_line_ids"][0][2]
        move_lines = self.env["account.move.line"].browse(move_line_ids)
        move_lines_to_do = move_lines.filtered(
            lambda x: x.account_id == asset.category_id.asset_account_id
        )
        wiz_vals["context"]["default_move_line_ids"] = [(6, 0, move_lines_to_do.ids)]
        wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(wiz_vals["context"])
            .create(
                {
                    "management_type": "dismiss",
                    "asset_id": asset.id,
                }
            )
        )
        with self.assertRaises(ValidationError) as exc:
            wiz.link_asset()
        self.assertEqual(
            exc.exception.args[0],
            "Cannot dismiss an asset earlier than the last depreciation date.\n"
            "(Dismiss date: %s, last depreciation date: %s)."
            % (today, second_depreciation_date),
        )
        sale_invoice.button_cancel()
        sale_invoice.button_draft()
        sale_invoice.invoice_date = second_depreciation_date + relativedelta(days=10)
        sale_invoice.action_post()
        self.assertEqual(sale_invoice.state, "posted")
        move_lines_to_do = move_lines.filtered(
            lambda x: x.account_id == asset.category_id.asset_account_id
        )
        wiz_vals["context"]["default_move_line_ids"] = [(6, 0, move_lines_to_do.ids)]
        wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(wiz_vals["context"])
            .create(
                {
                    "management_type": "dismiss",
                    "asset_id": asset.id,
                    "dismiss_date": sale_invoice.invoice_date,
                }
            )
        )
        asset = wiz.link_asset()
        self.assertTrue(asset.sold)

    def test_01_asset_from_purchase_invoice(self):
        # create purchase invoice and generate asset
        invoice_date = fields.Date.today()
        purchase_invoice = self._create_purchase_invoice(invoice_date)
        wiz_vals = purchase_invoice.open_wizard_manage_asset()
        move_line_ids = wiz_vals["context"]["default_move_line_ids"][0][2]
        move_lines = self.env["account.move.line"].browse(move_line_ids)
        move_lines_to_do = move_lines.filtered(
            lambda x: x.account_id == self.asset_category_1_company_1.asset_account_id
        )
        wiz_vals["context"]["default_move_line_ids"] = [(6, 0, move_lines_to_do.ids)]
        wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(wiz_vals["context"])
            .create(
                {
                    "management_type": "create",
                    "category_id": self.asset_category_1_company_1.id,
                    "name": "Test asset",
                }
            )
        )
        asset = wiz.link_asset()
        self.assertFalse(asset.dismiss_date)
        self.assertEqual(asset.purchase_amount, 7000)
        # dismiss asset with sale
        # create sale invoice and link to asset
        sale_invoice = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.env.ref("base.partner_demo").id,
                "journal_id": self.env["account.journal"]
                .search(
                    [
                        ("type", "=", "sale"),
                    ],
                    limit=1,
                )
                .id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": asset.category_id.asset_account_id.id,
                            "quantity": 1,
                            "price_unit": 6000,
                        },
                    )
                ],
            }
        )
        sale_invoice.action_post()
        wiz_vals = sale_invoice.open_wizard_manage_asset()
        move_line_ids = wiz_vals["context"]["default_move_line_ids"][0][2]
        move_lines = self.env["account.move.line"].browse(move_line_ids)
        move_lines_to_do = move_lines.filtered(
            lambda x: x.account_id == asset.category_id.asset_account_id
        )
        wiz_vals["context"]["default_move_line_ids"] = [(6, 0, move_lines_to_do.ids)]
        wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(wiz_vals["context"])
            .create(
                {
                    "management_type": "dismiss",
                    "asset_id": asset.id,
                }
            )
        )
        wiz.link_asset()
        self.assertTrue(asset.sold)

    def test_02_asset_partial_deductible_from_purchase_invoice(self):
        # create purchase invoice partial deductible and generate asset
        invoice_date = fields.Date.today()
        purchase_invoice = self._create_purchase_invoice(
            invoice_date, tax_ids=[(6, 0, [self.tax_22_partial_60.id])]
        )
        self.assertAlmostEqual(
            sum(
                line.debit
                for line in purchase_invoice.line_ids
                if line.account_id == self.asset_category_1_company_1.asset_account_id
            ),
            7000 + (7000 * 0.22 * 0.4),
        )
        wiz_vals = purchase_invoice.open_wizard_manage_asset()
        move_line_ids = wiz_vals["context"]["default_move_line_ids"][0][2]
        move_lines = self.env["account.move.line"].browse(move_line_ids)
        move_lines_to_do = move_lines.filtered(
            lambda x: x.account_id == self.asset_category_1_company_1.asset_account_id
        )
        wiz_vals["context"]["default_move_line_ids"] = [(6, 0, move_lines_to_do.ids)]
        wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(wiz_vals["context"])
            .create(
                {
                    "management_type": "create",
                    "category_id": self.asset_category_1_company_1.id,
                    "name": "Test asset",
                }
            )
        )
        asset = wiz.link_asset()
        self.assertAlmostEqual(asset.purchase_amount, 7000 + (7000 * 0.22 * 0.4), 2)

    def test_03_asset_from_purchase_invoice_increment(self):
        # create purchase invoice and generate asset
        today = fields.Date.today()
        invoice_date = today + relativedelta(years=-5)
        purchase_invoice = self._create_purchase_invoice(invoice_date)
        wiz_vals = purchase_invoice.open_wizard_manage_asset()
        move_line_ids = wiz_vals["context"]["default_move_line_ids"][0][2]
        move_lines = self.env["account.move.line"].browse(move_line_ids)
        move_lines_to_do = move_lines.filtered(
            lambda x: x.account_id == self.asset_category_1_company_1.asset_account_id
        )
        wiz_vals["context"]["default_move_line_ids"] = [(6, 0, move_lines_to_do.ids)]
        wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(wiz_vals["context"])
            .create(
                {
                    "management_type": "create",
                    "category_id": self.asset_category_1_company_1.id,
                    "name": "Test asset",
                }
            )
        )
        asset = wiz.link_asset()
        self.assertEqual(asset.purchase_amount, 7000)
        # fully depreciate the asset
        first_depreciation_date = today.replace(month=12, day=31) + relativedelta(
            years=-5
        )
        second_depreciation_date = today.replace(month=12, day=31) + relativedelta(
            years=-4
        )
        third_depreciation_date = today.replace(month=12, day=31) + relativedelta(
            years=-3
        )
        civ_type = self.env.ref("assets_management.ad_type_civilistico")
        depreciation_id = asset.depreciation_ids.filtered(
            lambda x: x.type_id == civ_type
        )
        self.assertAlmostEqual(depreciation_id.amount_depreciable, 7000)
        depreciation_id.percentage = 40.0
        depreciation_id.mode_id.line_ids.coefficient = 0.5
        self.assertEqual(
            asset.state, "non_depreciated", "Asset is not in non depreciated state!"
        )
        self._depreciate_asset(asset, first_depreciation_date)
        self._depreciate_asset(asset, second_depreciation_date)
        self._depreciate_asset(asset, third_depreciation_date)
        dep_lines = asset.depreciation_ids.line_ids
        self.assertEqual(len(dep_lines), 3)
        civ_dep_lines = dep_lines.filtered(
            lambda x: x.depreciation_id.type_id == civ_type
            and x.move_type == "depreciated"
        )
        self.assertAlmostEqual(sum(civ_dep_lines.mapped("amount")), 7000)
        self.assertEqual(asset.state, "totally_depreciated")
        # create an invoice to increment th totally depreciated asset
        increment_invoice = self._create_purchase_invoice(today, amount=2000)
        wiz_vals = increment_invoice.open_wizard_manage_asset()
        move_line_ids = wiz_vals["context"]["default_move_line_ids"][0][2]
        move_lines = self.env["account.move.line"].browse(move_line_ids)
        move_lines_to_do = move_lines.filtered(
            lambda x: x.account_id == self.asset_category_1_company_1.asset_account_id
        )
        wiz_vals["context"]["default_move_line_ids"] = [(6, 0, move_lines_to_do.ids)]
        wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(wiz_vals["context"])
            .create(
                {
                    "management_type": "update",
                    "category_id": self.asset_category_1_company_1.id,
                    "asset_id": asset.id,
                    "depreciation_type_ids": [(6, 0, civ_type.ids)],
                }
            )
        )
        wiz.link_asset()
        self.assertAlmostEqual(depreciation_id.amount_depreciable_updated, 9000)
        # create depreciation for year -2 or -1 should do nothing as asset is totally
        # depreciated
        fourth_depreciation_date = today.replace(month=12, day=31) + relativedelta(
            years=-2
        )
        self._depreciate_asset(asset, fourth_depreciation_date)
        self.assertAlmostEqual(sum(civ_dep_lines.mapped("amount")), 7000)
        # create depreciation for current year should depreciate totally (as computed
        # value 9000*40% = 3600 is greater than residual value)
        current_year_depreciation_date = today.replace(month=12, day=31)
        self._depreciate_asset(asset, current_year_depreciation_date)
        dep_lines = asset.depreciation_ids.line_ids
        civ_dep_lines = dep_lines.filtered(
            lambda x: x.depreciation_id.type_id == civ_type
            and x.move_type == "depreciated"
        )
        self.assertEqual(asset.state, "totally_depreciated")
        self.assertAlmostEqual(sum(civ_dep_lines.mapped("amount")), 9000)

    def test_04_asset_partial_depreciate_from_purchase_invoice_increment(self):
        # create purchase invoice and generate asset
        today = fields.Date.today()
        invoice_date = today + relativedelta(years=-5)
        purchase_invoice = self._create_purchase_invoice(invoice_date)
        wiz_vals = purchase_invoice.open_wizard_manage_asset()
        move_line_ids = wiz_vals["context"]["default_move_line_ids"][0][2]
        move_lines = self.env["account.move.line"].browse(move_line_ids)
        move_lines_to_do = move_lines.filtered(
            lambda x: x.account_id == self.asset_category_1_company_1.asset_account_id
        )
        wiz_vals["context"]["default_move_line_ids"] = [(6, 0, move_lines_to_do.ids)]
        wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(wiz_vals["context"])
            .create(
                {
                    "management_type": "create",
                    "category_id": self.asset_category_1_company_1.id,
                    "name": "Test asset",
                }
            )
        )
        asset = wiz.link_asset()
        self.assertEqual(asset.purchase_amount, 7000)
        # partially depreciate the asset
        first_depreciation_date = today.replace(month=12, day=31) + relativedelta(
            years=-5
        )
        second_depreciation_date = today.replace(month=12, day=31) + relativedelta(
            years=-3
        )
        civ_type = self.env.ref("assets_management.ad_type_civilistico")
        depreciation_id = asset.depreciation_ids.filtered(
            lambda x: x.type_id == civ_type
        )
        self.assertAlmostEqual(depreciation_id.amount_depreciable, 7000)
        depreciation_id.percentage = 40.0
        depreciation_id.mode_id.line_ids.coefficient = 0.5
        self.assertEqual(
            asset.state, "non_depreciated", "Asset is not in non depreciated state!"
        )
        self._depreciate_asset(asset, first_depreciation_date)
        self._depreciate_asset(asset, second_depreciation_date)
        dep_lines = asset.depreciation_ids.line_ids
        self.assertEqual(len(dep_lines), 2)
        civ_dep_lines = dep_lines.filtered(
            lambda x: x.depreciation_id.type_id == civ_type
            and x.move_type == "depreciated"
        )
        self.assertAlmostEqual(sum(civ_dep_lines.mapped("amount")), 7000 * 0.6)
        self.assertEqual(asset.state, "partially_depreciated")
        # create an invoice to increment th totally depreciated asset
        increment_invoice = self._create_purchase_invoice(today, amount=2000)
        wiz_vals = increment_invoice.open_wizard_manage_asset()
        move_line_ids = wiz_vals["context"]["default_move_line_ids"][0][2]
        move_lines = self.env["account.move.line"].browse(move_line_ids)
        move_lines_to_do = move_lines.filtered(
            lambda x: x.account_id == self.asset_category_1_company_1.asset_account_id
        )
        wiz_vals["context"]["default_move_line_ids"] = [(6, 0, move_lines_to_do.ids)]
        wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(wiz_vals["context"])
            .create(
                {
                    "management_type": "update",
                    "category_id": self.asset_category_1_company_1.id,
                    "asset_id": asset.id,
                    "depreciation_type_ids": [(6, 0, civ_type.ids)],
                }
            )
        )
        wiz.link_asset()
        self.assertAlmostEqual(depreciation_id.amount_depreciable_updated, 9000)
        # create depreciation for year -4 should do nothing as asset is already
        # depreciated in a later date
        third_depreciation_date = today.replace(month=12, day=31) + relativedelta(
            years=-4
        )
        self._depreciate_asset(asset, third_depreciation_date)
        self.assertAlmostEqual(sum(civ_dep_lines.mapped("amount")), 7000 * 0.6)
        # create depreciation for current year should depreciate totally (as computed
        # value 9000*40% = 3600 is greater than residual value)
        current_year_depreciation_date = today.replace(month=12, day=31)
        self._depreciate_asset(asset, current_year_depreciation_date)
        dep_lines = asset.depreciation_ids.line_ids
        self.assertEqual(len(dep_lines), 4)
        civ_dep_lines = dep_lines.filtered(
            lambda x: x.depreciation_id.type_id == civ_type
            and x.move_type == "depreciated"
        )
        self.assertEqual(len(civ_dep_lines), 3)
        self.assertEqual(asset.state, "partially_depreciated")
        self.assertAlmostEqual(
            sum(civ_dep_lines.mapped("amount")), 7000 * 0.6 + 9000 * 0.4
        )

    def test_entry_in_update_asset(self):
        """An entry adding to the asset account
        creates a positive accounting info."""
        asset = self._create_asset()
        added_amount = 100
        entry = self._create_entry(asset.category_id.asset_account_id, added_amount)
        # pre-condition
        self.assertFalse(asset.asset_accounting_info_ids)

        # Act
        self._update_asset(entry, asset)

        # Assert
        accounting_info = asset.asset_accounting_info_ids
        self.assertEqual(accounting_info.move_type, "in")
        depreciation_info = asset.depreciation_ids
        self.assertEqual(
            depreciation_info.amount_residual, asset.purchase_amount + added_amount
        )

    def test_entry_out_update_asset(self):
        """An entry removing from the asset account
        creates a negative accounting info."""
        asset = self._create_asset()
        removed_amount = 100
        entry = self._create_entry(asset.category_id.asset_account_id, -removed_amount)
        # pre-condition
        self.assertFalse(asset.asset_accounting_info_ids)

        # Act
        self._update_asset(entry, asset)

        # Assert
        accounting_info = asset.asset_accounting_info_ids
        self.assertEqual(accounting_info.move_type, "out")
        depreciation_info = asset.depreciation_ids
        self.assertEqual(
            depreciation_info.amount_residual, asset.purchase_amount - removed_amount
        )

    def _civil_depreciate_asset(self, asset):
        # Keep only one civil depreciation
        civil_depreciation_type = self.env.ref("assets_management.ad_type_civilistico")
        civil_depreciation = first(
            asset.depreciation_ids.filtered(
                lambda d: d.type_id == civil_depreciation_type
            )
        )
        (asset.depreciation_ids - civil_depreciation).unlink()

        civil_depreciation.line_ids = [
            (5, 0, 0),
            (
                0,
                0,
                {
                    "name": "2019",
                    "date": date(2019, 12, 31),
                    "move_type": "depreciated",
                    "amount": 500,
                },
            ),
            (
                0,
                0,
                {
                    "name": "2020",
                    "date": date(2020, 12, 31),
                    "move_type": "depreciated",
                    "amount": 500,
                },
            ),
        ]
        return True

    def _generate_fiscal_years(self, start_date, end_date):
        fiscal_years = range(
            start_date.year,
            end_date.year,
        )
        fiscal_years_values = list()
        for fiscal_year in fiscal_years:
            fiscal_year_values = {
                "name": "Fiscal Year %d" % fiscal_year,
                "date_from": date(fiscal_year, 1, 1),
                "date_to": date(fiscal_year, 12, 31),
            }
            fiscal_years_values.append(fiscal_year_values)
        return self.env["account.fiscal.year"].create(fiscal_years_values)

    def _get_report_values(self, report_type):
        if report_type == "previsional":
            wizard_model = "wizard.asset.previsional.report"
            report_model = "report_asset_previsional"
            export_method = "export_asset_previsional_report"
        elif report_type == "journal":
            wizard_model = "wizard.asset.journal.report"
            report_model = "report_asset_journal"
            export_method = "export_asset_journal_report"
        else:
            raise Exception("Report can only be 'journal' or 'previsional'")
        return export_method, report_model, wizard_model

    def _get_report(self, report_date, report_type):
        export_method, report_model, wizard_model = self._get_report_values(report_type)

        wiz = self.env[wizard_model].create(
            {
                "date": report_date,
            }
        )
        report_result = getattr(wiz, export_method)()
        report_ids = report_result["context"]["report_action"]["context"]["active_ids"]
        report = self.env[report_model].browse(report_ids)
        return report

    def test_journal_prev_year(self):
        """
        Previous year depreciation considers depreciation of all previous years
        """
        # Arrange: Create an asset bought in 2019
        # and totally depreciated in 2019 and 2020
        purchase_date = date(2019, 1, 1)
        asset = self._create_asset(purchase_date)
        asset.purchase_date = purchase_date
        self.assertEqual(asset.purchase_amount, 1000)
        self._civil_depreciate_asset(asset)
        self.assertEqual(asset.state, "totally_depreciated")

        # Act: Generate the asset journal report for 2022
        report_date = date(2022, 11, 7)
        self._generate_fiscal_years(purchase_date, report_date)
        report = self._get_report(report_date, "journal")

        # Assert: The previous year depreciation counts.the depreciation of 2020
        total = report.report_total_ids
        self.assertEqual(total.amount_depreciation_fund_curr_year, 1000)
        self.assertEqual(total.amount_depreciation_fund_prev_year, 1000)
