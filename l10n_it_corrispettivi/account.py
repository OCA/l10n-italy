# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>). 
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv
from tools.translate import _

class account_invoice(osv.osv):
    _inherit = 'account.invoice'
    _columns = {
        'corrispettivo': fields.boolean('Corrispettivo'),
        }

    def _get_journal(self, cr, uid, context=None):
        if context is None:
            context = {}
        res = False
        is_corrispettivo = context.get('corrispettivo', False)
        corr_journal = self.pool.get('ir.model.data').get_object(
            cr, uid, 'l10n_it_corrispettivi', 'journal_corrispettivi', context)
        if is_corrispettivo:
            res = corr_journal.id
        else:
            type_inv = context.get('type', 'out_invoice')
            user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
            company_id = context.get('company_id', user.company_id.id)
            type2journal = {'out_invoice': 'sale', 'in_invoice': 'purchase', 'out_refund': 'sale_refund', 'in_refund': 'purchase_refund'}
            refund_journal = {'out_invoice': False, 'in_invoice': False, 'out_refund': True, 'in_refund': True}
            journal_obj = self.pool.get('account.journal')
            res = journal_obj.search(cr, uid, [('type', '=', type2journal.get(type_inv, 'sale')),
                                                ('company_id', '=', company_id),
                                                ('refund_journal', '=', refund_journal.get(type_inv, False))])
            if corr_journal.id in res:
                res.remove(corr_journal.id)
            res = res and res[0] or False
        return res

    def _get_account(self, cr, uid, context=None):
        if context is None:
            context = {}
        is_corrispettivo = context.get('corrispettivo', False)
        res = False
        if is_corrispettivo:
            partner = self.pool.get('ir.model.data').get_object(
                cr, uid, 'l10n_it_corrispettivi', 'partner_corrispettivi', context)
            res = partner.property_account_receivable.id
        return res

    def _get_partner_id(self, cr, uid, context=None):
        if context is None:
            context = {}
        is_corrispettivo = context.get('corrispettivo', False)
        res = False
        if is_corrispettivo:
            partner = self.pool.get('ir.model.data').get_object(
                cr, uid, 'l10n_it_corrispettivi', 'partner_corrispettivi', context)
            res = partner.id
        return res

    def _get_address_invoice_id(self, cr, uid, context=None):
        if context is None:
            context = {}
        is_corrispettivo = context.get('corrispettivo', False)
        res = False
        if is_corrispettivo:
            partner = self.pool.get('ir.model.data').get_object(
                cr, uid, 'l10n_it_corrispettivi', 'partner_corrispettivi', context)
            if not partner.address:
                raise orm.except_orm(_('Error!'), 
                     _('No address specified for partner %s') % partner.name)
            res = partner.address[0].id
        return res

    _defaults = {
        'partner_id': _get_partner_id,
        'address_invoice_id': _get_address_invoice_id,
        'journal_id': _get_journal,
        'account_id': _get_account,
        }

account_invoice()
