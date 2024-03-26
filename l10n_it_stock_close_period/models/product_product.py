# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, _
import copy


class Product(models.Model):
    _inherit = "product.product"

    @api.multi
    def _get_last_average_price(self):
        last_price = 0
        origin = ""

        # from the last closing
        last_close = self.env["stock.close.period.line"].search([
            ("product_id", "=", self.id),
            ("state", "=", "done")
        ], limit=1, order="close_date")
        if last_close:
            last_price = last_close.price_unit
            origin = (_("Closing") + " [" + str(last_close.id) + "] " + last_close.close_id.name)

        # last history standard price
        if last_price == 0:
            history = self.env["product.price.history"].search([
                ("product_id", "=", self.id)
            ], order="datetime desc", limit=1)
            if history:
                last_price = history.cost
                origin = _("Last history standard price")

        return last_price, origin

    def _compute_qty_available(self, to_date):
        res = self._compute_quantities_available(to_date)
        return res

    def _compute_quantities_available(self, to_date=False):
        date = to_date

        # get quants
        quan = {}
        query2 = """
            SELECT 
                stock_quant.quantity, 
                stock_quant.product_id, 
                stock_quant.location_id, 
                stock_quant.lot_id, 
                stock_quant.package_id, 
                stock_quant.owner_id, 
                stock_quant.id
            FROM
                stock_quant,
                stock_location
            WHERE 
                stock_quant.location_id = stock_location.id and
                stock_quant.product_id = %r and 
                stock_location.company_id = %r
            ORDER BY 
                stock_quant.product_id, 
                stock_quant.location_id, 
                stock_quant.lot_id, 
                stock_quant.package_id, 
                stock_quant.owner_id;
        """ % (self.id, self.env.user.company_id.id)

        self.env.cr.execute(query2)
        for row2 in self._cr.fetchall():
            quant_qty = row2[0] * 1.0
            product_id = row2[1]
            location_id = row2[2]
            lot_id = row2[3] if self.tracking != "serial" else False
            package_id = row2[4]
            owner_id = row2[5]
            key = "%d_%d_%d_%d_%d" % (product_id, location_id, lot_id or False, package_id or False, owner_id or False)
            if key in quan:
                quan[key] = quan[key] + quant_qty
            else:
                quan[key] = quant_qty * 1.0

        # rename quan -> move
        move = quan

        # duplicate quan dict
        stock_now = copy.deepcopy(quan)

        # recompute moves if set request date
        # moves +
        query = """
            SELECT 
                sum(stock_move_line.qty_done), 
                stock_move_line.product_id, 
                stock_move_line.location_id, 
                stock_move_line.lot_id, 
                stock_move_line.package_id, 
                stock_move_line.owner_id, 
                stock_move_line.date
            FROM
                stock_move_line
            WHERE
                stock_move_line.date >= '%s' and 
                stock_move_line.state='done' and 
                stock_move_line.product_id = %r and 
                stock_move_line.company_id = %r
            GROUP BY 
                stock_move_line.product_id, 
                stock_move_line.location_id, 
                stock_move_line.lot_id, 
                stock_move_line.package_id, 
                stock_move_line.owner_id, 
                stock_move_line.date
            ORDER BY 
                stock_move_line.product_id, 
                stock_move_line.location_id, 
                stock_move_line.lot_id, 
                stock_move_line.package_id, 
                stock_move_line.owner_id, 
                stock_move_line.date desc;
        """ % (date, self.id, self.env.user.company_id.id)

        self.env.cr.execute(query)
        for row in self._cr.fetchall():
            move_qty = row[0]
            product_id = row[1]
            location_id = row[2]
            lot_id = row[3] if self.tracking != "serial" else False
            package_id = row[4]
            owner_id = row[5]
            key = "%d_%d_%d_%d_%d" % (product_id, location_id, lot_id or False, package_id or False, owner_id or False)
            if key in move:
                move[key] += move_qty
            else:
                move[key] = move_qty
                stock_now[key] = 0

        # moves -
        query = """                
            SELECT 
                sum(stock_move_line.qty_done), 
                stock_move_line.product_id, 
                stock_move_line.location_dest_id, 
                stock_move_line.lot_id, 
                stock_move_line.package_id, 
                stock_move_line.owner_id, 
                stock_move_line.date
            FROM
                stock_move_line
            WHERE 
                stock_move_line.date >= '%s' and 
                stock_move_line.state='done' and 
                stock_move_line.product_id = %r and 
                stock_move_line.company_id = %r
            GROUP BY
                stock_move_line.product_id, 
                stock_move_line.location_dest_id, 
                stock_move_line.lot_id, 
                stock_move_line.package_id, 
                stock_move_line.owner_id, 
                stock_move_line.date
            ORDER BY 
                stock_move_line.product_id, 
                stock_move_line.location_dest_id, 
                stock_move_line.lot_id, 
                stock_move_line.package_id, 
                stock_move_line.owner_id, 
                stock_move_line.date desc;
        """ % (date, self.id, self.env.user.company_id.id)

        self.env.cr.execute(query)
        for row in self._cr.fetchall():
            move_qty = row[0]
            product_id = row[1]
            location_dest_id = row[2]
            lot_id = row[3] if self.tracking != "serial" else False
            package_id = row[4]
            owner_id = row[5]
            key = "%d_%d_%d_%d_%d" % (
                product_id, location_dest_id, lot_id or False, package_id or False, owner_id or False)
            if key in move:
                move[key] -= move_qty
            else:
                move[key] = -move_qty
                stock_now[key] = 0

        # compute
        list_internal_quant = []
        for key, qty in move.items():
            key_split = key.split("_")
            product_id = int(key_split[0])
            uom_id = self.env["product.product"].browse(product_id).uom_id.id
            location_id = int(key_split[1])
            lot_id = int(key_split[2])
            if lot_id == 0:
                lot_id = None
            package_id = int(key_split[3])
            if package_id == 0:
                package_id = None
            owner_id = int(key_split[4])
            if owner_id == 0:
                owner_id = None
            mov = move[key] or 0.0
            qua = stock_now[key] or 0.0
            dif = qua - mov

            # only internal locations
            location_obj = self.env["stock.location"].search([("id", "=", location_id)], limit=1)
            if location_obj.usage == "internal":
                list_internal_quant.append(({
                    "date": date,
                    "product_id": product_id,
                    "uom_id": uom_id,
                    "location_id": location_id,
                    "lot_id": lot_id,
                    "package_id": package_id,
                    "owner_id": owner_id,
                    "stock_at_date": mov,
                    "stock_now": qua,
                    "diff_qty": dif,
                }))
        return list_internal_quant
