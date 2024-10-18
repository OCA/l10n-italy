# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StockDeliveryNoteBaseWizard(models.AbstractModel):
    _name = "stock.delivery.note.base.wizard"
    _inherit = "stock.picking.checker.mixin"
    _description = "Delivery Note Base"

    def _default_stock_pickings(self):
        active_ids = self.env.context.get("active_ids", [])

        return self.env["stock.picking"].browse(active_ids)

    def _domain_type_id(self):
        return [("company_id", "in", [False, self.env.company.id])]

    selected_picking_ids = fields.Many2many(
        "stock.picking", default=_default_stock_pickings, readonly=True
    )

    partner_sender_id = fields.Many2one(
        "res.partner", string="Sender", compute="_compute_fields"
    )
    partner_id = fields.Many2one(
        "res.partner", string="Recipient", compute="_compute_fields"
    )
    partner_shipping_id = fields.Many2one("res.partner", string="Shipping address")

    date = fields.Date()
    type_id = fields.Many2one(
        "stock.delivery.note.type",
        string="Type",
        domain=_domain_type_id,
    )

    error_message = fields.Html(compute="_compute_fields")
    warning_message = fields.Char("Warning", readonly=True, compute="_compute_fields")

    def _get_validation_errors(self, pickings):
        validators = [
            (self._check_pickings, True),
            (self._check_pickings_state, False),
            (self._check_pickings_types, False),
            (self._check_pickings_partners, False),
            (self._check_pickings_src_locations, False),
            (self._check_pickings_dest_locations, False),
            (self._check_delivery_notes, False),
        ]

        errors = []
        for validator, interrupt in validators:
            try:
                validator(pickings)

            except ValidationError as exc:
                errors.append(exc.args[0])

                if interrupt:
                    break

        return errors

    def _get_warning_message(self):
        """
        This method is used to be inherited and extended
        to display whatever message could be used to improve the
        user experience when creating a delivery note

        :return: message to be displayed
        """
        return False

    @api.depends("selected_picking_ids")
    def _compute_fields(self):
        try:
            self.error_message = False
            self.partner_sender_id = False
            self.partner_id = False
            self.check_compliance(self.selected_picking_ids)

        except ValidationError:
            values = {
                "title": self.env._("Warning!"),
                "errors": self._get_validation_errors(self.selected_picking_ids),
            }

            self.error_message = self.env["ir.ui.view"]._render_template(
                "l10n_it_delivery_note."
                "stock_delivery_note_wizard_error_message_template",
                values,
            )

        else:
            self.warning_message = self._get_warning_message()
            partners = self.selected_picking_ids.get_partners()
            self.partner_sender_id = partners[0]
            self.partner_id = partners[1]

    def confirm(self):
        raise NotImplementedError(
            "This functionality isn't ready yet. " "Please, come back later."
        )
