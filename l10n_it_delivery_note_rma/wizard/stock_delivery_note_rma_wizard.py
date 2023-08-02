from odoo import SUPERUSER_ID, api, fields, models


class StockDeliveryNoteRmaWizard(models.TransientModel):
    _name = "stock.delivery.note.rma.wizard"
    _description = "Stock Delivery Note Rma Wizard"

    def _domain_location_id(self):
        delivery_note = self.env["stock.delivery.note"].browse(
            self.env.context.get("active_id")
        )
        rma_loc = (
            self.env["stock.warehouse"]
            .search([("company_id", "=", delivery_note.company_id.id)])
            .mapped("rma_loc_id")
        )
        return [("id", "child_of", rma_loc.ids)]

    delivery_note_id = fields.Many2one(
        comodel_name="stock.delivery.note",
        default=lambda self: self.env.context.get("active_id", False),
    )
    line_ids = fields.One2many(
        comodel_name="stock.delivery.note.line.rma.wizard",
        inverse_name="wizard_id",
        string="Lines",
    )
    location_id = fields.Many2one(
        comodel_name="stock.location",
        string="RMA location",
        domain=_domain_location_id,
        default=lambda r: r.delivery_note_id.warehouse_id.rma_loc_id.id,
    )
    commercial_partner_id = fields.Many2one(
        comodel_name="res.partner",
        related="delivery_note_id.partner_id.commercial_partner_id",
        string="Commercial entity",
    )
    partner_shipping_id = fields.Many2one(
        comodel_name="res.partner",
        string="Shipping Address",
        help="Will be used to return the goods when the RMA is completed",
    )
    custom_description = fields.Text(
        help="Values coming from portal RMA request form custom fields",
    )

    def create_rma(self):
        self.ensure_one()
        user_has_group_portal = self.env.user.has_group(
            "base.group_portal"
        ) or self.env.user.has_group("base.group_public")
        lines = self.line_ids.filtered(lambda r: r.quantity > 0.0)
        val_list = [line._prepare_rma_values() for line in lines]
        rma_model = (
            self.env["rma"].with_user(SUPERUSER_ID)
            if user_has_group_portal
            else self.env["rma"]
        )
        rma = rma_model.create(val_list)
        return rma

    def create_and_open_rma(self):
        self.ensure_one()
        rma = self.create_rma()
        if not rma:
            return
        action = self.sudo().env.ref("rma.rma_action").read()[0]
        if len(rma) > 1:
            action["domain"] = [("id", "in", rma.ids)]
        elif rma:
            action.update(
                res_id=rma.id,
                view_mode="form",
                view_id=False,
                views=False,
            )
        return action


class StockDeliveryNoteLineRmaWizard(models.TransientModel):
    _name = "stock.delivery.note.line.rma.wizard"
    _description = "Stock Delivery Note Line Rma Wizard"

    partner_shipping_id = fields.Many2one(
        string="Shipping Address",
        comodel_name="res.partner",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Shipping address for current RMA.",
    )
    partner_invoice_id = fields.Many2one(
        string="Invoice Address",
        comodel_name="res.partner",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Refund address for current RMA.",
    )

    wizard_id = fields.Many2one(
        comodel_name="stock.delivery.note.rma.wizard", string="Wizard"
    )
    delivery_note_id = fields.Many2one(
        comodel_name="stock.delivery.note",
        default=lambda self: self.env["stock.delivery.note"].browse(
            self.env.context.get("active_id", False)
        ),
    )
    allowed_product_ids = fields.Many2many(
        comodel_name="product.product", compute="_compute_allowed_product_ids"
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        required=True,
        domain="[('id', 'in', allowed_product_ids)]",
    )
    uom_category_id = fields.Many2one(
        comodel_name="uom.category",
        related="product_id.uom_id.category_id",
    )
    quantity = fields.Float(
        string="Quantity",
        digits="Product Unit of Measure",
        required=True,
    )
    uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Unit of Measure",
        domain="[('category_id', '=', uom_category_id)]",
        required=True,
    )
    allowed_picking_ids = fields.Many2many(
        comodel_name="stock.picking", compute="_compute_allowed_picking_ids"
    )
    picking_id = fields.Many2one(
        comodel_name="stock.picking",
        string="Delivery order",
        domain="[('id', 'in', allowed_picking_ids)]",
    )
    move_id = fields.Many2one(comodel_name="stock.move", compute="_compute_move_id")
    operation_id = fields.Many2one(
        comodel_name="rma.operation",
        string="Requested operation",
    )
    delivery_note_line_id = fields.Many2one(
        comodel_name="stock.delivery.note.line",
    )
    sale_line_id = fields.Many2one(
        comodel_name="sale.order.line",
    )
    description = fields.Text()

    @api.onchange("product_id")
    def onchange_product_id(self):
        self.picking_id = False
        self.uom_id = self.product_id.uom_id

    @api.depends("picking_id")
    def _compute_move_id(self):
        for record in self:
            move_id = False
            if record.picking_id:
                move_id = record.picking_id.move_lines.filtered(
                    lambda r: (r.state == "done")
                )
            record.move_id = move_id[0]

    @api.depends("delivery_note_id")
    def _compute_allowed_product_ids(self):
        for record in self:
            product_ids = record.delivery_note_id.line_ids.mapped("product_id.id")
            record.allowed_product_ids = product_ids

    @api.depends("product_id")
    def _compute_allowed_picking_ids(self):
        for record in self:
            line = record.delivery_note_id.line_ids.filtered(
                lambda r: r.product_id == record.product_id
            )
            record.allowed_picking_ids = line.mapped("move_id.picking_id").filtered(
                lambda x: x.state == "done"
            )

    def _prepare_rma_values(self):
        self.ensure_one()
        description = (self.description or "") + (
            self.wizard_id.custom_description or ""
        )
        partner_invoice_id = False
        partner_shipping_id = False
        if self.delivery_note_id.partner_id:
            address = self.delivery_note_id.partner_id.address_get(
                ["invoice", "delivery"]
            )
            partner_invoice_id = address.get("invoice", False)
            partner_shipping_id = address.get("delivery", False)
        partner_rma_id = (
            self.delivery_note_id.sale_ids[0].partner_id
            if self.delivery_note_id.sale_ids
            else self.delivery_note_id.partner_id
        )
        self.partner_invoice_id = partner_invoice_id or self.delivery_note_id.partner_id
        self.partner_shipping_id = (
            partner_shipping_id or self.delivery_note_id.partner_id
        )
        self.partner_shipping_id = (
            self.wizard_id.partner_shipping_id or self.partner_shipping_id
        )
        return {
            "partner_id": partner_rma_id.id,
            "partner_invoice_id": self.partner_invoice_id.id,
            "partner_shipping_id": self.partner_shipping_id.id,
            "origin": self.delivery_note_id.name,
            "company_id": self.delivery_note_id.company_id.id,
            "location_id": self.wizard_id.location_id.id,
            "delivery_note_id": self.delivery_note_id.id,
            "picking_id": self.picking_id.id,
            "move_id": self.move_id.id,
            "product_id": self.product_id.id,
            "product_uom_qty": self.quantity,
            "product_uom": self.uom_id.id,
            "operation_id": self.operation_id.id,
            "description": description,
        }
