# Copyright 2022 Dinamiche Aziendali srl
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

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
            emp = self.env["hr.employee"].browse(employee["id"])
            employee["fiscal_operator_number"] = emp.fiscal_operator_number
        return employees
