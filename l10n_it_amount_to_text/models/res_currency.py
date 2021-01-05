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

        formatted_amount = "%.{}f".format(self.decimal_places) % amount
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
            amount_words = tools.ustr("{amt_value} {amt_word}").format(
                amt_value=_num2words(integer_value, lang=lang.iso_code),
                amt_word=self.currency_unit_label.lower(),
            )
            if not self.is_zero(amount - integer_value):
                amount_words += (
                    " "
                    + "e"
                    + tools.ustr(" {amt_value} {amt_word}").format(
                        amt_value=_num2words(fractional_value, lang=lang.iso_code),
                        amt_word=self.currency_subunit_label.lower(),
                    )
                )
            return amount_words
