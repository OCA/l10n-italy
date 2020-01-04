# Copyright 2019 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class Ddt(models.Model):

    _inherit = 'stock.picking.package.preparation'

    @api.multi
    def action_invoice_create(self):
        invoice_ids = super(Ddt, self).action_invoice_create()
        invoice_model = self.env['account.invoice']
        for invoice in invoice_model.browse(invoice_ids):
            invoice.tax_stamp = invoice.is_tax_stamp_applicable()
        return invoice_ids
