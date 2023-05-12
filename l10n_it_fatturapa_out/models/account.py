# Copyright 2014 Davide Corio
# Copyright 2016 Lorenzo Battistini - Agile Business Group

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_is_zero
from odoo.tools.translate import _

fatturapa_attachment_state_mapping = {
    "ready": "ready",
    "sent": "sent",
    "validated": "delivered",
    "sender_error": "error",
    "recipient_error": "accepted",
    "accepted": "accepted",
    "rejected": "error",
}


class AccountInvoice(models.Model):
    _inherit = "account.move"

    fatturapa_attachment_out_id = fields.Many2one(
        "fatturapa.attachment.out", "E-invoice Export File", readonly=True, copy=False
    )

    has_pdf_invoice_print = fields.Boolean(
        related="fatturapa_attachment_out_id.has_pdf_invoice_print", readonly=True
    )

    fatturapa_state = fields.Selection(
        [
            ("ready", "Ready to Send"),
            ("sent", "Sent"),
            ("delivered", "Delivered"),
            ("accepted", "Accepted"),
            ("error", "Error"),
        ],
        string="E-invoice State",
        compute="_compute_fatturapa_state",
        store="true",
    )

    @api.depends("fatturapa_attachment_out_id.state")
    def _compute_fatturapa_state(self):
        for record in self:
            record.fatturapa_state = fatturapa_attachment_state_mapping.get(
                record.fatturapa_attachment_out_id.state
            )

    def preventive_checks(self):
        def _check_taxes(invoice):
            if not all(
                aml.tax_ids for aml in invoice.invoice_line_ids if aml.product_id
            ):
                raise UserError(
                    _("Invoice %s contains product lines w/o taxes") % invoice.name
                )

            # see odoo/addons/account/models/account_tax.py
            # amount is defined as fields.Float(digits=(16, 4), ...)
            for tax in invoice.invoice_line_ids.tax_ids.filtered(
                lambda t: float_is_zero(t.amount, precision_digits=4)
            ):
                if not tax.kind_id:
                    raise UserError(
                        _(
                            "Invoice %(invoice)s: a tax exemption kind"
                            " must be specified for tax %(tax)s"
                        )
                        % {"invoice": invoice.name, "tax": tax.name}
                    )
                if not tax.law_reference:
                    raise UserError(
                        _(
                            "Invoice %(invoice)s: the law reference"
                            " must be specified for tax %(tax)s"
                        )
                        % {"invoice": invoice.name, "tax": tax.name}
                    )

        for invoice in self:
            if not invoice.is_sale_document():
                raise UserError(
                    _("Impossible to generate XML: not a customer invoice: %s")
                    % invoice.name
                )

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

            _check_taxes(invoice)

            company_id = invoice.company_id
            if company_id.vat != company_id.partner_id.vat:
                raise UserError(
                    _("Invoice %s: company and company partner must have same vat")
                    % invoice.name
                )
        return

    def button_draft(self):
        for invoice in self:
            if (
                invoice.fatturapa_state != "error"
                and invoice.fatturapa_attachment_out_id
            ):
                raise UserError(
                    _(
                        "Invoice %s has XML and can't be reset to draft. "
                        "Delete the XML before."
                    )
                    % invoice.name
                )
        res = super(AccountInvoice, self).button_draft()
        return res
