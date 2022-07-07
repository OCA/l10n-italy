#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.fields import first

from .rc_common import ReverseChargeCommon


class TestAccountRCType(ReverseChargeCommon):

    def test_with_supplier_self_invoice(self):
        """
        Check that Reverse Charge Types
        that require a supplier self invoice,
        must have an Original Purchase Tax in the mapping.
        """
        rc_type = self.rc_type_eeu
        rc_type_mapping = first(rc_type.tax_ids)
        self.assertTrue(rc_type.with_supplier_self_invoice)
        self.assertTrue(rc_type_mapping.original_purchase_tax_id)

        with self.assertRaises(ValidationError) as ve:
            rc_type_mapping.original_purchase_tax_id = False
        exc_message = ve.exception.args[0]

        self.assertIn("Original Purchase Tax is required", exc_message)
        self.assertIn(rc_type.display_name, exc_message)
