# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.l10n_multi_country.tests.test_base import TestHideFieldsBase


class TestAccountMixin(TestHideFieldsBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_it = cls.env["res.company"].create({
            "name": "Italy test company",
            "country_id": cls.env.ref("base.it").id,
        })

    def test_show_it_fields_account_group(self):
        self.assertTrue(
            "'invisible': [('company_country_code','!=', 'IT')]}" in
            self._get_field_name_attrs(
                'account_balance_sign', self.company_it, 'account.group', False
            )
        )

    def test_show_it_fields_account_account_type(self):
        self.assertTrue(
            "'invisible': [('company_country_code','!=', 'IT')]}" in
            self._get_field_name_attrs(
                'account_balance_sign', self.company_it, 'account.account.type', False
            )
        )
