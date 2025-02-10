# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError

from ..mixins.delivery_mixin import (
    _default_volume_uom,
    _default_weight_uom,
    _domain_volume_uom,
    _domain_weight_uom,
)
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

INVOICE_STATUSES = [
    ("no", "Nothing to invoice"),
    ("to invoice", "To invoice"),
    ("invoiced", "Fully invoiced"),
]
DOMAIN_INVOICE_STATUSES = [s[0] for s in INVOICE_STATUSES]


class StockDeliveryNote(models.Model):
    _name = "stock.delivery.note"
    _inherit = [
        "portal.mixin",
        "mail.thread",
        "mail.activity.mixin",
        "stock.picking.checker.mixin",
        "shipping.information.updater.mixin",
        "l10n_it_delivery_note.delivery_mixin",
    ]
    _description = "Delivery Note"
    _order = "date DESC, id DESC"
    _check_company_auto = True

    def _default_company(self):
        return self.env.company

    def _default_type(self):
        return self.env["stock.delivery.note.type"].search(
            [
                ("code", "=", DOMAIN_PICKING_TYPES[1]),
                ("company_id", "=", self.env.company.id),
            ],
            limit=1,
        )

    def _default_volume_uom(self):
        return _default_volume_uom(self)

    def _domain_volume_uom(self):
        return _domain_volume_uom(self)

    def _default_weight_uom(self):
        return _default_weight_uom(self)

    def _domain_weight_uom(self):
        return _domain_weight_uom(self)

    active = fields.Boolean(default=True)
    name = fields.Char(
        readonly=True,
        index=True,
        copy=False,
        tracking=True,
    )
    partner_ref = fields.Char(
        string="Partner reference",
        index=True,
        copy=False,
        tracking=True,
    )

    state = fields.Selection(
        DELIVERY_NOTE_STATES,
        copy=False,
        default=DOMAIN_DELIVERY_NOTE_STATES[0],
        required=True,
        tracking=True,
    )

    partner_sender_id = fields.Many2one(
        "res.partner",
        string="Sender",
        default=_default_company,
        readonly=True,
        required=True,
        tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Recipient",
        readonly=True,
        required=True,
        index=True,
        tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )
    partner_shipping_id = fields.Many2one(
        "res.partner",
        string="Shipping address",
        required=True,
        tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )

    carrier_id = fields.Many2one(
        "res.partner",
        string="Carrier",
        tracking=True,
    )
    delivery_method_id = fields.Many2one(
        "delivery.carrier",
        string="Delivery method",
        tracking=True,
    )

    date = fields.Date(copy=False)
    type_id = fields.Many2one(
        "stock.delivery.note.type",
        string="Type",
        default=_default_type,
        readonly=True,
        required=True,
        index=True,
        check_company=True,
    )

    sequence_id = fields.Many2one("ir.sequence", readonly=True, copy=False)
    type_code = fields.Selection(
        string="Type of Operation", related="type_id.code", store=True
    )
    packages = fields.Integer()
    volume = fields.Float()

    volume_uom_id = fields.Many2one(
        "uom.uom",
        string="Volume UoM",
        default=_default_volume_uom,
        domain=_domain_volume_uom,
    )
    gross_weight = fields.Float(
        string="Gross weight",
        store=True,
        readonly=False,
        compute="_compute_weights",
    )
    gross_weight_uom_id = fields.Many2one(
        "uom.uom",
        string="Gross weight UoM",
        default=_default_weight_uom,
        domain=_domain_weight_uom,
    )
    net_weight = fields.Float(
        string="Net weight",
        store=True,
        readonly=False,
        compute="_compute_weights",
    )
    net_weight_uom_id = fields.Many2one(
        "uom.uom",
        string="Net weight UoM",
        default=_default_weight_uom,
        domain=_domain_weight_uom,
    )

    transport_condition_id = fields.Many2one(
        "stock.picking.transport.condition",
        string="Condition of transport",
    )
    goods_appearance_id = fields.Many2one(
        "stock.picking.goods.appearance",
        string="Appearance of goods",
    )
    transport_reason_id = fields.Many2one(
        "stock.picking.transport.reason",
        string="Reason of transport",
    )
    transport_method_id = fields.Many2one(
        "stock.picking.transport.method",
        string="Method of transport",
    )

    transport_datetime = fields.Datetime(string="Transport date")

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
    lines_have_so_number = fields.Boolean(
        compute="_compute_lines_have_so_number",
    )
    lines_have_customer_ref = fields.Boolean(
        compute="_compute_lines_have_customer_ref",
    )

    picking_ids = fields.One2many(
        "stock.picking",
        "delivery_note_id",
        string="Pickings",
        check_company=True,
    )
    pickings_picker = fields.Many2many(
        "stock.picking",
        compute="_compute_get_pickings",
        inverse="_inverse_set_pickings",
        check_company=True,
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
    note = fields.Html(string="Internal note")

    can_change_number = fields.Boolean(compute="_compute_boolean_flags")
    show_product_information = fields.Boolean(compute="_compute_boolean_flags")
    company_id = fields.Many2one("res.company", required=True, default=_default_company)

    # Sync with delivery mixin fields
    delivery_transport_reason_id = fields.Many2one(
        related="transport_reason_id",
        readonly=True,
    )
    delivery_transport_condition_id = fields.Many2one(
        related="transport_condition_id",
        readonly=True,
    )
    delivery_transport_method_id = fields.Many2one(
        related="transport_method_id",
        readonly=True,
    )
    delivery_carrier_id = fields.Many2one(
        related="carrier_id",
        readonly=True,
    )
    delivery_goods_appearance_id = fields.Many2one(
        related="goods_appearance_id",
        readonly=True,
    )
    delivery_volume_uom_id = fields.Many2one(
        related="volume_uom_id",
        readonly=True,
        default=None,
        domain=None,
    )
    delivery_volume = fields.Float(
        related="volume",
        readonly=True,
    )
    delivery_gross_weight_uom_id = fields.Many2one(
        related="gross_weight_uom_id",
        readonly=True,
        default=None,
        domain=None,
    )
    delivery_gross_weight = fields.Float(
        related="gross_weight",
        readonly=True,
    )
    delivery_net_weight_uom_id = fields.Many2one(
        related="net_weight_uom_id",
        readonly=True,
        default=None,
        domain=None,
    )
    delivery_net_weight = fields.Float(
        related="net_weight",
        readonly=True,
    )
    delivery_transport_datetime = fields.Datetime(
        related="transport_datetime",
        readonly=True,
    )
    delivery_packages = fields.Integer(
        related="packages",
        readonly=True,
    )
    delivery_note = fields.Html(
        related="note",
        readonly=True,
    )

    _sql_constraints = [
        (
            "name_uniq",
            "unique(name, company_id)",
            "The Delivery note must have unique numbers.",
        )
    ]

    @api.depends("name", "partner_id", "partner_ref", "partner_id.display_name")
    def _compute_display_name(self):
        for note in self:
            if not note.name:
                name = f"{note.partner_id.display_name}"
                if note.create_date:
                    create_date = note.create_date.strftime(DATETIME_FORMAT)
                    name += f" - {create_date}"

            else:
                name = note.name

                if note.partner_ref and note.type_code == "incoming":
                    name += f" ({note.partner_ref})"
            note.display_name = name

    @api.depends("state", "line_ids", "line_ids.invoice_status")
    def _compute_invoice_status(self):
        for note in self:
            lines = note.line_ids.filtered(lambda line: line.sale_line_id)
            invoice_status = DOMAIN_INVOICE_STATUSES[0]
            if lines:
                if all(
                    line.invoice_status == DOMAIN_INVOICE_STATUSES[2] for line in lines
                ):
                    note.state = DOMAIN_DELIVERY_NOTE_STATES[2]
                    invoice_status = DOMAIN_INVOICE_STATUSES[2]
                elif any(
                    line.invoice_status == DOMAIN_INVOICE_STATUSES[1] for line in lines
                ):
                    invoice_status = DOMAIN_INVOICE_STATUSES[1]
            note.invoice_status = invoice_status

    def _compute_get_pickings(self):
        for note in self:
            note.pickings_picker = note.picking_ids

    @api.depends("picking_ids")
    def _compute_weights(self):
        for note in self:
            # fill gross & net weight from pickings
            gross_weight = net_weight = 0.0
            if note.picking_ids:
                # this is the unit used for shipping_weight
                weight_uom = self.env[
                    "product.template"
                ]._get_weight_uom_id_from_ir_config_parameter()
                for pick in note.picking_ids:
                    gross_weight += weight_uom._compute_quantity(
                        pick.shipping_weight, note.gross_weight_uom_id
                    )
                    net_weight += weight_uom._compute_quantity(
                        pick.shipping_weight, note.net_weight_uom_id
                    )
            note.gross_weight = gross_weight
            note.net_weight = net_weight

    @api.onchange("picking_ids")
    def _onchange_picking_ids(self):
        self._compute_weights()

    @api.onchange("delivery_method_id")
    def _onchange_delivery_method_id(self):
        self.carrier_id = self.delivery_method_id.partner_id

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
        can_change_number = self.env.user.has_group(
            "l10n_it_delivery_note.can_change_number"
        )
        show_product_information = self.env.user.has_group(
            "l10n_it_delivery_note.show_product_related_fields"
        )

        for note in self:
            note.can_change_number = note.state == "draft" and can_change_number
            note.show_product_information = show_product_information

    def _compute_access_url(self):
        res = super()._compute_access_url()
        for dn in self:
            dn.access_url = f"/my/delivery-notes/{dn.id}"
        return res

    def _compute_lines_have_so_number(self):
        for sdn in self:
            sdn.lines_have_so_number = (
                sdn.company_id.display_ref_order_dn_report
                and any(line.sale_order_number for line in sdn.line_ids)
            )

    def _compute_lines_have_customer_ref(self):
        for sdn in self:
            sdn.lines_have_customer_ref = (
                sdn.company_id.display_ref_customer_dn_report
                and any(line.sale_order_client_ref for line in sdn.line_ids)
            )

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
                    self.env._(
                        "You cannot set this delivery note type due"
                        " of a different numerator configuration."
                    )
                )
            if self.picking_type and self.type_id.code != self.picking_type:
                raise UserError(
                    self.env._(
                        "You cannot set this delivery note type due"
                        " of a different type with related pickings."
                    )
                )

            if self._update_generic_shipping_information(self.type_id):
                return {
                    "warning": {
                        "title": self.env._("Warning!"),
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
                        "title": self.env._("Warning!"),
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
        return True

    def ensure_annulability(self):
        if self.mapped("invoice_ids"):
            raise UserError(
                self.env._(
                    "You cannot cancel this delivery note. "
                    "There is at least one invoice"
                    " related to this delivery note."
                )
            )

    def action_draft(self):
        self.write({"state": DOMAIN_DELIVERY_NOTE_STATES[0]})
        self.line_ids.sync_invoice_status()

    def _action_confirm(self):
        for note in self:
            sequence = note.type_id.sequence_id

            note.state = DOMAIN_DELIVERY_NOTE_STATES[1]
            if not note.date:
                note.date = datetime.date.today()

            if not note.name:
                # Avoid duplicates
                while True:
                    name = sequence.with_context(
                        ir_sequence_date=note.date
                    ).next_by_id()
                    if not self.search(
                        [("name", "=", name), ("company_id", "=", note.company_id.id)]
                    ):
                        break

                note.name = name
                note.sequence_id = sequence

    def action_confirm(self):
        for note in self:
            if (
                note.type_code == "incoming"
                and not note.partner_ref
                and self.env.user.has_group(
                    "l10n_it_delivery_note.group_required_partner_ref"
                )
            ):
                raise UserError(
                    note.env._(
                        "The field 'Partner reference' is "
                        "mandatory to validate the Delivery Note."
                    )
                )

            warning_message = False
            carrier_ids = note.mapped("picking_ids.carrier_id")
            carrier_partner_ids = carrier_ids.mapped("partner_id")
            if len(carrier_partner_ids) > 1:
                warning_message = note.env._(
                    "This delivery note contains pickings "
                    "related to different transporters. "
                    "Are you sure you want to proceed?\n"
                    "Carrier Partners: %(carrier_partners)s",
                    carrier_partners=", ".join(carrier_partner_ids.mapped("name")),
                )
            elif len(carrier_ids) > 1:
                warning_message = note.env._(
                    "This delivery note contains pickings related to different "
                    "delivery methods from the same transporter. "
                    "Are you sure you want to proceed?\n"
                    "Delivery Methods: %(carriers)s",
                    carriers=", ".join(carrier_ids.mapped("name")),
                )
            elif (
                carrier_partner_ids
                and note.carrier_id
                and note.carrier_id != carrier_partner_ids
            ):
                warning_message = note.env._(
                    "The carrier set in Delivery Note is different "
                    "from the carrier set in picking(s). "
                    "Are you sure you want to proceed?"
                )
            elif (
                carrier_ids
                and note.delivery_method_id
                and carrier_ids != note.delivery_method_id
            ):
                warning_message = note.env._(
                    "The shipping method set in Delivery Note is different "
                    "from the shipping method set in picking(s). "
                    "Are you sure you want to proceed?"
                )
            if warning_message:
                return {
                    "type": "ir.actions.act_window",
                    "name": note.env._("Warning"),
                    "res_model": "stock.delivery.note.confirm.wizard",
                    "view_type": "form",
                    "target": "new",
                    "view_mode": "form",
                    "context": {
                        "default_delivery_note_id": note.id,
                        "default_warning_message": warning_message,
                        **self._context,
                    },
                }
            else:
                note._action_confirm()

    def _check_delivery_notes_before_invoicing(self):
        for delivery_note_id in self:
            if not delivery_note_id.sale_ids:
                raise UserError(
                    delivery_note_id.env._("%s hasn't sale order!")
                    % delivery_note_id.display_name
                )
            if (
                len(
                    delivery_note_id.mapped("sale_ids.picking_ids.picking_type_id.code")
                )
                > 1
            ):
                raise UserError(
                    delivery_note_id.env._(
                        "Sale orders related to %s have return! "
                        "For invoicing, go to sale orders."
                    )
                    % delivery_note_id.display_name
                )
            if delivery_note_id.invoice_status == "invoiced":
                raise UserError(
                    delivery_note_id.env._("%s is already invoiced!")
                    % delivery_note_id.display_name
                )
            if delivery_note_id.state == "draft":
                raise UserError(
                    delivery_note_id.env._("%s is in draft!")
                    % delivery_note_id.display_name
                )
            for line in delivery_note_id.line_ids:
                if line.product_id.invoice_policy == "order":
                    raise UserError(
                        delivery_note_id.env._(
                            "In %(ddt_name)s there is %(product_name)s"
                            " with invoicing policy 'order'"
                        )
                        % {
                            "ddt_name": delivery_note_id.display_name,
                            "product_name": line.product_id.name,
                        }
                    )

    def _fix_quantities_to_invoice(self, lines, invoice_method):
        cache = {}

        pickings_lines = lines.retrieve_pickings_lines(self.picking_ids)
        other_lines = lines - pickings_lines

        if not invoice_method or invoice_method == "dn":
            for line in other_lines:
                cache[line] = line.fix_qty_to_invoice()
        elif invoice_method == "service":
            for line in other_lines:
                if line.product_id.type != "service":
                    cache[line] = line.fix_qty_to_invoice()

        pickings_move_ids = self.mapped("picking_ids.move_ids")
        for line in pickings_lines.filtered(lambda line: len(line.move_ids) > 1):
            move_ids = line.move_ids & pickings_move_ids
            qty_to_invoice = sum(move_ids.mapped("quantity"))

            if qty_to_invoice < line.qty_to_invoice:
                cache[line] = line.fix_qty_to_invoice(qty_to_invoice)

        return cache

    def action_invoice(self, invoice_method=False):
        self._check_delivery_notes_before_invoicing()

        payment_term_ids = [self.env["account.payment.term"]]
        payment_term_ids += [
            payment_term_id
            for payment_term_id in self.mapped("sale_ids.payment_term_id")
        ]
        for payment_term_id in payment_term_ids:
            sale_ids = self.mapped("sale_ids").filtered(
                lambda s, pay_term_id=payment_term_id: s.payment_term_id == pay_term_id
            )
            if not sale_ids:
                continue
            orders_lines = sale_ids.mapped("order_line").filtered(
                lambda l: l.product_id  # noqa: E741
            )

            downpayment_lines = orders_lines.filtered(lambda l: l.is_downpayment)  # noqa: E741
            invoiceable_lines = orders_lines.filtered(lambda l: l.is_invoiceable)  # noqa: E741

            cache = self._fix_quantities_to_invoice(
                invoiceable_lines - downpayment_lines, invoice_method
            )

            for downpayment in downpayment_lines:
                order = downpayment.order_id
                order_lines = order.order_line.filtered(
                    lambda l: l.product_id and not l.is_downpayment  # noqa: E741
                )

                if order_lines.filtered(lambda l: l.need_to_be_invoiced):  # noqa: E741
                    cache[downpayment] = downpayment.fix_qty_to_invoice()

            invoice_ids = sale_ids.filtered(
                lambda o: o.invoice_status == DOMAIN_INVOICE_STATUSES[1]
            )._create_invoices(final=True)

            for line, vals in cache.items():
                line.write(vals)

            orders_lines._compute_qty_to_invoice()

            for line in self.mapped("line_ids"):
                line.write({"invoice_status": "invoiced"})
            for delivery_note in self:
                ready_invoice_ids = [
                    invoice_id
                    for invoice_id in delivery_note.sale_ids.mapped("invoice_ids").ids
                    if invoice_id in invoice_ids.ids
                ]
                delivery_note.write(
                    {
                        "invoice_ids": [
                            (4, invoice_id) for invoice_id in ready_invoice_ids
                        ]
                    }
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

    @api.model
    def _get_sync_fields(self):
        """
        Returns a list of fields that can be used to
         synchronize the state of the Delivery Note
        """
        return [
            "date",
            "transport_datetime",
            "transport_condition_id",
            "goods_appearance_id",
            "transport_reason_id",
            "transport_method_id",
            "gross_weight",
            "net_weight",
            "packages",
            "volume",
        ]

    def _get_report_base_filename(self):
        self.ensure_one()
        return f"Delivery Note - {self.name}"

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
        action = self.env["ir.actions.act_window"]._for_xml_id("sale.action_orders")
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

    @api.model_create_multi
    def create(self, vals_list):
        notes = super().create(vals_list)
        for note in notes:
            if note.picking_ids:
                note.update_detail_lines()
        return notes

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
        warehouse = self.env["stock.location"].browse(location_id).warehouse_id

        if warehouse and warehouse.partner_id:
            partner = warehouse.partner_id

            location_address += f"{partner.name}, "
            if partner.street:
                location_address += f"{partner.street} - "

            location_address += f"{partner.zip} {partner.city}"
            if partner.state_id:
                location_address += f" ({partner.state_id.name})"

        return location_address
