# Copyright 2021 Sergio Corato <https://github.com/sergiocorato>
# Copyright 2022 Simone Rubino - TAKOBI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import date

from odoo import fields
from odoo.fields import first
from odoo.tests.common import TransactionCase
from dateutil.relativedelta import relativedelta


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
        self.env['asset.category.depreciation.type'].create({
            'base_coeff': 25.0,
            'category_id': self.asset_category_1.id,
            'depreciation_type_id': self.env.ref(
                'assets_management.ad_type_civilistico').id,
            'mode_id': self.env.ref(
                'assets_management.ad_mode_materiale').id,
        })

    def _create_asset(self):
        asset = self.env['asset.asset'].create({
            'name': 'Test asset',
            'category_id': self.asset_category_1.id,
            'company_id': self.env.ref('base.main_company').id,
            'currency_id': self.env.ref('base.main_company').currency_id.id,
            'purchase_amount': 1000.0,
            'purchase_date': fields.Date.today() + relativedelta(days=-366),
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
        wiz.do_generate()

    def _civil_depreciate_asset(self, asset):
        # Keep only one civil depreciation
        civil_depreciation_type = self.env.ref(
            'assets_management.ad_type_civilistico')
        civil_depreciation = first(asset.depreciation_ids.filtered(
            lambda d: d.type_id == civil_depreciation_type
        ))
        (asset.depreciation_ids - civil_depreciation).unlink()

        civil_depreciation.line_ids = [
            (5, 0, 0),
            (0, 0, {
                'name': '2019',
                'date': date(2019, 12, 31),
                'move_type': 'depreciated',
                'amount': 500,
            }),
            (0, 0, {
                'name': '2020',
                'date': date(2020, 12, 31),
                'move_type': 'depreciated',
                'amount': 500,
            }),
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
        return self.env['account.fiscal.year'].create(fiscal_years_values)

    def _get_report_values(self, report_type):
        if report_type == 'previsional':
            wizard_model = 'wizard.asset.previsional.report'
            report_model = 'report_asset_previsional'
            export_method = 'export_asset_previsional_report'
        elif report_type == 'journal':
            wizard_model = 'wizard.asset.journal.report'
            report_model = 'report_asset_journal'
            export_method = 'export_asset_journal_report'
        else:
            raise Exception("Report can only be 'journal' or 'previsional'")
        return export_method, report_model, wizard_model

    def _get_report(self, report_date, report_type):
        export_method, report_model, wizard_model = \
            self._get_report_values(report_type)

        wiz = self.env[wizard_model].create({
            'date': report_date,
        })
        report_result = getattr(wiz, export_method)()
        report_ids = report_result['context']['active_ids']
        report = self.env[report_model].browse(report_ids)
        return report

    def test_journal_prev_year(self):
        """
        Previous year depreciation considers depreciation of all previous years
        """
        # Arrange: Create an asset bought in 2019
        # and totally depreciated in 2019 and 2020
        asset = self._create_asset()
        purchase_date = date(2019, 1, 1)
        asset.purchase_date = purchase_date
        self.assertEqual(asset.purchase_amount, 1000)
        self._civil_depreciate_asset(asset)
        self.assertEqual(asset.state, 'totally_depreciated')

        # Act: Generate the asset journal report for 2022
        report_date = date(2022, 11, 7)
        self._generate_fiscal_years(purchase_date, report_date)
        report = self._get_report(report_date, 'journal')

        # Assert: The previous year depreciation counts.the depreciation of 2020
        total = report.report_total_ids
        self.assertEqual(total.amount_depreciation_fund_curr_year, 1000)
        self.assertEqual(total.amount_depreciation_fund_prev_year, 1000)
