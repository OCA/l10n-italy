# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
# Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
# Copyright (C) 2012 Associazione Odoo Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2016 Andrea Cometa (Apulia Software)
# Email: a.cometa@apuliasoftware.it
# Copyright (C) 2016 KTec S.r.l.
# (<http://www.ktec.it>).
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################

from odoo import fields, models


class AccountPaymentTerm(models.Model):
    # flag riba utile a distinguere la modalità di pagamento
    _inherit = 'account.payment.term'
    
    riba = fields.Boolean('Riba', default=False)


class ResBankAddField(models.Model):
    _inherit = 'res.bank'
    banca_estera = fields.Boolean('Banca Estera')


class ResPartnerBankAdd(models.Model):
    _inherit = 'res.partner.bank'

    codice_sia = fields.Char(
        "SIA Code", size=5,
        help="Identification Code of the Company in the System Interbank")


# se distinta_line_ids == None allora non è stata emessa
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    distinta_line_ids = fields.One2many(
        'riba.distinta.move.line', 'move_line_id', "Dettaglio riba",
        default=None)
    riba = fields.Boolean(
        related='invoice.payment_term.riba', string='RiBa', store=False)
    unsolved_invoice_ids = fields.Many2many(
        'account.invoice', 'invoice_unsolved_line_rel', 'line_id',
        'invoice_id', 'Unsolved Invoices')
    iban = fields.Char(
        related='partner_id.bank_ids.iban', string='IBAN', store=False)

    def fields_view_get(
        self, cr, uid, view_id=None, view_type='form',
        context={}, toolbar=False, submenu=False
    ):
        # Special view for account.move.line object
        # (for ex. tree view contains user defined fields)
        # ToDO: da controllare
        result = super(AccountMoveLine, self).fields_view_get(
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
            return super(models.Model, self).fields_view_get(
                cr, uid, view_id, view_type, context, toolbar=toolbar,
                submenu=submenu)
        else:
            return result


class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    unsolved_move_line_ids = fields.Many2many(
        'account.move.line', 'invoice_unsolved_line_rel', 'invoice_id',
        'line_id', 'Unsolved journal items')
