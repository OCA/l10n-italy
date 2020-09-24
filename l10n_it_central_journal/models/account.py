# Copyright 2018 Gianmarco Conte (gconte@dinamicheaziendali.it)

from odoo import models, fields
import odoo.addons.decimal_precision as dp


class AccountJournalInherit(models.Model):
    _inherit = "account.journal"

    central_journal_exclude = fields.Boolean('Exclude from General Journal')


class DateRangeInherit(models.Model):
    _inherit = "date.range"

    date_last_print = fields.Date('Last printed date')
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
