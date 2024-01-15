# Copyright 2023 Giuseppe Borruso (gborruso@dinamicheaziendali.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date, timedelta
from unittest import mock

from dateutil.relativedelta import relativedelta
from freezegun import freeze_time

from odoo import api, fields
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon

_module_ns = "odoo.addons.currency_rate_update_boi"
_file_ns = _module_ns + ".models.res_currency_rate_provider_BOI"
_BOI_provider_class = _file_ns + ".ResCurrencyRateProviderBOI"


@tagged("post_install", "-at_install")
class TestCurrencyRateUpdate(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.Company = cls.env["res.company"]
        cls.CurrencyRate = cls.env["res.currency.rate"]
        cls.CurrencyRateProvider = cls.env["res.currency.rate.provider"]

        cls.today = fields.Date.today()
        cls.eur_currency = cls.env.ref("base.EUR")
        cls.usd_currency = cls.env.ref("base.USD")
        cls.gbp_currency = cls.env.ref("base.GBP")
        cls.company = cls.Company.create(
            {"name": "Test company", "currency_id": cls.eur_currency.id}
        )
        cls.env.user.company_ids += cls.company
        cls.env.user.company_id = cls.company
        cls.ecb_provider = cls.CurrencyRateProvider.create(
            {
                "service": "BOI",
                "currency_ids": [
                    (4, cls.usd_currency.id),
                    (4, cls.gbp_currency.id),
                    (4, cls.env.user.company_id.currency_id.id),
                ],
            }
        )
        cls.CurrencyRate.search([]).unlink()

    @api.model
    def _get_no_weekend_date(self, compute_date):
        if compute_date.weekday() in [5, 6]:
            days_to_friday = 4 - compute_date.weekday()
            return compute_date + timedelta(days=days_to_friday)
        else:
            return compute_date

    def test_supported_currencies_BOI(self):
        self.ecb_provider._get_supported_currencies()

    def test_error_BOI(self):
        with mock.patch(_BOI_provider_class + "._obtain_rates", return_value=None):
            self.ecb_provider._update(self.today, self.today)

    def test_update_BOI_yesterday(self):
        compute_date = self._get_no_weekend_date(self.today - relativedelta(days=1))
        self.ecb_provider._update(compute_date, self.today)

        rates = self.CurrencyRate.search(
            [("currency_id", "=", self.usd_currency.id)], limit=1
        )
        self.assertTrue(rates)

        self.CurrencyRate.search([("company_id", "=", self.company.id)]).unlink()

    def test_update_BOI_month(self):
        compute_date = self._get_no_weekend_date(self.today - relativedelta(months=1))
        self.ecb_provider._update(compute_date, self.today)

        rates = self.CurrencyRate.search(
            [("currency_id", "=", self.usd_currency.id)], limit=1
        )
        self.assertTrue(rates)

        self.CurrencyRate.search([("company_id", "=", self.company.id)]).unlink()

    def test_update_BOI_year(self):
        compute_date = self._get_no_weekend_date(self.today - relativedelta(years=1))
        self.ecb_provider._update(compute_date, self.today)

        rates = self.CurrencyRate.search(
            [("currency_id", "=", self.usd_currency.id)], limit=1
        )
        self.assertTrue(rates)

        self.CurrencyRate.search([("company_id", "=", self.company.id)]).unlink()

    def test_update_BOI_scheduled(self):
        self.ecb_provider.interval_type = "days"
        self.ecb_provider.interval_number = 14
        self.ecb_provider.next_run = self._get_no_weekend_date(
            self.today - relativedelta(days=1)
        )
        self.ecb_provider._scheduled_update()

        rates = self.CurrencyRate.search(
            [("currency_id", "=", self.usd_currency.id)], limit=1
        )
        self.assertTrue(rates)

        self.CurrencyRate.search([("company_id", "=", self.company.id)]).unlink()

    def test_update_BOI_sequence(self):
        self.ecb_provider.interval_type = "days"
        self.ecb_provider.interval_number = 2
        self.ecb_provider.last_successful_run = None
        self.ecb_provider.next_run = date(2019, 4, 1)

        self.ecb_provider._scheduled_update()
        self.assertEqual(self.ecb_provider.last_successful_run, date(2019, 4, 1))
        self.assertEqual(self.ecb_provider.next_run, date(2019, 4, 3))
        rates = self.CurrencyRate.search(
            [
                ("company_id", "=", self.company.id),
                ("currency_id", "=", self.usd_currency.id),
            ]
        )
        self.assertEqual(len(rates), 1)

        self.ecb_provider._scheduled_update()
        self.assertEqual(self.ecb_provider.last_successful_run, date(2019, 4, 3))
        self.assertEqual(self.ecb_provider.next_run, date(2019, 4, 5))
        rates = self.CurrencyRate.search(
            [
                ("company_id", "=", self.company.id),
                ("currency_id", "=", self.usd_currency.id),
            ]
        )
        self.assertEqual(len(rates), 2)

        self.CurrencyRate.search([("company_id", "=", self.company.id)]).unlink()

    @freeze_time("2022-04-19 22:00")
    def test_update_BOI_with_daily(self):
        self.ecb_provider.interval_type = "days"
        self.ecb_provider.interval_number = 1
        self.ecb_provider.last_successful_run = date(2021, 4, 19)

        self.ecb_provider._scheduled_update()

        self.assertEqual(self.ecb_provider.last_successful_run, date(2022, 4, 19))

    def test_foreign_base_currency(self):
        self.test_update_BOI_yesterday()
        self.test_update_BOI_month()
        self.test_update_BOI_year()
        self.test_update_BOI_scheduled()
        self.test_update_BOI_sequence()
