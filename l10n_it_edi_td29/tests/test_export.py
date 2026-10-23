# Copyright 2026 Nextev Srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command

from .common import Common


class TestExport(Common):
    def test_td29_communication(self):
        """A vendor bill flagged as TD29 generates a communication XML
        for omitted or irregular invoicing."""
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
        bill = (
            self.env["account.move"]
            .with_company(self.company)
            .create(
                {
                    "move_type": "in_invoice",
                    "invoice_date": "2024-01-01",
                    "date": "2024-01-01",
                    "partner_id": self.italian_partner_a.id,
                    "l10n_it_edi_is_td29": True,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "test line",
                                "price_unit": 100.0,
                                "quantity": 1,
                                "tax_ids": [Command.set(purchase_tax_22.ids)],
                            }
                        ),
                    ],
                }
            )
        )
        bill.action_post()
        # TD29 is a mere communication to the Tax Agency: it must not be
        # flagged as a self-invoice, otherwise other modules (e.g. VAT
        # registries) would treat it as a reverse charge document
        self.assertFalse(bill.l10n_it_edi_is_self_invoice)
        self._assert_export_invoice(bill, "td29_communication.xml")
