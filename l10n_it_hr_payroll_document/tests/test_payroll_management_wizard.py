# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.addons.l10n_it_hr_payroll_document.tests.common import Common


class TestPayrollManagementWizard(Common):
    def test_send(self):
        """Payrolls can be sent to the employees."""
        # Arrange
        employee = self.employee_emp
        employee.identification_id = "RSSMRA84H04H501X"
        wizard = self._create_wizard(
            "Ottobre", "l10n_it_hr_payroll_document/tests/data/cedolini.pdf".split("/")
        )

        # Act
        result_action = wizard.send_payrolls()

        # Assert
        self.assertEqual(result_action["params"]["title"], "Payrolls sent")

    def test_not_found(self):
        """If the employee is not found, payrolls are not sent."""
        # Arrange
        employee = self.employee_emp
        employee.identification_id = "XSSMRA84H04H501X"
        wizard = self._create_wizard(
            "Ottobre", "l10n_it_hr_payroll_document/tests/data/cedolini.pdf".split("/")
        )

        # Act
        result_action = wizard.send_payrolls()

        # Assert
        self.assertEqual(result_action["params"]["title"], "Employees not found")
