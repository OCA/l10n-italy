from odoo import api, fields, models


class HrEmployeeInherit(models.AbstractModel):
    _inherit = "hr.employee"

    fiscal_operator_number = fields.Char(
        string="Fiscal Printer Operator", size=1, default="1", tracking=True
    )

    @api.onchange("fiscal_operator_number")
    def _onchange_fiscal_operator_number(self):
        for rec in self:
            if rec.user_id:
                rec.user_id.fiscal_operator_number = rec.fiscal_operator_number
