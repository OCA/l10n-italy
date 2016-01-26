# -*- coding: utf-8 -*-
#
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
#

from openerp.osv import fields, orm


class account_payment_term(orm.Model):
    # flag riba utile a distinguere la modalità di pagamento
    _inherit = 'account.payment.term'

    _columns = {
        'riba': fields.boolean('Riba'),
    }
    _defaults = {
        'riba': False,
    }


class res_bank_add_field(orm.Model):
    _inherit = 'res.bank'
    _columns = {
        'banca_estera': fields.boolean('Banca Estera'),
    }


class res_partner_bank_add(orm.Model):
    _inherit = 'res.partner.bank'
    _columns = {
        'codice_sia': fields.char(
            'Codice SIA', size=5,
            help="Identification Code of the Company in the System Interbank")
    }


# se distinta_line_ids == None allora non è stata emessa
class account_move_line(orm.Model):
    _inherit = "account.move.line"

    _columns = {
        'distinta_line_ids': fields.one2many(
            'riba.distinta.move.line', 'move_line_id', "Dettaglio riba"),
        'riba': fields.related('invoice', 'payment_term', 'riba',
                               type='boolean', string='RiBa', store=False),
        'unsolved_invoice_ids': fields.many2many(
            'account.invoice', 'invoice_unsolved_line_rel', 'line_id',
            'invoice_id', 'Unsolved Invoices'),
        'iban': fields.related(
            'partner_id', 'bank_ids', 'iban', type='char', string='IBAN',
            store=False),
    }
    _defaults = {
        'distinta_line_ids': None,
    }

    def fields_view_get(
        self, cr, uid, view_id=None, view_type='form',
        context=None, toolbar=False, submenu=False
    ):
        # Special view for account.move.line object
        # (for ex. tree view contains user defined fields)
        result = super(account_move_line, self).fields_view_get(
            cr, uid, view_id, view_type, context, toolbar=toolbar,
            submenu=submenu)
        try:
            view_payments_tree_id = self.pool.get(
                'ir.model.data').get_object_reference(
                cr, uid, 'l10n_it_ricevute_bancarie',
                'view_riba_da_emettere_tree')
        except ValueError:
            return result
        if view_id == view_payments_tree_id[1]:
            # Use RiBa list - grazie a eLBati @ account_due_list
            return super(orm.Model, self).fields_view_get(
                cr, uid, view_id, view_type, context, toolbar=toolbar,
                submenu=submenu)
        else:
            return result


class account_invoice(orm.Model):

    def _get_is_unsolved(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            res[invoice.id] = False
            reconciled_unsolved = 0
            for unsolved_move_line in invoice.unsolved_move_line_ids:
                if unsolved_move_line.reconcile_id:
                    reconciled_unsolved += 1
            if len(invoice.unsolved_move_line_ids) != reconciled_unsolved:
                res[invoice.id] = True
        return res

    def _get_invoice_by_move_line(self, cr, uid, ids, context=None):
        result = []
        for move_line in self.pool['account.move.line'].browse(
            cr, uid, ids, context=context
        ):
            result.extend([i.id for i in move_line.unsolved_invoice_ids])
        return list(set(result))

    _inherit = "account.invoice"
    _columns = {
        'unsolved_move_line_ids': fields.many2many(
            'account.move.line', 'invoice_unsolved_line_rel', 'invoice_id',
            'line_id', 'Unsolved journal items'),
        'is_unsolved': fields.function(
            _get_is_unsolved, type='boolean',
            string="The unsolved is open",
            store={
                'account.invoice': (
                    lambda self, cr, uid, ids, c={}: ids, [
                        'unsolved_move_line_ids'], 10
                ),
                'account.move.line': (_get_invoice_by_move_line, [
                    'unsolved_invoice_ids', 'reconcile_id'], 10),
            }
        ),
    }
