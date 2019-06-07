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
    location_id = fields.Many2one(
        comodel_name='stock.location', string='Location', required=True,
        domain="[('usage', '=', 'internal')]")

    @api.onchange('date_range_id')
    def onchange_date_range_id(self):
        self.from_date = self.date_range_id.date_start
        self.to_date = self.date_range_id.date_end

    @api.multi
    def button_export_pdf(self):
        self.ensure_one()
        report_type = 'qweb-pdf'
        return self._export(report_type)

    def _prepare_report_stock_journal(self):
        self.ensure_one()
        return {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'location_id': self.location_id.id,
        }

    def _export(self, report_type):
        """Default export is PDF."""
        model = self.env['stock_journal_report']
        report = model.create(self._prepare_report_stock_journal())
        report.compute_data_for_report()
        return report.print_report(report_type)

