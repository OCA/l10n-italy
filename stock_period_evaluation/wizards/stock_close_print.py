# Copyright (C) 2023-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Marco Calcagni <mcalcagni@dinamicheaziendali.it>
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockClosePrint(models.TransientModel):
    _name = "stock.close.print.wizard"
    _description = "Stock Close Print Wizard"

    close_period_id = fields.Many2one("stock.close.period", string="Close Period")

    def generate_report(self):
        rows = self.env["stock.close.period.line"].search(
            [
                ("close_id", "=", self.close_period_id.id),
            ],
            order="product_code",
        )
        datas = {
            "ids": rows.ids,
            "model": "stock.close.period.line",
            "form": {
                "close_name": self.close_period_id.name,
            },
        }

        return self.env.ref(
            "stock_period_evaluation.report_xlsx_stock_close_print"
        ).report_action(
            self,
            data=datas,
            config=False,
        )
