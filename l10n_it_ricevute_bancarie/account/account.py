# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2012 Andrea Cometa.
#    Email: info@andreacometa.it
#    Web site: http://www.andreacometa.it
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2012 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv
from tools.translate import _


class account_payment_term(osv.osv):
    # flag riba utile a distinguere la modalità di pagamento
    _inherit = 'account.payment.term'
    
    _columns = {
        'riba' : fields.boolean('Riba'),
    }
    _defaults = {
        'riba': False,
    }
account_payment_term()

class res_bank_add_field(osv.osv):
    _inherit = 'res.bank'
    _columns = {
        'banca_estera' : fields.boolean('Banca Estera'),
    }
res_bank_add_field()

class res_partner_bank_add(osv.osv):
    _inherit = 'res.partner.bank'
    _columns = {
        'codice_sia' : fields.char('Codice SIA', size=5, help="Identification Code of the Company in the System Interbank")    
    }
res_partner_bank_add()

# se distinta_line_ids == None allora non è stata emessa
class account_move_line(osv.osv):
    _inherit = "account.move.line"

    _columns = {
        'distinta_line_ids' : fields.one2many('riba.distinta.move.line', 'move_line_id', "Dettaglio riba"),
        'riba': fields.related('invoice', 'payment_term', 'riba', 
            type='boolean', string='RiBa', store=False),
        'unsolved_invoice_ids': fields.many2many('account.invoice', 'invoice_unsolved_line_rel', 'line_id', 'invoice_id', 'Unsolved Invoices'),
        'iban' : fields.related('partner_id', 'bank_ids', 'iban', type='char', string='IBAN', store=False),
    }
    _defaults = {
        'distinta_line_ids' : None,
    }

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context={}, toolbar=False, submenu=False):
        view_payments_tree_id = self.pool.get('ir.model.data').get_object_reference(
            cr, uid, 'l10n_it_ricevute_bancarie', 'view_riba_da_emettere_tree')
        if view_id == view_payments_tree_id[1]:
            # Use RiBa list - grazie a eLBati @ account_due_list
            result = super(osv.osv, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar=toolbar, submenu=submenu)
        else:
            # Use special views for account.move.line object (for ex. tree view contains user defined fields)
            result = super(account_move_line, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar=toolbar, submenu=submenu)
        return result

account_move_line()

class account_invoice(osv.osv):
    _inherit = "account.invoice"
    _columns = {
        'unsolved_move_line_ids': fields.many2many('account.move.line', 'invoice_unsolved_line_rel', 'invoice_id', 'line_id', 'Unsolved journal items'),
        }

    def action_cancel(self, cr, uid, ids, context=None):
        invoices = self.browse(cr, uid, ids, context=context)
        for invoice in invoices:
            # we get move_lines with date_maturity and check if they are
            # present in some riba_distinta_line
            move_line_model = self.pool['account.move.line']
            rdml_model = self.pool['riba.distinta.move.line']
            move_line_ids = move_line_model.search(
                cr, uid, [('move_id', '=', invoice.move_id.id),
                          ('date_maturity', '!=', False)])
            if move_line_ids:
                riba_line_ids = rdml_model.search(
                    cr, uid, [('move_line_id', '=', move_line_ids)])
                if riba_line_ids:
                    if isinstance(riba_line_ids, list):
                        riba_line_ids = riba_line_ids[0]
                    distinta = rdml_model.browse(cr, uid, riba_line_ids)
                    raise osv.except_osv(
                        _('Attention!'),
                        _('Invoice is linked to RI.BA. list nr {}').format(
                            distinta.riba_line_id.distinta_id.name
                        ))
        res = super(account_invoice, self).action_cancel(cr, uid, ids, context)
        return res
