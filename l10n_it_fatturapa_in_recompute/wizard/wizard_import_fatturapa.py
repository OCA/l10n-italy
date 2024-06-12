# Copyright 2022 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class WizardImportFatturapa(models.TransientModel):
    _inherit = "wizard.import.fatturapa"

    def _get_compute_on_einvoice_values(self):
        return bool(self.env.user.company_id.compute_on_einvoice_values)

    def _get_e_invoice_detail_level(self):
        if self.env.user.company_id.compute_on_einvoice_values:
            return '2'

    @api.onchange('compute_on_einvoice_values')
    def onchange_compute_on_einvoice_values(self):
        if self.compute_on_einvoice_values:
            self.e_invoice_detail_level = '2'

    compute_on_einvoice_values = fields.Boolean(
        default=_get_compute_on_einvoice_values,
        string="Compute on einvoice values precision")

    e_invoice_detail_level = fields.Selection(
        default=_get_e_invoice_detail_level)

    def set_e_invoice_lines(self, FatturaBody, invoice_data):
        # total override without super() to exclude creation of einvoice_lines
        # when created from set_invoice_line_ids, that create them always for
        # e_invoice_detail_level == 2
        e_invoice_lines = self.env['einvoice.line'].browse()
        if self.e_invoice_detail_level != '2' \
                or self.env.context.get('linked_invoice', False):
            for line in FatturaBody.DatiBeniServizi.DettaglioLinee:
                e_invoice_lines |= self.create_e_invoice_line(line)
        if e_invoice_lines:
            invoice_data['e_invoice_line_ids'] = [(6, 0, e_invoice_lines.ids)]

    def set_invoice_line_ids(
            self, FatturaBody, credit_account_id, partner, wt_founds,
            invoice_data):
        # recreate invoice lines to add a secure link to einvoice_line
        res = super().set_invoice_line_ids(
            FatturaBody, credit_account_id, partner, wt_founds, invoice_data
        )
        invoice_lines = []
        invoice_line_model = self.env['account.invoice.line']
        if self.e_invoice_detail_level == '2':
            # Clean invoice lines already created
            invoice_line_model.browse(
                invoice_data.get('invoice_line_ids')[0][2]
            ).unlink()
            # Recreate invoice lines with link to e_invoice_line
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
        return res

    @api.multi
    def importFatturaPA(self):
        res = super().importFatturaPA()
        if self.compute_on_einvoice_values:
            new_invoices = self.env['account.invoice'].search(res.get('domain'))
            new_invoices.write({
                'compute_on_einvoice_values': True,
            })
            for line in new_invoices.mapped('invoice_line_ids'):
                line.with_context(compute_on_einvoice_values=True)._compute_price()
            new_invoices.compute_taxes()
        return res
