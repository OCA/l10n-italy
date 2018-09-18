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
            dt = self.env['fiscal.document.type'].search([
                ('journal_ids', 'in', [journal.id])]).ids
            if dt:
                res['value']['fiscal_document_type_id'] = dt[0] or False
        return res

    def _get_document_fiscal_type(self, type=None, partner=None,
                                  fiscal_position=None):
        dt = []
        doc_id = False
        if not type:
            type = 'out_invoice'

        # Partner
        if partner:
            # out_refund and in_refund would be managed together as out_refund
            # but creating another field in partner
            if type == 'out_invoice':
                doc_id = partner.out_fiscal_document_type.id or False
            elif type == 'in_invoice':
                doc_id = partner.in_fiscal_document_type.id or False
        # Fiscal Position
        if not doc_id and fiscal_position:
            doc_id = fiscal_position.fiscal_document_type_id.id or False
        if not doc_id and not dt:
            # A 'nota di debito' is a particular case of invoice, not refund.
            # So it is registered as an out_invoice by the vendor, and an
            # in_invoice by the customer. This case can be managed only by hand
            if type == 'in_refund':
                type = 'out_refund'
            dt = self.env['fiscal.document.type'].search([
                (type, '=', True)]).ids
        if doc_id:
            dt.append(doc_id)
        return dt

    fiscal_document_type_id = fields.Many2one(
        'fiscal.document.type',
        string="Tipo documento fiscale",
        readonly=False)
