# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('partner_id', 'journal_id', 'type')
    def _set_document_fiscal_type(self):
        """
        - In base alla tipologia del documento vedere se nel partner è 
            impostato il tipo documento nella sezione acquisti o vendite
        - Se non c'è nulla nel partner, vedere se nella tabella esiste un
            elemento che risponda alla selezione x tipo documento e sezionale
        - Se non c'è nessuna relazione tipo documento-sezionale, cercare solo 
            x tipo documento.
        - Se non c'è nulla --> raise
        """
        dt = []
        doc_id = False
        if self.partner_id.id:
            if self.type in ('out_invoice', 'out_refund'):
                doc_id = self.partner_id.out_fiscal_document_type.id or False
            elif self.type in ('in_invoice', 'in_refund'):
                doc_id = self.partner_id.in_fiscal_document_type.id or False

        if not doc_id:
            dt = self.env['fiscal.document.type'].search(
                [('type', '=', self.type),
                 ('journal_id', '=', self.journal_id.id)], ).ids
        if not doc_id:
            dt = self.env['fiscal.document.type'].search(
                [('type', '=', self.type), ],).ids
        if doc_id:
            dt.append(doc_id)
        return {'domain': {'fiscal_document_type_id': [('id', 'in', dt)]}}

    fiscal_document_type_id = fields.Many2one(
        'fiscal.document.type',
        string="Tipo documento fiscale",
        required=True,
        readonly=False)
