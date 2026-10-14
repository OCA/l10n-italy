# Copyright 2026 Lorenzo Battistini
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models

from ..constants import OSS_EXEMPT_REASON, OSS_LAW_REFERENCE


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
            # OSS taxes have amount > 0, so the l10n_it constraint requiring
            # exoneration fields on 0% taxes does not cover them: without a
            # fallback, forcing AliquotaIVA to 0.00 on a tax missing these
            # fields would emit no Natura and be rejected by SDI (error 00400).
            result["l10n_it_exempt_reason"] = (
                result["l10n_it_exempt_reason"] or OSS_EXEMPT_REASON
            )
            result["l10n_it_law_reference"] = (
                result["l10n_it_law_reference"] or OSS_LAW_REFERENCE
            )
        return result

    def _l10n_it_edi_add_base_lines_xml_values(
        self, base_lines_aggregated_values, is_downpayment
    ):
        result = super()._l10n_it_edi_add_base_lines_xml_values(
            base_lines_aggregated_values, is_downpayment
        )
        for base_line, _aggregated_values in base_lines_aggregated_values:
            oss_taxes = (
                base_line["tax_ids"]
                .flatten_taxes_hierarchy()
                .filtered(self._l10n_it_edi_is_oss_tax)
            )
            if oss_taxes:
                it_values = base_line["it_values"]
                # Same SDI consistency requirement as in the tax lines
                # grouping: AliquotaIVA 0.00 requires a Natura code.
                it_values["natura"] = it_values["natura"] or OSS_EXEMPT_REASON
                it_values["altri_dati_gestionali_list"].append(
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
        # super() builds one entry per non-skipped grouping key, in
        # values_per_grouping_key order: pair them explicitly.
        grouping_keys = [
            values["grouping_key"]
            for values in values_per_grouping_key.values()
            if values["grouping_key"] and not values["grouping_key"].get("skip")
        ]
        for grouping_key, tax_line in zip(grouping_keys, tax_lines, strict=False):
            if grouping_key.get("is_oss"):
                tax_line["imposta"] = 0.0
        return tax_lines
