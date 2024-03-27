# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockDeliveryNoteLine(models.Model):
    _inherit = "stock.delivery.note.line"

    @api.model
    def _prepare_detail_lines(self, moves):
        """
        l10n_it_delivery_note does not depend on module purchase
        so it doesn't fill DN lines with the same
        price, currency, and taxes as the PO
        We need the fields properly filled for the invoice
        """
        lines = super()._prepare_detail_lines(moves)
        for move in moves:
            if move.sale_line_id or not move.purchase_line_id:
                continue
            line = next(line for line in lines if line["move_id"] == move.id)
            order_line = move.purchase_line_id
            order = order_line.order_id
            line["price_unit"] = order_line.price_unit
            line["currency_id"] = order.currency_id.id
            line["tax_ids"] = [(6, False, order_line.taxes_id.ids)]
        return lines

    def _prepare_vendor_move_line(self, move=False):
        self.ensure_one()
        aml_currency = move and move.currency_id or self.currency_id
        date = move and move.date or fields.Date.today()
        res = {
            "display_type": self.display_type,
            "sequence": self.sequence,
            "name": "%s: %s" % (self.delivery_note_id.name, self.name),
            "product_id": self.product_id.id,
            "product_uom_id": self.product_uom_id.id,
            "quantity": self.product_qty,
            "price_unit": self.currency_id._convert(
                self.price_unit, aml_currency, self.company_id, date, round=False
            ),
            "tax_ids": [(6, 0, self.tax_ids.ids)],
            "purchase_line_id": self.move_id.purchase_line_id.id,
            "delivery_note_line_id": self.id,
        }
        if not move:
            return res

        if self.currency_id == move.company_id.currency_id:
            currency = False
        else:
            currency = move.currency_id

        res.update(
            {
                "move_id": move.id,
                "currency_id": currency and currency.id or False,
                "date_maturity": move.invoice_date_due,
                "partner_id": move.partner_id.id,
            }
        )
        return res
