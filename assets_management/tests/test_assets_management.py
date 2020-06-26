# Copyright 2021 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestAssets(TransactionCase):

    def setUp(self):
        super().setUp()
        self.data_account_type_current_assets = self.env.ref(
            'account.data_account_type_current_assets')
        self.data_account_type_current_liabilities = self.env.ref(
            'account.data_account_type_current_liabilities')
        self.asset_category_1 = self.env['asset.category'].create({
            'name': 'Asset category 1',
            'asset_account_id': self.env['account.account'].search(
                [('user_type_id',
                  '=',
                  self.env.ref('account.data_account_type_fixed_assets').id)
                 ], limit=1).id,
            'depreciation_account_id': self.env['account.account'].search(
                [('user_type_id',
                  '=',
                  self.env.ref('account.data_account_type_expenses').id)
                 ], limit=1).id,
            'fund_account_id': self.env['account.account'].search(
                [('user_type_id',
                  '=',
                  self.env.ref('account.data_account_type_non_current_assets').id)
                 ], limit=1).id,
            'gain_account_id': self.env['account.account'].search(
                [('user_type_id',
                  '=',
                  self.env.ref('account.data_account_type_revenue').id)
                 ], limit=1).id,
            'journal_id': self.env['account.journal'].search(
                [('type', '=', 'general')], limit=1).id,
            'loss_account_id': self.env['account.account'].search(
                [('user_type_id',
                  '=',
                  self.env.ref('account.data_account_type_expenses').id)
                 ], limit=1).id,
        })

    def _create_asset(self):
        asset = self.env['asset.asset'].create({
            'name': 'Test asset',
            'category_id': self.asset_category_1.id,
            'company_id': self.env.ref('base.main_company').id,
            'currency_id': self.env.ref('base.main_company').currency_id.id,
            'purchase_amount': 1000.0,
        })
        return asset

    def test_create_depreciation(self):
        asset = self._create_asset()
        self.assertEqual(asset.state, 'non_depreciated',
                         'Asset is not in non depreciated state!')

        wiz_vals = asset.with_context(
            {'allow_reload_window': True}
        ).launch_wizard_generate_depreciations()
        wiz = self.env['wizard.asset.generate.depreciation'].with_context(
            wiz_vals['context']
        ).create({})
        # wiz.do_generate()
