# Copyright (c) 2020, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>

from odoo import fields, models

WIZARD_STEPS = [("initial", "Initial"), ("confirm", "Confirm")]
DOMAIN_WIZARD_STEPS = [s[0] for s in WIZARD_STEPS]


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _default_step(self):
        active_ids = self.env.context.get("active_ids", [])
        sale_order_ids = self.env["sale.order"].browse(active_ids)
        states = sale_order_ids.mapped("delivery_note_ids.state")

        if any(s == "draft" for s in states):
            return DOMAIN_WIZARD_STEPS[1]

        return DOMAIN_WIZARD_STEPS[0]

    step = fields.Selection(WIZARD_STEPS, string="Current step", default=_default_step)

    def action_step_confirm(self):
        self.step = DOMAIN_WIZARD_STEPS[0]

        return self.goto(context=self.env.context)

    def goto(self, **kwargs):
        self.ensure_one()

        return {
            "name": self.env._("Invoice Order"),
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "views": [(False, "form")],
            "view_mode": "form",
            "target": "new",
            **kwargs,
        }
