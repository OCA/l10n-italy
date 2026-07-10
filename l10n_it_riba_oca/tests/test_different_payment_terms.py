# Copyright 2026 Nextev Srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields

from .riba_common import TestRibaCommon


class TestDifferentPaymentTermsDueCost(TestRibaCommon):
    """Regression tests: one_a_maturity must not add duplicate expenses when two
    invoices for the same partner share a maturity date but use different RiBa
    payment terms."""

    def setUp(self):
        super().setUp()
        self.invoice.company_id.due_cost_service_id = self.service_due_cost.id
        self.partner.riba_policy_expenses = "one_a_maturity"
        # Single-maturity 60-day payment term
        self.payment_term_60 = self.env["account.payment.term"].create(
            {
                "name": "RiBa 60",
                "riba": True,
                "riba_payment_cost": 5.00,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "value": "percent",
                            "delay_type": "days_after",
                            "nb_days": 60,
                            "days_next_month": "0",
                        },
                    )
                ],
            }
        )

    def _make_invoice(self, payment_term, invoice_date="2026-01-01"):
        self.partner.property_account_receivable_id = self.account_rec1_id.id
        return self.env["account.move"].create(
            {
                "invoice_date": fields.Date.from_string(invoice_date),
                "move_type": "out_invoice",
                "journal_id": self.sale_journal.id,
                "partner_id": self.partner.id,
                "invoice_payment_term_id": payment_term.id,
                "riba_partner_bank_id": self.partner.bank_ids[0].id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": self.product1.name,
                            "product_id": self.product1.id,
                            "quantity": 1.0,
                            "price_unit": 100.00,
                            "account_id": self.sale_account.id,
                            "tax_ids": [[6, 0, []]],
                        },
                    )
                ],
            }
        )

    def _due_cost_count(self, invoice):
        return len(invoice.invoice_line_ids.filtered("due_cost_line"))

    def test_no_duplicate_sequential_different_terms(self):
        """FATTURA 1 (30/60GG) is posted first; its 60-day maturity coincides
        with FATTURA 2 (60GG). Posting FATTURA 2 afterwards must not create a
        second expense for that shared date."""
        # Same invoice date so the 60-day maturities coincide exactly.
        inv1 = self._make_invoice(self.payment_term1)  # 30/60GG -> 2 maturities
        inv2 = self._make_invoice(
            self.payment_term_60
        )  # 60GG   -> 1 maturity (same as inv1's second)

        inv1.action_post()
        inv2.action_post()

        # inv1 keeps expenses for both maturities (30-day and 60-day)
        self.assertEqual(self._due_cost_count(inv1), 2)
        # inv2's only maturity is already covered by inv1 – no new expense
        self.assertEqual(self._due_cost_count(inv2), 0)

    def test_no_duplicate_batch_different_terms(self):
        """Same scenario but both invoices are confirmed in a single action_post
        call (batch). inv1 is not yet 'posted' when inv2 is checked, so the fix
        must find inv1's draft receivable lines to detect the shared maturity."""
        inv1 = self._make_invoice(self.payment_term1)
        inv2 = self._make_invoice(self.payment_term_60)

        (inv1 | inv2).action_post()

        self.assertEqual(self._due_cost_count(inv1), 2)
        self.assertEqual(self._due_cost_count(inv2), 0)

    def test_expense_added_when_different_maturity(self):
        """Control: if FATTURA 2's maturity is genuinely new (no overlap with
        FATTURA 1), an expense must still be added for it."""
        # inv1: 30/60GG from 2026-01-01 -> maturities 2026-01-31 and 2026-03-02
        inv1 = self._make_invoice(self.payment_term1, invoice_date="2026-01-01")
        # inv2: 60GG from 2026-02-01 -> maturity 2026-04-02 (not in inv1's set)
        inv2 = self._make_invoice(self.payment_term_60, invoice_date="2026-02-01")

        inv1.action_post()
        inv2.action_post()

        self.assertEqual(self._due_cost_count(inv1), 2)
        # New maturity -> expense must be present
        self.assertEqual(self._due_cost_count(inv2), 1)
