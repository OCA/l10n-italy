# -*- coding: utf-8 -*-
# Author: Gianmarco Conte - Dinamiche Aziendali Srl
# Copyright 2017
# Dinamiche Aziendali Srl <www.dinamicheaziendali.it>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
import datetime


class AccountJournalInherit(models.Model):
    _inherit = "account.journal"

    central_journal_exclude = fields.Boolean('Exclude from Central \
            Journal')


class DateRangeInherit(models.Model):
    _inherit = "date.range"

    date_last_print = fields.Date('Last printed date')
    print_row = fields.Integer('Print row', required=True, default=30)
    progressive_page_number = fields.Integer(
        'Progressive of the page',
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
    period = fields.Many2one(
        comodel_name='date.range', string="Previous Period",
        domain="[('progressive_page_number', '>', 0)]", index=1)

    @api.onchange('period')
    def onchange_period(self):
        if self.period:
            self.date_last_print = self.period.date_last_print
            data_end = datetime.datetime.\
                strptime(self.period.date_end, '%Y-%m-%d')
            data_end += datetime.timedelta(days=1)
            self.date_start = data_end.strftime('%Y-%m-%d')
            self.progressive_page_number = self.period.progressive_page_number
            self.progressive_credit = self.period.progressive_credit
            self.progressive_debit = self.period.progressive_debit
            self.progressive_line_number = self.period.progressive_line_number
            self.print_row = self.period.print_row
