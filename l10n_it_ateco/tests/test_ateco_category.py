# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import new_test_user, tagged, users

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class TestAtecoCategory(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        new_test_user(
            cls.env,
            login="ateco_manager",
            groups="base.group_user,base.group_partner_manager",
        )
        cls.ateco_model = cls.env["ateco.category"]
        cls.old_code = cls.ateco_model.create(
            {
                "code": "Z99.99.1",
                "name": "Old test activity",
                "ateco_version": "2007",
            }
        )
        cls.new_code = cls.ateco_model.create(
            {
                "code": "Z99.99.10",
                "name": "New test activity",
                "ateco_version": "2025",
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test ATECO partner",
                "ateco_category_ids": [(6, 0, (cls.old_code | cls.new_code).ids)],
            }
        )

    def test_data_ateco_2025(self):
        """Module data is the ATECO 2025 hierarchy."""
        subcategory = self.env.ref("l10n_it_ateco.ateco_category_2025_A011100")
        self.assertEqual(subcategory.code, "A01.11.00")
        self.assertEqual(subcategory.ateco_version, "2025")
        self.assertEqual(subcategory.description, subcategory.name)
        self.assertTrue(subcategory.active)
        ancestors = []
        parent = subcategory.parent_id
        while parent:
            ancestors.append(parent.code)
            parent = parent.parent_id
        self.assertEqual(ancestors, ["A01.11.0", "A01.11", "A01.1", "A01", "A"])
        self.assertEqual(
            self.env.ref("l10n_it_ateco.ateco_category_2025_A").name,
            "Agricoltura, silvicoltura e pesca",
        )

    @users("ateco_manager")
    def test_archive_keeps_partner_codes(self):
        """Archived codes stay linked and visible on the partner."""
        old_code = self.old_code.with_env(self.env)
        partner = self.partner.with_env(self.env)
        old_code.action_archive()
        self.assertFalse(old_code.active)
        self.assertEqual(partner.ateco_category_ids, old_code | self.new_code)
        self.assertNotIn(
            old_code,
            self.env["ateco.category"].search([("code", "like", "Z99.99.")]),
        )

    @users("ateco_manager")
    def test_search_partner_archived_codes(self):
        """Partners with archived codes can be found."""
        domain = [
            ("ateco_category_ids.active", "=", False),
            ("id", "=", self.partner.id),
        ]
        partner_model = self.env["res.partner"]
        self.assertFalse(partner_model.search(domain))
        self.old_code.with_env(self.env).action_archive()
        self.assertEqual(partner_model.search(domain), self.partner)
