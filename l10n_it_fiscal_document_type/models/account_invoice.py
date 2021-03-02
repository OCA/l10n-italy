from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    @api.depends('partner_id', 'journal_id', 'type', 'fiscal_position_id')
    def _set_document_fiscal_type(self):
        for invoice in self:
            if invoice.state != 'draft':
                continue
            dt = invoice._get_document_fiscal_type(
                invoice.type, invoice.partner_id, invoice.fiscal_position_id,
                invoice.journal_id)
            if dt:
                invoice.fiscal_document_type_id = dt[0]

    def _get_document_fiscal_type(self, type=None, partner=None,
                                  fiscal_position=None, journal=None):
        dt = []
        doc_id = False
        if not type:
            type = 'out_invoice'

        # Partner
        if partner:
            if type in ('out_invoice'):
                doc_id = partner.out_fiscal_document_type.id or False
            elif type in ('in_invoice'):
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
        # Refund Document type
        if (dt or doc_id) and 'refund' in type:
            fdt = self.env['fiscal.document.type'].browse(doc_id or dt[0])
            if fdt and not fdt.out_refund\
                    and not fdt.in_refund\
                    and fdt.refund_fiscal_document_type_id:
                if dt:
                    dt[0] = fdt.refund_fiscal_document_type_id.id
                else:
                    dt.append(fdt.refund_fiscal_document_type_id.id)
        if doc_id:
            dt.append(doc_id)
        return dt

    fiscal_document_type_id = fields.Many2one(
        'fiscal.document.type',
        string="Fiscal Document Type",
        compute='_set_document_fiscal_type',
        store=True,
        readonly=False)
