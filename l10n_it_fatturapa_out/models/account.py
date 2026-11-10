# Copyright 2014 Davide Corio
# Copyright 2016 Lorenzo Battistini - Agile Business Group
# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

from .company import E_INVOICE_HIDE_LINE_TYPE_SELECTION

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
    fatturapa_payment_method_id = fields.Many2one(
        comodel_name="fatturapa.payment_method",
        string="Fiscal Payment Method",
        help="Fiscal Payment Method used in the e-invoice, "
        "defaults to the Payment Term's Fiscal Payment Method.",
        compute="_compute_fatturapa_payment_term_data",
        store=True,
        readonly=False,
    )
    fatturapa_payment_term_id = fields.Many2one(
        comodel_name="fatturapa.payment_term",
        string="Fiscal Payment Term",
        help="Fiscal Payment Term used in the e-invoice, "
        "defaults to the Payment Term's Fiscal Payment Term.",
        compute="_compute_fatturapa_payment_term_data",
        store=True,
        readonly=False,
    )
    e_invoice_hide_line_type = fields.Selection(
        selection=E_INVOICE_HIDE_LINE_TYPE_SELECTION,
        help="Choose which type of descriptive line "
        "will not be present in the e-invoice.\n"
        "If empty, the same field in the partner is evaluated.",
    )

    @api.depends("fatturapa_attachment_out_id.state")
    def _compute_fatturapa_state(self):
        for record in self:
            record.fatturapa_state = fatturapa_attachment_state_mapping.get(
                record.fatturapa_attachment_out_id.state
            )

    @api.depends(
        "invoice_payment_term_id",
    )
    def _compute_fatturapa_payment_term_data(self):
        for invoice in self:
            payment_term = invoice.invoice_payment_term_id
            invoice.fatturapa_payment_method_id = (
                payment_term.fatturapa_pm_id or invoice.fatturapa_payment_method_id
            )
            invoice.fatturapa_payment_term_id = (
                payment_term.fatturapa_pt_id or invoice.fatturapa_payment_term_id
            )

    def preventive_checks(self):
        for invoice in self:
            if not invoice.is_sale_document():
                raise UserError(
                    _("Impossible to generate XML: not a customer invoice: %s")
                    % invoice.name
                )

            if not all(
                aml.tax_ids for aml in invoice.invoice_line_ids if aml.product_id
            ):
                raise UserError(
                    _("Invoice %s contains product lines w/o taxes") % invoice.name
                )
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
        res = super().button_draft()
        return res
