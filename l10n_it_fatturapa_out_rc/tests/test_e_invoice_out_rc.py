import base64
from openerp.addons.l10n_it_reverse_charge.tests.rc_common import ReverseChargeCommon
from openerp.addons.l10n_it_fatturapa_out.tests.fatturapa_common import FatturaPACommon
from openerp.exceptions import Warning as UserError


class TestReverseCharge(ReverseChargeCommon, FatturaPACommon):

    def setUp(self):
        super(TestReverseCharge, self).setUp()
        self.company = self.rc_type_ieu.company_id
        self.company.vat = "IT10538570960"  # 06363391001 gives 00399 error
        self.company.fatturapa_art73 = False
        self.rc_type_ieu.partner_type = "other"
        self.rc_type_ieu.partner_id = self.company.partner_id.id
        self.rc_type_ieu.fiscal_document_type_id = self.env.ref(
            "l10n_it_fiscal_document_type.15").id
        self.tax_22vi.kind_id = self.env.ref("l10n_it_account_tax_kind.n6").id

    def set_sequence_journal_selfinvoice(self, invoice_number):
        inv_seq = self.journal_selfinvoice.sequence_id
        inv_seq.number_next_actual = invoice_number

    def set_bill_sequence(self, invoice_number):
        seq_pool = self.env['ir.sequence']
        inv_seq = seq_pool.search([('name', '=', 'Account Default Expenses Journal')])[0]
        inv_seq.number_next_actual = invoice_number

    def test_intra_EU(self):
        self.set_sequence_journal_selfinvoice(15)
        self.set_bill_sequence(25)
        self.supplier_intraEU.property_payment_term_id = self.term_15_30.id
        invoice = self.invoice_model.create({
            'partner_id': self.supplier_intraEU.id,
            'account_id': self.invoice_account,
            'journal_id': self.purchases_journal.id,
            'type': 'in_invoice',
            'date_invoice': '2019-01-15',
            'reference': 'EU-SUPPLIER-REF'
        })
        res = invoice.onchange_partner_id(invoice.type, invoice.partner_id.id)
        invoice.fiscal_position = res['value']['fiscal_position']

        invoice_line_vals = {
            'name': 'Invoice for sample product',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100,
            'invoice_line_tax_id': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        self.env['account.invoice.tax'].compute(invoice)
        invoice.signal_workflow('invoice_open')

        self.assertEqual(
            invoice.rc_self_invoice_id.fiscal_document_type_id.code, "TD17")
        with self.assertRaises(UserError):
            # Impossible to set IdFiscaleIVA
            self.run_wizard(invoice.rc_self_invoice_id.id)
        self.supplier_intraEU.vat = "BE0477472701"
        with self.assertRaises(UserError):
            # Street is not set
            self.run_wizard(invoice.rc_self_invoice_id.id)
        self.supplier_intraEU.street = "Street"
        self.supplier_intraEU.zip = "12345"
        self.supplier_intraEU.city = "city"
        self.supplier_intraEU.country_id = self.env.ref("base.be")
        res = self.run_wizard(invoice.rc_self_invoice_id.id)
        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT10538570960_00002.xml')
        xml_content = attachment.datas.decode('base64')
        self.check_content(
            xml_content, 'IT10538570960_00002.xml', "l10n_it_fatturapa_out_rc")
