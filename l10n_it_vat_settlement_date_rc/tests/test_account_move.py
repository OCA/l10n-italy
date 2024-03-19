#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime

from odoo.tests import tagged

from odoo.addons.l10n_it_reverse_charge.tests.rc_common import ReverseChargeCommon


@tagged("post_install", "-at_install")
class TestAccountMove(ReverseChargeCommon):
    def test_settlement_date_propagation(self):
        """The settlement date is propagated to the RC Self Invoice."""
        # Arrange
        invoice = self.create_invoice(
            self.supplier_intraEU,
            amounts=[
                100,
            ],
            taxes=self.tax_22ai,
            post=False,
        )
        invoice.l10n_it_vat_settlement_date = datetime.date(2020, 1, 1)

        # Act
        invoice.action_post()

        # Assert
        rc_self_invoice = invoice.rc_self_invoice_id
        self.assertEqual(
            invoice.l10n_it_vat_settlement_date,
            rc_self_invoice.l10n_it_vat_settlement_date,
        )
