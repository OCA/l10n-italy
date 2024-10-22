# Copyright 2019 Simone Rubino - Agile Business Group
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models
from odoo.tools import float_is_zero


class WizardExportFatturaPA(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def _get_efattura_class(self):
        efattura_class = super()._get_efattura_class()

        class EInvoiceOutTripleDiscount(efattura_class):
            def get_template_values(self):
                template_values = super().get_template_values()

                format_numbers_two = template_values["format_numbers_two"]

                def get_triple_ScontoMaggiorazione_values_list(line):
                    ScontoMaggiorazione_values_list = []

                    discount_fields = line._get_multiple_discount_field_names()

                    discounts_digits = line.fields_get(
                        allfields=discount_fields,
                        attributes=[
                            "digits",
                        ],
                    )
                    for discount_field in discount_fields:
                        discount_perc = line[discount_field]
                        all_digits, precision_digits = discounts_digits[discount_field][
                            "digits"
                        ]
                        is_discount_zero = float_is_zero(
                            discount_perc,
                            precision_digits=precision_digits,
                        )
                        if not is_discount_zero:
                            ScontoMaggiorazione_values = {
                                "Tipo": "SC",
                                "Percentuale": format_numbers_two(discount_perc),
                            }
                            ScontoMaggiorazione_values_list.append(
                                ScontoMaggiorazione_values
                            )
                    return ScontoMaggiorazione_values_list

                template_values[
                    "get_triple_ScontoMaggiorazione_values_list"
                ] = get_triple_ScontoMaggiorazione_values_list
                return template_values

        return EInvoiceOutTripleDiscount
