# -*- coding: utf-8 -*-
# Copyright © 2015 Alessandro Camilli (<http://www.openforce.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp.osv import orm, fields


class wizard_wt_move_payment_create(orm.TransientModel):
    _name = 'wizard.wt.move.payment.create'
    _description = 'WT wizard create move payment'

    def default_get(self, cr, uid, fields, context=None):
        res = super(wizard_wt_move_payment_create, self).default_get(
            cr, uid, fields, context=context)
        # Partner-Company for domain of bank
        # Selected
        active_ids = context and context.get('active_ids', [])
        res = {
            'wt_move_ids': active_ids
        }
        return res

    _columns = {
        'wt_move_ids': fields.many2many(
            'withholding.tax.move', 'wiz_wt_move_payment_create_rel',
            'wizard_id', 'wt_move_id', 'Wt Moves', readonly=True),
    }

    _defaults = {
    }

    def generate(self, cr, uid, ids, context=None):
        wt_move_ids = context.get('active_ids', [])
        wt_move_payment_obj = self.pool['withholding.tax.move.payment']
        wt_move_payment_obj.generate_from_moves(cr, uid, wt_move_ids)

        return {'type': 'ir.actions.act_window_close'}
