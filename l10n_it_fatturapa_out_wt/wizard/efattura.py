# Copyright 2021 Ciro Urselli <https://github.com/CiroBoxHub>
# Copyright 2021 Marco Colombo <https://github.com/TheMule71>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tools.float_utils import float_round

from odoo.addons.l10n_it_account.tools.account_tools import encode_for_export
from odoo.addons.l10n_it_fatturapa_out.wizard.efattura import (
    EFatturaOut as _EFatturaOut,
)

WT_TAX_CODE = {"inps": "RT03", "enasarco": "RT04", "enpam": "RT05", "other": "RT06"}


class EFatturaOut(_EFatturaOut):

    def get_template_values(self):
        """Add/override some functions used in the template"""

        template_values = super().get_template_values()
        format_numbers = template_values['format_numbers']

        def get_withholding_type(wt_types, partner):
            if wt_types == "ritenuta":
                if partner.is_company:
                    withholding_type = "RT02"
                else:
                    withholding_type = "RT01"
            else:
                withholding_type = WT_TAX_CODE[wt_types]
            return withholding_type

        def get_all_taxes_extend(record):
            """Generate summary data for taxes.
            Odoo does that for us, but only for nonzero taxes.
            SdI expects a summary for every tax mentioned in the invoice,
            even those with price_total == 0.
            """
            out_computed = {}
            # existing tax lines
            tax_ids = record.line_ids.filtered(lambda line: line.tax_line_id)
            for tax_id in tax_ids:
                tax_line_id = tax_id.tax_line_id
                aliquota = format_numbers(tax_line_id.amount)
                key = "{}_{}".format(aliquota, tax_line_id.kind_id.code)
                out_computed[key] = {
                    "AliquotaIVA": aliquota,
                    "Natura": tax_line_id.kind_id.code,
                    # 'Arrotondamento':'',
                    "ImponibileImporto": tax_id.tax_base_amount,
                    "Imposta": tax_id.price_total,
                    "EsigibilitaIVA": tax_line_id.payability,
                }
                if tax_line_id.law_reference:
                    out_computed[key]["RiferimentoNormativo"] = encode_for_export(
                        tax_line_id.law_reference, 100
                    )

            out = {}
            # check for missing tax lines
            for line in record.invoice_line_ids:
                if line.display_type in ("line_section", "line_note"):
                    # notes and sections
                    # we ignore line.tax_ids altogether,
                    # (it is popolated with a default tax usually)
                    # and use another tax in the template
                    continue
                for tax_id in line.tax_ids:
                    aliquota = format_numbers(tax_id.amount)
                    key = "{}_{}".format(aliquota, tax_id.kind_id.code)
                    if key in out_computed:
                        continue
                    if key not in out:
                        out[key] = {
                            "AliquotaIVA": aliquota,
                            "Natura": tax_id.kind_id.code,
                            # 'Arrotondamento':'',
                            "ImponibileImporto": line.price_subtotal,
                            "Imposta": 0.0,
                            "EsigibilitaIVA": tax_id.payability,
                        }
                        if tax_id.law_reference:
                            out[key]["RiferimentoNormativo"] = encode_for_export(
                                tax_id.law_reference, 100
                            )
                    else:
                        out[key]["ImponibileImporto"] += line.price_subtotal
                        out[key]["Imposta"] += 0.0

            wt_lines_to_write = record.withholding_tax_line_ids.filtered(
                lambda x: x.withholding_tax_id.wt_types not in ("ritenuta", "other")
                and x.withholding_tax_id.use_daticassaprev
            )
            for wt_line in wt_lines_to_write:
                tax_id = wt_line.withholding_tax_id.daticassprev_tax_id
                key = "{}_{}".format("0.00", tax_id.kind_id.code)   
                if key in out:
                    base_amount = (
                        float(out[key]["ImponibileImporto"]) + wt_line.tax
                    )
                    out[key]["ImponibileImporto"] = float_round(base_amount, 2)
                else:
                    out[key] = {
                        "AliquotaIVA": format_numbers(0.0),
                        "Natura": tax_id.kind_id.code,
                        # 'Arrotondamento':'',
                        "ImponibileImporto": float_round(wt_line.tax, 2),
                        "Imposta": 0.0,
                        "EsigibilitaIVA": tax_id.payability,
                    }
                    if tax_id.law_reference:
                        out[key]["RiferimentoNormativo"] = encode_for_export(
                            tax_id.law_reference, 100
                        )
            out.update(out_computed)
            return out

        template_values.update(
            {
                "get_withholding_type": get_withholding_type,
                "all_taxes": {
                    invoice.id: get_all_taxes_extend(
                        invoice) for invoice in self.invoices},
            }
        )

        return template_values
