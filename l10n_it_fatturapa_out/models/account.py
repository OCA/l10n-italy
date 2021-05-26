# Copyright 2014 Davide Corio
# Copyright 2016 Lorenzo Battistini - Agile Business Group


from odoo import fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class AccountInvoice(models.Model):
    _inherit = "account.move"

    fatturapa_attachment_out_id = fields.Many2one(
        "fatturapa.attachment.out", "E-invoice Export File", readonly=True, copy=False
    )

    has_pdf_invoice_print = fields.Boolean(
        related="fatturapa_attachment_out_id.has_pdf_invoice_print", readonly=True
    )

    def preventive_checks(self):
        for invoice in self:
            if (
                invoice.invoice_payment_term_id
                and invoice.invoice_payment_term_id.fatturapa_pt_id.code is False
            ):
                raise UserError(
                    _(
                        "Invoice %s fiscal payment term must be"
                        " set for the selected payment term %s",
                        invoice.name,
                        invoice.invoice_payment_term_id.name,
                    )
                )

            if (
                invoice.invoice_payment_term_id
                and invoice.invoice_payment_term_id.fatturapa_pm_id.code is False
            ):
                raise UserError(
                    _(
                        "Invoice %s fiscal payment method must be"
                        " set for the selected payment term %s",
                        invoice.name,
                        invoice.invoice_payment_term_id.name,
                    )
                )
        return

    def action_invoice_cancel(self):
        for invoice in self:
            if invoice.fatturapa_attachment_out_id:
                raise UserError(
                    _(
                        "Invoice %s has XML and can't be canceled. "
                        "Delete the XML before."
                    )
                    % invoice.number
                )
        res = super(AccountInvoice, self).action_invoice_cancel()
        return res
