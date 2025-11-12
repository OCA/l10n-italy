# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from codicefiscale import isvalid as is_fiscalcode_valid

from odoo import models


class Employee(models.Model):
    _inherit = "hr.employee"

    def _l10n_it_validate_payroll_identification(self, code=None):
        if code is None and len(self) == 1:
            code = self.identification_id

        # The Employee ID in an italian Company is the Fiscal Code
        if code:
            is_valid = is_fiscalcode_valid(code)
        else:
            is_valid = True
        return is_valid

    def _validate_payroll_identification(self, code=None):
        if self.env.company.country_id.code == "IT":
            is_valid = self._l10n_it_validate_payroll_identification(code=code)
        else:
            is_valid = super()._validate_payroll_identification(code=code)
        return is_valid
