
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class HrEmployeeBase(models.AbstractModel):
    
    _inherit = 'hr.employee.base'

    fiscal_operator_number = fields.Char("Fiscal Printer Operator",size=1, default="1",tracking=True)

class HrEmployee(models.AbstractModel):    
    _inherit = 'hr.employee'

    fiscal_operator_number = fields.Char("Fiscal Printer Operator",size=1, default="1",tracking=True)

    @api.depends('fiscal_operator_number')
    def _onchange_fiscal_operator_number(self):
        for rec in self:
            if rec.user_id:
                rec.user_id.fiscal_operator_number = rec.fiscal_operator_number

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    fiscal_operator_number = fields.Char("Fiscal Printer Operator",size=1, default="1")