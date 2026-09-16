# Copyright (C) 2023-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Marco Calcagni <mcalcagni@dinamicheaziendali.it>
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, time

from odoo import models
from odoo.tools import SQL


class Product(models.Model):
    _inherit = "product.product"

    def _get_cost(self):
        # overridable method to customize cost used for evaluation
        self.ensure_one()
        return self.standard_price

    def _compute_qty_available(self, to_date, company):
        res = self._compute_quantities_available(to_date, company)
        return res

    def _get_stock_key(self, product_id, location_id, lot_id, package_id, owner_id):
        """Key grouping the quantities, lots are not considered for serial numbers"""
        if self.tracking == "serial" or lot_id is None:
            lot_id = 0
        return f"{product_id}_{location_id}_{lot_id}_{package_id or 0}_{owner_id or 0}"

    def _get_moved_quantities(self, date_end, company, location_field):
        """Quantities of the move lines done after `date_end`.

        :param location_field: `location_id` or `location_dest_id`, the location
            the quantities are grouped by
        :return: rows of quantity, product, location, lot, package and owner
        """
        location = SQL.identifier("stock_move_line", location_field)
        self.env.cr.execute(
            SQL(
                """
                SELECT
                    SUM(stock_move_line.quantity),
                    stock_move_line.product_id,
                    %(location)s,
                    stock_move_line.lot_id,
                    stock_move_line.package_id,
                    stock_move_line.owner_id
                FROM
                    stock_move_line
                WHERE
                    stock_move_line.date > %(date_end)s
                    AND stock_move_line.state = 'done'
                    AND stock_move_line.product_id = %(product_id)s
                    AND stock_move_line.company_id = %(company_id)s
                GROUP BY
                    stock_move_line.product_id,
                    %(location)s,
                    stock_move_line.lot_id,
                    stock_move_line.package_id,
                    stock_move_line.owner_id
                ORDER BY
                    stock_move_line.product_id,
                    %(location)s,
                    stock_move_line.lot_id,
                    stock_move_line.package_id,
                    stock_move_line.owner_id;
                """,
                location=location,
                date_end=date_end,
                product_id=self.id,
                company_id=company.id,
            )
        )
        return self.env.cr.fetchall()

    def _compute_quantities_available(self, to_date, company):
        """Quantities of the product at the end of `to_date`, in internal locations.

        The quantities start from the current quants, then the move lines done
        after `to_date` are reverted: their quantity is added back to the source
        location and removed from the destination one.

        :return: a list of dict for each location, lot, package and owner, with
            the quantity at date, the current one and their difference
        """
        self.ensure_one()
        # moves done after the end of to_date are reverted from current quants
        date_end = datetime.combine(to_date, time.max)

        quants = {}
        self.env.cr.execute(
            SQL(
                """
                SELECT
                    stock_quant.quantity,
                    stock_quant.product_id,
                    stock_quant.location_id,
                    stock_quant.lot_id,
                    stock_quant.package_id,
                    stock_quant.owner_id
                FROM
                    stock_quant,
                    stock_location
                WHERE
                    stock_quant.location_id = stock_location.id
                    AND stock_quant.product_id = %s
                    AND stock_location.company_id = %s
                ORDER BY
                    stock_quant.product_id,
                    stock_quant.location_id,
                    stock_quant.lot_id,
                    stock_quant.package_id,
                    stock_quant.owner_id;
                """,
                self.id,
                company.id,
            )
        )
        for row in self.env.cr.fetchall():
            key = self._get_stock_key(*row[1:])
            quants[key] = quants.get(key, 0.0) + row[0]

        stock_at_date = dict(quants)
        # quantities moved after to_date left the source location, so they were
        # there at date, and entered the destination location later
        for location_field, sign in (("location_id", 1), ("location_dest_id", -1)):
            for row in self._get_moved_quantities(date_end, company, location_field):
                key = self._get_stock_key(*row[1:])
                stock_at_date[key] = stock_at_date.get(key, 0.0) + sign * row[0]
                quants.setdefault(key, 0.0)

        list_internal_quant = []
        for key, stock_at_date_qty in stock_at_date.items():
            product_id, location_id, lot_id, package_id, owner_id = (
                int(value) for value in key.split("_")
            )
            location = self.env["stock.location"].browse(location_id)
            if location.usage != "internal":
                continue
            stock_now_qty = quants[key]
            list_internal_quant.append(
                {
                    "date": to_date,
                    "product_id": product_id,
                    "uom_id": self.uom_id.id,
                    "location_id": location_id,
                    "lot_id": lot_id or None,
                    "package_id": package_id or None,
                    "owner_id": owner_id or None,
                    "stock_at_date_qty": stock_at_date_qty,
                    "stock_now_qty": stock_now_qty,
                    "diff_qty": stock_now_qty - stock_at_date_qty,
                }
            )
        return list_internal_quant
