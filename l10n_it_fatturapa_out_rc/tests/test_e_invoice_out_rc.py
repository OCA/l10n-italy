import base64
from odoo.addons.l10n_it_reverse_charge.tests.rc_common import ReverseChargeCommon
from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import FatturaPACommon
from odoo.exceptions import UserError
from odoo.tests import Form


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
        self.rc_type_eeu.partner_id = self.company.partner_id.id
        self.rc_type_eeu.fiscal_document_type_id = self.env.ref(
            "l10n_it_fiscal_document_type.15").id
        self.tax_22vi.kind_id = self.env.ref("l10n_it_account_tax_kind.n6").id
        self.supplier_intraEU.customer = True
        self.customer_invoice_account = self.env['account.account'].search(
            [('user_type_id', '=', self.env.ref(
                'account.data_account_type_receivable').id)], limit=1).id
        self.supplier_invoice_account = self.env['account.account'].search(
            [('user_type_id', '=', self.env.ref(
                'account.data_account_type_payable').id)], limit=1).id
        self.sale_invoice_line_account = self.env['account.account'].search(
            [('user_type_id', '=', self.env.ref(
                'account.data_account_type_revenue').id)], limit=1).id
        self.purchase_invoice_line_account = self.env['account.account'].search(
            [('user_type_id', '=', self.env.ref(
                'account.data_account_type_direct_costs').id)], limit=1).id

    def set_sequence_journal_selfinvoice(self, invoice_number, dt):
        inv_seq = self.journal_selfinvoice.sequence_id
        seq_date = self.env['ir.sequence.date_range'].search([
            ('sequence_id', '=', inv_seq.id),
            ('date_from', '<=', dt),
            ('date_to', '>=', dt),
        ], limit=1)
        if not seq_date:
            seq_date = inv_seq._create_date_range_seq(dt)
        seq_date.number_next_actual = invoice_number

    def set_bill_sequence(self, invoice_number, dt):
        seq_pool = self.env['ir.sequence']
        inv_seq = seq_pool.search([('name', '=', 'BILL Sequence')])[0]
        seq_date = self.env['ir.sequence.date_range'].search([
            ('sequence_id', '=', inv_seq.id),
            ('date_from', '<=', dt),
            ('date_to', '>=', dt),
        ], limit=1)
        if not seq_date:
            seq_date = inv_seq._create_date_range_seq(dt)
        seq_date.number_next_actual = invoice_number

    def test_intra_EU(self):
        self.set_sequence_journal_selfinvoice(15, '2020-12-01')
        self.set_bill_sequence(25, '2020-12-01')
        self.supplier_intraEU.property_payment_term_id = self.term_15_30.id
        invoice = self.invoice_model.create({
            'partner_id': self.supplier_intraEU.id,
            'account_id': self.invoice_account,
            'type': 'in_invoice',
            'date_invoice': '2020-12-01',
            'reference': 'EU-SUPPLIER-REF'
        })

        invoice_line_vals = {
            'name': 'Invoice for sample product',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100,
            'invoice_line_tax_ids': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice.compute_taxes()
        invoice.action_invoice_open()
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
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content, 'IT10538570960_00002.xml', "l10n_it_fatturapa_out_rc")

    def test_intra_EU_customer(self):
        self.set_sequence_journal_selfinvoice(15, '2020-12-01')
        self.set_bill_sequence(25, '2020-12-01')
        self.supplier_intraEU.property_payment_term_id = self.term_15_30.id
        invoice = self.invoice_model.create({
            'partner_id': self.supplier_intraEU.id,
            'account_id': self.customer_invoice_account,
            'type': 'out_invoice',
            'date_invoice': '2020-12-01',
            'reference': 'EU-CUSTOMER-REF'
        })

        invoice_line_vals = {
            'name': 'Invoice for sample product',
            'account_id': self.sale_invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100,
            'invoice_line_tax_ids': [(4, self.tax_22vi.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice.compute_taxes()
        invoice.action_invoice_open()
        self.assertFalse(invoice.rc_self_invoice_id)

    def test_intra_EU_draft(self):
        self.set_sequence_journal_selfinvoice(15, '2020-12-01')
        self.set_bill_sequence(25, '2020-12-01')
        self.supplier_intraEU.property_payment_term_id = self.term_15_30.id
        invoice = self.invoice_model.create({
            'partner_id': self.supplier_intraEU.id,
            'account_id': self.invoice_account,
            'type': 'in_invoice',
            'date_invoice': '2020-12-01',
            'reference': 'EU-SUPPLIER-REF'
        })

        invoice_line_vals = {
            'name': 'Invoice for sample product',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100,
            'invoice_line_tax_ids': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice.compute_taxes()
        invoice.action_invoice_open()
        self.assertEqual(invoice.rc_self_invoice_id.state, 'paid')
        invoice.journal_id.update_posted = True
        invoice.action_invoice_cancel()
        self.assertEqual(invoice.rc_self_invoice_id.state, 'cancel')
        with self.assertRaises(UserError):
            invoice.rc_self_invoice_id.action_invoice_draft()

    def test_intra_EU_supplier_refund(self):
        self.set_sequence_journal_selfinvoice(16, '2020-12-01')
        self.set_bill_sequence(26, '2020-12-01')
        self.supplier_intraEU.property_payment_term_id = self.term_15_30.id
        invoice = self.invoice_model.create({
            'partner_id': self.supplier_intraEU.id,
            'account_id': self.supplier_invoice_account,
            'type': 'in_refund',
            'date_invoice': '2020-12-01',
            'reference': 'EU-SUPPLIER-REF',
        })
        self.assertEqual(
            invoice.fiscal_document_type_id.code, "TD04")
        invoice_line_vals = {
            'name': 'Invoice for sample product',
            'account_id': self.purchase_invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100,
            'invoice_line_tax_ids': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice.compute_taxes()
        invoice.action_invoice_open()
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
        self.set_e_invoice_file_id(attachment, 'IT10538570960_00003.xml')
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content, 'IT10538570960_00003.xml', "l10n_it_fatturapa_out_rc")

    def test_extra_EU(self):
        self.set_bill_sequence(27, '2020-12-01')
        self.supplier_extraEU.property_payment_term_id = self.term_15_30.id
        self.rc_type_eeu.with_supplier_self_invoice = False
        invoice = self.invoice_model.create({
            'partner_id': self.supplier_extraEU.id,
            'account_id': self.invoice_account,
            'type': 'in_invoice',
            'date_invoice': '2020-12-01',
            'reference': 'EXEU-SUPPLIER-REF'
        })

        invoice_line_vals = {
            'name': 'Invoice for sample product',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100,
            'invoice_line_tax_ids': [(4, self.tax_22ae.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice.compute_taxes()
        invoice.action_invoice_open()
        self.assertEqual(
            invoice.rc_self_invoice_id.fiscal_document_type_id.code, "TD17")
        with self.assertRaises(UserError):
            # Impossible to set IdFiscaleIVA
            self.run_wizard(invoice.rc_self_invoice_id.id)
        self.supplier_extraEU.vat = "US484762844"
        with self.assertRaises(UserError):
            # Street is not set
            self.run_wizard(invoice.rc_self_invoice_id.id)
        self.supplier_extraEU.street = "Street"
        self.supplier_extraEU.zip = "12345"
        self.supplier_extraEU.city = "city"
        self.supplier_extraEU.country_id = self.env.ref("base.us")
        res = self.run_wizard(invoice.rc_self_invoice_id.id)
        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT10538570960_00004.xml')
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content, 'IT10538570960_00004.xml', "l10n_it_fatturapa_out_rc")

    def _configure_be_supplier(self, supplier):
        supplier_form = Form(supplier)
        supplier_form.property_payment_term_id = self.term_15_30
        supplier_form.vat = "BE0477472701"
        supplier_form.street = "Street"
        supplier_form.zip = "12345"
        supplier_form.city = "city"
        supplier_form.country_id = self.env.ref("base.be")
        supplier = supplier_form.save()
        return supplier

    def _create_rc_bill(self, supplier, tax):
        bill_model = self.invoice_model.with_context(type='in_invoice')
        bill_form = Form(bill_model)
        bill_form.partner_id = supplier
        bill_form.date_invoice = '2020-12-01'
        with bill_form.invoice_line_ids.new() as line:
            line.name = 'Bill for sample product'
            line.product_id = self.sample_product
            line.invoice_line_tax_ids.clear()
            line.invoice_line_tax_ids.add(tax)
        bill = bill_form.save()
        bill.action_invoice_open()
        return bill

    def test_intra_EU_multiple_suppliers(self):
        """
        Export multiple self-invoices coming from different suppliers.
        """
        # Arrange: Create 2 self invoices from 2 supplier bills
        # having different suppliers
        be_supplier = self._configure_be_supplier(self.supplier_intraEU)
        be_bill = self._create_rc_bill(be_supplier, self.tax_22ai)
        be_self_invoice = be_bill.rc_self_invoice_id
        self.assertTrue(be_self_invoice)

        bg_supplier = be_supplier.copy(default={
            'vat': 'BG1234567892',
            'country_id': self.env.ref("base.bg").id,
        })
        bg_bill = be_bill.copy(default={
            'partner_id': bg_supplier.id,
        })
        bg_bill.action_invoice_open()
        bg_self_invoice = bg_bill.rc_self_invoice_id
        self.assertTrue(bg_self_invoice)
        # pre-condition: The self-invoices are linked to different suppliers
        self_invoices = be_self_invoice | bg_self_invoice
        original_suppliers = self_invoices._get_original_suppliers()
        self.assertEqual(len(original_suppliers), 2)
        self.assertItemsEqual(original_suppliers, be_supplier | bg_supplier)

        # Act: Export the self-invoices
        result_action = self.run_wizard(self_invoices.ids)

        # Assert: 2 different attachments have been created
        result_model = result_action.get('res_model')
        result_domain = result_action.get('domain')
        result_records = self.env[result_model].search(result_domain)
        self.assertEqual(len(result_records), 2)

    def test_extra_EU_multiple_suppliers_additional_invoice(self):
        """
        Export multiple self-invoices coming from different suppliers.
        The Reverse Charge Type applied
        has "With additional supplier self invoice" enabled.
        """
        # Arrange: Create 2 self invoices from 2 supplier bills
        # having different suppliers.
        # Both supplier bills have "With additional supplier self invoice" enabled
        be_supplier = self._configure_be_supplier(self.supplier_extraEU)
        be_bill = self._create_rc_bill(be_supplier, self.tax_0_pur)
        fiscal_position = be_bill.fiscal_position_id
        reverse_charge_type = fiscal_position.rc_type_id
        self.assertTrue(reverse_charge_type.with_supplier_self_invoice)
        be_self_invoice = be_bill.rc_self_purchase_invoice_id.rc_self_invoice_id
        self.assertTrue(be_self_invoice)

        bg_supplier = be_supplier.copy(default={
            'vat': 'BG1234567892',
            'country_id': self.env.ref("base.bg").id,
        })
        bg_bill = be_bill.copy(default={
            'partner_id': bg_supplier.id,
        })
        bg_bill.action_invoice_open()
        fiscal_position = bg_bill.fiscal_position_id
        reverse_charge_type = fiscal_position.rc_type_id
        self.assertTrue(reverse_charge_type.with_supplier_self_invoice)
        bg_self_invoice = bg_bill.rc_self_purchase_invoice_id.rc_self_invoice_id
        self.assertTrue(bg_self_invoice)
        # pre-condition: The self-invoices are linked to different suppliers
        self_invoices = be_self_invoice | bg_self_invoice
        original_suppliers = self_invoices._get_original_suppliers()
        self.assertEqual(len(original_suppliers), 2)
        self.assertItemsEqual(original_suppliers, be_supplier | bg_supplier)

        # Act: Export the self-invoices
        result_action = self.run_wizard(self_invoices.ids)

        # Assert: 2 different attachments have been created
        result_model = result_action.get('res_model')
        result_domain = result_action.get('domain')
        result_records = self.env[result_model].search(result_domain)
        self.assertEqual(len(result_records), 2)
