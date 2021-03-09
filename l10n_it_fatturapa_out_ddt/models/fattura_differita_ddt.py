from odoo import api, models


class StockPickingPackagePreparation(models.Model):
    _inherit = 'stock.picking.package.preparation'

    @api.multi
    def action_invoice_create(self):
        invoice_ids = super().action_invoice_create()

        doc_type_obj = self.env['fiscal.document.type'].search(
            [('code', '=', 'TD24')], limit=1)

        invs_obj = self.env['account.invoice'].browse(invoice_ids)

        if doc_type_obj:
            for inv in invs_obj:
                inv.fiscal_document_type_id = doc_type_obj

        return invoice_ids
