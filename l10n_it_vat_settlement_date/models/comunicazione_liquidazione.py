from odoo import models


class ComunicazioneLiquidazioneVp(models.Model):
    _inherit = "comunicazione.liquidazione.vp"

    def _get_tax_context(self, period):
        res = super()._get_tax_context(period)
        res["use_l10n_it_vat_settlement_date"] = True
        return res
