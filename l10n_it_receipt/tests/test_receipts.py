# Copyright 2018 Simone Rubino
# Copyright 2022 Lorenzo Battistini

from odoo.addons.account_receipt_journal.tests.test_receipts \
    import TestReceipts
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestCorrispettivi(TestReceipts):

    def setUp(self):
        super(TestCorrispettivi, self).setUp()
        partner_model = self.env['res.partner']
        self.fiscal_pos_model = self.env['account.fiscal.position']
        self.journal_model = self.env['account.journal']
        self.corr_fiscal_position = self.fiscal_pos_model.create({
            'name': 'receipts fiscal position',
            'receipts': True,
            'company_id': self.env.user.company_id.id
        })
        self.no_corr_fiscal_position = self.fiscal_pos_model.create({
            'name': 'receipts fiscal position',
            'receipts': False,
            'company_id': self.env.user.company_id.id
        })
        self.corrispettivi_partner = partner_model.create({
            'name': 'Receipts partner',
            'use_receipts': True,
            'property_account_position_id': self.corr_fiscal_position.id
        })
        self.no_corrispettivi_partner = partner_model.create({
            'name': 'Receipts partner',
            'use_receipts': False,
            'property_account_position_id': self.no_corr_fiscal_position.id
        })

        self.account_receivable = self.env['account.account'].search(
            [('user_type_id', '=', self.env.ref(
                'account.data_account_type_receivable').id)], limit=1)

    def create_corrispettivi_invoice(self):
        corr_invoice = self.invoice_model \
            .with_context(default_move_type="out_receipt") \
            .create({'invoice_line_ids': [
                         (0, 0, {
                             'account_id': self.a_sale.id,
                             'product_id': self.env.ref('product.product_product_5').id,
                             'name': 'Corrispettivo',
                             'quantity': 1,
                             'price_unit': 10,
                             'tax_ids': [(6, 0, {self.tax22inc.id})]
                         }),
                     ]})
        return corr_invoice

    def test_get_corr_journal(self):
        """ Test that get_corr_journal gets a receipts journal
        or raises an UserError if none found"""
        corr_journal_id = self.journal_model.get_corr_journal()
        self.assertEqual(corr_journal_id.type, 'sale')
        self.assertTrue(corr_journal_id.corrispettivi)

        corr_journal_id.unlink()
        with self.assertRaises(UserError):
            self.journal_model.get_corr_journal()

    def test_get_corr_fiscal_pos(self):
        """ Test that get_corr_fiscal_pos gets a receipts (corrispettivi)
        fiscal position"""
        corr_fiscal_pos = self.fiscal_pos_model.get_corr_fiscal_pos()
        self.assertTrue(corr_fiscal_pos.corrispettivi)

    def test_corrispettivi_partner_onchange(self):
        """ Test onchange in partner. """
        # If the partner uses receipts,
        # the fiscal position must have the flag receipts (corrispettivi)
        self.corrispettivi_partner.onchange_use_corrispettivi()
        self.assertTrue(self.corrispettivi_partner
                        .property_account_position_id.corrispettivi)

        # If the partner does not use receipts
        # and it already has a fiscal position that is
        # receipts (corrispettivi), it must be removed
        self.no_corrispettivi_partner.write({
            'property_account_position_id': self.corr_fiscal_position.id})
        self.no_corrispettivi_partner.onchange_use_corrispettivi()
        self.assertFalse(
            self.no_corrispettivi_partner.property_account_position_id)

        # If the partner does not use receipts
        # and it already has a fiscal position that is
        # not receipts (corrispettivi), it must not be removed
        self.no_corrispettivi_partner.write({
            'property_account_position_id': self.no_corr_fiscal_position.id})
        self.no_corrispettivi_partner.onchange_use_corrispettivi()
        self.assertEqual(
            self.no_corrispettivi_partner.property_account_position_id,
            self.no_corr_fiscal_position)

    def test_invoice_creation_ok(self):
        """ Test invoice creation. """
        corr_invoice = self.create_corrispettivi_invoice()
        self.assertTrue(corr_invoice)

    def test_invoice_creation_ko(self):
        """ Test invoice creation fails . """
        self.journal_model.get_corr_journal().unlink()
        # if no receipts journal exists, raise
        # No journal found for receipts
        with self.assertRaises(UserError):
            self.create_corrispettivi_invoice()

    def test_invoice_refund_ok(self):
        """ Test invoice creation. """
        corr_invoice = self.create_corrispettivi_invoice()
        self.assertTrue(corr_invoice)
        corr_invoice.action_invoice_open()
        self.assertEqual(corr_invoice.state, 'open')
        refund_invoice_dict = self.env['account.invoice.refund'].with_context(
            active_ids=corr_invoice.ids).create({
                'filter_refund': 'refund',
                'description': 'A refund reason',
            }).invoice_refund()
        refund_invoice = self.invoice_model.search(refund_invoice_dict['domain'])
        self.assertTrue(refund_invoice)
        refund_invoice.action_invoice_open()

    def test_invoice_refund_modify_ok(self):
        """ Test invoice creation. """
        corr_invoice = self.create_corrispettivi_invoice()
        self.assertTrue(corr_invoice)
        corr_invoice.action_invoice_open()
        self.assertEqual(corr_invoice.state, 'open')
        refund_invoice_dict = self.env['account.invoice.refund'].with_context(
            active_ids=corr_invoice.ids).create({
                'filter_refund': 'modify',
                'description': 'A modify refund reason',
            }).invoice_refund()
        refund_invoice = self.invoice_model.search(refund_invoice_dict['domain'])
        self.assertTrue(refund_invoice)
        refund_invoice.action_invoice_open()

    def test_invoice_refund_cancel_ok(self):
        """ Test invoice creation. """
        corr_invoice = self.create_corrispettivi_invoice()
        self.assertTrue(corr_invoice)
        corr_invoice.action_invoice_open()
        self.assertEqual(corr_invoice.state, 'open')
        refund_invoice_dict = self.env['account.invoice.refund'].with_context(
            active_ids=corr_invoice.ids).create({
                'filter_refund': 'cancel',
                'description': 'A cancel refund reason',
            }).invoice_refund()
        refund_invoice = self.invoice_model.search(refund_invoice_dict['domain'])
        self.assertTrue(refund_invoice)
