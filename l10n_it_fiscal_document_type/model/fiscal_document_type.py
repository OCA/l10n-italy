# -*- coding: utf-8 -*-

from openerp import models, fields, tools


class FiscalDocumentType(models.Model):
    _name = 'fiscal.document.type'

    code = fields.Char(string='Codice', size=5)
    name = fields.Char(string='Nome', size=100)
    type = fields.Selection([
        ('out_invoice', 'Fattura vendita'),
        ('out_refund', 'Nota di credito'),
        ('in_invoice', 'Fattura acquisto'),
        ('in_refund', 'Nota di debito')
    ], string="Tipo"
    )
    journal_ids = fields.Many2many(
        'account.journal',
        'account_journal_fiscal_doc_type_rel',
        'fiscal_document_type_id',
        'journal_id',
        'Sezionali'
    )
