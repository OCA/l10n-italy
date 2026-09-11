#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from .common import Common


class TestAssetDepreciation(Common):
    def test_line_accounts(self):
        """Accounts can be overridden in asset depreciation.
        Overridden accounts are used in generated moves.
        """
        new_depreciation_account = self.expense_account.copy()

        purchase_date = date(2020, month=1, day=1)
        asset = self._create_asset(purchase_date)

        depreciation_date = date(2020, month=12, day=31)
        asset_depreciation = asset.depreciation_ids.filtered(
            lambda x, dev_type=self.civilistico_asset_dep_type: x.type_id == dev_type
        )
        asset_depreciation.percentage = 20.0
        # pre-condition: depreciation accounts default to category accounts
        self.assertEqual(
            asset_depreciation.depreciation_account_id,
            asset.category_id.depreciation_account_id,
        )
        self.assertEqual(
            asset_depreciation.gain_account_id, asset.category_id.gain_account_id
        )
        self.assertEqual(
            asset_depreciation.loss_account_id, asset.category_id.loss_account_id
        )

        # Act: change depreciation account and generate move
        asset_depreciation.depreciation_account_id = new_depreciation_account
        self._depreciate_asset(asset, depreciation_date)

        # Assert: new account is used in generated move
        depreciation_move = asset_depreciation.line_ids.move_id
        self.assertIn(new_depreciation_account, depreciation_move.line_ids.account_id)

    def test_depreciate_sale_loss_coefficient(self):
        """Depreciate and sale an asset with a sale invoice.
        Loss is proportional to the depreciation coefficient."""
        # Arrange
        asset_dep_type = self.civilistico_asset_dep_type
        asset_category = self.asset_category_1

        purchase_date = date(2020, month=1, day=1)
        depreciation_base_coeff = 0.2
        depreciation_percentage = 20.0
        depreciation_date = date(2020, month=12, day=31)
        depreciated_amount = 160
        sale_price = 500

        category_depreciation_type = asset_category.type_ids.filtered(
            lambda x, dep_type=asset_dep_type: x.depreciation_type_id == dep_type
        )
        category_depreciation_type.base_coeff = depreciation_base_coeff
        category_depreciation_type.percentage = depreciation_percentage
        category_depreciation_type.mode_id.line_ids.unlink()

        asset = self._create_asset(purchase_date)
        self.assertEqual(asset.category_id, asset_category)
        asset_depreciation = asset.depreciation_ids.filtered(
            lambda x, dep_type=asset_dep_type: x.type_id == dep_type
        )
        # pre-condition
        self.assertEqual(asset_depreciation.base_coeff, depreciation_base_coeff)
        self.assertEqual(asset_depreciation.percentage, depreciation_percentage)
        self.assertEqual(asset_depreciation.amount_residual, 200)

        # Act: Depreciate and dismiss with sale
        self._depreciate_asset(asset, depreciation_date)
        self.assertEqual(asset_depreciation.amount_residual, depreciated_amount)
        depreciation_lines = asset_depreciation.line_ids
        sale_invoice = self._create_sale_invoice(asset, amount=sale_price)
        self._link_asset_move(
            sale_invoice,
            "dismiss",
            wiz_values={
                "l10n_it_asset_id": asset,
            },
        )

        # Assert: Loss is proportional to `depreciation_base_coeff`
        depreciation_lines = asset_depreciation.line_ids - depreciation_lines
        self.assertRecordValues(
            depreciation_lines.sorted("move_type"),
            [
                {
                    "move_type": "loss",
                    "amount": abs(
                        sale_price * depreciation_base_coeff - depreciated_amount
                    ),
                },
                {
                    "move_type": "out",
                    "amount": sale_price * depreciation_base_coeff,
                },
            ],
        )

    def test_depreciate_update_loss_coefficient(self):
        """Depreciate and update an asset with a purchase invoice.
        'In' depreciation line is proportional to the depreciation coefficient."""
        # Arrange
        asset_dep_type = self.civilistico_asset_dep_type
        asset_category = self.asset_category_1

        purchase_date = date(2020, month=1, day=1)
        depreciation_base_coeff = 0.2
        depreciation_percentage = 20.0
        depreciation_date = date(2020, month=12, day=31)
        depreciated_amount = 160
        update_date = date(2021, month=6, day=6)
        update_price = 500

        category_depreciation_type = asset_category.type_ids.filtered(
            lambda x, dep_type=asset_dep_type: x.depreciation_type_id == dep_type
        )
        category_depreciation_type.base_coeff = depreciation_base_coeff
        category_depreciation_type.percentage = depreciation_percentage
        category_depreciation_type.mode_id.line_ids.unlink()

        asset = self._create_asset(purchase_date)
        self.assertEqual(asset.category_id, asset_category)
        asset_depreciation = asset.depreciation_ids.filtered(
            lambda x, dep_type=asset_dep_type: x.type_id == dep_type
        )
        # pre-condition
        self.assertEqual(asset_depreciation.base_coeff, depreciation_base_coeff)
        self.assertEqual(asset_depreciation.percentage, depreciation_percentage)
        self.assertEqual(asset_depreciation.amount_residual, 200)

        # Act: Depreciate and update with purchase
        self._depreciate_asset(asset, depreciation_date)
        self.assertEqual(asset_depreciation.amount_residual, depreciated_amount)
        depreciation_lines = asset_depreciation.line_ids
        purchase_invoice = self._create_purchase_invoice(
            update_date, amount=update_price
        )
        self._link_asset_move(
            purchase_invoice,
            "update",
            wiz_values={
                "l10n_it_asset_id": asset,
            },
        )

        # Assert: 'In' is proportional to `depreciation_base_coeff`
        depreciation_lines = asset_depreciation.line_ids - depreciation_lines
        self.assertRecordValues(
            depreciation_lines,
            [
                {
                    "move_type": "in",
                    "amount": update_price * depreciation_base_coeff,
                },
            ],
        )

    def test_depreciate_partial_sale_loss_coefficient(self):
        """Depreciate and partial depreciate an asset with a sale invoice.
        Loss is proportional to the depreciation coefficient."""
        # Arrange
        asset_dep_type = self.civilistico_asset_dep_type
        asset_category = self.asset_category_1

        purchase_date = date(2020, month=1, day=1)
        depreciation_base_coeff = 0.2
        depreciation_percentage = 20.0
        depreciation_date = date(2020, month=12, day=31)
        depreciated_amount = 160
        sale_price = 500
        depreciated_fund_amount = 100
        asset_purchase_amount = 200

        category_depreciation_type = asset_category.type_ids.filtered(
            lambda x, dep_type=asset_dep_type: x.depreciation_type_id == dep_type
        )
        category_depreciation_type.base_coeff = depreciation_base_coeff
        category_depreciation_type.percentage = depreciation_percentage
        category_depreciation_type.mode_id.line_ids.unlink()

        asset = self._create_asset(purchase_date)
        self.assertEqual(asset.category_id, asset_category)
        asset_depreciation = asset.depreciation_ids.filtered(
            lambda x, dep_type=asset_dep_type: x.type_id == dep_type
        )
        # pre-condition
        self.assertEqual(asset_depreciation.base_coeff, depreciation_base_coeff)
        self.assertEqual(asset_depreciation.percentage, depreciation_percentage)
        self.assertEqual(asset_depreciation.amount_residual, 200)

        # Act: Depreciate and update with purchase
        self._depreciate_asset(asset, depreciation_date)
        self.assertEqual(asset_depreciation.amount_residual, depreciated_amount)
        depreciation_lines = asset_depreciation.line_ids
        sale_invoice = self._create_sale_invoice(asset, amount=sale_price)
        self._link_asset_move(
            sale_invoice,
            "partial_dismiss",
            wiz_values={
                "l10n_it_asset_id": asset,
                "depreciated_fund_amount": depreciated_fund_amount,
                "asset_purchase_amount": asset_purchase_amount,
            },
        )

        # Assert: Create lines are proportional to `depreciation_base_coeff`
        depreciation_lines = asset_depreciation.line_ids - depreciation_lines
        self.assertRecordValues(
            depreciation_lines.sorted("move_type"),
            [
                {
                    "move_type": "depreciated",
                    "amount": -1 * depreciated_fund_amount * depreciation_base_coeff,
                },
                {
                    "move_type": "gain",
                    "amount": sale_price * depreciation_base_coeff
                    - (asset_purchase_amount - depreciated_fund_amount)
                    * depreciation_base_coeff,
                },
                {
                    "move_type": "out",
                    "amount": asset_purchase_amount * depreciation_base_coeff,
                },
            ],
        )
