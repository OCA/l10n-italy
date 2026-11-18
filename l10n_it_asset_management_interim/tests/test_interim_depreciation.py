# Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from odoo.exceptions import UserError
from odoo.fields import Command

from odoo.addons.l10n_it_asset_management.tests.common import Common


class TestInterimDepreciation(Common):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.interim_journal = cls.env["account.journal"].create(
            {
                "name": "Test interim journal",
                "code": "TINT",
                "type": "general",
            }
        )
        civil_type = cls.civilistico_asset_dep_type
        cls.category_depreciation_type = cls.asset_category_1.type_ids.filtered(
            lambda x: x.depreciation_type_id == civil_type
        )
        cls.category_depreciation_type.percentage = 20.0

    def _get_civil_depreciation(self, asset):
        return asset.depreciation_ids.filtered(
            lambda x: x.type_id == self.civilistico_asset_dep_type
        )

    def _generate_interim(self, assets, interim_date, reversal_date=None):
        wizard_values = {
            "company_id": self.env.ref("base.main_company").id,
            "date_dep": interim_date,
            "interim": True,
            "interim_journal_id": self.interim_journal.id,
            "l10n_it_asset_ids": [Command.set(assets.ids)],
        }
        if reversal_date:
            wizard_values["interim_reversal_date"] = reversal_date
        wizard = self.env["wizard.asset.generate.depreciation"].create(wizard_values)
        action = wizard.do_generate()
        moves = self.env["account.move"].search(action["domain"], order="date")
        self.assertEqual(len(moves), 2)
        return moves

    def _get_previsional_amount(self, asset, report_date):
        """Depreciation of the fiscal year shown by the previsional report."""
        report = self._get_report(report_date, "previsional")
        report_line = self.env[
            "report_asset_previsional_depreciation_line_year"
        ].search(
            [
                ("report_id", "=", report.id),
                (
                    "report_depreciation_id.depreciation_id",
                    "=",
                    self._get_civil_depreciation(asset).id,
                ),
            ],
            order="sequence desc",
            limit=1,
        )
        return report_line.amount_depreciated

    def _get_depreciation_balance(self, move):
        depreciation_account = self.asset_category_1.depreciation_account_id
        return sum(
            move.line_ids.filtered(
                lambda line: line.account_id == depreciation_account
            ).mapped("balance")
        )

    def test_first_year_without_pro_rata(self):
        """In the first fiscal year of an asset without pro rata temporis,
        the depreciation is the one of the previsional report.
        The entry is reversed and no depreciation line is created."""
        # Arrange
        purchase_date = date(2025, 7, 1)
        self._generate_fiscal_years(purchase_date, purchase_date)
        asset = self._create_asset(purchase_date)
        depreciation = self._get_civil_depreciation(asset)
        self.assertFalse(depreciation.pro_rata_temporis)
        self.assertEqual(depreciation.mode_id.line_ids.coefficient, 0.5)

        # Act
        move, reversal = self._generate_interim(asset, date(2025, 9, 30))

        # Assert
        amount = self._get_previsional_amount(asset, date(2025, 9, 30))
        self.assertTrue(amount)
        self.assertEqual(move.state, "posted")
        self.assertEqual(move.journal_id, self.interim_journal)
        self.assertEqual(move.date, date(2025, 9, 30))
        self.assertRecordValues(
            move.line_ids.sorted("balance"),
            [
                {
                    "account_id": self.asset_category_1.fund_account_id.id,
                    "balance": -amount,
                },
                {
                    "account_id": self.asset_category_1.depreciation_account_id.id,
                    "balance": amount,
                },
            ],
        )
        self.assertEqual(reversal.state, "posted")
        self.assertEqual(reversal.date, date(2025, 10, 1))
        self.assertEqual(reversal.reversed_entry_id, move)
        self.assertEqual(self._get_depreciation_balance(reversal), -amount)
        self.assertFalse(depreciation.line_ids)

    def test_following_year(self):
        """In the following fiscal years, the depreciation of the year
        is proportional to the part of the fiscal year passed."""
        # Arrange
        purchase_date = date(2025, 7, 1)
        self._generate_fiscal_years(purchase_date, date(2026, 12, 31))
        asset = self._create_asset(purchase_date)
        self._depreciate_asset(asset, date(2025, 12, 31))
        self.assertEqual(self._get_civil_depreciation(asset).amount_depreciated, 100)

        # Act
        move, reversal = self._generate_interim(asset, date(2026, 6, 30))

        # Assert
        self.assertEqual(
            self._get_depreciation_balance(move), round(200 * 181 / 365, 2)
        )

    def test_pro_rata_temporis(self):
        """With pro rata temporis, the depreciation is proportional
        to the days owned in the fiscal year."""
        # Arrange
        self.category_depreciation_type.mode_id.line_ids.unlink()
        self.category_depreciation_type.pro_rata_temporis = True
        purchase_date = date(2025, 7, 1)
        self._generate_fiscal_years(purchase_date, purchase_date)
        asset = self._create_asset(purchase_date)
        self.assertTrue(self._get_civil_depreciation(asset).pro_rata_temporis)

        # Act
        move, reversal = self._generate_interim(asset, date(2025, 9, 30))

        # Assert
        self.assertEqual(self._get_depreciation_balance(move), round(200 * 92 / 365, 2))

    def test_depreciation_lines_of_the_year(self):
        """Depreciation lines of the fiscal year are subtracted."""
        # Arrange
        self.category_depreciation_type.mode_id.line_ids.unlink()
        purchase_date = date(2025, 1, 1)
        self._generate_fiscal_years(purchase_date, purchase_date)
        asset = self._create_asset(purchase_date)
        self._depreciate_asset(asset, date(2025, 3, 31), period="month", period_count=3)
        self.assertEqual(self._get_civil_depreciation(asset).amount_depreciated, 50)

        # Act
        move, reversal = self._generate_interim(asset, date(2025, 6, 30))

        # Assert
        self.assertEqual(
            self._get_depreciation_balance(move), round(200 * 181 / 365 - 50, 2)
        )

    def test_grouped_journal_items(self):
        """Journal items of several assets are grouped by account."""
        # Arrange
        self.category_depreciation_type.mode_id.line_ids.unlink()
        self.category_depreciation_type.pro_rata_temporis = True
        purchase_date = date(2025, 7, 1)
        self._generate_fiscal_years(purchase_date, purchase_date)
        assets = self._create_asset(purchase_date) | self._create_asset(purchase_date)

        # Act
        move, reversal = self._generate_interim(
            assets, date(2025, 9, 30), reversal_date=date(2025, 10, 15)
        )

        # Assert
        self.assertEqual(len(move.line_ids), 2)
        self.assertEqual(
            self._get_depreciation_balance(move), 2 * round(200 * 92 / 365, 2)
        )
        self.assertEqual(reversal.date, date(2025, 10, 15))

    def test_previous_year_not_depreciated(self):
        """The previous fiscal year has to be depreciated first."""
        # Arrange
        purchase_date = date(2025, 7, 1)
        self._generate_fiscal_years(purchase_date, date(2026, 12, 31))
        asset = self._create_asset(purchase_date)

        # Act & Assert
        with self.assertRaisesRegex(UserError, "previous fiscal year"):
            self._generate_interim(asset, date(2026, 6, 30))

    def test_previsional_report_wizard(self):
        """The previsional report wizard creates the interim entry
        with the depreciation that the report shows at its date."""
        # Arrange
        purchase_date = date(2025, 7, 1)
        self._generate_fiscal_years(purchase_date, purchase_date)
        asset = self._create_asset(purchase_date)
        interim_date = date(2025, 9, 30)
        wizard = self.env["wizard.asset.previsional.report"].create(
            {
                "category_ids": [Command.set(asset.category_id.ids)],
                "date": interim_date,
                "interim_journal_id": self.interim_journal.id,
                "l10n_it_asset_ids": [Command.set(asset.ids)],
                "type_ids": [Command.set(self.civilistico_asset_dep_type.ids)],
            }
        )
        self.assertEqual(wizard.interim_reversal_date, date(2025, 10, 1))

        # Act
        action = wizard.button_create_interim_depreciation()

        # Assert
        move, reversal = self.env["account.move"].search(action["domain"], order="date")
        amount = self._get_previsional_amount(asset, interim_date)
        self.assertTrue(amount)
        self.assertEqual(self._get_depreciation_balance(move), amount)
        self.assertEqual(reversal.date, date(2025, 10, 1))
        self.assertFalse(self._get_civil_depreciation(asset).line_ids)
