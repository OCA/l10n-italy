#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo.addons.account_invoice_line_complimentary.tests.common import (
    create_complimentary_account,
    create_invoice,
    set_complimentary_account,
)
from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import (
    FatturaPACommon,
)


class TestExportComplimentary (FatturaPACommon):

    def setUp(self):
        super().setUp()
        self.complimentary_account = create_complimentary_account(self.env)

    def test_export(self):
        """A Complimentary Invoice Line creates a DettaglioLinea
        having TipoCessionePrestazione = AB."""
        # Arrange
        # Electronic Invoice setup
        invoice_date = '2020-01-01'
        self.set_sequences(1, invoice_date)

        # Complimentary setup
        complimentary_account = self.complimentary_account
        set_complimentary_account(self.env, complimentary_account)

        # Invoice with Complimentary line and Electronic Invoice fields
        invoice_values = {
            'partner_id': self.res_partner_fatturapa_2,
            'date_invoice': invoice_date,
            'payment_term_id': self.account_payment_term,
        }
        invoice_lines_values = [
            {
                'name': "Test Invoice Line",
                'price_unit': 100,
            },
            {
                'name': "Test Complimentary Invoice Line",
                'price_unit': 10,
                'is_complimentary': True,
            },
        ]
        invoice = create_invoice(
            self.env,
            invoice_values,
            invoice_lines_values,
            self.env.ref('l10n_it_fatturapa.tax_22'),
        )
        invoice.action_invoice_open()
        # pre-condition: Check Invoice total amounts
        self.assertEqual(invoice.amount_total, 134.2)
        self.assertEqual(invoice.residual, 122)

        # Act: Export the Invoice
        res = self.run_wizard(invoice.id)

        # Assert: Check the exported Electronic Invoice
        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00001.xml')
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content, 'IT06363391001_00001.xml',
            module_name='l10n_it_fatturapa_out_complimentary',
        )
