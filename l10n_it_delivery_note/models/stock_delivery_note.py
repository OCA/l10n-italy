# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>

import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from ..mixins.picking_checker import (
    DOMAIN_PICKING_TYPES,
    DONE_PICKING_STATE,
    PICKING_TYPES,
)

DATE_FORMAT = "%d/%m/%Y"
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"

DELIVERY_NOTE_STATES = [
    ("draft", "Draft"),
    ("confirm", "Validated"),
    ("invoiced", "Invoiced"),
    ("done", "Done"),
    ("cancel", "Cancelled"),
]
DOMAIN_DELIVERY_NOTE_STATES = [s[0] for s in DELIVERY_NOTE_STATES]

LINE_DISPLAY_TYPES = [("line_section", "Section"), ("line_note", "Note")]
DOMAIN_LINE_DISPLAY_TYPES = [t[0] for t in LINE_DISPLAY_TYPES]

DRAFT_EDITABLE_STATE = {"draft": [("readonly", False)]}
DONE_READONLY_STATE = {"done": [("readonly", True)]}

INVOICE_STATUSES = [
    ("no", "Nothing to invoice"),
    ("to invoice", "To invoice"),
    ("invoiced", "Fully invoiced"),
]
DOMAIN_INVOICE_STATUSES = [s[0] for s in INVOICE_STATUSES]


class StockDeliveryNote(models.Model):
    _name = "stock.delivery.note"
    _inherit = [
        "mail.thread",
        "mail.activity.mixin",
        "stock.picking.checker.mixin",
        "shipping.information.updater.mixin",
    ]
    _description = "Delivery Note"
    _order = "date DESC, id DESC"

    def _default_company(self):
        return self.env.company

    def _default_type(self):
        return self.env["stock.delivery.note.type"].search(
            [("code", "=", DOMAIN_PICKING_TYPES[1])], limit=1
        )

    def _default_volume_uom(self):
        return self.env.ref("uom.product_uom_litre", raise_if_not_found=False)

    def _domain_volume_uom(self):
        uom_category_id = self.env.ref(
            "uom.product_uom_categ_vol", raise_if_not_found=False
        )

        return [("category_id", "=", uom_category_id.id)]

    def _default_weight_uom(self):
        return self.env.ref("uom.product_uom_kgm", raise_if_not_found=False)

    def _domain_weight_uom(self):
        uom_category_id = self.env.ref(
            "uom.product_uom_categ_kgm", raise_if_not_found=False
        )

        return [("category_id", "=", uom_category_id.id)]

    active = fields.Boolean(default=True)
    name = fields.Char(
        string="Name",
        readonly=True,
        index=True,
        copy=False,
        tracking=True,
    )
    partner_ref = fields.Char(
        string="Partner reference",
        index=True,
        copy=False,
        states=DONE_READONLY_STATE,
        tracking=True,
    )

    state = fields.Selection(
        DELIVERY_NOTE_STATES,
        string="State",
        copy=False,
        default=DOMAIN_DELIVERY_NOTE_STATES[0],
        required=True,
        tracking=True,
    )

    partner_sender_id = fields.Many2one(
        "res.partner",
        string="Sender",
        states=DRAFT_EDITABLE_STATE,
        default=_default_company,
        readonly=True,
        required=True,
        tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Recipient",
        states=DRAFT_EDITABLE_STATE,
        readonly=True,
        required=True,
        index=True,
        tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )
    partner_shipping_id = fields.Many2one(
        "res.partner",
        string="Shipping address",
        states=DONE_READONLY_STATE,
        required=True,
        tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )

    carrier_id = fields.Many2one(
        "res.partner",
        string="Carrier",
        states=DONE_READONLY_STATE,
        tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )
    delivery_method_id = fields.Many2one(
        "delivery.carrier",
        string="Delivery method",
        states=DONE_READONLY_STATE,
        tracking=True,
    )

    date = fields.Date(string="Date", states=DRAFT_EDITABLE_STATE, copy=False)
    type_id = fields.Many2one(
        "stock.delivery.note.type",
        string="Type",
        default=_default_type,
        states=DRAFT_EDITABLE_STATE,
        readonly=True,
        required=True,
        index=True,
    )

    sequence_id = fields.Many2one("ir.sequence", readonly=True, copy=False)
    type_code = fields.Selection(
        string="Type of Operation", related="type_id.code", store=True
    )
    packages = fields.Integer(string="Packages", states=DONE_READONLY_STATE)
    volume = fields.Float(string="Volume", states=DONE_READONLY_STATE)

    volume_uom_id = fields.Many2one(
        "uom.uom",
        string="Volume UoM",
        default=_default_volume_uom,
        domain=_domain_volume_uom,
        states=DONE_READONLY_STATE,
    )
    gross_weight = fields.Float(string="Gross weight", states=DONE_READONLY_STATE)
    gross_weight_uom_id = fields.Many2one(
        "uom.uom",
        string="Gross weight UoM",
        default=_default_weight_uom,
        domain=_domain_weight_uom,
        states=DONE_READONLY_STATE,
    )
    net_weight = fields.Float(string="Net weight", states=DONE_READONLY_STATE)
    net_weight_uom_id = fields.Many2one(
        "uom.uom",
        string="Net weight UoM",
        default=_default_weight_uom,
        domain=_domain_weight_uom,
        states=DONE_READONLY_STATE,
    )

    transport_condition_id = fields.Many2one(
        "stock.picking.transport.condition",
        string="Condition of transport",
        states=DONE_READONLY_STATE,
    )
    goods_appearance_id = fields.Many2one(
        "stock.picking.goods.appearance",
        string="Appearance of goods",
        states=DONE_READONLY_STATE,
    )
    transport_reason_id = fields.Many2one(
        "stock.picking.transport.reason",
        string="Reason of transport",
        states=DONE_READONLY_STATE,
    )
    transport_method_id = fields.Many2one(
        "stock.picking.transport.method",
        string="Method of transport",
        states=DONE_READONLY_STATE,
    )

    transport_datetime = fields.Datetime(
        string="Transport date", states=DONE_READONLY_STATE
    )

    line_ids = fields.One2many(
        "stock.delivery.note.line", "delivery_note_id", string="Lines"
    )
    invoice_status = fields.Selection(
        INVOICE_STATUSES,
        string="Invoice status",
        compute="_compute_invoice_status",
        default=DOMAIN_INVOICE_STATUSES[0],
        readonly=True,
        store=True,
        copy=False,
    )

    picking_ids = fields.One2many(
        "stock.picking", "delivery_note_id", string="Pickings"
    )
    pickings_picker = fields.Many2many(
        "stock.picking",
        compute="_compute_get_pickings",
        inverse="_inverse_set_pickings",
    )

    picking_type = fields.Selection(
        PICKING_TYPES,
        string="Picking type",
        compute="_compute_picking_type",
        store=True,
    )

    sale_ids = fields.Many2many("sale.order", compute="_compute_sales")
    sale_count = fields.Integer(compute="_compute_sales")
    sales_transport_check = fields.Boolean(compute="_compute_sales", default=True)

    invoice_ids = fields.Many2many(
        "account.move",
        "stock_delivery_note_account_invoice_rel",
        "delivery_note_id",
        "invoice_id",
        string="Invoices",
        copy=False,
    )

    print_prices = fields.Boolean(
        string="Show prices on printed DN", related="type_id.print_prices", store=True
    )
    note = fields.Html(string="Internal note", states=DONE_READONLY_STATE)

    can_change_number = fields.Boolean(compute="_compute_boolean_flags")
    show_product_information = fields.Boolean(compute="_compute_boolean_flags")
    company_id = fields.Many2one("res.company", required=True, default=_default_company)

    @api.depends("name", "partner_id", "partner_ref", "partner_id.display_name")
    def name_get(self):
        result = []
        for note in self:
            if not note.name:
                partner_name = note.partner_id.display_name
                create_date = note.create_date.strftime(DATETIME_FORMAT)
                name = "{} - {}".format(partner_name, create_date)

            else:
                name = note.name

                if note.partner_ref and note.type_code == "incoming":
                    name = "{} ({})".format(name, note.partner_ref)
            result.append((note.id, name))

        return result

    @api.depends("state", "line_ids", "line_ids.invoice_status")
    def _compute_invoice_status(self):
        for note in self:
            lines = note.line_ids.filtered(lambda l: l.sale_line_id)

            if all(line.invoice_status == DOMAIN_INVOICE_STATUSES[2] for line in lines):
                note.state = DOMAIN_DELIVERY_NOTE_STATES[2]
                note.invoice_status = DOMAIN_INVOICE_STATUSES[2]

            elif any(
                line.invoice_status == DOMAIN_INVOICE_STATUSES[1] for line in lines
            ):
                note.invoice_status = DOMAIN_INVOICE_STATUSES[1]

            else:
                note.invoice_status = DOMAIN_INVOICE_STATUSES[0]

    def _compute_get_pickings(self):
        for note in self:
            note.pickings_picker = note.picking_ids

    def _inverse_set_pickings(self):
        for note in self:
            if note.pickings_picker:
                self.check_compliance(note.pickings_picker)

            note.picking_ids = note.pickings_picker

    @api.depends("picking_ids")
    def _compute_picking_type(self):
        for note in self.filtered(lambda n: n.picking_ids):
            picking_types = set(note.picking_ids.mapped("picking_type_code"))
            picking_types = list(picking_types)

            if len(picking_types) != 1:
                raise ValueError(
                    "You have just called this method on an "
                    "heterogeneous set of pickings.\n"
                    "All pickings should have the same "
                    "'picking_type_code' field value."
                )

            note.picking_type = picking_types[0]

    @api.depends("picking_ids")
    def _compute_sales(self):
        for note in self:
            sales = note.mapped("picking_ids.sale_id")

            note.sale_ids = sales
            note.sale_count = len(sales)

            tc = sales.mapped("default_transport_condition_id")
            ga = sales.mapped("default_goods_appearance_id")
            tr = sales.mapped("default_transport_reason_id")
            tm = sales.mapped("default_transport_method_id")
            note.sales_transport_check = all([len(x) < 2 for x in [tc, ga, tr, tm]])

    def _compute_boolean_flags(self):
        can_change_number = self.user_has_groups(
            "l10n_it_delivery_note.can_change_number"
        )
        show_product_information = self.user_has_groups(
            "l10n_it_delivery_note_base.show_product_related_fields"
        )

        for note in self:
            note.can_change_number = note.state == "draft" and can_change_number
            note.show_product_information = show_product_information

    @api.onchange("picking_type")
    def _onchange_picking_type(self):
        if self.picking_type:
            type_domain = [("code", "=", self.picking_type)]

        else:
            type_domain = []

        return {"domain": {"type_id": type_domain}}

    @api.onchange("type_id")
    def _onchange_type(self):
        if self.type_id:
            if self.name and self.type_id.sequence_id != self.sequence_id:
                raise UserError(
                    _(
                        "You cannot set this delivery note type due"
                        " of a different numerator configuration."
                    )
                )
            if self.picking_type and self.type_id.code != self.picking_type:
                raise UserError(
                    _(
                        "You cannot set this delivery note type due"
                        " of a different type with related pickings."
                    )
                )

            if self._update_generic_shipping_information(self.type_id):
                return {
                    "warning": {
                        "title": _("Warning!"),
                        "message": "Some of the shipping configuration have "
                        "been overwritten with"
                        " the default ones of the selected delivery"
                        " note type.\n"
                        "Please, make sure to check this "
                        "information before continuing.",
                    }
                }

    @api.onchange("partner_id")
    def _onchange_partner(self):
        self.partner_shipping_id = self.partner_id

        if self.partner_id:
            pickings_picker_domain = [
                ("delivery_note_id", "=", False),
                ("state", "=", DONE_PICKING_STATE),
                ("picking_type_code", "=", self.picking_type),
                ("partner_id", "=", self.partner_id.id),
            ]

        else:
            pickings_picker_domain = [("id", "=", False)]

        return {"domain": {"pickings_picker": pickings_picker_domain}}

    @api.onchange("partner_shipping_id")
    def _onchange_partner_shipping(self):
        if self.partner_shipping_id:
            changed = self._update_partner_shipping_information(
                self.partner_shipping_id
            )

            if changed:
                return {
                    "warning": {
                        "title": _("Warning!"),
                        "message": "Some of the shipping configuration have "
                        "been overwritten with"
                        " the default ones of the selected "
                        "shipping partner address.\n"
                        "Please, make sure to check this "
                        "information before continuing.",
                    }
                }

        else:
            self.delivery_method_id = False

    def check_compliance(self, pickings):
        super().check_compliance(pickings)

        self._check_delivery_notes(self.pickings_picker - self.picking_ids)

    def ensure_annulability(self):
        if self.mapped("invoice_ids"):
            raise UserError(
                _(
                    "You cannot cancel this delivery note. "
                    "There is at least one invoice"
                    " related to this delivery note."
                )
            )

    def action_draft(self):
        self.write({"state": DOMAIN_DELIVERY_NOTE_STATES[0]})
        self.line_ids.sync_invoice_status()

    def action_confirm(self):
        for note in self:
            sequence = note.type_id.sequence_id

            note.state = DOMAIN_DELIVERY_NOTE_STATES[1]
            if not note.date:
                note.date = datetime.date.today()

            if not note.name:
                note.name = sequence.next_by_id()
                note.sequence_id = sequence

    def _fix_quantities_to_invoice(self, lines):
        cache = {}

        pickings_lines = lines.retrieve_pickings_lines(self.picking_ids)
        other_lines = lines - pickings_lines

        for line in other_lines:
            cache[line] = line.fix_qty_to_invoice()

        pickings_move_ids = self.mapped("picking_ids.move_lines")
        for line in pickings_lines.filtered(lambda l: len(l.move_ids) > 1):
            move_ids = line.move_ids & pickings_move_ids
            qty_to_invoice = sum(move_ids.mapped("quantity_done"))

            if qty_to_invoice < line.qty_to_invoice:
                cache[line] = line.fix_qty_to_invoice(qty_to_invoice)

        return cache

    def action_invoice(self):
        self.ensure_one()

        orders_lines = self.mapped("sale_ids.order_line").filtered(
            lambda l: l.product_id
        )

        downpayment_lines = orders_lines.filtered(lambda l: l.is_downpayment)
        invoiceable_lines = orders_lines.filtered(lambda l: l.is_invoiceable)

        cache = self._fix_quantities_to_invoice(invoiceable_lines - downpayment_lines)

        for downpayment in downpayment_lines:
            order = downpayment.order_id
            order_lines = order.order_line.filtered(
                lambda l: l.product_id and not l.is_downpayment
            )

            if order_lines.filtered(lambda l: l.need_to_be_invoiced):
                cache[downpayment] = downpayment.fix_qty_to_invoice()

        invoice_ids = self.sale_ids.filtered(
            lambda o: o.invoice_status == DOMAIN_INVOICE_STATUSES[1]
        )._create_invoices(final=True)

        for line, vals in cache.items():
            line.write(vals)

        orders_lines._get_to_invoice_qty()

        for line in self.line_ids:
            line.write({"invoice_status": "invoiced"})
        if all(line.invoice_status == "invoiced" for line in self.line_ids):
            self.write(
                {"invoice_ids": [(4, invoice_id) for invoice_id in invoice_ids.ids]}
            )
            self._compute_invoice_status()
            invoices = self.env["account.move"].browse(invoice_ids.ids)
            invoices.update_delivery_note_lines()

    def action_done(self):
        self.write({"state": DOMAIN_DELIVERY_NOTE_STATES[3]})

    def action_cancel(self):
        self.ensure_annulability()

        self.write({"state": DOMAIN_DELIVERY_NOTE_STATES[4]})

    def action_print(self):
        return self.env.ref(
            "l10n_it_delivery_note.delivery_note_report_action"
        ).report_action(self)

    def update_transport_datetime(self):
        self.transport_datetime = datetime.datetime.now()

    def goto(self, **kwargs):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "views": [(False, "form")],
            "view_mode": "form",
            "target": "current",
            **kwargs,
        }

    def goto_sales(self, **kwargs):
        sales = self.mapped("sale_ids")
        action = self.env.ref("sale.action_orders").read()[0]
        action.update(kwargs)

        if len(sales) > 1:
            action["domain"] = [("id", "in", sales.ids)]

        elif len(sales) == 1:
            action["views"] = [(self.env.ref("sale.view_order_form").id, "form")]
            action["res_id"] = sales.id

        else:
            action = {"type": "ir.actions.act_window_close"}

        return action

    def _create_detail_lines(self, move_ids):
        if not move_ids:
            return

        moves = self.env["stock.move"].browse(move_ids)
        lines_vals = self.env["stock.delivery.note.line"]._prepare_detail_lines(moves)

        self.write({"line_ids": [(0, False, vals) for vals in lines_vals]})

    def _delete_detail_lines(self, move_ids):
        if not move_ids:
            return

        lines = self.env["stock.delivery.note.line"].search(
            [("move_id", "in", move_ids)]
        )

        self.write({"line_ids": [(2, line.id, False) for line in lines]})

    def update_detail_lines(self):
        for note in self:
            lines_move_ids = note.mapped("line_ids.move_id").ids
            pickings_move_ids = note.mapped("picking_ids.valid_move_ids").ids

            move_ids_to_create = [
                line for line in pickings_move_ids if line not in lines_move_ids
            ]
            move_ids_to_delete = [
                line for line in lines_move_ids if line not in pickings_move_ids
            ]

            note._create_detail_lines(move_ids_to_create)
            note._delete_detail_lines(move_ids_to_delete)

    @api.model
    def create(self, vals):
        res = super().create(vals)

        if "picking_ids" in vals:
            res.update_detail_lines()

        return res

    def write(self, vals):
        res = super().write(vals)

        if "picking_ids" in vals:
            self.update_detail_lines()

        return res

    def unlink(self):
        self.ensure_annulability()

        return super().unlink()

    @api.model
    def get_location_address(self, location_id):
        location_address = ""
        warehouse = self.env["stock.warehouse"].search(
            [("lot_stock_id", "=", location_id)]
        )

        if warehouse and warehouse.partner_id:
            partner = warehouse.partner_id

            location_address += "{}, ".format(partner.name)
            if partner.street:
                location_address += "{} - ".format(partner.street)

            location_address += "{} {}".format(partner.zip, partner.city)
            if partner.state_id:
                location_address += " ({})".format(partner.state_id.name)

        return location_address


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
    sequence = fields.Integer(string="Sequence", required=True, default=10, index=True)
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
    price_unit = fields.Monetary(string="Unit price", currency_field="currency_id")
    currency_id = fields.Many2one(
        "res.currency", string="Currency", required=True, default=_default_currency
    )
    discount = fields.Float(string="Discount", digits="Discount")
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
                "product_qty": move.product_uom_qty,
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

    @api.model
    def create(self, vals):
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

        return super().create(vals)

    def write(self, vals):
        if "display_type" in vals and self.filtered(
            lambda l: l.display_type != vals["display_type"]
        ):
            raise UserError(
                _(
                    "You cannot change the type of a delivery note line. "
                    "Instead you should delete the current line"
                    " and create a new line of the proper type."
                )
            )

        return super().write(vals)

    def sync_invoice_status(self):
        for line in self.filtered(lambda l: l.sale_line_id):
            invoice_status = line.sale_line_id.invoice_status
            line.invoice_status = (
                DOMAIN_INVOICE_STATUSES[1]
                if invoice_status == "upselling"
                else invoice_status
            )
