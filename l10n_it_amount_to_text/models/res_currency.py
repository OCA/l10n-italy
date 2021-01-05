# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th)
# Copyright 2022 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from num2words import num2words

from odoo import models, tools

CURRENCY_NAME = {"Dollars": "dollari", "Euros": "euro", "Cents": "centesimi"}


class Currency(models.Model):
    _inherit = "res.currency"

    def _convert_currency_name_hook(self, label):
        """Hooks to add currency translation.
        Currently supported currencies are USD and EUR"""
        return CURRENCY_NAME[label]

    def amount_to_text(self, amount):
        self.ensure_one()
        lang_code = self.env.context.get("lang") or False
        if lang_code != "it_IT":
            return super().amount_to_text(amount)

        formatted = "%.{}f".format(self.decimal_places) % amount
        parts = formatted.partition(".")
        integer_value = int(parts[0])
        fractional_value = int(parts[2] or 0)
        lang = (
            self.env["res.lang"]
            .with_context(active_test=False)
            .search([("code", "=", lang_code)])
        )
        currency_unit_label = self._convert_currency_name_hook(self.currency_unit_label)
        amount_words = tools.ustr("{amt_value} {amt_word}").format(
            amt_value=num2words(integer_value, lang=lang.iso_code),
            amt_word=currency_unit_label,
        )
        if not self.is_zero(amount - integer_value):
            currency_subunit_label = self._convert_currency_name_hook(
                self.currency_subunit_label
            )
            amount_words += (
                " "
                + "e"
                + tools.ustr(" {amt_value} {amt_word}").format(
                    amt_value=num2words(fractional_value, lang=lang.iso_code),
                    amt_word=currency_subunit_label,
                )
            )
        return amount_words
