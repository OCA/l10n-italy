# Copyright 2017 Lorenzo Battistini

from odoo.tests.common import TransactionCase

from odoo.addons.l10n_it_account.tools.account_tools import fpa_schema_get_enum


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
        revenue_account_type = \
            self.env.ref('account.data_account_type_revenue')
        revenue_account = self.env['account.account'].search(
            [('user_type_id', '=', revenue_account_type.id)], limit=1)
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

    def test_compare_with_fpa_schema(self):
        """Check that the values we define in this module are
        the same as those defined in FPA xsd"""

        my_codes = self.doc_type_model.search([]).mapped("code")

        # XXX hardcoded: fattura elettronica semplificata
        my_codes = [code for code in my_codes if code not in ["TD07", "TD08", "TD09"]]

        # XXX hardcoded: esterometro
        my_codes = [code for code in my_codes if code not in ["TD10", "TD11", "TD12"]]

        # from fatturapa xml Schema
        xsd_codes = [code for code, descr in fpa_schema_get_enum("TipoDocumentoType")]

        self.assertCountEqual(my_codes, xsd_codes)
