from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    refund_date = fields.Date(string="Refund date reference")
    refund_report = fields.Integer(string="Closure reference")
    refund_doc_num = fields.Integer(string="Document Number")
    refund_cash_fiscal_serial = fields.Char(string="Refund Cash Serial")

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
        res = super(PosOrder, self)._order_fields(ui_order)
        res["lottery_code"] = ui_order.get("lottery_code", "")
        res["refund_date"] = ui_order.get("refund_date", False)
        res["refund_report"] = ui_order.get("refund_report", False)
        res["refund_doc_num"] = ui_order.get("refund_doc_num", False)
        res["refund_cash_fiscal_serial"] = ui_order.get(
            "refund_cash_fiscal_serial", False
        )
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
    def update_fiscal_receipt_debug_info(self, pos_order):
        po = self.search([("pos_reference", "=", pos_order.get("name"))])
        debug_info = pos_order.get("fiscal_printer_debug_info")
        if po:
            po.write(
                {
                    "fiscal_printer_debug_info": debug_info,
                }
            )
        return True

    @api.model
    def update_fiscal_receipt_values(self, pos_order):
        po = self.search([("pos_reference", "=", pos_order.get("name"))])
        receipt_no = int(pos_order.get("fiscal_receipt_number"))
        receipt_date = pos_order.get("fiscal_receipt_date")
        receipt_amount = float(pos_order.get("fiscal_receipt_amount"))
        fiscal_z_rep_number = int(pos_order.get("fiscal_z_rep_number"))
        fiscal_printer_serial = (
            pos_order.get("fiscal_printer_serial")
            or self.config_id.fiscal_printer_serial
            )

        fiscal_operator_number = pos_order.get("fiscal_operator_number")
        
        if po:
            po.write(
                {
                    "fiscal_receipt_number": receipt_no,
                    "fiscal_receipt_date": receipt_date,
                    "fiscal_receipt_amount": receipt_amount,
                    "fiscal_z_rep_number": fiscal_z_rep_number,
                    "fiscal_printer_serial": fiscal_printer_serial,
                    "fiscal_operator_number": fiscal_operator_number,
                }
            )
        return True

    @api.model
    def create_from_ui(self, orders, draft=False):
        order_ids = super(PosOrder, self).create_from_ui(orders, draft)
        for order in orders:
            if order["data"].get("fiscal_receipt_number"):
                self.update_fiscal_receipt_values(order["data"])
            if order["data"].get("fiscal_printer_debug_info"):
                self.update_fiscal_receipt_debug_info(order["data"])
        return order_ids

    def _export_for_ui(self, order):
        result = super(PosOrder, self)._export_for_ui(order)
        result.update(
            {
                "lottery_code": order.lottery_code,
                "refund_date": order.refund_date,
                "refund_report": order.refund_report,
                "refund_doc_num": order.refund_doc_num,
                "refund_cash_fiscal_serial": order.refund_cash_fiscal_serial,
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
