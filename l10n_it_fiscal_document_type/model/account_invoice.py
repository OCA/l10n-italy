# -*- coding: utf-8 -*-

from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def onchange_partner_id(self, type, partner_id, date_invoice=False,
                            payment_term=False, partner_bank_id=False,
                            company_id=False):
        res = super(AccountInvoice, self).onchange_partner_id(
            type, partner_id, date_invoice, payment_term, partner_bank_id,
            company_id)
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            fiscal_position = partner.property_account_position
            res['value']['fiscal_document_type_id'] = \
                self._get_document_fiscal_type(
                    type=type, partner=partner,
                    fiscal_position=fiscal_position)[0] or False
        return res

    @api.multi
    def onchange_journal_id(self, journal_id=False):
        res = super(AccountInvoice, self).onchange_journal_id(
            journal_id=journal_id)
        if journal_id:
            journal = self.env['account.journal'].browse(journal_id)
            res['value']['fiscal_document_type_id'] = (
                self._get_document_fiscal_type(
                    journal=journal)[0] or False)
        return res

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
