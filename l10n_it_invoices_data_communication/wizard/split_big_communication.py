# -*- coding: utf-8 -*-

from odoo import api, models, exceptions, _


class SplitBigCommunication(models.TransientModel):
    _name = "wizard.split.big.invoices.communication"
    _description = "Split big invoices communication"

    @api.multi
    def split(self):
        comunicazione_ids = self._context.get('active_ids')
        communications = self.env['comunicazione.dati.iva'].browse(
            comunicazione_ids)
        communications.ensure_one()
        if not communications.check_1k_limit():
            res = communications.split_communications()
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'comunicazione.dati.iva',
                'domain': [('id', 'in', res.ids)],
            }
        else:
            raise exceptions.UserError(_(
                'Limit not exceeded. Split not needed'))
