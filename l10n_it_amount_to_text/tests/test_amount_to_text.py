# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th)
# Copyright 2022 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from num2words import num2words

from odoo.tests.common import SavepointCase


class TestAmountToText(SavepointCase):
    def test_01_currency_it_amount_to_text(self):
        """check that amount_to_text correctly converts text
        to italian language"""
        currency = self.env.ref("base.EUR")
        amount = 1050.75
        amount_text_en = currency.amount_to_text(amount)
        self.assertEqual(
            amount_text_en, "One Thousand And Fifty Euros and Seventy-Five Cents"
        )
        amount_text_it = currency.with_context({"lang": "it_IT"}).amount_to_text(amount)
        try:
            # num2words version 0.5.12+
            num2words(amount, to="currency", lang="it")
            self.assertEqual(
                amount_text_it, "millecinquanta euro e settantacinque centesimi"
            )
        except NotImplementedError:
            # num2words version 0.5.6 (core odoo)
            self.assertEqual(
                amount_text_it, "one thousand and fifty euro, seventy-five cents"
            )

    def test_02_currency_unit_it_amount_to_text(self):
        """check that amount_to_text correctly converts currency
        unit/subunit in italian language singular form"""
        currency = self.env.ref("base.EUR")
        amount = 1.01
        amount_text_it_unit = currency.with_context({"lang": "it_IT"}).amount_to_text(
            amount
        )
        self.assertEqual(amount_text_it_unit, "un euro e un centesimo")

    def test_03_currency_usd_amount_to_text(self):
        """check that amount_to_text works as expected"""
        currency = self.env.ref("base.USD")
        amount = 1050.75
        amount_text_usd = currency.amount_to_text(amount)
        self.assertEqual(
            amount_text_usd, "One Thousand And Fifty Dollars and Seventy-Five Cents"
        )
