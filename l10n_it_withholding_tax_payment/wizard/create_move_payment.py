# -*- coding: utf-8 -*-
# Copyright © 2015 Alessandro Camilli (<http://www.openforce.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models, fields, api


class WizardWtMovePaymentCreate(models.TransientModel):
    _name = 'wizard.wt.move.payment.create'
    _description = 'WT wizard create move payment'

    @api.model
    def default_get(self, fields):
        res = super(WizardWtMovePaymentCreate, self).default_get(fields)
        active_ids = self._context.get('active_ids', [])
        res = {
            'wt_move_ids': active_ids
        }
        return res

    wt_move_ids = fields.Many2many(
        'withholding.tax.move', 'wiz_wt_move_payment_create_rel',
        'wizard_id', 'wt_move_id', 'Wt Moves', readonly=True)

    def generate(self):
        wt_move_payment_obj = self.env['withholding.tax.move.payment']
        wt_move_payment_obj.generate_from_moves(self.wt_move_ids)

        return {'type': 'ir.actions.act_window_close'}
