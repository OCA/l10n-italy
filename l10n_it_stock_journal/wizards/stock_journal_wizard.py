# Copyright 2019 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class StockJournalWizard(models.TransientModel):

    _name = 'stock.journal.wizard'

    date_range_id = fields.Many2one(
        comodel_name='date.range',
        string='Date range'
    )
    from_date = fields.Date(required=True)
    to_date = fields.Date(required=True)

    @api.onchange('date_range_id')
    def onchange_date_range_id(self):
        self.from_date = self.date_range_id.date_start
        self.to_date = self.date_range_id.date_end

    def _get_moves(self, wizard):
        return self.env['stock.move'].search([
            ('date', '>=', self.from_date),
            ('date', '<=', self.to_date),
            ('state', '=', 'done')], order='date, name')

    @api.multi
    def button_export_pdf(self):
        self.ensure_one()
        report_type = 'qweb-pdf'
        return self._export(report_type)

    @api.multi
    def button_export_pdf(self):
        self.ensure_one()
        wizard = self
        moves = self._get_moves(wizard)
        products = moves.mapped('product_id').sorted(
            key=lambda p: (p.default_code or p.name))

        """
        for move in moves:
            result.setdefault(move.product_id.id, []).append(move)
        for product_id, moves in result.iteritems():
        """

        action = {
            'type': 'ir.actions.act_window',
            'name': 'Action Name',  # TODO
            'res_model': 'result.model',  # TODO
            # 'domain': [('id', '=', result_ids)],  # TODO
            'view_mode': 'form,tree',
        }
        return action

    def _prepare_report_stock_journal(self):
        self.ensure_one()
        return {
            'date_from': self.date_from,
            'date_to': self.date_to,
        }

    def _export(self, report_type):
        """Default export is PDF."""
        model = self.env['stock.journal.report']
        report = model.create(self._prepare_report_stock_journal())
        report.compute_data_for_report()
        return report.print_report(report_type)

