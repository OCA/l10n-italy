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
