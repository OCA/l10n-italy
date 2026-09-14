# Copyright (C) 2023-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Marco Calcagni <mcalcagni@dinamicheaziendali.it>
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# Copyright 2024 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime, time

from odoo import _, api, models
from odoo.tools import float_compare, float_is_zero

_logger = logging.getLogger(__name__)


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_last_closing(self, closing_id, product_id):
        # default value
        start_qty = 0
        start_price = 0

        if closing_id.last_closed_id:
            last_closed_id = closing_id.last_closed_id
            # search product
            closing_line_id = self.env["stock.close.period.line"].search(
                [("close_id", "=", last_closed_id.id), ("product_id", "=", product_id)],
                limit=1,
            )
            if closing_line_id:
                start_qty = closing_line_id.product_qty
                start_price = closing_line_id.price_unit

        return start_qty, start_price

    @api.model
    def _get_right_invoice_lines(self, purchase_line_id):
        return purchase_line_id.invoice_lines.filtered(
            lambda il: il.move_id.is_purchase_document()
        )

    @api.model
    def _get_invoiced_amount_qty(self, purchase_line_id):
        """Invoiced amount, in company currency, and quantity, in product UoM, of
        the posted bills of the purchase line, net of the posted refunds."""
        amount = qty = 0.0
        product_uom = purchase_line_id.product_id.uom_id
        invoice_lines = self._get_right_invoice_lines(purchase_line_id).filtered(
            lambda il: il.parent_state == "posted"
        )
        for invoice_line in invoice_lines:
            line_qty = invoice_line.product_uom_id._compute_quantity(
                invoice_line.quantity, product_uom
            )
            # refund lines have a negative balance but a positive quantity
            amount += invoice_line.balance
            qty += (
                -line_qty if invoice_line.move_id.move_type == "in_refund" else line_qty
            )
        return amount, qty

    @api.model
    def _get_purchased_qty(self, move_id):
        """Quantity, in product UoM, entering the internal locations with the move.

        It is negative for returns and zero for moves between internal locations.
        """
        qty = move_id.product_uom._compute_quantity(
            move_id.quantity, move_id.product_id.uom_id
        )
        if (
            move_id.location_id.usage != "internal"
            and move_id.location_dest_id.usage == "internal"
        ):
            return qty
        if (
            move_id.location_id.usage == "internal"
            and move_id.location_dest_id.usage != "internal"
        ):
            return -qty
        return 0.0

    @api.model
    def _get_closing_product_qty(self, closing_line_id):
        """Quantity of the product in all the lines of the closing"""
        return sum(
            self.env["stock.close.period.line"]
            .search(
                [
                    ("close_id", "=", closing_line_id.close_id.id),
                    ("product_id", "=", closing_line_id.product_id.id),
                ]
            )
            .mapped("product_qty")
        )

    def _get_additional_landed_cost_new(self, move_id, company_id):
        """Hook to add landed costs to the purchase average.

        It is called by `_get_cost_stock_move_purchase_average` for each move of
        the period, and the returned amount is added to `cumulative_landed_cost`.
        FIFO and LIFO methods do not use it.

        :param move_id: stock.move done in the period
        :param company_id: id of the company of the closing
        :return: landed cost of the move in company currency, 0 by default
        """
        return 0

    def _write_evaluation(self, closing_line_id, values):
        """Write the evaluation `values` on the closing line.

        If no price has been found, the product cost is used instead.
        """
        price_digits = self.env["decimal.precision"].precision_get("Product Price")
        if float_is_zero(values["price_unit"], precision_digits=price_digits):
            closing_line_id.write(
                {
                    "price_unit": closing_line_id.product_id._get_cost(),
                    "evaluation_method": "standard",
                }
            )
        else:
            closing_line_id.write(dict(values, evaluation_method="purchase"))

    @api.model
    def _get_cost_stock_move_purchase_average(self, last_close_date, closing_line_id):
        """Evaluate the closing line with the weighted average purchase cost.

        The average includes the quantity and price of the last closing and the
        quantities purchased in the period, net of the returns to vendor, with
        the price of their purchase line.
        """
        product_id = closing_line_id.product_id
        company_id = closing_line_id.close_id.company_id.id
        # moves of last close date are already evaluated in the last closing
        min_date = datetime.combine(last_close_date, time.max)
        max_date = datetime.combine(closing_line_id.close_id.close_date, time.max)

        # get all moves (exclude by default inventory moves)
        move_ids = self.env["stock.move"].search(
            [
                ("state", "=", "done"),
                ("product_qty", ">", 0),
                ("product_id", "=", product_id.id),
                ("date", ">", min_date),
                ("date", "<=", max_date),
                ("company_id", "=", company_id),
                ("location_id.usage", "!=", "inventory"),
                ("location_dest_id.usage", "!=", "inventory"),
            ],
            order="date",
        )

        # get start data from last close
        start_qty, start_price = self._get_last_closing(
            closing_line_id.close_id, product_id.id
        )
        if start_qty:
            inventory_amount = start_price * start_qty
            inventory_qty = start_qty
        else:
            inventory_amount = 0
            inventory_qty = 0

        cumulative_amount = 0
        cumulative_landed_cost = 0
        cumulative_qty = 0
        for move_id in move_ids.filtered(lambda m: m.purchase_line_id):
            # evaluate the quantity moved in the period, not the quantity of the
            # purchase line, that can be received with more moves or returned
            move_qty = self._get_purchased_qty(move_id)
            if move_qty:
                cumulative_amount += move_qty * move_id._get_purchase_price_unit()
                cumulative_qty += move_qty

            additional_landed_cost_new = self._get_additional_landed_cost_new(
                move_id, company_id
            )
            cumulative_landed_cost += additional_landed_cost_new

        total_qty = cumulative_qty + inventory_qty
        if float_is_zero(total_qty, precision_rounding=product_id.uom_id.rounding):
            price_unit = 0
        else:
            price_unit = (
                inventory_amount + cumulative_amount + cumulative_landed_cost
            ) / total_qty

        self._write_evaluation(
            closing_line_id,
            {
                "price_unit": price_unit,
                "inventory_amount": inventory_amount,
                "inventory_qty": inventory_qty,
                "cumulative_amount": cumulative_amount,
                "cumulative_landed_cost": cumulative_landed_cost,
                "cumulative_qty": cumulative_qty,
            },
        )

    def _get_cost_stock_move_standard(self, closing_line_id):
        closing_line_id.price_unit = closing_line_id.product_id._get_cost()
        closing_line_id.evaluation_method = "standard"

    def _check_consistency(self, closing_line_id):
        """Hook to skip the evaluation of inconsistent closing lines.

        It is called by `_recompute_cost_stock_move_purchase` before evaluating
        each closing line: the lines for which it returns False are not evaluated
        and keep their current values.

        :param closing_line_id: stock.close.period.line to be evaluated
        :return: True to evaluate the line, False to skip it
        """
        return True

    @api.model
    def _search_same_product_value(self, closing_line_id):
        other_closing_line_id = self.env["stock.close.period.line"].search(
            [
                ("close_id", "=", closing_line_id.close_id.id),
                ("product_id", "=", closing_line_id.product_id.id),
                ("price_unit", "!=", 0),
            ],
            limit=1,
        )
        closing_line_id.price_unit = other_closing_line_id.price_unit
        closing_line_id.inventory_amount = other_closing_line_id.inventory_amount
        closing_line_id.inventory_qty = other_closing_line_id.inventory_qty
        closing_line_id.cumulative_amount = other_closing_line_id.cumulative_amount
        closing_line_id.cumulative_landed_cost = (
            other_closing_line_id.cumulative_landed_cost
        )
        closing_line_id.cumulative_qty = other_closing_line_id.cumulative_qty
        closing_line_id.evaluation_method = other_closing_line_id.evaluation_method

    def _get_cost_stock_move_lifo_fifo(self, closing_line_id, evaluation_method=False):
        """Evaluate the closing line with the FIFO or LIFO method.

        The price is the average of the prices of the quantities that
        `price_calculation` assigns to the moves of the period, which are
        detailed in `evaluation_details`.
        """
        product_id = closing_line_id.product_id
        # get start data from last close
        start_qty, start_price = self._get_last_closing(
            closing_line_id.close_id, product_id.id
        )
        res = self.price_calculation(
            closing_line_id,
            evaluation_method or closing_line_id.close_id.force_evaluation_method,
            start_qty,
            start_price,
        )
        res_dict = [
            {
                "product_id": x[0],
                "evaluated_qty": x[1],
                "price_unit": x[2],
                "moved_qty": x[3],
                "origin": x[4],
                "date": x[5],
            }
            for x in res
            if len(x) == 6
        ]
        line_total = closing_line_id._format_value(
            sum([x["evaluated_qty"] * x["price_unit"] for x in res_dict]),
        )
        closing_line_id.evaluation_details = "\n".join(
            [
                f"{x['origin'] or ''} - {x['date']}: "
                f"{closing_line_id._format_value(x['evaluated_qty'])} x "
                f"{closing_line_id._format_value(x['price_unit'])} = "
                f"{closing_line_id._format_value(x['evaluated_qty'] * x['price_unit'])}"
                for x in res_dict
            ]
            + [_("Total: %s") % line_total]
        )
        cumulative_amount = 0
        cumulative_qty = 0
        qty_moved = 0

        for match in res:
            qty_to_be_evaluated = match[1]
            price = match[2]
            qty = match[3]
            qty_moved += qty
            cumulative_amount += qty_to_be_evaluated * price
            cumulative_qty += qty_to_be_evaluated
        if float_is_zero(cumulative_qty, precision_rounding=product_id.uom_id.rounding):
            price_unit = 0.0
        else:
            price_unit = cumulative_amount / cumulative_qty

        if start_qty:
            inventory_amount = start_price * start_qty
            inventory_qty = start_qty
        else:
            inventory_amount = 0
            inventory_qty = 0

        self._write_evaluation(
            closing_line_id,
            {
                "price_unit": price_unit,
                "inventory_amount": inventory_amount,
                "inventory_qty": inventory_qty,
                "cumulative_amount": cumulative_amount,
                "cumulative_landed_cost": 0,
                "cumulative_qty": cumulative_qty,
            },
        )

    @api.model
    def price_calculation(self, line, valuation_type, start_qty, start_price):
        """Assign the quantity of the closing line to the moves of the period.

        The move lines are searched between the last close date and the close
        date, for the FIFO method only the incoming ones, otherwise the incoming
        and outgoing ones. They are sorted from the newest day to the oldest one,
        and in the same day the incoming move lines come after the other ones,
        as if they were done before them.

        :return: the tuples of `_get_tuples`
        """
        line.ensure_one()
        # do not exclude inventory moves, as they are needed to compute qty at date
        move_line_domain = [
            ("state", "=", "done"),
            ("product_id", "=", line.product_id.id),
            ("quantity", ">", 0),
            ("date", "<=", line.close_id.close_date),
            ("date", ">", line.close_id.last_close_date),
            ("company_id", "=", line.close_id.company_id.id),
        ]
        if valuation_type in ["fifo", "purchase"]:
            # search for incoming moves
            move_line_domain += [
                ("location_id.usage", "!=", "internal"),
                ("location_dest_id.usage", "=", "internal"),
                # todo only purchases? ("purchase_line_id", "!=", False),
            ]
        else:
            # search for incoming and outgoing moves
            # fixme this search even internal moves
            move_line_domain += [
                "|",
                ("location_id.usage", "=", "internal"),
                ("location_dest_id.usage", "=", "internal"),
            ]

        def sort_key(move_line):
            is_incoming = (
                move_line.location_id.usage != "internal"
                and move_line.location_dest_id.usage == "internal"
            )
            return (
                move_line.date.date(),
                not is_incoming,
                move_line.date,
                move_line.id,
            )

        move_line_ids = sorted(
            self.search(move_line_domain), key=sort_key, reverse=True
        )
        res = self._get_tuples(
            line, move_line_ids, valuation_type, start_qty, start_price
        )
        return res

    @api.model
    def _get_tuples(self, line, move_line_ids, valuation_type, start_qty, start_price):
        """Split the quantity to be evaluated among the move lines.

        The quantity of the product in the closing is assigned going back from
        the newest move line to the oldest one, each one with the price of its
        purchase line (see `update_tuple`):

        - fifo: the quantity is taken from the incoming moves, until it is all
          assigned;
        - lifo: the stock is rebuilt backwards through incoming and outgoing
          moves, and each incoming move gets the part of the quantity that is
          above the stock before it.

        The quantity not assigned to any move gets the price of the last closing.

        :param line: the closing line
        :param move_line_ids: move lines sorted from the newest to the oldest
        :param valuation_type: fifo or lifo
        :param start_qty: product quantity of the last closing
        :param start_price: product price of the last closing
        :return: a list of tuple with
        [(product_id, qty_to_be_evaluated, new_price, qty_from, origin, date)]
        """
        tuples = []
        # the price is copied to the other lines of the product, so evaluate
        # the quantity in all the locations
        qty_to_be_evaluated = qty_at_date = self._get_closing_product_qty(line)
        # get all moves without the lot in the inventory line because it is not relevant
        flag = False
        for ml in move_line_ids:
            uom_from = ml.move_id.product_uom
            # Convert to UoM of the product each time
            qty_from = ml.quantity
            product_qty = uom_from._compute_quantity(qty_from, ml.product_id.uom_id)
            # Get price from the purchase line
            price_unit = 0
            if ml.move_id.purchase_line_id:
                price_unit = ml.move_id._get_purchase_price_unit()

            qty_to_be_evaluated, flag, qty_at_date = self.update_tuple(
                qty_to_be_evaluated,
                product_qty,
                tuples,
                ml,
                price_unit,
                qty_from,
                qty_at_date,
                valuation_type,
            )
            if flag:
                break
        if not float_is_zero(
            qty_to_be_evaluated, precision_rounding=line.product_id.uom_id.rounding
        ):
            # create a tuple for the residual not evaluated
            tuples.append(
                (
                    line.product_id.id,
                    qty_to_be_evaluated,
                    start_price,
                    start_qty,
                    "Residual not evaluated",
                    "Date not evaluated",
                )
            )
        # fix zero values in the tuples, do not get price from product anymore
        tuples = self._fix_zero_values(tuples)
        return tuples

    def _fix_zero_values(self, tuples):
        fixed_tuples = []
        _logger.info(f"Current tuples are {tuples}")
        for i, raw_tuple in enumerate(tuples):
            if not raw_tuple[2]:
                # n.b. the order of the tuples is from the newer to the oldest
                if len(tuples) > i + 1 and tuples[i + 1] and tuples[i + 1][2]:
                    # 1. get the price from the previous evaluation tuple if exists
                    price_unit = tuples[i + 1][2]
                elif i != 0 and tuples[i - 1][2]:
                    # 2. get the price from the next evaluation tuple if not the first
                    price_unit = tuples[i - 1][2]
                else:
                    # 3. get the price from the product
                    price_unit = (
                        self.env["product.product"].browse(raw_tuple[0])._get_cost()
                    )
                fixed_tuples.append(
                    (
                        raw_tuple[0],
                        raw_tuple[1],
                        price_unit,
                        raw_tuple[3],
                        raw_tuple[4],
                        raw_tuple[5],
                    )
                )
            else:
                fixed_tuples.append(raw_tuple)
        _logger.info(f"Fixed tuples are {fixed_tuples}")
        return fixed_tuples

    @staticmethod
    def update_tuple(
        qty_to_be_evaluated,
        product_qty,
        tuples,
        ml,
        price_unit,
        qty_from,
        qty_at_date,
        valuation_type,
    ):
        """Assign part of the quantity to be evaluated to the move line `ml`.

        The tuple of the assigned quantity is appended to `tuples`.

        :param qty_to_be_evaluated: quantity not assigned yet
        :param product_qty: quantity of the move line, in product UoM
        :param qty_at_date: stock before the moves already processed (LIFO only)
        :return: the quantity still to be evaluated, True if it is all
            assigned, and the stock before the move line
        """
        rounding = ml.product_id.uom_id.rounding
        if valuation_type == "fifo":
            if (
                float_compare(
                    qty_to_be_evaluated, product_qty, precision_rounding=rounding
                )
                >= 0
            ):
                tuples.append(
                    (
                        ml.product_id.id,
                        product_qty,
                        price_unit,
                        qty_from,
                        ml.origin,
                        ml.date.strftime("%d/%m/%Y"),
                    )
                )
                qty_to_be_evaluated -= product_qty
            else:
                tuples.append(
                    (
                        ml.product_id.id,
                        qty_to_be_evaluated,
                        price_unit,
                        qty_from * qty_to_be_evaluated / product_qty,
                        ml.origin,
                        ml.date.strftime("%d/%m/%Y"),
                    )
                )
                return 0, True, qty_at_date
        elif valuation_type == "lifo":
            # create a tuple for every move that is an income (purchase or inventory)
            # not used for an outgoing with these values:
            # [(product.id, qty outgoing for this move, cost of purchased product,
            # qty moved)]
            # out (sale, out inventory, etc)
            if (
                ml.location_id.usage == "internal"
                and ml.location_dest_id.usage != "internal"
            ):
                qty_at_date += product_qty
            # in (purchase, in inventory, etc)
            if (
                ml.location_id.usage != "internal"
                and ml.location_dest_id.usage == "internal"
            ):
                qty_at_date -= product_qty
                above_stock = (
                    float_compare(
                        qty_to_be_evaluated, qty_at_date, precision_rounding=rounding
                    )
                    > 0
                )
                stock_compare = float_compare(
                    qty_at_date, 0, precision_rounding=rounding
                )
                # if the quantity to be evaluated is greater than the stock before
                # the move, and that stock is positive, the part above it comes
                # from this move and is evaluated with its price
                if above_stock and stock_compare > 0:
                    tuples.append(
                        (
                            ml.product_id.id,
                            qty_to_be_evaluated - qty_at_date,
                            price_unit,
                            qty_from,
                            ml.origin,
                            ml.date.strftime("%d/%m/%Y"),
                        )
                    )
                    qty_to_be_evaluated = qty_at_date
                # if the stock before the move is zero or negative, all the
                # remaining quantity comes from this move
                elif above_stock:
                    tuples.append(
                        (
                            ml.product_id.id,
                            qty_to_be_evaluated,
                            price_unit,
                            qty_from * qty_to_be_evaluated / product_qty,
                            ml.origin,
                            ml.date.strftime("%d/%m/%Y"),
                        )
                    )
                    return 0, True, qty_at_date
        elif valuation_type == "average":
            tuples.append(
                (
                    ml.product_id.id,
                    product_qty,
                    price_unit,
                    qty_from,
                    ml.origin,
                    ml.date.strftime("%d/%m/%Y"),
                )
            )
        return qty_to_be_evaluated, False, qty_at_date

    @api.model
    def _evaluate_product(
        self, closing_id, closing_line_id, last_close_date, product_id
    ):
        if closing_id.force_evaluation_method in ["lifo", "fifo"]:
            self._get_cost_stock_move_lifo_fifo(closing_line_id)
        elif (
            closing_id.force_evaluation_method != "no_force"
            and not closing_line_id.evaluation_method
        ):
            if closing_id.force_evaluation_method == "purchase":
                self._get_cost_stock_move_purchase_average(
                    last_close_date, closing_line_id
                )
            if closing_id.force_evaluation_method == "standard":
                self._get_cost_stock_move_standard(closing_line_id)
        else:
            if product_id.categ_id.property_cost_method == "fifo":
                self._get_cost_stock_move_lifo_fifo(closing_line_id, "fifo")
            elif product_id.categ_id.property_cost_method == "average":
                self._get_cost_stock_move_purchase_average(
                    last_close_date, closing_line_id
                )
            elif product_id.categ_id.property_cost_method == "standard":
                self._get_cost_stock_move_standard(closing_line_id)

    def _recompute_cost_stock_move_purchase(self, closing_id):
        _logger.info("[1/2] Start recompute cost product purchase")

        # search only lines not elaborated
        closing_line_ids = self.env["stock.close.period.line"].search(
            [
                ("close_id", "=", closing_id.id),
                ("evaluation_method", "not in", ["manual"]),
            ]
        )

        last_close_date = closing_id.last_close_date

        # all closing line ready to elaborate
        elaborated_products = self.env["product.product"]
        for closing_line_id in closing_line_ids:
            if not self._check_consistency(closing_line_id):
                continue
            product_id = closing_line_id.product_id
            if product_id.id in elaborated_products.ids:
                self._search_same_product_value(closing_line_id)
                continue
            elaborated_products |= product_id

            self._evaluate_product(
                closing_id, closing_line_id, last_close_date, product_id
            )

        _logger.info("[1/2] Finish recompute average cost product")

    def _write_results(self, closing_id):
        decimal = self.env["decimal.precision"].precision_get("Product Price")

        _logger.info("[2/2] Start writing results")

        # compute amount
        amount = 0
        for closing_line_id in closing_id.line_ids:
            row_value = (
                closing_line_id.product_qty if closing_line_id.product_qty > 0 else 0
            ) * closing_line_id.price_unit
            amount += round(row_value, decimal)

        # set amount closing
        closing_id.amount = amount

        _logger.info("[2/2] Finish writing results")

    def recompute_average_cost_period_purchase(self, closing_id):
        _logger.info("Recompute average cost period. Making in 2 phases:")
        _logger.info("[1/2] Recompute cost product purchase")
        _logger.info("[2/2] Write results")

        self._recompute_cost_stock_move_purchase(closing_id)
        self._write_results(closing_id)

        _logger.info("End recompute average cost product")
