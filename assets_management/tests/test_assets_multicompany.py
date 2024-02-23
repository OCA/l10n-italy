# Copyright 2023 Nextev Srl <odoo@nextev.it>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests.common import Form, users

from .test_assets_common import TestAssets


class TestAssetsMulticompany(TestAssets):
    @users("user")
    def test_00_create_depreciation_mode_multicompany(self):
        """
        It checks that you cannot change the default associated company upon
        asset depreciation mode creation
        """
        mode_form = Form(self.env["asset.depreciation.mode"])
        mode_form.name = "Move 1"
        mode_form.save()
        with self.assertRaises(
            AssertionError, msg="can't write on readonly field company_id"
        ):
            mode_form.company_id = self.company_2
