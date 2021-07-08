# Copyright 2021 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        fiscal_position_id = invoice_vals['fiscal_position_id']
        if fiscal_position_id:
            intrastat = self.env['account.fiscal.position'].browse(
                fiscal_position_id).intrastat
            invoice_vals.update({'intrastat': intrastat})
        return invoice_vals
