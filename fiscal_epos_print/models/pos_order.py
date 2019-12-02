# coding=utf-8

from odoo import fields, models, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    refund_date = fields.Date(string='Refund date reference')
    refund_report = fields.Integer(string='Report reference', digits=(4, 0))
    refund_doc_num = fields.Integer(string='Document Number', digits=(4, 0))
    refund_cash_fiscal_serial = fields.Char(string='Refund Cash Serial')

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        res['refund_date'] = ui_order['refund_date'] or False
        res['refund_report'] = ui_order['refund_report'] or False
        res['refund_doc_num'] = ui_order['refund_doc_num'] or False
        res['refund_cash_fiscal_serial'] = \
            ui_order['refund_cash_fiscal_serial'] or False
        return res

    # This is on pos_order_mgmt to send back the fields of already existing
    # pos.order
    @api.multi
    def _prepare_done_order_for_pos(self):
        res = super(PosOrder, self)._prepare_done_order_for_pos()
        res['refund_date'] = self.refund_date
        res['refund_report'] = self.refund_report
        res['refund_doc_num'] = self.refund_doc_num
        res['refund_cash_fiscal_serial'] = self.refund_cash_fiscal_serial
        return res
