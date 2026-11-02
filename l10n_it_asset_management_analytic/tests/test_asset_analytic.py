# Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from odoo.fields import Command

from odoo.addons.l10n_it_asset_management.tests.common import Common


class TestAssetAnalytic(Common):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        plan = cls.env["account.analytic.plan"].create({"name": "Test plan"})
        cls.analytic_account, cls.other_analytic_account, cls.model_account = cls.env[
            "account.analytic.account"
        ].create(
            [
                {"name": name, "plan_id": plan.id}
                for name in ("Asset account", "Other account", "Model account")
            ]
        )
        cls.distribution = {str(cls.analytic_account.id): 100}
        cls.other_distribution = {str(cls.other_analytic_account.id): 100}
        cls.model_distribution = {str(cls.model_account.id): 100}
        # A distribution model applying to every journal item
        cls.env["account.analytic.distribution.model"].create(
            {"analytic_distribution": cls.model_distribution}
        )

        civil_type = cls.civilistico_asset_dep_type
        category_depreciation_type = cls.asset_category_1.type_ids.filtered(
            lambda x: x.depreciation_type_id == civil_type
        )
        category_depreciation_type.percentage = 20.0
        category_depreciation_type.mode_id.line_ids.unlink()

    def _get_civil_depreciation(self, asset):
        return asset.depreciation_ids.filtered(
            lambda x: x.type_id == self.civilistico_asset_dep_type
        )

    def _get_move_lines_distribution(self, move):
        return {line.account_id: line.analytic_distribution for line in move.line_ids}

    def test_asset_distribution_from_category(self):
        """The asset takes the distribution of its category, which can be changed."""
        self.asset_category_1.analytic_distribution = self.distribution

        asset = self._create_asset(date(2020, 1, 1))
        self.assertEqual(asset.analytic_distribution, self.distribution)

        asset.analytic_distribution = self.other_distribution
        self.assertEqual(asset.analytic_distribution, self.other_distribution)

    def test_asset_distribution_from_invoice(self):
        """The asset created from an invoice
        takes the distribution of the invoice lines."""
        purchase_invoice = self._create_purchase_invoice(date(2020, 1, 1))
        asset_lines = purchase_invoice.line_ids.filtered(
            lambda line: line.account_id == self.asset_category_1.asset_account_id
        )
        purchase_invoice.button_draft()
        asset_lines.analytic_distribution = self.distribution
        purchase_invoice.action_post()

        wiz_values = purchase_invoice.open_wizard_manage_asset()["context"]
        wiz_values["default_move_line_ids"] = [Command.set(asset_lines.ids)]
        wiz = (
            self.env["wizard.account.move.manage.asset"]
            .with_context(**wiz_values)
            .create(
                {
                    "management_type": "create",
                    "category_id": self.asset_category_1.id,
                    "name": "Test asset from invoice",
                }
            )
        )
        asset = wiz.link_asset()

        self.assertEqual(asset.analytic_distribution, self.distribution)

    def test_depreciation_entry_distribution(self):
        """The depreciation entry has the distribution of the asset
        on the expense line, the fund line follows the distribution
        models; the depreciation line keeps
        the distribution the asset had when the line was created."""
        asset = self._create_asset(date(2020, 1, 1))
        asset.analytic_distribution = self.distribution
        category = asset.category_id

        self._depreciate_asset(asset, date(2020, 12, 31))
        asset.analytic_distribution = self.other_distribution

        depreciation_line = self._get_civil_depreciation(asset).line_ids.filtered(
            lambda line: line.move_type == "depreciated"
        )
        self.assertEqual(depreciation_line.analytic_distribution, self.distribution)
        self.assertEqual(
            self._get_move_lines_distribution(depreciation_line.move_id),
            {
                category.depreciation_account_id: self.distribution,
                category.fund_account_id: self.model_distribution,
            },
        )

    def test_depreciation_entry_without_distribution(self):
        """Without distribution on the asset,
        the distribution models are applied as usual."""
        asset = self._create_asset(date(2020, 1, 1))
        self.assertFalse(asset.analytic_distribution)
        category = asset.category_id

        self._depreciate_asset(asset, date(2020, 12, 31))

        depreciation_line = self._get_civil_depreciation(asset).line_ids.filtered(
            lambda line: line.move_type == "depreciated"
        )
        self.assertEqual(
            self._get_move_lines_distribution(depreciation_line.move_id),
            {
                category.depreciation_account_id: self.model_distribution,
                category.fund_account_id: self.model_distribution,
            },
        )

    def test_dismiss_entries_distribution(self):
        """The gain entry has the distribution of the asset
        on the income line, the other lines follow the distribution models."""
        asset = self._create_asset(date(2020, 1, 1))
        asset.analytic_distribution = self.distribution
        category = asset.category_id
        depreciation = self._get_civil_depreciation(asset)
        self._depreciate_asset(asset, date(2020, 12, 31))
        self.assertEqual(depreciation.amount_residual, 800)

        sale_invoice = self._create_sale_invoice(asset, amount=900)
        self._link_asset_move(
            sale_invoice,
            "dismiss",
            wiz_values={
                "l10n_it_asset_id": asset,
            },
        )

        gain_line = depreciation.line_ids.filtered(
            lambda line: line.move_type == "gain"
        )
        self.assertEqual(gain_line.analytic_distribution, self.distribution)
        self.assertEqual(
            self._get_move_lines_distribution(gain_line.move_id),
            {
                depreciation.gain_account_id: self.distribution,
                category.asset_account_id: self.model_distribution,
            },
        )
        self.assertEqual(
            self._get_move_lines_distribution(depreciation.dismiss_move_id),
            {
                category.asset_account_id: self.model_distribution,
                category.fund_account_id: self.model_distribution,
            },
        )
