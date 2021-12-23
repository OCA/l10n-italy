# Copyright 2017 Lorenzo Battistini

from odoo.tests.common import TransactionCase
from odoo.tests import Form


class TestDocType(TransactionCase):

    def setUp(self):
        super(TestDocType, self).setUp()
        self.journalrec = self.env['account.journal'].search(
            [('type', '=', 'sale')])[0]
        self.doc_type_model = self.env['fiscal.document.type']
        self.TD01 = self.doc_type_model.search(
            [('code', '=', 'TD01')], limit=1)
        self.TD04 = self.doc_type_model.search(
            [('code', '=', 'TD04')], limit=1)
        self.inv_model = self.env['account.invoice']
        self.partner3 = self.env.ref('base.res_partner_3')
        self.fp = self.env["account.fiscal.position"].create({
            "name": "FP",
            "fiscal_document_type_id": self.TD01.id,
        })

    def test_doc_type(self):
        self.TD01.journal_ids = [self.journalrec.id]
        invoice = self.inv_model.create({
            'partner_id': self.partner3.id
        })
        invoice._set_document_fiscal_type()
        self.assertEqual(invoice.fiscal_document_type_id.id, self.TD01.id)

        invoice2 = self.inv_model.create({
            'partner_id': self.partner3.id
        })
        self.assertEqual(invoice2.fiscal_document_type_id.id, self.TD01.id)

    def test_doc_type_update(self):
        """Check that document type is updated when updating invoice type."""
        revenue_account_type = self.env.ref(
            'account.data_account_type_revenue'
        )
        revenue_account = self.env["account.account"].search(
            [("user_type_id", "=", revenue_account_type.id)], limit=1
        )
        invoice = self.inv_model.create({
            'partner_id': self.partner3.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.env.ref('product.product_product_5').id,
                'quantity': 10.0,
                'account_id': revenue_account.id,
                'name': 'product test 5',
                'price_unit': 100.00,
            })]})
        self.assertEqual(invoice.fiscal_document_type_id, self.TD01)

        invoice.type = 'out_refund'
        self.assertEqual(invoice.fiscal_document_type_id, self.TD04)

    def test_doc_type_refund(self):
        self.TD01.journal_ids = [self.journalrec.id]
        invoice = self.inv_model.create({
            'partner_id': self.partner3.id
        })
        invoice._set_document_fiscal_type()
        refund = invoice.refund(
            invoice.date_invoice,
            invoice.date,
            'refund test',
            invoice.journal_id.id
        )
        self.assertEqual(refund.fiscal_document_type_id.id, self.TD04.id)

        invoice = self.inv_model.create({
            'partner_id': self.partner3.id,
            "fiscal_position_id": self.fp.id,
        })
        invoice._set_document_fiscal_type()
        refund = invoice.refund(
            invoice.date_invoice,
            invoice.date,
            'refund test',
            invoice.journal_id.id
        )
        self.assertEqual(refund.fiscal_document_type_id.id, self.TD04.id)

    def _set_recompute_document_type(self, invoice, doc_type):
        """Set a document type and recompute the field."""
        # Set document type
        invoice_form = Form(invoice)
        invoice_form.fiscal_document_type_id = doc_type
        invoice = invoice_form.save()
        self.assertEqual(invoice.fiscal_document_type_id, doc_type)

        # Recompute document type for the invoice
        invoice._set_document_fiscal_type()
        return invoice

    def test_keep_edited_invoice(self):
        """Check that the changes performed by the user
        are kept through a recomputation if acceptable."""
        invoice = self.inv_model.create({
            'partner_id': self.partner3.id
        })
        self.assertTrue(invoice.fiscal_document_type_id)

        # Change document type to a not accepted TD04 and check it gets changed
        td04 = self.TD04
        invoice = self._set_recompute_document_type(invoice, td04)
        self.assertNotEqual(invoice.fiscal_document_type_id, td04)

        # Change document type to an accepted TD02 and check it is kept
        td02 = self.doc_type_model.search([("code", "=", "TD02")], limit=1)
        invoice = self._set_recompute_document_type(invoice, td02)
        self.assertEqual(invoice.fiscal_document_type_id, td02)
