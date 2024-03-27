# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    delivery_note_id = fields.Many2one(
        "stock.delivery.note",
        store=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
        string="Delivery Note",
        help="Auto-complete from a past delivery note.",
    )

    @api.onchange("delivery_note_id")
    def _onchange_delivery_note_auto_complete(self):
        """
        Load from an old delivery note.
        The non-stored field must be empty at the end of this function.
        """
        if not self.delivery_note_id:
            return
        # Copy data from DN
        invoice_vals = self.delivery_note_id.with_company(
            self.delivery_note_id.company_id
        )._prepare_vendor_invoice()
        invoice_vals["currency_id"] = (
            self.line_ids and self.currency_id or invoice_vals.get("currency_id")
        )
        del invoice_vals["ref"]
        self.update(invoice_vals)

        # Copy DN lines.
        dn_lines = self.delivery_note_id.line_ids - self.line_ids.mapped(
            "delivery_note_line_id"
        )
        new_lines = self.env["account.move.line"]
        sequence = max(self.line_ids.mapped("sequence")) + 1 if self.line_ids else 10
        for line in dn_lines.filtered(lambda l: not l.display_type):
            line_vals = line._prepare_vendor_move_line(self)
            line_vals.update({"sequence": sequence})
            new_line = new_lines.new(line_vals)
            sequence += 1
            new_line.account_id = new_line._get_computed_account()
            new_line._onchange_price_subtotal()
            new_lines += new_line
        new_lines._onchange_mark_recompute_taxes()

        # Compute invoice_origin.
        origins = set(
            self.line_ids.mapped("delivery_note_line_id.delivery_note_id.name")
        )
        self.invoice_origin = ",".join(list(origins))

        # Compute ref.
        refs = self._get_invoice_reference()
        self.ref = ", ".join(refs)

        # Compute payment_reference.
        if len(refs) == 1:
            self.payment_reference = refs[0]

        self.delivery_note_id = False
        self._onchange_currency()
