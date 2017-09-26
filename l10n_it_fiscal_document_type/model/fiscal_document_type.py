# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FiscalDocumentType(models.Model):
    _name = 'fiscal.document.type'

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

    @api.model
    def create(self, vals):
        res = super(FiscalDocumentType, self).create(vals)
        res.journal_ids.check_doc_type_relation()
        return res

    @api.multi
    def write(self, vals):
        res = super(FiscalDocumentType, self).write(vals)
        for doc in self:
            doc.journal_ids.check_doc_type_relation()
        return res
