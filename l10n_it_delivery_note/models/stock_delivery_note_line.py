# Copyright 2022 Dinamiche Aziendali srl
# (http://www.dinamicheaziendali.it/)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import UserError

DATE_FORMAT = "%d/%m/%Y"
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"

LINE_DISPLAY_TYPES = [("line_section", "Section"), ("line_note", "Note")]
DOMAIN_LINE_DISPLAY_TYPES = [t[0] for t in LINE_DISPLAY_TYPES]

INVOICE_STATUSES = [
    ("no", "Nothing to invoice"),
    ("to invoice", "To invoice"),
    ("invoiced", "Fully invoiced"),
]
DOMAIN_INVOICE_STATUSES = [s[0] for s in INVOICE_STATUSES]


class StockDeliveryNoteLine(models.Model):
    _name = "stock.delivery.note.line"
    _description = "Delivery Note Line"
    _order = "sequence, id"

    def _default_currency(self):
        return self.env.company.currency_id

    def _default_unit_uom(self):
        return self.env.ref("uom.product_uom_unit", raise_if_not_found=False)

    delivery_note_id = fields.Many2one(
        "stock.delivery.note", string="Delivery Note", required=True, ondelete="cascade"
    )
    company_id = fields.Many2one(
        "res.company",
        related="delivery_note_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
    sequence = fields.Integer(required=True, default=10, index=True)
    name = fields.Text(string="Description", required=True)
    display_type = fields.Selection(
        LINE_DISPLAY_TYPES, string="Line type", default=False
    )
    product_id = fields.Many2one("product.product", string="Product")
    product_description = fields.Text(related="product_id.description_sale")
    product_qty = fields.Float(
        string="Quantity", digits="Product Unit of Measure", default=1.0
    )
    product_uom_id = fields.Many2one("uom.uom", string="UoM", default=_default_unit_uom)
    price_unit = fields.Float(string="Unit price", digits="Product Price")
    currency_id = fields.Many2one(
        "res.currency", string="Currency", required=True, default=_default_currency
    )
    discount = fields.Float(digits="Discount")
    tax_ids = fields.Many2many("account.tax", string="Taxes")

    move_id = fields.Many2one(
        "stock.move",
        string="Warehouse movement",
        readonly=True,
        copy=False,
        check_company=True,
    )
    sale_line_id = fields.Many2one(
        "sale.order.line", related="move_id.sale_line_id", store=True, copy=False
    )
    sale_order_number = fields.Char(
        compute="_compute_sale_order_number",
        store=True,
    )
    sale_order_client_ref = fields.Char(
        "Customer Reference",
        compute="_compute_sale_order_client_ref",
        store=True,
    )
    invoice_status = fields.Selection(
        INVOICE_STATUSES,
        string="Invoice status",
        required=True,
        default=DOMAIN_INVOICE_STATUSES[0],
        copy=False,
    )

    _sql_constraints = [
        (
            "move_uniq",
            "unique(move_id)",
            "You cannot assign the same warehouse movement to "
            "different delivery notes!",
        )
    ]

    @property
    def is_invoiceable(self):
        return self.invoice_status == DOMAIN_INVOICE_STATUSES[1]

    @api.depends("sale_line_id.order_id.name")
    def _compute_sale_order_number(self):
        for sdnl in self:
            sdnl.sale_order_number = sdnl.sale_line_id.order_id.name or ""

    @api.depends("sale_line_id.order_id.client_order_ref")
    def _compute_sale_order_client_ref(self):
        for sdnl in self:
            sdnl.sale_order_client_ref = (
                sdnl.sale_line_id.order_id.client_order_ref or ""
            )

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            name = self.product_id.name
            if self.product_id.description_sale:
                name += "\n" + self.product_id.description_sale

            self.name = name

            product_uom_domain = [
                ("category_id", "=", self.product_id.uom_id.category_id.id)
            ]

        else:
            product_uom_domain = []

        return {"domain": {"product_uom_id": product_uom_domain}}

    @api.model
    def _prepare_detail_lines(self, moves):
        lines = []
        for move in moves:
            name = move.product_id.name
            if move.product_id.description_sale:
                name += "\n" + move.product_id.description_sale

            line = {
                "move_id": move.id,
                "name": name,
                "product_id": move.product_id.id,
                "product_qty": move.quantity,
                "product_uom_id": move.product_uom.id,
            }

            if move.sale_line_id:
                order_line = move.sale_line_id
                order = order_line.order_id

                line["price_unit"] = order_line.price_unit
                line["currency_id"] = order.currency_id.id
                line["discount"] = order_line.discount
                line["tax_ids"] = [(6, False, order_line.tax_id.ids)]
                line["invoice_status"] = DOMAIN_INVOICE_STATUSES[1]

            lines.append(line)

        return lines

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("display_type"):
                vals.update(
                    {
                        "product_id": False,
                        "product_qty": 0.0,
                        "product_uom_id": False,
                        "price_unit": 0.0,
                        "discount": 0.0,
                        "tax_ids": [(5, False, False)],
                    }
                )
        return super().create(vals_list)

    def write(self, vals):
        if "display_type" in vals and self.filtered(
            lambda note_line: note_line.display_type != vals["display_type"]
        ):
            raise UserError(
                self.env._(
                    "You cannot change the type of a delivery note line. "
                    "Instead you should delete the current line"
                    " and create a new line of the proper type."
                )
            )

        return super().write(vals)

    def sync_invoice_status(self):
        for line in self.filtered(lambda note_line: note_line.sale_line_id):
            invoice_status = line.sale_line_id.invoice_status
            line.invoice_status = (
                DOMAIN_INVOICE_STATUSES[1]
                if invoice_status == "upselling"
                else invoice_status
            )
