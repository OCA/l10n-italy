# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.tools import float_is_zero


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _l10n_it_edi_add_base_lines_xml_values(
        self, base_lines_aggregated_values, is_downpayment
    ):
        res = super()._l10n_it_edi_add_base_lines_xml_values(
            base_lines_aggregated_values, is_downpayment
        )
        for base_line, _aggregated_values in base_lines_aggregated_values:
            vat_tax = (
                base_line["tax_ids"]
                .flatten_taxes_hierarchy()
                .filtered(lambda t: t._l10n_it_filter_kind("vat") and t.amount >= 0)[:1]
            )

            if vat_tax.oss_country_id:
                base_line["it_values"]["oss_country_id"] = vat_tax.oss_country_id

                vat_tax_amount = "%.*f" % (
                    2,
                    vat_tax.amount
                    if not float_is_zero(vat_tax.amount, precision_digits=2)
                    else 0.0,
                )
                base_line["it_values"]["altri_dati_gestionali_list"].extend(
                    [
                        {
                            "tipo_dato": "OSS",
                            "riferimento_testo": vat_tax_amount,
                            "riferimento_numero": None,
                            "riferimento_data": None,
                        },
                    ]
                )
        return res

    def _l10n_it_edi_get_tax_lines_xml_values(
        self, base_lines_aggregated_values, values_per_grouping_key
    ):
        tax_lines = super()._l10n_it_edi_get_tax_lines_xml_values(
            base_lines_aggregated_values, values_per_grouping_key
        )

        values_without_skip = {
            k: v
            for k, v in values_per_grouping_key.items()
            if v.get("grouping_key", False) and not v["grouping_key"].get("skip", False)
        }

        for tax_line, values in zip(
            tax_lines, values_without_skip.values(), strict=True
        ):
            tax_line["oss_country_id"] = values["grouping_key"].get(
                "oss_country_id", None
            )

        return tax_lines

    @api.model
    def _l10n_it_edi_grouping_function_tax_lines(self, base_line, tax_data):
        res = super()._l10n_it_edi_grouping_function_tax_lines(base_line, tax_data)
        if not tax_data:
            return None
        tax = tax_data["tax"]

        res["oss_country_id"] = tax.oss_country_id or None

        return res
