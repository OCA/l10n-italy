# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th)
# Copyright 2022 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from num2words import num2words

from odoo.tests.common import TransactionCase


class TestAmountToText(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["res.lang"]._activate_lang("it_IT")

    def test_01_currency_it_amount_to_text(self):
        """check that amount_to_text correctly converts text
        to italian language"""
        currency = self.env.ref("base.EUR")
        amount = 1050.75
        amount_text_en = currency.amount_to_text(amount)
        self.assertEqual(
            amount_text_en, "One Thousand And Fifty Euros and Seventy-Five Cents"
        )
        amount_text_it = currency.with_context(lang="it_IT").amount_to_text(amount)
        num2words(amount, to="currency", lang="it")
        self.assertEqual(
            amount_text_it, "millecinquanta euro e settantacinque centesimi"
        )

    def test_02_currency_unit_it_amount_to_text(self):
        """check that amount_to_text correctly converts currency
        unit/subunit to italian language singular form"""
        currency = self.env.ref("base.EUR")
        amount = 1.01
        amount_text_it_unit = currency.with_context(lang="it_IT").amount_to_text(amount)
        self.assertEqual(amount_text_it_unit, "un euro e un centesimo")

    def test_03_currency_usd_amount_to_text(self):
        """check that amount_to_text works as expected"""
        currency = self.env.ref("base.USD")
        amount = 1050.75
        amount_text_usd = currency.amount_to_text(amount)
        self.assertEqual(
            amount_text_usd, "One Thousand And Fifty Dollars and Seventy-Five Cents"
        )

    def test_04_currency_zero_fractional_value_it_amount_to_text(self):
        """check that amount_to_text correctly converts currency
        with zero fractional value"""
        currency = self.env.ref("base.EUR")
        amount = 3.00
        amount_text_it_zero_fractional = currency.with_context(
            lang="it_IT"
        ).amount_to_text(amount)
        self.assertEqual(amount_text_it_zero_fractional, "tre euro e zero centesimi")

    def test_05_currency_aed_amount_to_text(self):
        """check that amount_to_text works in italian language
        using a currency different from EUR/USD/GBP/CNY"""
        currency = self.env.ref("base.AED")
        amount = 1050.75
        amount_text_aed = currency.with_context(lang="it_IT").amount_to_text(amount)
        self.assertEqual(amount_text_aed, "millecinquanta dirham e settantacinque fils")
