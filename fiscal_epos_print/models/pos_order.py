from odoo import fields, models, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    refund_date = fields.Date(string='Refund date reference')
    refund_report = fields.Integer(string='Closure reference', digits=(4, 0))
    refund_doc_num = fields.Integer(string='Document Number', digits=(4, 0))
    refund_cash_fiscal_serial = fields.Char(string='Refund Cash Serial')

    fiscal_receipt_number = fields.Integer(
        string='Fiscal receipt number', digits=(4, 0))
    fiscal_receipt_amount = fields.Float("Fiscal receipt amount")
    fiscal_receipt_date = fields.Date(
        "Fiscal receipt date", digits=(4, 0))
    fiscal_z_rep_number = fields.Integer("Fiscal closure number")
    fiscal_printer_serial = fields.Char(string='Fiscal Printer Serial')
    fiscal_printer_debug_info = fields.Text("Debug info", readonly=True)

    # TODO allow to save code on customer and load customer, if present
    lottery_code = fields.Char(string='Lottery Code')

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        res['lottery_code'] = ui_order.get('lottery_code')
        res['refund_date'] = ui_order['refund_date'] or False
        res['refund_report'] = ui_order['refund_report'] or False
        res['refund_doc_num'] = ui_order['refund_doc_num'] or False
        res['refund_cash_fiscal_serial'] = \
            ui_order['refund_cash_fiscal_serial'] or False
        res['fiscal_receipt_number'] = \
            ui_order['fiscal_receipt_number'] or False
        res['fiscal_receipt_amount'] = \
            ui_order['fiscal_receipt_amount'] or False
        res['fiscal_receipt_date'] = ui_order['fiscal_receipt_date'] or False
        res['fiscal_z_rep_number'] = ui_order['fiscal_z_rep_number'] or False
        res['fiscal_printer_serial'] = \
            ui_order['fiscal_printer_serial'] or False
        res['fiscal_printer_debug_info'] = \
            ui_order['fiscal_printer_debug_info'] or False
        return res

    # This is on pos_order_mgmt to send back the fields of already existing
    # pos.order
    @api.multi
    def _prepare_done_order_for_pos(self):
        res = super(PosOrder, self)._prepare_done_order_for_pos()
        res['lottery_code'] = self.lottery_code
        res['refund_date'] = self.refund_date
        res['refund_report'] = self.refund_report
        res['refund_doc_num'] = self.refund_doc_num
        res['refund_cash_fiscal_serial'] = self.refund_cash_fiscal_serial
        res['fiscal_receipt_number'] = self.fiscal_receipt_number
        res['fiscal_receipt_amount'] = self.fiscal_receipt_amount
        res['fiscal_receipt_date'] = self.fiscal_receipt_date
        res['fiscal_z_rep_number'] = self.fiscal_z_rep_number
        res['fiscal_printer_serial'] = self.fiscal_printer_serial
        res['fiscal_printer_debug_info'] = self.fiscal_printer_debug_info
        return res

    @api.model
    def update_fiscal_receipt_debug_info(self, pos_order):
        po = self.search([('pos_reference', '=', pos_order.get('name'))])
        debug_info = pos_order.get('fiscal_printer_debug_info')
        if po:
            po.write({
                'fiscal_printer_debug_info': debug_info,
            })
        return True

    @api.model
    def update_fiscal_receipt_values(self, pos_order):
        po = self.search([('pos_reference', '=', pos_order.get('name'))])
        receipt_no = int(pos_order.get('fiscal_receipt_number'))
        receipt_date = pos_order.get('fiscal_receipt_date')
        receipt_amount = float(pos_order.get('fiscal_receipt_amount'))
        fiscal_z_rep_number = int(pos_order.get('fiscal_z_rep_number'))
        fiscal_printer_serial = pos_order.get('fiscal_printer_serial') or \
            self.config_id.fiscal_printer_serial
        if po:
            po.write({
                'fiscal_receipt_number': receipt_no,
                'fiscal_receipt_date': receipt_date,
                'fiscal_receipt_amount': receipt_amount,
                'fiscal_z_rep_number': fiscal_z_rep_number,
                'fiscal_printer_serial': fiscal_printer_serial,
            })
        return True

    @api.model
    def create_from_ui(self, orders):
        res = super(PosOrder, self).create_from_ui(orders)
        for order in orders:
            if order['data'].get('fiscal_receipt_number'):
                self.update_fiscal_receipt_values(order['data'])
            if order['data'].get('fiscal_printer_debug_info'):
                self.update_fiscal_receipt_debug_info(order['data'])
        return res
