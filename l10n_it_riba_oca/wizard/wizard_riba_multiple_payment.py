#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class RibaPaymentMultiple(models.TransientModel):
    _name = "riba.payment.multiple"
    _description = "Pay multiple RiBa lines"

    riba_ids = fields.Many2many(
        comodel_name="riba.slip",
        default=lambda model: model.env.context["active_ids"],
        readonly=True,
        required=True,
        string="Selected RiBas",
    )
    payment_date = fields.Date(
        compute="_compute_payment_date",
        help="Defaults to the 'Payment date' in the RiBas.\n"
        "If empty, the due date in each line will be used.",
        readonly=False,
        store=True,
    )
    riba_line_ids = fields.Many2many(
        comodel_name="riba.slip.line",
        compute="_compute_riba_line_ids",
        domain="["
        "'&',"
        "('slip_id', 'in', riba_ids),"
        # The following domain must match the domain
        # that shows the 'Pay' button in each RiBa line
        "'|',"
        "'&',"
        "('type', '=', 'sbf'),"
        "('state', '=', 'credited'),"
        "'&',"
        "('type', '=', 'incasso'),"
        "('state', '=', 'confirmed'),"
        "]",
        readonly=False,
        store=True,
        string="RiBa lines to be paid",
    )

    @api.depends(
        "riba_ids.date_paid",
    )
    def _compute_payment_date(self):
        for wizard in self:
            ribas = wizard.riba_ids
            wizard.payment_date = max(ribas.mapped("date_paid"))

    @api.depends(
        "riba_ids.line_ids",
    )
    def _compute_riba_line_ids(self):
        riba_lines_domain = self.fields_get(
            allfields=[
                "riba_line_ids",
            ],
            attributes=[
                "domain",
            ],
        )["riba_line_ids"]["domain"]
        for wizard in self:
            ribas = wizard.riba_ids
            wizard_riba_lines_domain = safe_eval(
                riba_lines_domain,
                globals_dict={
                    "riba_ids": ribas.ids,
                },
            )
            wizard.riba_line_ids = ribas.line_ids.filtered_domain(
                wizard_riba_lines_domain
            )

    def pay(self):
        self.ensure_one()
        lines = self.riba_line_ids
        if not lines:
            raise UserError(self.env._("Please select the RiBa lines to be paid"))
        incasso_lines = lines.filtered(lambda line: line.type == "incasso")
        sbf_lines = lines - incasso_lines
        # type "incasso" lines need to be set as paid only without settlement
        # and account moves creation
        incasso_lines.state = "paid"
        # type "sbf" lines need to be settled and account moves created
        if sbf_lines:
            sbf_lines.riba_line_settlement(
                date=self.payment_date,
            )
        # set the state of the RiBa slips to 'paid' if all their lines are paid
        for slip in lines.slip_id:
            if list(set(slip.line_ids.mapped("state"))) == ["paid"]:
                slip.state = "paid"

    def skip(self):
        active_id = self.env.context.get("active_id") or False
        if not active_id:
            raise UserError(self.env._("No active ID found."))
        riba_slip = self.env["riba.slip"].browse(active_id)
        riba_slip.state = "paid"
        riba_slip.line_ids.state = "paid"
        return {"type": "ir.actions.act_window_close"}
