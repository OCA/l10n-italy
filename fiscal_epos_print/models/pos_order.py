import logging

from odoo import api, fields, models
from odoo.tools import float_is_zero

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = "pos.order"

    refund_date = fields.Date(string="Refund date reference")
    refund_report = fields.Integer(string="Closure reference")
    refund_doc_num = fields.Integer(string="Document Number")
    refund_cash_fiscal_serial = fields.Char(string="Refund Cash Serial")
    refund_full_refund = fields.Boolean(string="Full Refund", default=False)
    fiscal_receipt_number = fields.Integer(
        string="Fiscal receipt number",
    )
    fiscal_receipt_amount = fields.Float("Fiscal receipt amount")
    fiscal_receipt_date = fields.Date("Fiscal receipt date")
    fiscal_z_rep_number = fields.Integer("Fiscal closure number")
    fiscal_printer_serial = fields.Char()
    fiscal_printer_debug_info = fields.Text("Debug info", readonly=True)
    fiscal_operator_number = fields.Text("Fiscal Operator", readonly=True)

    # TODO allow to save code on customer and load customer, if present
    lottery_code = fields.Char()

    @api.model
    def _order_fields(self, ui_order):
        res = super()._order_fields(ui_order)
        res["lottery_code"] = ui_order.get("lottery_code", "")
        res["refund_date"] = ui_order.get("refund_date", False)
        res["refund_report"] = ui_order.get("refund_report", False)
        res["refund_doc_num"] = ui_order.get("refund_doc_num", False)
        res["refund_cash_fiscal_serial"] = ui_order.get(
            "refund_cash_fiscal_serial", False
        )
        res["refund_full_refund"] = ui_order.get("refund_full_refund", False)
        res["fiscal_receipt_number"] = ui_order.get("fiscal_receipt_number", False)
        res["fiscal_receipt_amount"] = ui_order.get("fiscal_receipt_amount", False)
        res["fiscal_receipt_date"] = ui_order.get("fiscal_receipt_date", False)
        res["fiscal_z_rep_number"] = ui_order.get("fiscal_z_rep_number", False)
        res["fiscal_printer_serial"] = ui_order.get("fiscal_printer_serial", False)
        res["fiscal_printer_debug_info"] = ui_order.get(
            "fiscal_printer_debug_info", False
        )
        res["fiscal_operator_number"] = ui_order.get("fiscal_operator_number", False)
        return res

    @api.model
    def create_from_ui(self, orders, draft=False):
        if self.env.company.country_id.id == self.env.ref("base.it").id:
            draft = True
        order_ids = super().create_from_ui(orders, draft)
        process_order_ids = []
        for order in orders:
            if order["data"].get("pricelist_id", False):
                pricelist_id = self.env["product.pricelist"].browse(
                    order["data"]["pricelist_id"]
                )
                precision = pricelist_id.currency_id.decimal_places
            else:
                precision = self.env.company.currency_id.decimal_places
            if (
                order["data"].get("fiscal_receipt_number", False)
                or order["data"].get("to_invoice", False)
                or float_is_zero(order["data"].get("amount_total", 0), precision)
            ) and self.env.company.country_id.id == self.env.ref("base.it").id:
                order_name = order["data"].get("name")
                try:
                    existing_draft_orders = self.search(
                        [
                            ("pos_reference", "=", order_name),
                            ("state", "=", "draft"),
                        ]
                    )
                    for existing_draft_order in existing_draft_orders:
                        process_order_ids.append(
                            self._process_order(order, False, existing_draft_order)
                        )
                except Exception as e:
                    _logger.exception(
                        "An error occurred when processing the PoS order %s", order_name
                    )
                    pos_session = self.env["pos.session"].browse(
                        order["data"].get("pos_session_id", 0)
                    )
                    pos_session._handle_order_process_fail(order, e, draft)
                    raise
        if process_order_ids:
            order_ids = self.env["pos.order"].search_read(
                domain=[("id", "in", process_order_ids)],
                fields=["id", "pos_reference", "account_move"],
                load=False,
            )
        return order_ids

    def _export_for_ui(self, order):
        result = super()._export_for_ui(order)
        result.update(
            {
                "lottery_code": order.lottery_code,
                "refund_date": order.refund_date,
                "refund_report": order.refund_report,
                "refund_doc_num": order.refund_doc_num,
                "refund_cash_fiscal_serial": order.refund_cash_fiscal_serial,
                "refund_full_refund": order.refund_full_refund,
                "fiscal_receipt_number": order.fiscal_receipt_number,
                "fiscal_receipt_amount": order.fiscal_receipt_amount,
                "fiscal_receipt_date": order.fiscal_receipt_date,
                "fiscal_z_rep_number": order.fiscal_z_rep_number,
                "fiscal_printer_serial": order.fiscal_printer_serial,
                "fiscal_printer_debug_info": order.fiscal_printer_debug_info,
                "fiscal_operator_number": order.fiscal_operator_number,
            }
        )
        return result
