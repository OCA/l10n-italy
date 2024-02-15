# Copyright 2021 Sergio Corato <https://github.com/sergiocorato>
# Copyright 2022 Simone Rubino - TAKOBI
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import date

from odoo import fields
from odoo.exceptions import AccessError, ValidationError
from odoo.fields import Command
from odoo.tools.date_utils import relativedelta

from .common import Common


class TestAssets(Common):
    def test_00_create_asset_depreciate_and_sale(self):
        today = fields.Date.today()
        asset = self._create_asset(today + relativedelta(years=-1))
        first_depreciation_date = today.replace(month=12, day=31) + relativedelta(
            years=-1
        )
        second_depreciation_date = today.replace(month=12, day=31)
        self._generate_fiscal_years(
            asset.purchase_date,
            max(
                first_depreciation_date,
                second_depreciation_date,
            ),
        )
        civ_type = self.env.ref("l10n_it_asset_management.ad_type_civilistico")
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
                    Command.create(
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
        wiz_vals["context"]["default_move_line_ids"] = [
            Command.set(move_lines_to_do.ids)
        ]
        wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(**wiz_vals["context"])
            .create(
                {
                    "management_type": "dismiss",
                    "l10n_it_asset_id": asset.id,
                }
            )
        )
        with self.assertRaises(ValidationError) as exc:
            wiz.link_asset()
        self.assertEqual(
            exc.exception.args[0],
            "Cannot dismiss an asset earlier than the last depreciation date.\n"
            "(Dismiss date: {}, last depreciation date: {}).".format(
                today, second_depreciation_date
            ),
        )
        sale_invoice.button_cancel()
        sale_invoice.button_draft()
        new_invoice_date = second_depreciation_date + relativedelta(days=10)
        with self.assertRaises(ValidationError) as ve:
            sale_invoice.invoice_date = new_invoice_date
        exc_message = ve.exception.args[0]
        self.assertIn("doesn't match the sequence number", exc_message)
        self.assertIn("clear the Journal Entry's Number to proceed", exc_message)
        self.assertNotEqual(sale_invoice.state, "posted")
        sale_invoice.name = False
        sale_invoice.invoice_date = new_invoice_date
        sale_invoice.action_post()
        self.assertEqual(sale_invoice.state, "posted")
        move_lines_to_do = move_lines.filtered(
            lambda x: x.account_id == asset.category_id.asset_account_id
        )
        wiz_vals["context"]["default_move_line_ids"] = [
            Command.set(move_lines_to_do.ids)
        ]
        wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(**wiz_vals["context"])
            .create(
                {
                    "management_type": "dismiss",
                    "l10n_it_asset_id": asset.id,
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
            lambda x: x.account_id == self.asset_category_1.asset_account_id
        )
        wiz_vals["context"]["default_move_line_ids"] = [
            Command.set(move_lines_to_do.ids)
        ]
        wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(**wiz_vals["context"])
            .create(
                {
                    "management_type": "create",
                    "category_id": self.asset_category_1.id,
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
                    Command.create(
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
        wiz_vals["context"]["default_move_line_ids"] = [
            Command.set(move_lines_to_do.ids)
        ]
        wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(**wiz_vals["context"])
            .create(
                {
                    "management_type": "dismiss",
                    "l10n_it_asset_id": asset.id,
                }
            )
        )
        wiz.link_asset()
        self.assertTrue(asset.sold)

    def test_02_asset_partial_deductible_from_purchase_invoice(self):
        # create purchase invoice partial deductible and generate asset
        invoice_date = fields.Date.today()
        purchase_invoice = self._create_purchase_invoice(
            invoice_date, tax_ids=[Command.set([self.tax_22_partial_60.id])]
        )
        self.assertAlmostEqual(
            sum(
                line.debit
                for line in purchase_invoice.line_ids
                if line.account_id == self.asset_category_1.asset_account_id
            ),
            7000 + (7000 * 0.22 * 0.4),
        )
        wiz_vals = purchase_invoice.open_wizard_manage_asset()
        move_line_ids = wiz_vals["context"]["default_move_line_ids"][0][2]
        move_lines = self.env["account.move.line"].browse(move_line_ids)
        move_lines_to_do = move_lines.filtered(
            lambda x: x.account_id == self.asset_category_1.asset_account_id
        )
        wiz_vals["context"]["default_move_line_ids"] = [
            Command.set(move_lines_to_do.ids)
        ]
        wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(**wiz_vals["context"])
            .create(
                {
                    "management_type": "create",
                    "category_id": self.asset_category_1.id,
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
            lambda x: x.account_id == self.asset_category_1.asset_account_id
        )
        wiz_vals["context"]["default_move_line_ids"] = [
            Command.set(move_lines_to_do.ids)
        ]
        wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(**wiz_vals["context"])
            .create(
                {
                    "management_type": "create",
                    "category_id": self.asset_category_1.id,
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
        # create depreciation for year -2 or -1 should do nothing as asset is totally
        # depreciated
        fourth_depreciation_date = today.replace(month=12, day=31) + relativedelta(
            years=-2
        )
        # create depreciation for current year should depreciate totally (as computed
        # value 9000*40% = 3600 is greater than residual value)
        current_year_depreciation_date = today.replace(month=12, day=31)
        self._generate_fiscal_years(
            asset.purchase_date,
            max(
                first_depreciation_date,
                second_depreciation_date,
                third_depreciation_date,
                fourth_depreciation_date,
                current_year_depreciation_date,
            ),
        )
        civ_type = self.env.ref("l10n_it_asset_management.ad_type_civilistico")
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
            lambda x: x.account_id == self.asset_category_1.asset_account_id
        )
        wiz_vals["context"]["default_move_line_ids"] = [
            Command.set(move_lines_to_do.ids)
        ]
        wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(**wiz_vals["context"])
            .create(
                {
                    "management_type": "update",
                    "category_id": self.asset_category_1.id,
                    "l10n_it_asset_id": asset.id,
                    "depreciation_type_ids": [Command.set(civ_type.ids)],
                }
            )
        )
        wiz.link_asset()
        self.assertAlmostEqual(depreciation_id.amount_depreciable_updated, 9000)
        self._depreciate_asset(asset, fourth_depreciation_date)
        self.assertAlmostEqual(sum(civ_dep_lines.mapped("amount")), 7000)
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
            lambda x: x.account_id == self.asset_category_1.asset_account_id
        )
        wiz_vals["context"]["default_move_line_ids"] = [
            Command.set(move_lines_to_do.ids)
        ]
        wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(**wiz_vals["context"])
            .create(
                {
                    "management_type": "create",
                    "category_id": self.asset_category_1.id,
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
        # create depreciation for year -4 should do nothing as asset is already
        # depreciated in a later date
        third_depreciation_date = today.replace(month=12, day=31) + relativedelta(
            years=-4
        )
        # create depreciation for current year should depreciate totally (as computed
        # value 9000*40% = 3600 is greater than residual value)
        current_year_depreciation_date = today.replace(month=12, day=31)
        self._generate_fiscal_years(
            asset.purchase_date,
            max(
                first_depreciation_date,
                second_depreciation_date,
                third_depreciation_date,
                current_year_depreciation_date,
            ),
        )
        civ_type = self.env.ref("l10n_it_asset_management.ad_type_civilistico")
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
            lambda x: x.account_id == self.asset_category_1.asset_account_id
        )
        wiz_vals["context"]["default_move_line_ids"] = [
            Command.set(move_lines_to_do.ids)
        ]
        wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(**wiz_vals["context"])
            .create(
                {
                    "management_type": "update",
                    "category_id": self.asset_category_1.id,
                    "l10n_it_asset_id": asset.id,
                    "depreciation_type_ids": [Command.set(civ_type.ids)],
                }
            )
        )
        wiz.link_asset()
        self.assertAlmostEqual(depreciation_id.amount_depreciable_updated, 9000)
        self._depreciate_asset(asset, third_depreciation_date)
        self.assertAlmostEqual(sum(civ_dep_lines.mapped("amount")), 7000 * 0.6)
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
        self._link_asset_move(
            entry,
            "update",
            wiz_values={
                "l10n_it_asset_id": asset,
            },
        )

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
        self._link_asset_move(
            entry,
            "update",
            wiz_values={
                "l10n_it_asset_id": asset,
            },
        )

        # Assert
        accounting_info = asset.asset_accounting_info_ids
        self.assertEqual(accounting_info.move_type, "out")
        depreciation_info = asset.depreciation_ids
        self.assertEqual(
            depreciation_info.amount_residual, asset.purchase_amount - removed_amount
        )

    def test_max_amount_depreciable(self):
        """
        Set max amount depreciable in category line,
        if the asset has a higher amount, the max amount is set as depreciable instead.
        """
        # Arrange
        purchase_amount = 1000
        max_depreciable_amount = 120
        category = self.asset_category_1
        civ_type = self.env.ref("l10n_it_asset_management.ad_type_civilistico")
        category_civ_depreciation_type = category.type_ids.filtered(
            lambda x: x.depreciation_type_id == civ_type
        )
        category_civ_depreciation_type.update(
            {
                "base_max_amount": max_depreciable_amount,
            }
        )
        purchase_invoice = self._create_purchase_invoice(
            fields.Date.today(), amount=purchase_amount
        )
        # pre-condition
        self.assertEqual(purchase_invoice.amount_untaxed, purchase_amount)
        self.assertEqual(
            category_civ_depreciation_type.base_max_amount, max_depreciable_amount
        )
        self.assertGreater(purchase_amount, max_depreciable_amount)

        # Act
        asset = self._link_asset_move(
            purchase_invoice,
            "create",
            wiz_values={
                "name": "Test asset",
                "category_id": category,
            },
        )

        # Assert
        self.assertEqual(asset.category_id, category)
        civ_depreciation = asset.depreciation_ids.filtered(
            lambda x: x.type_id == civ_type
        )
        self.assertEqual(civ_depreciation.base_max_amount, max_depreciable_amount)
        self.assertEqual(civ_depreciation.amount_depreciable, max_depreciable_amount)

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

    def test_monthly_depreciation(self):
        """
        Monthly depreciation uses 1/12 of the coefficient
        of the year the depreciation is in.
        """
        # Arrange
        purchase_date = date(2019, 1, 1)
        asset = self._create_asset(purchase_date)
        first_depreciation_date = date(2019, 1, 31)
        second_depreciation_date = date(2020, 1, 31)
        third_depreciation_date = date(2021, 1, 31)
        self._generate_fiscal_years(
            asset.purchase_date,
            max(
                first_depreciation_date,
                second_depreciation_date,
                third_depreciation_date,
            ),
        )
        civ_depreciation_type = self.env.ref(
            "l10n_it_asset_management.ad_type_civilistico"
        )
        civ_depreciation = asset.depreciation_ids.filtered(
            lambda x: x.type_id == civ_depreciation_type
        )
        civ_depreciation.percentage = 12.0
        depreciation_mode = asset.category_id.type_ids.mode_id
        # pre-condition
        self.assertEqual(asset.purchase_date, purchase_date)
        self.assertEqual(civ_depreciation.amount_depreciable, 1000)
        self.assertRecordValues(
            depreciation_mode.line_ids,
            [
                {
                    "from_year_nr": 1,
                    "to_year_nr": 1,
                    "application": "coefficient",
                    "coefficient": 0.5,
                },
            ],
        )

        # Act
        self._depreciate_asset(asset, first_depreciation_date, period="month")
        self._depreciate_asset(asset, second_depreciation_date, period="month")
        self._depreciate_asset(
            asset, third_depreciation_date, period="month", period_count=2
        )

        # Assert
        self.assertRecordValues(
            civ_depreciation.line_ids,
            [
                {
                    "date": first_depreciation_date,
                    "amount": 5,
                },
                {
                    "date": second_depreciation_date,
                    "amount": 10,
                },
                {
                    "date": third_depreciation_date,
                    "amount": 20,
                },
            ],
        )

    def test_missing_fiscal_year_warning(self):
        """
        If some years are not configured as fiscal years,
        the wizard shows a warning.
        """
        # Arrange
        purchase_date = date(2019, 1, 1)
        asset = self._create_asset(purchase_date)
        depreciation_date = date(2020, 1, 1)

        # Act
        depreciate_wizard = self._depreciate_asset_wizard(asset, depreciation_date)

        # Assert 1: some fiscal years are missing
        self.assertTrue(depreciate_wizard.missing_fiscal_year_warning)

        # Act 2: Generate missing years
        self._generate_fiscal_years(
            asset.purchase_date,
            depreciation_date,
        )

        # Assert 2: no fiscal years are missing
        depreciate_wizard = self._depreciate_asset_wizard(asset, depreciation_date)
        self.assertFalse(depreciate_wizard.missing_fiscal_year_warning)

    def test_override_journal(self):
        """
        Set an "Override Journal" in the depreciation wizard,
        the journal entries are created in the selected journal.
        """
        # Arrange
        override_journal = self.env["account.journal"].create(
            {
                "name": "Test override journal",
                "code": "TOJ",
                "type": "general",
            }
        )
        purchase_date = date(2019, 1, 1)
        asset = self._create_asset(purchase_date)
        depreciation_date = date(2019, 1, 31)
        self._generate_fiscal_years(
            asset.purchase_date,
            depreciation_date,
        )
        civ_depreciation_type = self.env.ref(
            "l10n_it_asset_management.ad_type_civilistico"
        )
        civ_depreciation = asset.depreciation_ids.filtered(
            lambda x: x.type_id == civ_depreciation_type
        )
        civ_depreciation.percentage = 12.0
        depreciate_asset_wizard = self._depreciate_asset_wizard(
            asset,
            depreciation_date,
            period="month",
            override_journal=override_journal,
        )
        # pre-condition
        self.assertNotEqual(
            depreciate_asset_wizard.journal_id, asset.category_id.journal_id
        )

        # Act
        depreciate_asset_wizard.do_generate()

        # Assert
        account_move = asset.depreciation_ids.line_ids.move_id
        self.assertEqual(account_move.journal_id, depreciate_asset_wizard.journal_id)

    def test_same_asset_report_residual_partial_depreciation(self):
        """
        Partially depreciate an asset,
        the residual value in the asset and in the report are the same.
        """
        # Arrange
        purchase_date = date(2019, 1, 1)
        purchase_amount = 1000
        sale_date = date(2020, 6, 15)
        sale_amount = 500
        partial_dismiss_purchase_amount = 600
        partial_dismiss_fund_amount = 0
        report_date = date(2021, 12, 31)
        expected_residual_amount = 400

        asset = self._create_asset(asset_date=purchase_date)
        sale_invoice = self._create_sale_invoice(
            asset, amount=sale_amount, invoice_date=sale_date
        )
        self._link_asset_move(
            sale_invoice,
            "partial_dismiss",
            wiz_values={
                "l10n_it_asset_id": asset,
                "asset_purchase_amount": partial_dismiss_purchase_amount,
                "depreciated_fund_amount": partial_dismiss_fund_amount,
            },
        )
        # pre-condition
        self.assertEqual(asset.purchase_amount, purchase_amount)
        self.assertEqual(
            asset.depreciation_ids.amount_residual, expected_residual_amount
        )

        # Act
        self._generate_fiscal_years(purchase_date, report_date)
        report = self._get_report(report_date, "journal")

        # Assert
        asset_report = report.report_l10n_it_asset_ids.filtered(
            lambda ar: ar.l10n_it_asset_id == asset
        )
        asset_report_depreciation_line = (
            asset_report.report_depreciation_ids.report_depreciation_year_line_ids
        )
        self.assertEqual(
            asset_report_depreciation_line.amount_residual, expected_residual_amount
        )

    def test_open_manage_asset_wiz(self):
        manager_user = self.user
        account_user = self.account_user
        forbidden_user = self.env.ref("base.user_demo")
        forbidden_user.groups_id -= self.env.ref(
            "l10n_it_asset_management.group_asset_user"
        ) | self.env.ref("account.group_account_manager")
        self.assertFalse(
            forbidden_user.has_group("l10n_it_asset_management.group_asset_user")
        )

        invoice = self.env["account.move"].search([("line_ids", "!=", False)])[0]
        with self.assertRaises(AccessError):
            invoice.with_user(forbidden_user).open_wizard_manage_asset()
        invoice.with_user(manager_user).open_wizard_manage_asset()
        invoice.with_user(account_user).open_wizard_manage_asset()

        asset_category = self.env["asset.category"].search([])[0]
        asset_category.asset_account_id = invoice.invoice_line_ids.mapped("account_id")
        asset_wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(show_asset=True)
            .create(
                [
                    {
                        "name": "Test Asset Name",
                        "category_id": asset_category.id,
                        "management_type": "create",
                        "move_ids": [(6, 0, invoice.ids)],
                        "move_line_ids": [(6, 0, invoice.invoice_line_ids.ids)],
                    }
                ]
            )
        )
        with self.assertRaises(AccessError):
            asset_wiz.with_user(forbidden_user).link_asset()
        asset_wiz.with_user(manager_user).link_asset()
        asset_wiz.with_user(account_user).link_asset()
