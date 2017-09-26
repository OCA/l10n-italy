# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('partner_id', 'journal_id', 'type', 'fiscal_position_id')
    def _set_document_fiscal_type(self):
        dt = self._get_document_fiscal_type(
            self.type, self.partner_id, self.fiscal_position_id,
            self.journal_id)
        if len(dt) == 1:
            self.fiscal_document_type_id = dt[0]

    def _get_document_fiscal_type(self, type=None, partner=None,
                                  fiscal_position=None, journal=None):
        dt = []
        doc_id = False
        if not type:
            type = 'out_invoice'

        # Partner
        if partner:
            if type in ('out_invoice', 'out_refund'):
                doc_id = partner.out_fiscal_document_type.id or False
            elif type in ('in_invoice', 'in_refund'):
                doc_id = partner.in_fiscal_document_type.id or False
        # Fiscal Position
        if not doc_id and fiscal_position:
            doc_id = fiscal_position.fiscal_document_type_id.id or False
        # Journal
        if not doc_id and journal:
            dt = self.env['fiscal.document.type'].search([
                ('journal_ids', 'in', [journal.id])]).ids
        if not doc_id and not dt:
            dt = self.env['fiscal.document.type'].search([
                (type, '=', True)]).ids
        if doc_id:
            dt.append(doc_id)
        return dt

    fiscal_document_type_id = fields.Many2one(
        'fiscal.document.type',
        string="Tipo documento fiscale",
        readonly=False)
