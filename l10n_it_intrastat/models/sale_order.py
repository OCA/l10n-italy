from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        fiscal_position_id = invoice_vals["fiscal_position_id"]
        if fiscal_position_id:
            intrastat = (
                self.env["account.fiscal.position"].browse(fiscal_position_id).intrastat
            )
            invoice_vals.update({"intrastat": intrastat})
        return invoice_vals
