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

        def get_withholding_type(wt_types, partner):
            if wt_types == "ritenuta":
                if partner.is_company:
                    withholding_type = "RT02"
                else:
                    withholding_type = "RT01"
            else:
                withholding_type = WT_TAX_CODE[wt_types]
            return withholding_type

        def get_all_taxes(record):
            template_values = super(EFatturaOut, self).get_template_values()
            _get_all_taxes = template_values["get_all_taxes"]
            format_numbers = template_values["format_numbers"]

            all_taxes = _get_all_taxes(record)

            wt_lines_to_write = record.withholding_tax_line_ids.filtered(
                lambda x: x.withholding_tax_id.wt_types not in ("ritenuta", "other")
                and x.withholding_tax_id.use_daticassaprev
            )
            for wt_line in wt_lines_to_write:
                tax_id = wt_line.withholding_tax_id.daticassprev_tax_id
                key = "{}_{}".format("0.00", tax_id.kind_id.code)
                if key in all_taxes:
                    base_amount = (
                        float(all_taxes[key]["ImponibileImporto"]) + wt_line.tax
                    )
                    all_taxes[key]["ImponibileImporto"] = float_round(base_amount, 2)
                else:
                    all_taxes[key] = {
                        "AliquotaIVA": format_numbers(0.0),
                        "Natura": tax_id.kind_id.code,
                        # 'Arrotondamento':'',
                        "ImponibileImporto": float_round(wt_line.tax, 2),
                        "Imposta": 0.0,
                        "EsigibilitaIVA": tax_id.payability,
                    }
                    if tax_id.law_reference:
                        all_taxes[key]["RiferimentoNormativo"] = encode_for_export(
                            tax_id.law_reference, 100
                        )
            return all_taxes

        template_values = super().get_template_values()
        template_values.update(
            {
                "get_withholding_type": get_withholding_type,
                "get_all_taxes": get_all_taxes,
            }
        )

        return template_values
