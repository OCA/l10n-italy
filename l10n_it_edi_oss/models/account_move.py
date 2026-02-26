# Copyright 2026 Lorenzo Battistini
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _l10n_it_edi_get_oss_line_values(
        self, aml, base_line, vat_tax, n7_tax, n22_tax
    ):
        # Prevent the native l10n_it_edi from splitting OSS lines into
        # base + VAT amount with incorrect Natura codes (N7 / N2.2).
        # Our grouping overrides handle OSS formatting on the original
        # single line (Natura N3.2, AltriDatiGestionali with actual rate).
        return [base_line]

    def _l10n_it_edi_is_oss_tax(self, tax):
        """Check if a tax is an EU OSS tax by the OSS tag on repartition lines."""
        oss_tag = self.env.ref("l10n_eu_oss.tag_oss", raise_if_not_found=False)
        return oss_tag and oss_tag in tax.invoice_repartition_line_ids.tag_ids

    @api.model
    def _l10n_it_edi_grouping_function_base_lines(self, base_line, tax_data):
        result = super()._l10n_it_edi_grouping_function_base_lines(base_line, tax_data)
        if result and tax_data and self._l10n_it_edi_is_oss_tax(tax_data["tax"]):
            result["tax_amount_field"] = 0.0
        return result

    @api.model
    def _l10n_it_edi_grouping_function_tax_lines(self, base_line, tax_data):
        result = super()._l10n_it_edi_grouping_function_tax_lines(base_line, tax_data)
        if result and tax_data and self._l10n_it_edi_is_oss_tax(tax_data["tax"]):
            result["tax_amount_field"] = 0.0
            result["is_oss"] = True
        return result

    def _l10n_it_edi_add_base_lines_xml_values(
        self, base_lines_aggregated_values, is_downpayment
    ):
        result = super()._l10n_it_edi_add_base_lines_xml_values(
            base_lines_aggregated_values, is_downpayment
        )
        for base_line, _aggregated_values in base_lines_aggregated_values:
            oss_taxes = base_line["tax_ids"].filtered(self._l10n_it_edi_is_oss_tax)
            if oss_taxes:
                base_line["it_values"]["altri_dati_gestionali_list"].append(
                    {
                        "tipo_dato": "OSS",
                        "riferimento_testo": f"{oss_taxes[0].amount:.2f}",
                        "riferimento_numero": None,
                        "riferimento_data": None,
                    }
                )
        return result

    def _l10n_it_edi_get_tax_lines_xml_values(
        self, base_lines_aggregated_values, values_per_grouping_key
    ):
        tax_lines = super()._l10n_it_edi_get_tax_lines_xml_values(
            base_lines_aggregated_values, values_per_grouping_key
        )
        # Set imposta to 0.0 for OSS entries.
        # Iterate values_per_grouping_key in the same order as super() to
        # correlate grouping keys with the returned tax_lines by index.
        idx = 0
        for values in values_per_grouping_key.values():
            grouping_key = values["grouping_key"]
            if not grouping_key or grouping_key.get("skip"):
                continue
            if grouping_key.get("is_oss") and idx < len(tax_lines):
                tax_lines[idx]["imposta"] = 0.0
            idx += 1
        return tax_lines
