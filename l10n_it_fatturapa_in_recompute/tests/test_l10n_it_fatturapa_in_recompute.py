from odoo.addons.l10n_it_fatturapa_in.tests.fatturapa_common import (
    FatturapaCommon)
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_round


class TestInvoiceRecompute(FatturapaCommon):

    def setUp(self):
        super().setUp()
        self.invoice_model = self.env['account.invoice']
        self.invoice_line_model = self.env['account.invoice.line']
        self.partner_model = self.env['res.partner']

    def test_00_xml_import_without_custom_precision(self):
        res = self.run_wizard(
            'test0', 'IT01234567890_FPR20.xml',
            module_name='l10n_it_fatturapa_in_recompute')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertFalse(invoice.compute_on_einvoice_values)
        self.assertEqual(
            invoice.invoice_line_ids[0].name, 'Imposta erariale di consumo')
        self.assertEqual(invoice.invoice_line_ids[1].name, 'Oneri di dispacciamento')
        self.assertEqual(
            invoice.invoice_line_ids[0].invoice_line_tax_ids.name,
            '22% e-bill')
        self.assertNotEqual(invoice.amount_total, 880.46)
        self.assertNotEqual(invoice.amount_tax, 158.77)
        self.assertEqual(invoice.e_invoice_amount_tax, 158.77)

        with self.assertRaises(ValidationError):
            invoice.action_invoice_open()

    def test_01_xml_import_with_custom_precision(self):
        price_precision = self.env['decimal.precision'].search([
            ('name', '=', 'Product Price')
        ])
        res = self.run_wizard(
            'test2', 'IT01234567890_FPR21.xml',
            module_name='l10n_it_fatturapa_in_recompute',
            wiz_values={
                'price_decimal_digits': 7,
            })
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(invoice.compute_on_einvoice_values)
        self.assertEqual(
            invoice.invoice_line_ids[0].name, 'Imposta erariale di consumo')
        self.assertEqual(invoice.invoice_line_ids[1].name,
                         'Oneri di dispacciamento')
        self.assertEqual(
            invoice.invoice_line_ids[0].invoice_line_tax_ids.name,
            '22% e-bill')
        self.assertEqual(invoice.amount_total, 880.46)
        self.assertEqual(invoice.amount_tax, 158.77)
        self.assertEqual(invoice.e_invoice_amount_tax, 158.77)
        # TODO decimal precision in price_unit remains the custom one, leading to
        #  unusefulness of this module, while actually it is the default: how to
        #  simulate?
        invoice.action_invoice_cancel()
        invoice.action_invoice_draft()
        invoice.write({'compute_on_einvoice_values': False})
        for line in invoice.invoice_line_ids:
            line.price_unit = float_round(line.price_unit, price_precision.digits,
                                          rounding_method='DOWN')
            line._compute_price()
        invoice.compute_taxes()

        self.assertEqual(
            invoice.e_invoice_validation_message,
            "Untaxed amount (605.05) does not match with e-bill untaxed amount (721.69)"
            ",\nTaxed amount (133.11) does not match with e-bill taxed amount (158.77),"
            "\nTotal amount (738.16) does not match with e-bill total amount (880.46)."
        )

        invoice.action_cancel()
        invoice.action_invoice_draft()
        invoice.write({'compute_on_einvoice_values': True})
        invoice.compute_taxes()
        self.assertFalse(invoice.e_invoice_validation_message)

        invoice.action_invoice_open()

        partner = invoice.partner_id
        partner.e_invoice_detail_level = '0'
        res = self.run_wizard(
            'test3', 'IT01234567890_FPR21.xml',
            module_name='l10n_it_fatturapa_in_recompute')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(len(invoice.invoice_line_ids) == 0)
