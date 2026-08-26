from odoo import fields, models


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
    fiscal_printer_debug_info = fields.Text("Debug info")
    fiscal_operator_number = fields.Text("Fiscal Operator")
    lottery_code = fields.Char()
