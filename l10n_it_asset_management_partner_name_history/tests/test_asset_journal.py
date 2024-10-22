#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime

from dateutil.relativedelta import relativedelta

from odoo.tests import Form, TransactionCase

from odoo.addons.partner_name_history.tests.common import (
    _get_name_from_date,
    _set_partner_name,
)


class TestAssetJournal(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test",
            }
        )
        category_account = cls.env["account.account"].create(
            {
                "name": "Test Asset Account",
                "code": "TAA",
                "account_type": "expense",
            }
        )
        category_journal = cls.env["account.journal"].create(
            {
                "name": "Test Asset Journal",
                "code": "TAJ",
                "type": "general",
            }
        )
        cls.category = cls.env["asset.category"].create(
            {
                "name": "Asset category 1",
                "asset_account_id": category_account.id,
                "depreciation_account_id": category_account.id,
                "fund_account_id": category_account.id,
                "gain_account_id": category_account.id,
                "journal_id": category_journal.id,
                "loss_account_id": category_account.id,
            }
        )

        cls.currency = cls.env.ref("base.main_company").currency_id

    def _get_report_content(self, to_date):
        wizard_form = Form(self.env["wizard.asset.journal.report"])
        wizard_form.date = to_date
        wizard = wizard_form.save()
        res = wizard.with_context(
            discard_logo_check=True,
        ).button_export_asset_journal_html()

        report_name = res["report_name"]
        report_action = self.env["ir.actions.report"].search(
            [
                ("report_type", "=", res["report_type"]),
                ("report_name", "=", report_name),
            ]
        )
        report_ids = res["context"]["active_ids"]
        content, _type = report_action._render_qweb_html(report_name, report_ids)
        return content

    def test_report(self):
        """The report shows the old name for old assets."""
        # Arrange
        one_day = relativedelta(days=1)
        partner = self.partner
        category = self.category
        currency = self.currency
        original_partner_name = partner.name
        change_dates = [
            datetime.date(2019, 1, 1),
            datetime.date(2020, 1, 1),
        ]
        date_to_names = {date: _get_name_from_date(date) for date in change_dates}
        for change_date, name in date_to_names.items():
            _set_partner_name(
                partner,
                name,
                date=change_date,
            )
        assets = self.env["asset.asset"].create(
            [
                {
                    "name": "Test",
                    "category_id": category.id,
                    "currency_id": currency.id,
                    "supplier_id": partner.id,
                    "purchase_date": date,
                }
                for date in [
                    change_dates[0] - one_day,
                    change_dates[0] + one_day,
                    change_dates[1] - one_day,
                    change_dates[1] + one_day,
                ]
            ]
        )
        purchase_dates = assets.mapped("purchase_date")

        # Act
        content = self._get_report_content(max(purchase_dates))

        # Assert
        content = content.decode()
        last_partner_name = partner.name
        self.assertIn(original_partner_name, content)
        self.assertIn(_get_name_from_date(change_dates[0]), content)
        self.assertIn(last_partner_name, content)
