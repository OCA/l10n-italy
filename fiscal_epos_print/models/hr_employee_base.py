from odoo import fields, models


class HrEmployeeBaseInherit(models.AbstractModel):
    _name = "hr.employee.base"
    _inherit = ["hr.employee.base", "mail.thread"]

    fiscal_operator_number = fields.Char(
        string="Fiscal Printer Operator", size=1, default="1", tracking=True
    )
