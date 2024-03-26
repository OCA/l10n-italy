# Copyright 2020 Openindustry.it SAS
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import *
import logging
import unicodecsv
import base64

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class StockCloseImportWizard(models.TransientModel):
    _name = "stock.close.import.wizard"
    _description = "Stock Close Import Wizard"

    file = fields.Binary("File")
    close_id = fields.Many2one("stock.close.period", string="Stock Close Period")
    log = []

    @api.multi
    def import_csv(self):
        # set done close_id
        wcp = self.env["stock.close.period"]
        closing_id = wcp.search([("id", "=", self.close_id.id)])
        closing_id.work_start = datetime.now()

        try:
            file_to_import = base64.decodebytes(self.file).splitlines()
            reader = unicodecsv.reader(file_to_import, encoding="utf-8", delimiter=";")
            lines = []
            headers = False

            for index, row in enumerate(reader):
                headers = row
                break

            parsed_data_lines = unicodecsv.DictReader(
                file_to_import,
                fieldnames=headers,
                encoding="utf-8",
                delimiter=";"
            )

            for index, row in enumerate(parsed_data_lines):
                if index == 0:
                    continue
                lines.append({
                    "CODE": str(row["CODE"]),
                    "COST": str(row["COST"]).replace(",", "."),
                    "QTY": str(row["QTY"]).replace(",", "."),
                })
            self.log = []
            products = self.load_products(lines)
            if self.log:
                raise Exception(*self.log)
            wcpl = self.env["stock.close.period.line"]
            self.log = []
            total = 0.0
            dp_qty = 4
            dp_price = 5
            for index, row in enumerate(lines):
                product_id = products[row["CODE"]].id
                unit_cost = round(float(row["COST"]), dp_price)
                qty = round(float(row["QTY"]), dp_qty)
                total += unit_cost * qty
                wcpl.with_context(tracking_disable=True).create({
                    "close_id": self.close_id.id,
                    "product_id": product_id,
                    "price_unit": unit_cost,
                    "product_qty": qty,
                    "product_uom_id": products[row["CODE"]].product_tmpl_id.uom_id.id,
                    "evaluation_method": "",
                })

            # set done close_id
            closing_id.amount = total
            closing_id.work_end = datetime.now()
            closing_id.state = "done"

        except Exception as e:
            raise UserError(e)

    def load_products(self, lines):
        product = self.env["product.product"]
        products = {}
        for index, row in enumerate(lines):
            default_code = row["CODE"]
            product_obj = product.search([("default_code", "=", default_code)], limit=1)
            if not product_obj:
                error_string = "Prodotto %s non trovato" % default_code
                if error_string not in self.log:
                    self.log.append(error_string)
                continue
            products[default_code] = product_obj[0]
        return products
