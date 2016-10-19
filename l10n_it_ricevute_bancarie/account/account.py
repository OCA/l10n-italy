# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) 2016 Andrea Cometa (Apulia Software)
# Email: a.cometa@apuliasoftware.it
# Web site: http://www.apuliasoftware.it
# Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
# Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
# Copyright (C) 2012 Associazione Odoo Italia
# (<http://www.odoo-italia.org>).
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################

from odoo import fields, models

class account_payment_term(orm.Model):
    # flag riba utile a distinguere la modalità di pagamento
    _inherit = 'account.payment.term'
    
    _columns = {
        'riba' : fields.boolean('Riba'),
    }
    _defaults = {
        'riba': False,
    }


class res_bank_add_field(orm.Model):
    _inherit = 'res.bank'
    _columns = {
        'banca_estera' : fields.boolean('Banca Estera'),
    }


class res_partner_bank_add(orm.Model):
    _inherit = 'res.partner.bank'
    _columns = {
        'codice_sia' : fields.char('Codice SIA', size=5, help="Identification Code of the Company in the System Interbank")    
    }


# se distinta_line_ids == None allora non è stata emessa
class account_move_line(orm.Model):
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

    def fields_view_get(
        self, cr, uid, view_id=None, view_type='form',
        context={}, toolbar=False, submenu=False
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
    _inherit = "account.invoice"
    _columns = {
        'unsolved_move_line_ids': fields.many2many('account.move.line', 'invoice_unsolved_line_rel', 'invoice_id', 'line_id', 'Unsolved journal items'),
        }
