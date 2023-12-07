from odoo import api, models
from odoo.tools.float_utils import float_round

from odoo.addons.l10n_it_account.tools.account_tools import encode_for_export
from odoo.addons.l10n_it_fatturapa_out.wizard.wizard_export_fatturapa import (
    format_numbers,
)


class WizardExportFatturapa(models.TransientModel):
    WT_TAX_CODE = {"inps": "RT03", "enasarco": "RT04", "enpam": "RT05", "other": "RT06"}

    _inherit = "wizard.export.fatturapa"

    @api.model
    def getAllTaxes(self, invoice):
        def _key(tax_id):
            return tax_id.id

        res = super().getAllTaxes(invoice)
        wt_lines_to_write = invoice.withholding_tax_line_ids.filtered(
            lambda x: x.withholding_tax_id.wt_types not in ("ritenuta", "other")
            and x.withholding_tax_id.use_daticassaprev
        )
        for wt_line in wt_lines_to_write:
            tax_id = wt_line.withholding_tax_id.daticassprev_tax_id
            key = _key(tax_id)
            if key in res:
                base_amount = float(res[key]["ImponibileImporto"]) + wt_line.tax
                res[key]["ImponibileImporto"] = float_round(base_amount, 2)
            else:
                res[key] = {
                    "AliquotaIVA": format_numbers(0.0),
                    "Natura": tax_id.kind_id.code,
                    # possibile tag (non gestito)
                    # 'Arrotondamento':'',
                    "ImponibileImporto": float_round(wt_line.tax, 2),
                    "Imposta": 0.0,
                    "EsigibilitaIVA": tax_id.payability,
                }
                if tax_id.law_reference:
                    res[key]["RiferimentoNormativo"] = encode_for_export(
                        tax_id.law_reference, 100
                    )
        return res

    @api.model
    def getPayments(self, invoice):
        payments = super().getPayments(invoice)
        wt_hack_rate = (
            invoice.amount_net_pay / invoice.amount_total
            if invoice.withholding_tax_line_ids
            else 1.0
        )
        for payment in payments:
            payment.amount_currency *= wt_hack_rate
            payment.debit *= wt_hack_rate
        return payments

    @api.model
    def getWithholdingType(self, wt_types, partner):
        if wt_types == "ritenuta":
            if partner.is_company:
                withholding_type = "RT02"
            else:
                withholding_type = "RT01"
        else:
            withholding_type = self.WT_TAX_CODE[wt_types]
        return withholding_type

    @api.model
    def getTemplateValues(self, template_values):
        def get_withholding_type(wt_types, partner):
            return self.getWithholdingType(wt_types, partner)

        template_values = super().getTemplateValues(template_values)
        template_values.update({"get_withholding_type": get_withholding_type})
        return template_values
