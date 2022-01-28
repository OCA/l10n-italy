#  Copyright 2022 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestRiBaCommon(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.menu_model = self.env["ir.ui.menu"]
        self.root_riba_menu = self.browse_ref("l10n_it_ricevute_bancarie.menu_riba")
        self.new_parent = self.browse_ref("base.menu_custom")

    def test_sibling_moved(self):
        """Check that RiBa menu is moved when a sibling changes parent."""
        root_riba_parent_menu = self.root_riba_menu.parent_id
        sibling_menu = self.menu_model.search(
            [
                ("parent_id", "=", root_riba_parent_menu.id),
            ],
            limit=1,
        )
        # pre-condition: menus have same parent
        self.assertEqual(root_riba_parent_menu, sibling_menu.parent_id)

        # Change sibling's parent
        sibling_menu.parent_id = self.new_parent

        # Check that RiBa menu's parent has changed according to its sibling
        self.assertEqual(self.root_riba_menu.parent_id, sibling_menu.parent_id)
        self.assertNotEqual(self.root_riba_menu.parent_id, root_riba_parent_menu)

    def test_not_sibling_not_moved(self):
        """Check that RiBa menu is not moved when a menu
        that is not a sibling changes parent."""
        root_riba_parent_menu = self.root_riba_menu.parent_id
        not_sibling_menu = self.menu_model.search(
            [
                ("parent_id", "!=", root_riba_parent_menu.id),
            ],
            limit=1,
        )
        # pre-condition: menus have different parent
        self.assertNotEqual(root_riba_parent_menu, not_sibling_menu.parent_id)

        # Change not-sibling menu's parent
        not_sibling_menu.parent_id = self.new_parent

        # Check RiBa menu's parent is not changed
        self.assertEqual(self.root_riba_menu.parent_id, root_riba_parent_menu)
