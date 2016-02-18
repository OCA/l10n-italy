# -*- coding: utf-8 -*-
# Copyright © 2015 Alessandro Camilli (<http://www.openforce.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp.osv import orm, fields
from openerp.tools.translate import _
from openerp import netsvc
import logging

logger = logging.getLogger(__name__)


class wizard_wt_move_payment_create(orm.TransientModel):
    _name = 'wizard.wt.move.payment.create'
    _description = 'WT wizard create move payment'
    
    def default_get(self, cr, uid, fields, context=None):
        user_obj = self.pool['res.users']
        res = super(wizard_wt_move_payment_create, self).default_get(cr, uid, 
                                                    fields, context=context)
        # Partner-Company for domain of bank
        user = user_obj.browse(cr, uid, uid)
        # Selected
        active_ids = context and context.get('active_ids', [])
        res = {
            'wt_move_ids': active_ids
            }
        return res

    _columns = {
        'wt_move_ids': fields.many2many(
            'withholding.tax.move', 'wiz_wt_move_payment_create_rel', 'wizard_id',
            'wt_move_id', 'Wt Moves', readonly=True),
        }

    _defaults = {
        }

    def generate(self, cr, uid, ids, context=None):
        wt_move_ids = context.get('active_ids', [])
        wt_move_payment_obj = self.pool['withholding.tax.move.payment']
        res_id = wt_move_payment_obj.generate_from_moves(cr, uid, wt_move_ids)
        
        return {'type': 'ir.actions.act_window_close'}
        
    '''
    def cancel_sepa(self, cr, uid, ids, context=None):
        sepa_export = self.browse(cr, uid, ids[0], context=context)
        self.pool.get('banking.export.sepa').unlink(
            cr, uid, sepa_export.file_id.id, context=context)
        return {'type': 'ir.actions.act_window_close'}

    def save_sepa(self, cr, uid, ids, context=None):
        sepa_export = self.browse(cr, uid, ids[0], context=context)
        self.pool.get('banking.export.sepa').write(
            cr, uid, sepa_export.file_id.id, {'state': 'sent'},
            context=context)
        wf_service = netsvc.LocalService('workflow')
        for order in sepa_export.payment_order_ids:
            wf_service.trg_validate(uid, 'payment.order', order.id, 'done', cr)
        return {'type': 'ir.actions.act_window_close'}'''
