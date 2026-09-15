# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from codicefiscale import isvalid as is_fiscalcode_valid

from odoo import exceptions

from odoo.addons.l10n_it_hr_payroll_document.tests.common import Common


class TestEmployee(Common):
    def test_employee_fc_valid(self):
        """The fiscal code is a valid identification for an employee."""
        # Arrange
        employee = self.employee_emp
        # pre-condition
        self.assertEqual(self.env.company.country_id, self.env.ref("base.it"))

        # Act
        employee.identification_id = "RSSMRA84H04H501X"

        # Assert
        self.assertTrue(employee.identification_id)

    def test_employee_fc_not_valid(self):
        """A wrong fiscal code cannot be an identification for an employee."""
        # Arrange
        bad_fiscal_code = "RSSMRA84H04H501Xaa"
        employee = self.employee_emp
        # pre-condition
        self.assertEqual(self.env.company.country_id, self.env.ref("base.it"))
        self.assertFalse(is_fiscalcode_valid(bad_fiscal_code))

        # Act
        with self.assertRaises(exceptions.ValidationError) as ve:
            employee.identification_id = bad_fiscal_code

        # Assert
        exc_message = ve.exception.args[0]
        self.assertIn("identification ID is not valid", exc_message)
