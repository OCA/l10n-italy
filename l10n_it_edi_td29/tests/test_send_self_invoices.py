# Copyright 2026 Lorenzo Battistini
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo import Command

from .common import Common

UPLOAD_SINGLE = (
    "odoo.addons.l10n_it_edi.models.account_move.AccountMove"
    "._l10n_it_edi_upload_single"
)


class TestSendSelfInvoices(Common):
    def test_send_td29(self):
        """TD29 communications are sent in bulk like self-invoices."""
        purchase_tax_22 = (
            self.env["account.tax"]
            .with_company(self.company)
            .create(
                {
                    "name": "22% purchase",
                    "amount": 22.0,
                    "amount_type": "percent",
                    "type_tax_use": "purchase",
                }
            )
        )
        td29_bill, bill = (
            self.env["account.move"]
            .with_company(self.company)
            .create(
                [
                    {
                        "move_type": "in_invoice",
                        "invoice_date": "2026-01-10",
                        "date": "2026-01-10",
                        "partner_id": self.italian_partner_a.id,
                        "l10n_it_edi_is_td29": is_td29,
                        "invoice_line_ids": [
                            Command.create(
                                {
                                    "name": "test line",
                                    "price_unit": 100.0,
                                    "tax_ids": [Command.set(purchase_tax_22.ids)],
                                }
                            ),
                        ],
                    }
                    for is_td29 in (True, False)
                ]
            )
        )
        (td29_bill | bill).action_post()

        with patch(
            UPLOAD_SINGLE, return_value={"id_transaction": "SDI ID"}
        ) as upload_single:
            (td29_bill | bill).action_l10n_it_edi_ext_send_self_invoices()

        # Only the TD29 communication is sent:
        # the other bill is not a self-invoice, so it is skipped
        self.assertEqual(upload_single.call_count, 1)
        self.assertTrue(td29_bill.is_move_sent)
        self.assertEqual(td29_bill.l10n_it_edi_state, "processing")
        self.assertFalse(bill.is_move_sent)
        self.assertFalse(bill.l10n_it_edi_attachment_id)
