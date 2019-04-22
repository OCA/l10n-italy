# -*- coding: utf-8 -*-

from odoo import models


class ComunicazioneLiquidazioneVp(models.Model):
    _inherit = 'comunicazione.liquidazione.vp'

    def _get_tax_context(self, period):
        context = super(
            ComunicazioneLiquidazioneVp, self)._get_tax_context(period)
        context['exclude_from_vat_statement_amount'] = True
        return context
