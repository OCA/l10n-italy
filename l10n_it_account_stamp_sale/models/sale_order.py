# Copyright 2019 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def action_invoice_create(self, grouped=False, final=False):
        invoice_ids = super(SaleOrder, self).action_invoice_create(
            grouped=grouped, final=final
        )
        invoice_model = self.env["account.move"]
        for invoice in invoice_model.browse(invoice_ids):
            invoice.tax_stamp = invoice.is_tax_stamp_applicable()
        return invoice_ids
