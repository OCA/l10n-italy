# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.exceptions import UserError


class StockDeliveryNote(models.Model):
    _inherit = "stock.delivery.note"

    def _prepare_vendor_invoice(self):
        move_type = self._context.get("default_move_type", "in_invoice")
        journal = (
            self.env["account.move"]
            .with_context(default_move_type=move_type)
            ._get_default_journal()
        )
        if not journal:
            raise UserError(
                _(
                    "Please define an accounting purchase journal for the company %s (%s)."
                )
                % (self.company_id.name, self.company_id.id)
            )

        partner_invoice_id = self.partner_sender_id.commercial_partner_id.address_get(
            ["invoice"]
        )["invoice"]
        partner_bank_id = (
            self.partner_sender_id.commercial_partner_id.bank_ids.filtered_domain(
                [
                    "|",
                    ("company_id", "=", False),
                    ("company_id", "=", self.company_id.id),
                ]
            )[:1]
        )
        invoice_vals = {
            "ref": self.partner_ref or "",
            "move_type": move_type,
            "narration": self.env["ir.fields.converter"].text_from_html(self.note),
            "currency_id": self.line_ids.mapped("currency_id")[:1].id,
            "invoice_user_id": self.env.user.id,
            "partner_id": partner_invoice_id,
            "fiscal_position_id": self.env["account.fiscal.position"]
            .get_fiscal_position(partner_invoice_id)
            .id,
            "payment_reference": self.partner_ref or "",
            "partner_bank_id": partner_bank_id.id,
            "invoice_origin": self.name,
            "company_id": self.company_id.id,
        }
        return invoice_vals
