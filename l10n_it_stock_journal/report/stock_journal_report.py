# Copyright 2019 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp


class StockJournalReport(models.TransientModel):

    _name = 'stock.journal.report'

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product'
    )
    initial_balance = fields.Float(
        string='Initial Balance',
        digits=dp.get_precision('Product Unit of Measure'))
    line_ids = fields.One2many(
        comodel_name='stock.journal.report.line',
        inverse_name='report_id'
    )


class StockJournalReportLine(models.TransientModel):

    _name = 'stock.journal.report.line'

    move_date = fields.Date(string='Move Date')
    move_number = fields.Integer(string='Move Number')  # move ID
    origin = fields.Char(string='Origin Document Number')
    move_origin = fields.Date(string='Origin Document Date')
    reason = fields.Char(string='Reason')  # picking type
    incomining_qty = fields.Float(
        string='Incoming Quantity',
        digits=dp.get_precision('Product Unit of Measure'))  # carico
    outcoming_qty = fields.Float(
        string='Outcoming Quantity',
        digits=dp.get_precision('Product Unit of Measure'))  # scarico