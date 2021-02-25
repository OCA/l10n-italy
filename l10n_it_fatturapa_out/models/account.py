# Copyright 2014 Davide Corio
# Copyright 2016 Lorenzo Battistini - Agile Business Group

from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools.translate import _

fatturapa_attachment_state_mapping = {
    'ready': 'ready',
    'sent': 'sent',
    'validated': 'delivered',
    'sender_error': 'error',
    'recipient_error': 'accepted',
    'accepted': 'accepted',
    'rejected': 'error'
}


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fatturapa_attachment_out_id = fields.Many2one(
        'fatturapa.attachment.out', 'E-invoice Export File',
        readonly=True, copy=False)

    has_pdf_invoice_print = fields.Boolean(
        related='fatturapa_attachment_out_id.has_pdf_invoice_print',
        readonly=True)

    fatturapa_state = fields.Selection(
        [
            ('ready', 'Ready to Send'),
            ('sent', 'Sent'),
            ('delivered', 'Delivered'),
            ('accepted', 'Accepted'),
            ('error', 'Error'),
        ],
        string='E-invoice State',
        compute='_compute_fatturapa_state',
        store='true',
    )

    @api.multi
    @api.depends('fatturapa_attachment_out_id.state')
    def _compute_fatturapa_state(self):
        for record in self:
            record.fatturapa_state = fatturapa_attachment_state_mapping.get(
                record.fatturapa_attachment_out_id.state
            )

    def preventive_checks(self):
        # hook for preventive checks. Override and raise exception, in case
        return

    @api.multi
    def action_invoice_cancel(self):
        for invoice in self:
            if (
                invoice.fatturapa_state != "error"
                and invoice.fatturapa_attachment_out_id
                and not self.env.context.get("skip_e_invoice_cancel_check")
            ):
                raise UserError(_(
                    "Invoice %s has XML and can't be canceled. "
                    "Delete the XML before."
                ) % invoice.number)
        res = super(AccountInvoice, self).action_invoice_cancel()
        return res

    def get_first_non_zero_tax(self):
        for line in self.invoice_line_ids:
            if (
                not line.display_type and line.price_subtotal and
                len(line.invoice_line_tax_ids) == 1
            ):
                return line.invoice_line_tax_ids[0]
        return False

    def set_taxes_for_descriptive_lines(self):
        for line in self.invoice_line_ids:
            if line.display_type:
                non_zero_tax = self.get_first_non_zero_tax()
                if non_zero_tax:
                    line.invoice_line_tax_ids = [(6, 0, [non_zero_tax.id])]
