# Copyright 2026 Simone Rubino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import tagged

from odoo.addons.point_of_sale.tests.test_frontend import TestPointOfSaleHttpCommon


@tagged("post_install", "-at_install")
class TestUi(TestPointOfSaleHttpCommon):
    # TODO: Delete if merged https://github.com/odoo/odoo/pull/240587
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pos_user.groups_id += cls.env.ref("base.group_system")

    def test_fiscal_code_search(self):
        """A Customer can be found using its fiscal code."""
        # Arrange
        self.env["res.partner"].create(
            {
                "name": "Test Customer with fiscal code",
                "is_company": False,
                "l10n_it_codice_fiscale": "RSSMRA84H04H501X",
            }
        )
        pos_config = self.main_pos_config
        pos_user = self.pos_user
        pos_config.with_user(pos_user).open_ui()

        # Assert
        self.start_pos_tour(
            "SearchByFiscalCode",
        )
