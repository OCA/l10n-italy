from odoo import api, models

FATTURA_DIFFERITA_CODES = [
    "TD24",
    "TD25",
]
FATTURA_DIFFERITA_DEFAULT_CODE = "TD24"


class StockPickingPackagePreparation(models.Model):
    _inherit = 'stock.picking.package.preparation'

    @api.multi
    def action_invoice_create(self):
        invoice_ids = super().action_invoice_create()

        doc_type_obj = self.env['fiscal.document.type'].search(
            [('code', '=', FATTURA_DIFFERITA_DEFAULT_CODE)], limit=1)

        invs_obj = self.env['account.invoice'].browse(invoice_ids)

        if doc_type_obj:
            for inv in invs_obj:
                if (
                    inv.fiscal_document_type_id.code not in FATTURA_DIFFERITA_CODES and
                    inv.company_id.auto_set_deferred_invoice_type
                ):
                    # Use the default one
                    inv.fiscal_document_type_id = doc_type_obj

        return invoice_ids
