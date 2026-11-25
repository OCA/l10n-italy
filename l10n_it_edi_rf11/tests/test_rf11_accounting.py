# Copyright 2024-2026 Innovyou srl <http://www.innovyou.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestRf11Accounting(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.payments_journal = cls.company_data["default_journal_misc"]
        cls.env.company.payments_74ter_journal_id = cls.payments_journal
        cls.agency = cls.env["res.partner"].create(
            {"name": "Agenzia Viaggi", "is_74ter_agent": True}
        )
        cls.customer = cls.env["res.partner"].create(
            {
                "name": "Cliente",
                "agent_74ter_id": cls.agency.id,
                "invoices_paid_by_agent": True,
            }
        )

    def test_invoice_paid_by_agency(self):
        """Posting transfers the customer receivable to the agency."""
        invoice = self.init_invoice(
            "out_invoice",
            partner=self.customer,
            amounts=[100.0],
            taxes=self.env["account.tax"],
            post=False,
        )
        invoice.agent_74ter_id = self.agency
        invoice.to_be_paid_by_agent_74ter = True
        invoice.action_post()

        # The customer receivable has been settled (residual is zero).
        self.assertEqual(invoice.amount_residual, 0.0)

        # A write-off entry was booked in the dedicated journal.
        entry = self.env["account.move"].search(
            [
                ("journal_id", "=", self.payments_journal.id),
                ("move_type", "=", "entry"),
            ]
        )
        self.assertTrue(entry)

        # The agency now carries the receivable.
        agency_receivable = entry.line_ids.filtered(
            lambda line: line.partner_id == self.agency
            and line.account_id.account_type == "asset_receivable"
        )
        self.assertTrue(agency_receivable)
        self.assertAlmostEqual(agency_receivable.balance, 100.0)

    def test_without_flag_no_entry(self):
        """Without the 'paid by agency' flag nothing extra is booked."""
        invoice = self.init_invoice(
            "out_invoice",
            partner=self.customer,
            amounts=[100.0],
            taxes=self.env["account.tax"],
            post=False,
        )
        invoice.agent_74ter_id = self.agency
        invoice.to_be_paid_by_agent_74ter = False
        invoice.action_post()

        self.assertEqual(invoice.amount_residual, 100.0)
        self.assertFalse(
            self.env["account.move"].search(
                [
                    ("journal_id", "=", self.payments_journal.id),
                    ("move_type", "=", "entry"),
                ]
            )
        )
