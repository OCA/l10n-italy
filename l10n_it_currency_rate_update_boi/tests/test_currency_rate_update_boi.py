# Copyright 2023 Giuseppe Borruso (gborruso@dinamicheaziendali.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta
from unittest import mock

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon

_module_ns = "odoo.addons.l10n_it_currency_rate_update_boi"
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
        # all currencies but EUR and USD are archived by default
        cls.gbp_currency.active = True
        cls.company = cls.Company.create(
            {"name": "Test company", "currency_id": cls.eur_currency.id}
        )
        cls.env.user.company_ids += cls.company
        cls.env.user.company_id = cls.company
        cls.ecb_provider = cls.CurrencyRateProvider.create(
            {
                "service": "BOI",
                "currency_ids": [
                    fields.Command.set([cls.usd_currency.id, cls.gbp_currency.id])
                ],
            }
        )
        cls.CurrencyRate.search([]).unlink()
        # create fake return data from BOI
        compute_date = cls._get_no_weekend_date(cls.today - relativedelta(days=1))
        cls.mock_rates = {str(compute_date): {"USD": "1.1446", "GBP": "0.85880"}}

    @classmethod
    def _get_no_weekend_date(cls, compute_date):
        if compute_date.weekday() in [5, 6]:
            days_to_friday = 4 - compute_date.weekday()
            return compute_date + timedelta(days=days_to_friday)
        else:
            return compute_date

    def test_supported_currencies_BOI(self):
        self.ecb_provider._get_supported_currencies()

    def test_update_BOI_yesterday(self):
        with mock.patch(
            _BOI_provider_class + "._obtain_rates", return_value=self.mock_rates
        ):
            compute_date = self._get_no_weekend_date(self.today - relativedelta(days=1))
            self.ecb_provider._update(compute_date, self.today)

            rates = self.CurrencyRate.search(
                [("currency_id", "=", self.usd_currency.id)], limit=1
            )
            self.assertEqual(rates.company_rate, 1.1446)
