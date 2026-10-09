# Copyright 2026 Lorenzo Battistini
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo import Command
from odoo.exceptions import UserError

from .common import Common

UPLOAD_SINGLE = (
    "odoo.addons.l10n_it_edi.models.account_move.AccountMove"
    "._l10n_it_edi_upload_single"
)


class TestSendSelfInvoices(Common):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.french_partner = cls.env["res.partner"].create(
            {
                "name": "Alessi",
                "vat": "FR15437982937",
                "country_id": cls.env.ref("base.fr").id,
                "street": "Avenue Test rue",
                "zip": "84000",
                "city": "Avignon",
                "is_company": True,
            }
        )
        cls.purchase_rc_tax = (
            cls.env["account.tax"]
            .with_company(cls.company)
            .create(
                {
                    "name": "22% purchase Reverse Charge",
                    "amount": 22.0,
                    "amount_type": "percent",
                    "type_tax_use": "purchase",
                    "invoice_repartition_line_ids": cls.repartition_lines(
                        cls.RepartitionLine(100, "base", ("+03", "+vj9")),
                        cls.RepartitionLine(100, "tax", ("+5v",)),
                        cls.RepartitionLine(-100, "tax", ("-4v",)),
                    ),
                    "refund_repartition_line_ids": cls.repartition_lines(
                        cls.RepartitionLine(100, "base", ("-03", "-vj9")),
                        cls.RepartitionLine(100, "tax", False),
                        cls.RepartitionLine(-100, "tax", False),
                    ),
                }
            )
        )
        cls.purchase_tax = (
            cls.env["account.tax"]
            .with_company(cls.company)
            .create(
                {
                    "name": "22% purchase",
                    "amount": 22.0,
                    "amount_type": "percent",
                    "type_tax_use": "purchase",
                }
            )
        )

    def _create_bill(self, partner, tax):
        return (
            self.env["account.move"]
            .with_company(self.company)
            .create(
                {
                    "move_type": "in_invoice",
                    "invoice_date": "2026-01-10",
                    "date": "2026-01-10",
                    "partner_id": partner.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "Product A",
                                "product_id": self.product_a.id,
                                "price_unit": 100.0,
                                "tax_ids": [Command.set(tax.ids)],
                            }
                        ),
                    ],
                }
            )
        )

    def _send_self_invoices(self, moves, upload_errors=None):
        """Send `moves` in bulk, uploading the moves of `upload_errors`
        raises the mapped error.

        Return the notification action and the uploaded moves.
        """
        upload_errors = upload_errors or {}
        uploaded_moves = self.env["account.move"]

        def upload_single(move, file):
            nonlocal uploaded_moves
            if move in upload_errors:
                raise upload_errors[move]
            uploaded_moves |= move
            return {"id_transaction": f"SDI ID {move.id}"}

        with patch(UPLOAD_SINGLE, side_effect=upload_single, autospec=True):
            action = moves.action_l10n_it_edi_ext_send_self_invoices()
        return action, uploaded_moves

    def test_send_self_invoices(self):
        """Only the self-invoices among the selected moves are sent."""
        self_invoices = self._create_bill(
            self.french_partner, self.purchase_rc_tax
        ) | self._create_bill(self.french_partner, self.purchase_rc_tax)
        bill = self._create_bill(self.italian_partner_a, self.purchase_tax)
        draft_self_invoice = self._create_bill(
            self.french_partner, self.purchase_rc_tax
        )
        (self_invoices | bill).action_post()
        self.assertTrue(all(self_invoices.mapped("l10n_it_edi_is_self_invoice")))
        self.assertFalse(bill.l10n_it_edi_is_self_invoice)

        action, uploaded_moves = self._send_self_invoices(
            self_invoices | bill | draft_self_invoice
        )

        self.assertEqual(uploaded_moves, self_invoices)
        for self_invoice in self_invoices:
            self.assertTrue(self_invoice.is_move_sent)
            self.assertEqual(self_invoice.l10n_it_edi_state, "processing")
            self.assertEqual(
                self_invoice.l10n_it_edi_transaction, f"SDI ID {self_invoice.id}"
            )
            self.assertTrue(self_invoice.l10n_it_edi_attachment_id)
        self.assertFalse(bill.l10n_it_edi_attachment_id)
        self.assertFalse(draft_self_invoice.l10n_it_edi_attachment_id)
        self.assertEqual(action["params"]["type"], "success")

        # Self-invoices already sent are not sent again
        with self.assertRaises(UserError):
            self._send_self_invoices(self_invoices)

    def test_send_self_invoices_commit(self):
        """Each self-invoice is committed right after being sent."""
        self_invoices = self._create_bill(
            self.french_partner, self.purchase_rc_tax
        ) | self._create_bill(self.french_partner, self.purchase_rc_tax)
        self_invoices.action_post()
        committed_sent_moves = []

        def commit():
            committed_sent_moves.append(
                self_invoices.filtered("l10n_it_edi_transaction")
            )

        with (
            patch.object(
                self.registry["account.move"], "_can_commit", return_value=True
            ),
            patch.object(self.env.cr, "commit", side_effect=commit),
        ):
            self._send_self_invoices(self_invoices)

        self.assertEqual(committed_sent_moves, [self_invoices[0], self_invoices])

    def test_send_self_invoices_errors(self):
        """A self-invoice with errors does not stop the others from being sent
        and does not roll back the ones already sent."""
        first_self_invoice = self._create_bill(
            self.french_partner, self.purchase_rc_tax
        )
        check_error_self_invoice = self._create_bill(
            self.american_partner, self.purchase_rc_tax
        )
        user_error_self_invoice = self._create_bill(
            self.french_partner, self.purchase_rc_tax
        )
        unexpected_error_self_invoice = self._create_bill(
            self.french_partner, self.purchase_rc_tax
        )
        last_self_invoice = self._create_bill(self.french_partner, self.purchase_rc_tax)
        sent_self_invoices = first_self_invoice | last_self_invoice
        error_self_invoices = (
            check_error_self_invoice
            | user_error_self_invoice
            | unexpected_error_self_invoice
        )
        # Errors happen after the first self-invoice is sent
        self_invoices = first_self_invoice | error_self_invoices | last_self_invoice
        self_invoices.action_post()

        with self.assertLogs(
            "odoo.addons.l10n_it_edi_extension.models.account_move", level="ERROR"
        ) as logs:
            action, uploaded_moves = self._send_self_invoices(
                self_invoices,
                upload_errors={
                    user_error_self_invoice: UserError(self.env._("Upload failed")),
                    unexpected_error_self_invoice: KeyError("unexpected"),
                },
            )

        self.assertEqual(uploaded_moves, sent_self_invoices)
        for self_invoice in sent_self_invoices:
            self.assertTrue(self_invoice.is_move_sent)
            self.assertEqual(self_invoice.l10n_it_edi_state, "processing")
            self.assertTrue(self_invoice.l10n_it_edi_attachment_id)
        for error_self_invoice in error_self_invoices:
            self.assertFalse(error_self_invoice.is_move_sent)
            self.assertFalse(error_self_invoice.l10n_it_edi_state)
            self.assertFalse(error_self_invoice.l10n_it_edi_attachment_id)
        # Export check errors are in the warning of the document,
        # the other errors are in the notification
        self.assertTrue(check_error_self_invoice.l10n_it_edi_header)
        message = action["params"]["message"]
        self.assertEqual(action["params"]["type"], "warning")
        self.assertIn(check_error_self_invoice.name, message)
        self.assertIn(f"{user_error_self_invoice.name}: Upload failed", message)
        self.assertIn(unexpected_error_self_invoice.name, message)
        # Only unexpected errors are logged
        self.assertEqual(len(logs.records), 1)
        self.assertIn(unexpected_error_self_invoice.name, logs.output[0])
