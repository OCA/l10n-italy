# @author: Andrea Piovesana <andrea.m.piovesana@gmail.com>
from odoo import fields, models


class StockDeliveryNoteLine(models.Model):
    _inherit = 'stock.delivery.note.line'

    purchase_line_id = fields.Many2one('purchase.order.line',
                                       related='move_id.purchase_line_id',
                                       store=True)
