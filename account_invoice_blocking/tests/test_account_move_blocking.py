# Copyright 2016 Acsone SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.account.tests.account_test_savepoint import AccountTestInvoicingCommon


class TestAccountMoveBlocking(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.in_invoice = cls.init_invoice("in_invoice")
        cls.out_invoice = cls.init_invoice("out_invoice")

    def test_in_invoice_blocking(self):
        self.assertFalse(self.in_invoice.blocked)
        line = self.in_invoice.line_ids.filtered(
            lambda r: r.account_id.user_type_id
            == self.env.ref("account.data_account_type_payable")
        )
        self.assertTrue(line)
        self.assertFalse(line.blocked)
        self.assertFalse(any(il.blocked for il in (self.in_invoice.line_ids - line)))
        self.in_invoice.blocked = True
        self.assertTrue(line.blocked)
        self.assertFalse(any(il.blocked for il in (self.in_invoice.line_ids - line)))

    def test_out_invoice_blocking(self):
        self.assertFalse(self.out_invoice.blocked)
        line = self.out_invoice.line_ids.filtered(
            lambda r: r.account_id.user_type_id
            == self.env.ref("account.data_account_type_receivable")
        )
        self.assertTrue(line)
        self.assertFalse(line.blocked)
        self.assertFalse(any(il.blocked for il in (self.out_invoice.line_ids - line)))
        self.out_invoice.blocked = True
        self.assertTrue(line.blocked)
        self.assertFalse(any(il.blocked for il in (self.out_invoice.line_ids - line)))
