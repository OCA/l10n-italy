# Copyright 2014-2019 Dinamiche Aziendali srl
# (http://www.dinamicheaziendali.it/)
# @author: Marco Calcagni <mcalcagni@dinamicheaziendali.it>
# @author: Gianmarco Conte <gconte@dinamicheaziendali.it>
# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

from ..mixins.picking_checker import DOMAIN_PICKING_TYPES, DONE_PICKING_STATE
from .stock_delivery_note import DOMAIN_DELIVERY_NOTE_STATES

CANCEL_MOVE_STATE = "cancel"


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking", "shipping.information.updater.mixin"]

    delivery_note_id = fields.Many2one(
        "stock.delivery.note", string="Delivery Note", copy=False
    )
    delivery_note_sequence_id = fields.Many2one(
        "ir.sequence", related="delivery_note_id.sequence_id"
    )
    delivery_note_state = fields.Selection(
        string="DN State", related="delivery_note_id.state"
    )
    delivery_note_partner_ref = fields.Char(related="delivery_note_id.partner_ref")
    delivery_note_partner_shipping_id = fields.Many2one(
        "res.partner", related="delivery_note_id.partner_shipping_id"
    )

    delivery_note_carrier_id = fields.Many2one(
        "res.partner", string="DN Carrier", related="delivery_note_id.carrier_id"
    )
    delivery_method_id = fields.Many2one(
        "delivery.carrier", related="delivery_note_id.delivery_method_id"
    )

    delivery_note_type_id = fields.Many2one(
        "stock.delivery.note.type", related="delivery_note_id.type_id"
    )
    delivery_note_type_code = fields.Selection(related="delivery_note_type_id.code")
    delivery_note_date = fields.Date(string="DN Date", related="delivery_note_id.date")
    delivery_note_note = fields.Html(related="delivery_note_id.note")

    transport_condition_id = fields.Many2one(
        "stock.picking.transport.condition",
        related="delivery_note_id.transport_condition_id",
    )
    goods_appearance_id = fields.Many2one(
        "stock.picking.goods.appearance", related="delivery_note_id.goods_appearance_id"
    )
    transport_reason_id = fields.Many2one(
        "stock.picking.transport.reason", related="delivery_note_id.transport_reason_id"
    )
    transport_method_id = fields.Many2one(
        "stock.picking.transport.method", related="delivery_note_id.transport_method_id"
    )

    transport_datetime = fields.Datetime(related="delivery_note_id.transport_datetime")

    packages = fields.Integer(string="DN Packages", related="delivery_note_id.packages")
    delivery_note_volume = fields.Float(
        string="DN Volume", related="delivery_note_id.volume"
    )
    delivery_note_volume_uom_id = fields.Many2one(
        "uom.uom", related="delivery_note_id.volume_uom_id"
    )
    gross_weight = fields.Float(related="delivery_note_id.gross_weight")
    gross_weight_uom_id = fields.Many2one(
        "uom.uom", related="delivery_note_id.gross_weight_uom_id"
    )
    net_weight = fields.Float(related="delivery_note_id.net_weight")
    net_weight_uom_id = fields.Many2one(
        "uom.uom", related="delivery_note_id.net_weight_uom_id"
    )

    valid_move_ids = fields.One2many(
        "stock.move", "picking_id", domain=[("state", "!=", CANCEL_MOVE_STATE)]
    )
    picking_type_code = fields.Selection(
        string="DN Operation Type", related="picking_type_id.code"
    )

    use_delivery_note = fields.Boolean(compute="_compute_boolean_flags")
    use_advanced_behaviour = fields.Boolean(compute="_compute_boolean_flags")
    delivery_note_exists = fields.Boolean(compute="_compute_boolean_flags")
    delivery_note_draft = fields.Boolean(compute="_compute_boolean_flags")
    delivery_note_readonly = fields.Boolean(compute="_compute_boolean_flags")
    delivery_note_visible = fields.Boolean(compute="_compute_boolean_flags")
    can_be_invoiced = fields.Boolean(compute="_compute_boolean_flags")

    @property
    def _delivery_note_fields(self):
        from collections import OrderedDict

        fields = OrderedDict(
            {
                key: field
                for key, field in self._fields.items()
                if field.related and field.related.split(".")[0] == "delivery_note_id"
            }
        )

        type(self)._delivery_note_fields = fields

        return fields

    def _compute_boolean_flags(self):
        from_delivery_note = self.env.context.get("from_delivery_note")
        use_advanced_behaviour = self.user_has_groups(
            "l10n_it_delivery_note.use_advanced_delivery_notes"
        )

        for picking in self:
            picking.use_delivery_note = (
                not from_delivery_note and picking.state == DONE_PICKING_STATE
            )

            picking.delivery_note_visible = use_advanced_behaviour
            picking.use_advanced_behaviour = use_advanced_behaviour

            picking.delivery_note_draft = False
            picking.delivery_note_readonly = True
            picking.delivery_note_exists = False
            picking.can_be_invoiced = False

            if picking.use_delivery_note and picking.delivery_note_id:
                picking.delivery_note_exists = True
                picking.delivery_note_draft = (
                    picking.delivery_note_id.state == DOMAIN_DELIVERY_NOTE_STATES[0]
                )
                picking.delivery_note_readonly = (
                    picking.delivery_note_id.state == DOMAIN_DELIVERY_NOTE_STATES[3]
                )
                picking.can_be_invoiced = bool(picking.delivery_note_id.sale_ids)

    @api.onchange("delivery_note_type_id")
    def _onchange_delivery_note_type(self):
        if self.delivery_note_type_id:
            if (
                self.delivery_note_id.name
                and self.delivery_note_type_id.sequence_id
                != self.delivery_note_sequence_id
            ):
                raise UserError(
                    _(
                        "You cannot set this delivery note type due"
                        " of a different numerator configuration."
                    )
                )

            if self._update_generic_shipping_information(self.delivery_note_type_id):
                return {
                    "warning": {
                        "title": _("Warning!"),
                        "message": "Some of the shipping configuration have "
                        "been overwritten with"
                        " the default ones of the selected "
                        "delivery note type.\n"
                        "Please, make sure to check this "
                        "information before continuing.",
                    }
                }

    @api.onchange("delivery_note_partner_shipping_id")
    def _onchange_delivery_note_partner_shipping(self):
        if self.delivery_note_partner_shipping_id:
            changed = self._update_partner_shipping_information(
                self.delivery_note_partner_shipping_id
            )

            if changed:
                return {
                    "warning": {
                        "title": _("Warning!"),
                        "message": "Some of the shipping configuration have "
                        "been overwritten with"
                        " the default ones of the selected shipping"
                        " partner address.\n"
                        "Please, make sure to check this "
                        "information before continuing.",
                    }
                }

        else:
            self.delivery_method_id = False

    def _add_delivery_cost_to_so(self):
        self.ensure_one()

        super(
            StockPicking, self.with_context(default_delivery_picking_id=self.id)
        )._add_delivery_cost_to_so()
        return True

    def action_delivery_note_create(self):
        self.ensure_one()

        return {
            "name": _("Create a new delivery note"),
            "type": "ir.actions.act_window",
            "res_model": "stock.delivery.note.create.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"active_ids": self.ids},
        }

    def action_delivery_note_select(self):
        self.ensure_one()

        return {
            "name": _("Select an existing delivery note"),
            "type": "ir.actions.act_window",
            "res_model": "stock.delivery.note.select.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"active_ids": self.ids},
        }

    def action_delivery_note_draft(self):
        self.ensure_one()

        return self.delivery_note_id.action_draft()

    def action_delivery_note_confirm(self):
        self.ensure_one()

        return self.delivery_note_id.action_confirm()

    def action_delivery_note_invoice(self):
        self.ensure_one()

        return self.delivery_note_id.action_invoice()

    def action_delivery_note_done(self):
        self.ensure_one()

        return self.delivery_note_id.action_done()

    def action_delivery_note_cancel(self):
        self.ensure_one()

        return self.delivery_note_id.action_cancel()

    def action_delivery_note_print(self):
        self.ensure_one()

        return self.delivery_note_id.action_print()

    def _check_delivery_note_consistency(self):
        if len(set(self.mapped("picking_type_code"))) != 1:
            raise ValidationError(
                _(
                    "You have just called this method on an "
                    "heterogeneous set of pickings.\n"
                    "All pickings should have the same "
                    "'picking_type_code' field value."
                )
            )

        if (
            len(self.mapped("partner_id")) != 1
            and self.location_dest_id.usage == "customer"
        ):
            raise ValidationError(
                _(
                    "You have just called this method on an heterogeneous set "
                    "of pickings.\n"
                    "All pickings should have the same 'partner_id' field value."
                )
            )

        if len(self.mapped("location_id")) != 1:
            raise ValidationError(
                _(
                    "You have just called this method on an heterogeneous set "
                    "of pickings.\n"
                    "All pickings should have the same 'location_id' field value."
                )
            )

        if len(self.mapped("location_dest_id")) != 1:
            raise ValidationError(
                _(
                    "You have just called this method on an heterogeneous "
                    "set of pickings.\n"
                    "All pickings should have the same 'location_dest_id' "
                    "field value."
                )
            )

    def _must_create_delivery_note(self):
        use_advanced_behaviour = self.user_has_groups(
            "l10n_it_delivery_note.use_advanced_delivery_notes"
        )
        if use_advanced_behaviour:
            return False

        type_code = list(set(self.mapped("picking_type_code")))[0]
        if type_code == DOMAIN_PICKING_TYPES[0]:
            return False

        elif type_code != DOMAIN_PICKING_TYPES[1]:
            src_location_id = self.mapped("location_id")
            dest_location_id = self.mapped("location_dest_id")

            if src_location_id.is_virtual() or dest_location_id.is_virtual():
                return False

        return True

    def button_validate(self):
        delivery_note_to_create = self._must_create_delivery_note()
        if not self.delivery_note_id and delivery_note_to_create:
            self._check_delivery_note_consistency()
        res = super().button_validate()
        if delivery_note_to_create and not self.delivery_note_id:
            delivery_note = self._create_delivery_note()
            self.write({"delivery_note_id": delivery_note.id})
            if self.sale_id:
                self.sale_id._assign_delivery_notes_invoices(self.sale_id.invoice_ids)
        return res

    def _create_delivery_note(self):
        partners = self._get_partners()
        type_id = self.env["stock.delivery.note.type"].search(
            [("code", "=", self.picking_type_code)], limit=1
        )
        return self.env["stock.delivery.note"].create(
            {
                "partner_sender_id": partners[0].id,
                "partner_id": partners[1].id,
                "partner_shipping_id": partners[1].id,
                "type_id": type_id.id,
                "date": self.date_done,
                "delivery_method_id": self.partner_id.property_delivery_carrier_id.id,
                "transport_condition_id": (
                    self.sale_id.default_transport_condition_id.id
                    or partners[1].default_transport_condition_id.id
                    or type_id.default_transport_condition_id.id
                ),
                "goods_appearance_id": (
                    self.sale_id.default_goods_appearance_id.id
                    or partners[1].default_goods_appearance_id.id
                    or type_id.default_goods_appearance_id.id
                ),
                "transport_reason_id": (
                    self.sale_id.default_transport_reason_id.id
                    or partners[1].default_transport_reason_id.id
                    or type_id.default_transport_reason_id.id
                ),
                "transport_method_id": (
                    self.sale_id.default_transport_method_id.id
                    or partners[1].default_transport_method_id.id
                    or type_id.default_transport_method_id.id
                ),
            }
        )

    def delivery_note_update_transport_datetime(self):
        self.delivery_note_id.update_transport_datetime()

    def _get_partners(self):
        partner_id = self.mapped("partner_id")
        src_location_id = self.mapped("location_id")
        dest_location_id = self.mapped("location_dest_id")

        src_warehouse_id = src_location_id.warehouse_id
        dest_warehouse_id = dest_location_id.warehouse_id

        src_partner_id = src_warehouse_id.partner_id
        dest_partner_id = dest_warehouse_id.partner_id

        if not src_partner_id:
            src_partner_id = partner_id

            if not dest_partner_id:
                raise ValueError(
                    "Fields 'src_partner_id' and 'dest_partner_id' "
                    "cannot be both unset."
                )

        elif not dest_partner_id:
            dest_partner_id = partner_id

        return (src_partner_id, dest_partner_id)

    def get_partners(self):
        self._check_delivery_note_consistency()

        return self._get_partners()

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

    def goto_delivery_note(self, **kwargs):
        return self.delivery_note_id.goto(**kwargs)

    def update_delivery_note_fields(self, vals):
        note_fields = self._delivery_note_fields

        if any(key in note_fields for key in vals.keys()):
            delivery_note_vals = {
                note_fields[key].related.split(".")[1]: value
                for key, value in vals.items()
                if key in note_fields
            }

            self.mapped("delivery_note_id").write(delivery_note_vals)

    def write(self, vals):
        res = super().write(vals)

        if self.mapped("delivery_note_id"):
            self.update_delivery_note_fields(vals)

            if "delivery_note_id" in vals:
                self.mapped("delivery_note_id").update_detail_lines()

        return res

    def _create_backorder(self):
        """When we make a backorder of a picking the delivery note lines needed
        to be updated otherwise stock_delivery_note_line_move_uniq constraint is raised"""
        backorders = super()._create_backorder()
        for backorder in backorders:
            backorder.backorder_id.delivery_note_id.update_detail_lines()
        return backorders
