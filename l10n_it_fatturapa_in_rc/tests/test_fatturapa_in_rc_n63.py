from odoo.addons.l10n_it_fatturapa_in.tests.fatturapa_common import (
    FatturapaCommon)
from odoo.tests import tagged


class TestInvoiceRCN63(FatturapaCommon):

    def setUp(self):
        super(TestInvoiceRCN63, self).setUp()
        self.invoice_model = self.env['account.invoice']
        self.invoice_line_model = self.env['account.invoice.line']
        self.partner_model = self.env['res.partner']
        self._create_account()
        self._create_taxes()
        self._create_journals()
        self._create_rc_types()
        self._create_rc_type_taxes()
        self._create_fiscal_position()

    def _create_account(self):
        account_model = self.env['account.account']
        self.account_selfinvoice = account_model.create({
            'code': '295000',
            'name': 'selfinvoice temporary',
            'user_type_id': self.env.ref(
                'account.data_account_type_current_liabilities').id
        })

    def _create_taxes(self):
        tax_model = self.env['account.tax']
        self.tax_n63ai = tax_model.create({
            'name': "Acquisti Art. 17 c. 6 lett. a) ter (22%)",
            'type_tax_use': 'purchase',
            'amount': 22,
            'kind_id': self.env.ref('l10n_it_account_tax_kind.n6_3').id,
            'sequence': 20,
        })
        self.tax_n63vi = tax_model.create({
            'name': "Acquisti Art. 17 c. 6 lett. a) ter (22%) (integrazione)",
            'type_tax_use': 'sale',
            'amount': 22,
            'kind_id': self.env.ref('l10n_it_account_tax_kind.n6_3').id,
            'law_reference': 'articoli 23 e 25 D.P.R. 633/1972',
            'sequence': 20,
        })

    def _create_journals(self):
        journal_model = self.env['account.journal']
        self.journal_selfinvoice = journal_model.create({
            'name': 'selfinvoice',
            'type': 'sale',
            'code': 'SLF',
            'update_posted': True
        })
        self.journal_reconciliation = journal_model.create({
            'name': 'RC reconciliation',
            'type': 'bank',
            'code': 'SLFRC',
            'default_credit_account_id': self.account_selfinvoice.id,
            'default_debit_account_id': self.account_selfinvoice.id,
            'update_posted': True
        })
        self.journal_selfinvoice_extra = journal_model.create({
            'name': 'Extra Selfinvoice',
            'type': 'sale',
            'code': 'SLFEX',
            'update_posted': True
        })

    def _create_rc_types(self):
        rc_type_model = self.env['account.rc.type']
        self.rc_type_n6_3 = rc_type_model.create({
            'name': 'Acquisti Art. 17 c. 6 lett. a) ter (22%)',
            'method': 'selfinvoice',
            'partner_type': 'other',
            'partner_id': self.env.ref('base.main_partner').id,
            'journal_id': self.journal_selfinvoice.id,
            'payment_journal_id': self.journal_reconciliation.id,
            'transitory_account_id': self.account_selfinvoice.id,
            'e_invoice_suppliers': True,
        })

    def _create_rc_type_taxes(self):
        rc_type_tax_model = self.env['account.rc.type.tax']
        self.rc_type_tax_n6_3 = rc_type_tax_model.create({
            'rc_type_id': self.rc_type_n6_3.id,
            'purchase_tax_id': self.tax_n63ai.id,
            'sale_tax_id': self.tax_n63vi.id
        })
        self.rc_type_n6_3.tax_ids = [(6, 0, self.rc_type_tax_n6_3.ids)]

    def _create_fiscal_position(self):
        model_fiscal_position = self.env['account.fiscal.position']
        self.fiscal_position_rc_n6_3 = model_fiscal_position.create({
            'name': 'Acquisti Art. 17 c. 6 lett. a) ter (22%) ITA',
            'rc_type_id': self.rc_type_n6_3.id
        })

    def test_00_xml_import_n63(self):
        res = self.run_wizard(
            'test2', 'IT01234567890_FPR05.xml',
            module_name='l10n_it_fatturapa_in_rc')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        # Set invoice with RC fiscal position
        invoice.fiscal_position_id=self.fiscal_position_rc_n6_3.id
        # Set all invoice lines as RC line
        for line in invoice.invoice_line_ids:
            line.update({
                "invoice_line_tax_ids": [(4, self.tax_n63ai.id)],
                "rc": True,
            })
        self.assertEqual(invoice.invoice_line_ids[0].name, 'BENE 1')
        self.assertTrue(invoice.invoice_line_ids[0].rc)
        self.assertEqual(invoice.invoice_line_ids[1].name, 'SPEDIZIONE')
        self.assertTrue(invoice.invoice_line_ids[1].rc)
        self.assertEqual(
            invoice.invoice_line_ids[0].invoice_line_tax_ids.name,
            'Acquisti Art. 17 c. 6 lett. a) ter (22%)')
        self.assertEqual(invoice.amount_total, 102.01)
        self.assertEqual(invoice.get_tax_amount_added_for_rc(), 18.32)
        self.assertEqual(invoice.amount_tax, 18.76)
        self.assertEqual(invoice.e_invoice_amount_tax, 0.0)
        invoice.action_invoice_open()
        self.assertAlmostEqual(invoice.rc_self_invoice_id.amount_total, 102.01)
        self.assertEqual(invoice.rc_self_invoice_id.amount_tax, 18.32)
        self.assertEqual(invoice.rc_self_invoice_id.amount_untaxed, 85.25)
        self.assertEqual(
            invoice.rc_self_invoice_id.invoice_line_ids.
            invoice_line_tax_ids.name,
            'Acquisti Art. 17 c. 6 lett. a) ter (22%) (integrazione)'
        )

        partner = invoice.partner_id
        partner.e_invoice_detail_level = '0'
        res = self.run_wizard(
            'test3', 'IT01234567890_FPR05.xml',
            module_name='l10n_it_fatturapa_in_rc')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(len(invoice.invoice_line_ids) == 0)
