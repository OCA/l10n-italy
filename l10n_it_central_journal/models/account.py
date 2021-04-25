# Copyright 2018 Gianmarco Conte (gconte@dinamicheaziendali.it)

from odoo import models, fields, api
from odoo.tools.date_utils import relativedelta
import odoo.addons.decimal_precision as dp


class AccountJournalInherit(models.Model):
    _inherit = "account.journal"

    central_journal_exclude = fields.Boolean('Exclude from General Journal')


class DateRangeInherit(models.Model):
    _inherit = "date.range"

    date_last_print = fields.Date('Last printed date')
    print_row = fields.Integer('Print row', required=True, default=30)
    progressive_page_number = fields.Integer('Progressive of the page',
                                             default=0)
    progressive_line_number = fields.Integer('Progressive line', default=0)
    progressive_credit = fields.Float(
        'Progressive Credit',
        digits=dp.get_precision('Account'),
        default=lambda *a: float())
    progressive_debit = fields.Float(
        'Progressive Debit',
        digits=dp.get_precision('Account'),
        default=lambda *a: float())
    period = fields.Many2one(comodel_name='date.range', string="Previous Period",
                             domain="[('progressive_page_number', '>', 0)]", index=1)

    @api.onchange('period')
    def onchange_period( self):
        if self.period:
            self.date_last_print = self.period.date_last_print
            self.date_start = self.period.date_end + relativedelta(days=1)
            self.progressive_page_number = self.period.progressive_page_number
            self.progressive_credit = self.period.progressive_credit
            self.progressive_debit = self.period.progressive_debit
            self.progressive_line_number = self.period.progressive_line_number
            self.print_row = self.period.print_row
