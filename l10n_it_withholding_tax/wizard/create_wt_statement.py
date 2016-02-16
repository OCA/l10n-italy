# -*- coding: utf-8 -*-
# Copyright © 2015 Alessandro Camilli (<http://www.openforce.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp.osv import fields, orm
from openerp.tools.translate import _


class wizard_create_wt_statement(orm.TransientModel):

    def default_get(self, cr, uid, fields, context=None):

        move_obj = self.pool['account.move']
        res = super(wizard_create_wt_statement, self).default_get(
            cr, uid, fields, context=context)

        # Account moves selected
        active_ids = context and context.get('active_ids', [])
        if len(active_ids) > 1:
            raise orm.except_orm(_('Warning!'),
                                 _('You can choose Only ONE move.'))
        # Controllo se esiste già il movimento
        domain = [('move_id', '=', active_ids[0])]
        st_ids = self.pool['withholding.tax.statement'].search(cr, uid, domain)
        if st_ids:
            raise orm.except_orm(_('Warning!'),
                                 _('This Move is already present in the WT'))
        data = move_obj._prepare_wt_values(cr, uid, active_ids)
        res = data
        return res

    _name = "withholding.tax.wizard.create.statement"

    _columns = {

        'move_id': fields.many2one('account.move', 'Account Move',
                                   readonly=True),
        'partner_id': fields.many2one('res.partner', 'Partner',
                                      required=True),
        'date': fields.date('Date', required=True),
        'base': fields.float('Base'),
        'tax': fields.float('Tax'),
        'withholding_tax_id': fields.many2one(
            'withholding.tax', 'Withholding Tax', required=True),
        'wt_account_move_line_id': fields.many2one(
            'account.move.line', 'Account Move line', required=True),
        'amount': fields.float('WT amount')

    }

    def create_wt_statement(self, cr, uid, ids, context=None):

        for wiz in self.browse(cr, uid, ids):
            # Statement
            val = {
                'move_id': wiz.move_id.id,
                'date': wiz.date,
                'partner_id': wiz.partner_id.id,
                'withholding_tax_id': wiz.withholding_tax_id.id,
                'base': wiz.base,
                'tax': wiz.tax,
            }
            statement_id = self.pool['withholding.tax.statement'].create(
                cr, uid, val)
            # Moves
            val = {
                'statement_id': statement_id,
                'account_move_id': wiz.move_id.id,
                'date': wiz.date,
                'partner_id': wiz.partner_id.id,
                'move_line_id': wiz.wt_account_move_line_id.id,
                'withholding_tax_id': wiz.withholding_tax_id.id,
                'amount': wiz.amount,
            }
            self.pool['withholding.tax.move'].create(
                cr, uid, val)

        view_ref = self.pool.get('ir.model.data').get_object_reference(
            cr, uid, 'openforce_withholding_tax',
            'of_withholding_statement_view_form')
        return {
            'name': _('Withholding Tax Statement'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_ref[1] or False,
            'res_model': 'withholding.tax.statement',
            'res_id': statement_id or False,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'domain': '[]',
        }
