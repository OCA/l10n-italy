# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.hr_payroll_document.tests.common import (
    TestHrPayrollDocument as PayrollCommon,
)


class Common(PayrollCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.update(
            {
                "country_id": cls.env.ref("base.it"),
                "vat": "12345670017",
            }
        )
