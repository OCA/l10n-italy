# Copyright 2022 Dinamiche Aziendali srl
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_pos_payment_method(self):
        result = super()._loader_params_pos_payment_method()
        result["search_params"]["fields"].append("fiscalprinter_payment_type")
        result["search_params"]["fields"].append("fiscalprinter_payment_index")
        return result

    def _loader_params_account_tax(self):
        result = super()._loader_params_account_tax()
        result["search_params"]["fields"].append("fpdeptax")
        return result

    def _loader_params_hr_employee(self):
        result = super()._loader_params_hr_employee()
        result["search_params"]["fields"].append("fiscal_operator_number")
        return result

    def _get_pos_ui_hr_employee(self, params):
        employees = super()._get_pos_ui_hr_employee(params)
        for employee in employees:
            emp = self.env['hr.employee'].browse(employee['id'])
            employee['fiscal_operator_number'] = emp.fiscal_operator_number
        return employees
    #     employees = self.env['hr.employee'].search_read(**params['search_params'])
    #     employee_ids = [employee['id'] for employee in employees]
    #     user_ids = [employee['user_id'] for employee in employees if employee['user_id']]
    #     manager_ids = self.env['res.users'].browse(user_ids).filtered(lambda user: self.config_id.group_pos_manager_id in user.groups_id).mapped('id')

    #     employees_barcode_pin = self.env['hr.employee'].browse(employee_ids).get_barcodes_and_pin_hashed()
    #     bp_per_employee_id = {bp_e['id']: bp_e for bp_e in employees_barcode_pin}
    #     for employee in employees:
    #         employee['role'] = 'manager' if employee['user_id'] and employee['user_id'] in manager_ids else 'cashier'
    #         employee['barcode'] = bp_per_employee_id[employee['id']]['barcode']
    #         employee['pin'] = bp_per_employee_id[employee['id']]['pin']
    #         employee['fiscal_operator_number'] = bp_per_employee_id[employee['id']]['fiscal_operator_number']

    #     return employees
