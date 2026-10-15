# Copyright (C) 2018-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# Copyright (c) 2024, Nextev Srl <odoo@nextev.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

INVOICE_STATUSES = [
    ("no", "Nothing to invoice"),
    ("to invoice", "To invoice"),
    ("invoiced", "Fully invoiced"),
]
DOMAIN_INVOICE_STATUSES = [s[0] for s in INVOICE_STATUSES]


class StockDeliveryNoteInvoiceWizard(models.TransientModel):
    _name = "stock.delivery.note.invoice.wizard"
    _description = "Delivery Note Invoice"

    @api.model
    def _get_default_invoice_date(self):
        return fields.Date.context_today(self)

    @api.model
    def _get_default_has_down_payments(self):
        dn_ids = self.env["stock.delivery.note"].browse(
            self.env.context.get("active_ids", [])
        )
        if dn_ids:
            return bool(dn_ids.mapped("sale_ids.order_line").filtered("is_downpayment"))

    invoice_date = fields.Date(
        string="Invoice/Bill Date", default=_get_default_invoice_date
    )
    invoice_method = fields.Selection(
        [("dn", "Only DN"), ("service", "With Service")],
        default="dn",
        required=True,
    )

    # Down Payment logic
    has_down_payments = fields.Boolean(
        string="Has down payments", default=_get_default_has_down_payments
    )
    deduct_down_payments = fields.Boolean(string="Deduct down payments", default=True)

    def create_invoices(self):
        delivery_note_ids = self.env["stock.delivery.note"].browse(
            self._context.get("active_ids", [])
        )
        if len(delivery_note_ids.mapped("partner_id")) > 1:
            raise UserError(_("You must select only delivery notes from one partner."))
        delivery_note_ids.action_invoice(
            invoice_method=self.invoice_method, final=self.deduct_down_payments
        )
        invoices_ids = delivery_note_ids.mapped("invoice_ids")
        if not invoices_ids:
            raise UserError(
                _("You must select only delivery notes with SO associated.")
            )
        for invoice in invoices_ids:
            invoice.invoice_date = self.invoice_date
        if len(invoices_ids) > 1:
            return {
                "name": _("Invoices"),
                "type": "ir.actions.act_window",
                "res_model": "account.move",
                "view_type": "list",
                "view_mode": "list",
                "views": [[False, "list"], [False, "form"]],
                "domain": [("id", "in", invoices_ids.ids)],
            }
        elif len(invoices_ids) == 1:
            return {
                "name": invoices_ids.display_name,
                "type": "ir.actions.act_window",
                "res_model": "account.move",
                "view_type": "form",
                "view_mode": "form",
                "views": [[False, "form"]],
                "res_id": invoices_ids.id,
            }
