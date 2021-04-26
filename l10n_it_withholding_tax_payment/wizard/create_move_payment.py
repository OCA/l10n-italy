# Copyright 2015 Alessandro Camilli (<http://www.openforce.it>)
# Copyright 2019 Matteo Bilotta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models


class WizardWtMovePaymentCreate(models.TransientModel):
    _name = "wizard.wt.move.payment.create"
    _description = "Create WT Payment Move Wizard"

    def _default_wt_moves(self):
        return self._context.get("active_ids", [])

    wt_move_ids = fields.Many2many(
        "withholding.tax.move",
        "wiz_wt_move_payment_create_rel",
        "wizard_id",
        "wt_move_id",
        "WT Moves",
        readonly=True,
        default=_default_wt_moves,
    )

    def generate(self):
        wt_move_payment_obj = self.env["withholding.tax.move.payment"]
        wt_payment = wt_move_payment_obj.generate_from_moves(self.wt_move_ids)
        view = self.env["ir.model.data"].get_object_reference(
            "l10n_it_withholding_tax_payment", "view_withholding_move_payment_form"
        )
        view_id = view[1] or False

        return {
            "name": _("Withholding Tax Payment"),
            "view_type": "form",
            "view_mode": "form",
            "res_model": "withholding.tax.move.payment",
            "res_id": wt_payment.id,
            "type": "ir.actions.act_window",
            "view_id": [view_id],
        }
