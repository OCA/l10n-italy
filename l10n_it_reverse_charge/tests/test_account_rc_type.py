#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError, ValidationError
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

    def test_tax_map_find(self):
        """
        Check that Reverse Charge Types can map
        Original Purchase Tax to Purchase Tax.
        """
        rc_type = self.rc_type_eeu
        rc_type_mapping = first(rc_type.tax_ids)
        key_tax = rc_type_mapping.original_purchase_tax_id

        mapped_tax = rc_type.map_tax(
            key_tax,
            'original_purchase_tax_id',
            'purchase_tax_id',
        )

        value_tax = rc_type_mapping.purchase_tax_id
        self.assertEqual(value_tax, mapped_tax)

    def test_tax_map_not_found(self):
        """
        Check that Reverse Charge Types
        raise an Error when can't map a tax.
        """
        rc_type = self.rc_type_eeu
        key_taxes = rc_type.tax_ids.mapped('original_purchase_tax_id')
        other_tax = self.env['account.tax'].search(
            [
                ('id', 'not in', key_taxes.ids),
            ],
            limit=1,
        )
        self.assertTrue(other_tax)

        with self.assertRaises(UserError) as ue:
            rc_type.map_tax(
                other_tax,
                'original_purchase_tax_id',
                'purchase_tax_id',
            )
        exc_message = ue.exception.args[0]

        self.assertIn("Can't find tax mapping", exc_message)
        self.assertIn(rc_type.display_name, exc_message)
        self.assertIn(other_tax.display_name, exc_message)
