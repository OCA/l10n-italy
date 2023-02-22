#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import (FatturaPACommon)
from odoo.tests import Form


class TestXMLGeneration (FatturaPACommon):

    def test_fixed_discount(self):
        """Generate an e-invoice for an invoice having a fixed discount.
        Check that the ScontoMaggiorazione is present in the generated e-invoice.
        """
        # Setup for fixing date and sequence of new invoices
        date_invoice = '2020-01-01'
        self.set_sequences(1, date_invoice)

        # Arrange: Create an invoice with one line costing 100
        # and fixed discount of 20
        invoice_form = Form(self.env['account.invoice'])
        invoice_form.partner_id = self.res_partner_fatturapa_2
        invoice_form.date_invoice = date_invoice
        with invoice_form.invoice_line_ids.new() as line:
            line.name = "Test fixed discount"
            line.price_unit = 1000
            line.discount_fixed = 20
            line.invoice_line_tax_ids.clear()
            line.invoice_line_tax_ids.add(self.tax_22)
        invoice = invoice_form.save()
        invoice.action_invoice_open()
        # pre-condition: Check invoice totals
        self.assertEqual(invoice.amount_untaxed, 980)
        self.assertEqual(invoice.amount_tax, 215.6)
        self.assertEqual(invoice.amount_total, 1195.6)

        # Act: Generate the e-invoice
        action = self.run_wizard(invoice.id)
        e_invoice = self.env[action['res_model']].browse(action['res_id'])

        # Assert: The E-invoice matches the XML in tests data
        file_name = 'IT06363391001_00001.xml'
        self.set_e_invoice_file_id(e_invoice, file_name)
        xml_content = base64.decodebytes(e_invoice.datas)
        self.check_content(
            xml_content,
            file_name,
            module_name='l10n_it_fatturapa_out_fd',
        )
