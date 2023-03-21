from odoo import api, fields, models


class Rma(models.Model):
    _inherit = "rma"

    delivery_note_id = fields.Many2one(
        comodel_name="stock.delivery.note",
        string="Delivery Note",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    allowed_picking_ids = fields.Many2many(
        comodel_name="stock.picking",
        compute="_compute_allowed_picking_ids",
    )
    picking_id = fields.Many2one()

    allowed_move_ids = fields.Many2many(
        comodel_name="stock.delivery.note.line",
        compute="_compute_allowed_move_ids",
    )
    move_id = fields.Many2one()
    allowed_product_ids = fields.Many2many(
        comodel_name="product.product",
        compute="_compute_allowed_product_ids",
    )
    product_id = fields.Many2one()

    @api.depends("partner_id", "delivery_note_id")
    def _compute_allowed_picking_ids(self):
        for rec in self:
            if not rec.partner_id:
                rec.allowed_picking_ids = False  # don't populate a big list
            else:
                commercial_partner = rec.partner_id.commercial_partner_id
                domain = [
                    ("state", "=", "done"),
                    ("picking_type_id.code", "=", "outgoing"),
                    ("partner_id", "child_of", commercial_partner.id),
                ]
                rec.allowed_picking_ids = self.env["stock.picking"].search(domain)

    @api.depends("delivery_note_id", "picking_id")
    def _compute_allowed_move_ids(self):
        for rec in self:
            if rec.delivery_note_id:
                delvery_note_move = rec.delivery_note_id.line_ids.mapped("move_id")
                rec.allowed_move_ids = delvery_note_move.filtered(
                    lambda r: r.picking_id == self.picking_id and r.state == "done"
                ).ids
            else:
                rec.allowed_move_ids = self.picking_id.move_lines.ids

    @api.depends("delivery_note_id")
    def _compute_allowed_product_ids(self):
        for rec in self:
            if rec.delivery_note_id:
                rec.allowed_product_ids = (
                    rec.delivery_note_id.line_ids.filtered(
                        lambda r: r.product_id.type in ["consu", "product"]
                    )
                    .mapped("product_id")
                    .ids
                )
            else:
                rec.allowed_product_ids = False  # don't populate a big list

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        super()._onchange_partner_id()
        self.delivery_note_id = False

    @api.onchange("delivery_note_id")
    def _onchange_delivery_note_id(self):
        self.product_id = self.picking_id = False

    def _prepare_refund(self, invoice_form, origin):
        """Inject user from delivery note (if any)"""
        res = super()._prepare_refund(invoice_form, origin)
        if self.delivery_note_id:
            invoice_form.invoice_user_id = self.delivery_note_id.activity_user_id
        return res
