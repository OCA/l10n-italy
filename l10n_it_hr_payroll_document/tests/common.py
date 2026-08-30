# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.hr_payroll_document.tests.common import (
    TestHrPayrollDocument as PayrollCommon,
)


class Common(PayrollCommon):
    def setUp(self):
        super().setUp()
        # This has to be repeated before each test
        # because the setUp in super removes it
        self.env.company.country_id = self.env.ref("base.it")
