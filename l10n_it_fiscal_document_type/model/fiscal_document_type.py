# -*- coding: utf-8 -*-

from openerp import models, fields


class FiscalDocumentType(models.Model):
    _name = 'fiscal.document.type'

    code = fields.Char(string='Codice', size=5)
    name = fields.Char(string='Nome', size=100)
    code = fields.Char(string='Codice', size=5)
    name = fields.Char(string='Nome', size=100)
    out_invoice = fields.Boolean(string='Fattura vendita')
    in_invoice = fields.Boolean(string='Fattura acquisto')
    out_refund = fields.Boolean(string='Nota di credito')
    in_refund = fields.Boolean(string='Nota di debito')
    priority = fields.Integer(string='Priority', default='3')


    journal_ids = fields.Many2many(
        'account.journal',
        'account_journal_fiscal_doc_type_rel',
        'fiscal_document_type_id',
        'journal_id',
        'Sezionali'
    )

    _order = 'code, priority asc'
