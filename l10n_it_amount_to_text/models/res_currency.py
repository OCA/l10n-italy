# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th)
# Copyright 2022 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from num2words import num2words

from odoo import models, tools


class Currency(models.Model):
    _inherit = "res.currency"

    def amount_to_text(self, amount):
        self.ensure_one()
        lang = tools.get_lang(self.env)
        lang_code = lang.code
        if lang_code != "it_IT":
            return super().amount_to_text(amount)

        def _num2words(number, lang):
            try:
                return num2words(number, lang=lang)
            except NotImplementedError:
                return num2words(number, lang="en")

        formatted_amount = f"%.{self.decimal_places}f" % amount
        parts = formatted_amount.partition(".")
        integer_value = int(parts[0])
        fractional_value = int(parts[2] or 0)

        # use num2words native 'currency' option to handle exceptions.
        # eg. 'uno euro' -> 'un euro', 'uno centesimi' -> 'un centesimo'"""
        try:
            return num2words(
                formatted_amount, to="currency", lang=lang.iso_code, currency=self.name
            )
        except NotImplementedError:
            num_words = _num2words(integer_value, lang=lang.iso_code)
            currency_label = self.currency_unit_label.lower()
            amount_words = f"{num_words} {currency_label}"

            if not self.is_zero(amount - integer_value):
                fractional_words = _num2words(fractional_value, lang=lang.iso_code)
                subunit_label = self.currency_subunit_label.lower()
                amount_words += f" e {fractional_words} {subunit_label}"

            return amount_words
