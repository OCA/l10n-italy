from odoo import models, api, fields


class StockClosePrint(models.TransientModel):
    _name = "stock.close.print.wizard"
    _description = "Stock Close Print Wizard"

    close_name = fields.Many2one(comodel_name="stock.close.period", string="Close Period")

    @api.multi
    def generate_report(self):
        rows = self.env["stock.close.period.line"].search([("close_id", "=", self.close_name.id)], order="product_code")
        datas = {
            "ids": rows.ids,
            "model": "stock.close.period.line",
            "form": {
                "close_name": self.close_name.name,
            }
        }

        return self.env.ref(
            "l10n_it_stock_close_period.report_xlsx_stock_close_print").report_action(self, data=datas, config=False)
