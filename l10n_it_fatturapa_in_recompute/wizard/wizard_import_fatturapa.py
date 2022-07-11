# Copyright 2022 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class WizardImportFatturapa(models.TransientModel):
    _inherit = "wizard.import.fatturapa"

    def set_e_invoice_lines(self, FatturaBody, invoice_data):
        e_invoice_lines = self.env['einvoice.line'].browse()
        if self.e_invoice_detail_level != '2':  # FIXME or mode == 'link':
            for line in FatturaBody.DatiBeniServizi.DettaglioLinee:
                e_invoice_lines |= self.create_e_invoice_line(line)
        if e_invoice_lines:
            invoice_data['e_invoice_line_ids'] = [(6, 0, e_invoice_lines.ids)]

    def set_invoice_line_ids(
            self, FatturaBody, credit_account_id, partner, wt_founds,
            invoice_data):

        if self.e_invoice_detail_level == '0':
            return
        super().set_invoice_line_ids(
            FatturaBody, credit_account_id, partner, wt_founds, invoice_data
        )
        invoice_lines = []
        invoice_line_model = self.env['account.invoice.line']
        if self.e_invoice_detail_level == '2':
            # Clean invoice line created and recreate with link
            e_invoice_lines = self.env['einvoice.line'].browse()
            for line in FatturaBody.DatiBeniServizi.DettaglioLinee:
                invoice_line_data = self._prepareInvoiceLine(
                    credit_account_id, line, wt_founds)
                product = self.get_line_product(line, partner)
                e_invoice_line = self.create_e_invoice_line(line)
                e_invoice_lines |= e_invoice_line
                invoice_line_data.update({'e_invoice_line_id': e_invoice_line.id})
                self._set_invoice_lines(product, invoice_line_data, invoice_lines,
                                        invoice_line_model)
            if e_invoice_lines:
                invoice_data['e_invoice_line_ids'] = [(6, 0, e_invoice_lines.ids)]
        invoice_data['invoice_line_ids'] = [(6, 0, invoice_lines)]

    @api.multi
    def importFatturaPA(self):
        res = super().importFatturaPA()
        if (
            self.price_decimal_digits != self.env['decimal.precision'].search([
                ('name', '=', 'Product Price')
            ], limit=1).digits or
            self.quantity_decimal_digits != self.env['decimal.precision'].search([
                ('name', '=', 'Product Unit of Measure')
            ], limit=1).digits or
            self.discount_decimal_digits != self.env['decimal.precision'].search([
                ('name', '=', 'Discount')
                ], limit=1).digits):
            new_invoices = self.env['account.invoice'].search(res.get('domain'))
            new_invoices.write({
                'compute_on_einvoice_values': True,
            })
        return res
