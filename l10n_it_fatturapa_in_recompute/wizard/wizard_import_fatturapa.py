# Copyright 2022 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class WizardImportFatturapa(models.TransientModel):
    _inherit = "wizard.import.fatturapa"

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
