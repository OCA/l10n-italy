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

    invoice_date = fields.Date(
        string="Invoice/Bill Date", default=_get_default_invoice_date
    )
    invoice_method = fields.Selection(
        [("dn", "Only DN"), ("service", "With Service")],
        default="dn",
        required=True,
    )

    def create_invoices(self):
        delivery_note_ids = self.env["stock.delivery.note"].browse(
            self._context.get("active_ids", [])
        )
        if len(delivery_note_ids.mapped("partner_id")) > 1:
            raise UserError(_("You must select only delivery notes from one partner."))
        delivery_note_ids.action_invoice(self.invoice_method)
        invoices_ids = delivery_note_ids.mapped("invoice_ids")
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
        return {
            "name": invoices_ids.display_name,
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_type": "form",
            "view_mode": "form",
            "views": [[False, "form"]],
            "res_id": invoices_ids.id,
        }
