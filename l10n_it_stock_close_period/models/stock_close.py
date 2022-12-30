# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class StockClosePeriod(models.Model):
    _name = "stock.close.period"
    _description = "Stock Close Period"

    name = fields.Char(
        string="Reference",
        readonly=True,
        required=True,
        states={"draft": [("readonly", False)], "confirm": [("readonly", False)]})
    line_ids = fields.One2many(
        "stock.close.period.line",
        "close_id",
        string="Product",
        copy=True,
        readonly=False,
        states={"done": [("readonly", True)]})
    state = fields.Selection([
        ("draft", "Draft"),
        ("confirm", "In Progress"),
        ("done", "Validated"),
        ("cancel", "Cancelled")
    ], copy=False, index=True, readonly=True, default="draft", string="Status")
    close_date = fields.Date(
        "Close Date",
        readonly=True,
        required=True,
        default=fields.Date.context_today,
        states={"draft": [("readonly", False)], "confirm": [("readonly", False)]},
        help="The date that will be used for the store the product quantity and average cost.")
    amount = fields.Float(string="Stock Amount Value", readonly=True, copy=False)
    work_start = fields.Datetime("Work Start", readonly=True, default=fields.Datetime.now)
    work_end = fields.Datetime("Work End", readonly=True)
    force_evaluation_method = fields.Selection([
        ("no_force", "No Force"),
        ("purchase", "Purchase"),
        ("standard", "Standard")
    ], string="Force Evaluation method", default="no_force", copy=False,
        help="Force Evaluation method will be used only for compute purchase costs.")
    force_archive = fields.Boolean(
        default=False,
        help="Marks as archive the inventory move lines used during the process.")
    purchase_ok = fields.Boolean(default=False, readonly=True, help="Marks if action 'Compute Purchase' is processed.")
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.user.company_id)

    @api.model
    def create(self, values):
        if self._check_existing():
            closing_id = False
        else:
            closing_id = super(StockClosePeriod, self).create(values)
        return closing_id

    @api.multi
    def unlink(self):
        if self.state in ["confirm", "done"]:
            raise UserError(_(
                "State in '%s'. You can only delete in state 'Draft' or 'Cancelled'." % self.state
            ))
        return super(StockClosePeriod, self).unlink()

    def _check_existing(self):
        existings = self.search([("state", "=", "confirm"), ("company_id", "=", self.company_id.id)])
        if existings:
            raise UserError(_("You cannot have two stock closing in state 'in Progress'"))
        return existings

    def action_set_to_draft(self):
        if self.state == "cancel":
            # clear data
            wcpl = self.env["stock.close.period.line"].search([("close_id", "=", self.id)])
            if wcpl:
                wcpl.unlink()
            self.state = "draft"
            self.amount = 0
            self.purchase_ok = False

    def action_start(self):
        if not self._check_existing():
            for closing in self.filtered(lambda x: x.state not in ("done", "cancel")):
                # add product line
                closing._get_product_lines()
                # set confirm status
                self.state = "confirm"
        return True

    def _get_product_lines(self):
        # add all products actived not services type
        query = """
            INSERT INTO 
                stock_close_period_line(
                    close_id,
                    product_id,
                    product_code,
                    product_name,
                    product_uom_id,
                    categ_name,
                    product_qty,
                    price_unit
                )
            SELECT
                %r AS close_id,
                product_product.id AS product_id,
                product_template.default_code AS product_code,
                product_template.name AS product_name,
                product_template.uom_id AS product_uom,   
                product_category.complete_name AS complete_name,
                0 AS product_qty,
                0 AS price_unit
            FROM
                product_template,
                product_product,
                product_category
            WHERE
                -- product_template.active = True AND
                product_template.type != 'service' AND
                product_product.product_tmpl_id = product_template.id AND
                product_template.categ_id = product_category.id AND
                (product_template.company_id = %r OR product_template.company_id IS NULL)
            ORDER BY
                product_product.id;
        """ % (self.id, self.company_id.id)
        self.env.cr.execute(query)

        # get quantity on end period for each product
        closing_line_ids = self.env["stock.close.period.line"].search([("close_id", "=", self.id)])

        for closing_line_id in closing_line_ids:
            # giacenza fine periodo
            product_id = closing_line_id.product_id
            list_product_qty = product_id._compute_qty_available(self.close_date)
            count = 0
            for line in list_product_qty:
                if count == 0:
                    closing_line_id.product_qty = line["stock_at_date"]
                    closing_line_id.location_id = line["location_id"]
                    closing_line_id.lot_id = line["lot_id"]
                    closing_line_id.owner_id = line["owner_id"]
                else:
                    self.env["stock.close.period.line"].create({
                        "close_id": self.id,
                        "product_id": line["product_id"],
                        "product_uom_id": line["uom_id"],
                        "product_qty": line["stock_at_date"],
                        "location_id": line["location_id"],
                        "lot_id": line["lot_id"],
                        "owner_id": line["owner_id"],
                        "price_unit": 0
                    })
                count += 1

    def action_recalculate_purchase(self):
        if not self._check_qty_available():
            raise UserError(_("Is not possible continue the execution. There are product with quantities < 0."))

        self.env["stock.move.line"].recompute_average_cost_period_purchase()
        self.purchase_ok = True
        if self.force_archive:
            self._deactivate_moves()
        self.work_end = datetime.now()
        return True

    def action_cancel(self):
        self.state = "cancel"
        return True

    def action_force_done(self):
        for closing in self:
            closing.state = "done"
            closing.amount = sum(closing.mapped("line_ids.amount_line"))

    def action_done(self):
        self.state = "done"
        self.amount = sum(self.mapped("line_ids.amount_line"))
        query = """
            DELETE FROM
                stock_close_period_line
            WHERE
                close_id = %s
                AND product_qty = 0
                AND price_unit = 0;
        """ % self.id
        self.env.cr.execute(query)
        return True

    def action_recompute_amount(self):
        for closing in self:
            closing.amount = sum(closing.mapped("line_ids.amount_line"))

    def _check_qty_available(self):
        # if a negative value, can't continue
        negative = self.env["stock.close.period.line"].search([("close_id", "=", self.id), ("product_qty", "<", 0)])
        if negative:
            res = False
        else:
            res = True
        return res

    def _deactivate_moves(self):
        # set active = False on stock_move and stock_move_line
        query = """
            UPDATE 
                stock_move
            SET 
                active = false 
            WHERE
                date <= date(%r) and 
                state = 'done' and 
                company_id == %r or 
                company_id is null;
        """ % (self.close_date, self.company_id.id)
        self.env.cr.execute(query)

        query = """
            UPDATE 
                stock_move_line 
            SET 
                active = false 
            WHERE
                date <= date(%r) and 
                state = 'done'
                company_id == %r or 
                company_id is null;
        """ % (self.close_date, self.company_id.id)
        self.env.cr.execute(query)

        return True


class StockClosePeriodLine(models.Model):
    _name = "stock.close.period.line"
    _description = "Stock Close Period Line"
    _rec_name = "product_id"

    close_id = fields.Many2one("stock.close.period", string="Stock Close Period", index=True, ondelete="cascade")
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        domain=[("type", "=", "product")],
        index=True,
        required=True)
    product_name = fields.Char(string="Product Name", related="product_id.name", store=True, readonly=True)
    product_code = fields.Char(string="Product Code", related="product_id.default_code", store=True, readonly=True)
    product_uom_id = fields.Many2one(
        "uom.uom",
        string="UOM",
        required=True,
        default=lambda self: self.env.ref("uom.product_uom_unit", raise_if_not_found=True))
    categ_name = fields.Char(
        string="Category Name",
        related="product_id.categ_id.complete_name",
        store=True,
        readonly=True)
    evaluation_method = fields.Selection([
        ("purchase", "Purchase"),
        ("standard", "Standard"),
        ("manual", "Manual")
    ], string="Evaluation method", copy=False)
    product_qty = fields.Float(string="End Quantity", digits=dp.get_precision("Product Unit of Measure"), default=0)
    price_unit = fields.Float(string="End Average Price", digits=dp.get_precision("Product Price"))
    amount_line = fields.Float(
        string="Amount Line",
        compute="_compute_amount_line",
        digits=dp.get_precision("Product Price"))
    location_id = fields.Many2one("stock.location", string="Location")
    lot_id = fields.Many2one("stock.production.lot", string="Lot/Serial Number")
    owner_id = fields.Many2one("res.partner", string="Owner")
    company_id = fields.Many2one("res.company", string="Company", related="close_id.company_id", store=True)

    @api.depends("product_qty", "price_unit")
    def _compute_amount_line(self):
        for line in self:
            line.amount_line = line.product_qty * line.price_unit
