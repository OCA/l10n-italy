# Copyright 2019 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp


class StockJournalReport(models.TransientModel):
    """ Here, we just define class fields.
    For methods, go more bottom at this file.

    The class hierarchy is :
    * StockJournalReport
    ** StockJournalReportProduct
        *** StockJournalMoveReport
    """

    _name = 'stock_journal_report'

    from_date = fields.Date()
    to_date = fields.Date()
    location_id = fields.Many2one(
        comodel_name='stock.location', string='Location')
    product_report_ids = fields.One2many(
        comodel_name='stock_journal_product_report',
        inverse_name='report_id'
    )


class StockJournalProductReport(models.TransientModel):

    _name = 'stock_journal_product_report'

    report_id = fields.Many2one(
        comodel_name='stock_journal_report',
        string='Stock Journal Report'
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product'
    )
    initial_balance = fields.Float(
        string='Initial Balance',
        digits=dp.get_precision('Product Unit of Measure'))
    move_report_ids = fields.One2many(
        comodel_name='stock_journal_move_report',
        inverse_name='report_id'
    )


class StockJournalMoveReport(models.TransientModel):

    _name = 'stock_journal_move_report'

    report_id = fields.Many2one(
        comodel_name='stock_journal_product_report',
        string='Stock Journal Product Report'
    )
    move_date = fields.Date(string='Move Date')
    move_number = fields.Integer(string='Move Number')  # move ID
    origin = fields.Char(string='Origin Document Number')
    origin_date = fields.Date(string='Origin Document Date')
    reason = fields.Char(string='Reason')  # picking type
    loading_qty = fields.Float(
        string='Loading Quantity',
        digits=dp.get_precision('Product Unit of Measure'))  # carico
    unloading_qty = fields.Float(
        string='Unloading Quantity',
        digits=dp.get_precision('Product Unit of Measure'))  # scarico


class StockJournalReportCompute(models.TransientModel):
    """ Here, we just define methods.
    For class fields, go more top at this file.
    """

    _inherit = 'stock_journal_report'

    @api.multi
    def print_report(self, report_type='qweb-pdf'):
        self.ensure_one()
        report_name = 'l10n_it_stock_journal.stock_journal_report'
        context = dict(self.env.context)
        action = self.env['ir.actions.report'].search(
            [('report_name', '=', report_name),
             ('report_type', '=', report_type)], limit=1)
        return action.with_context(context).report_action(self, config=False)

    def _get_moves(self):
        return self.env['stock.move'].search([
            ('date', '>=', self.from_date),
            ('date', '<=', self.to_date),
            '|',
            ('location_id', 'child_of', self.location_id.id),
            ('location_dest_id', 'child_of', self.location_id.id),
            ('state', '=', 'done')], order='date, name')

    def _get_moves_filtered_by_product(self, moves, product):
        return moves.filtered(
            lambda m: m.product_id.id == product.id)

    def _create_product_report(self, product):
        return self.env['stock_journal_product_report'].create({
            'product_id': product.id,
            'report_id': self.id,
            'initial_balance': 0.0,
        })

    def _create_move_report(self, move, product_report):
        return self.env['stock_journal_move_report'].create({
            'report_id': product_report.id,
            'move_date': fields.Date.today(), #move.date,
            'move_number': move.id,
            'origin': '',
            'origin_date': fields.Date.today(),
            'reason': move.picking_id.picking_type_id.name,
            'loading_qty': (move.product_uom_qty
                             if move.usage == 'loading'
                             else 0.0),
            'unloading_qty': (move.product_uom_qty
                              if move.usage == 'unloading'
                              else 0.0),
        })

    @api.multi
    def compute_data_for_report(self):
        moves = self._get_moves()
        products = moves.mapped('product_id').sorted(
            key=lambda p: (p.default_code or p.name))
        for product in products:
            product_report = self._create_product_report(product)
            moves = self._get_moves_filtered_by_product(moves, product)
            for move in moves:
                if move.usage != 'internal':
                    self._create_move_report(move, product_report)


