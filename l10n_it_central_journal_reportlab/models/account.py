# Copyright 2018 Gianmarco Conte (gconte@dinamicheaziendali.it)

from odoo import models, fields
import odoo.addons.decimal_precision as dp


class AccountJournalInherit(models.Model):
    _inherit = "account.journal"

    central_journal_exclude_reportlab = fields.Boolean(
        string='Exclude from General Journal (Reportlab)'
    )


class DateRangeInherit(models.Model):
    _inherit = "date.range"

    date_last_print_reportlab = fields.Date('Last printed date (Reportlab)')
    progressive_page_number_reportlab = fields.Integer(
        string='Progressive of the page (Reportlab)',
        default=0
    )
    progressive_line_number_reportlab = fields.Integer(
        string='Progressive line (Reportlab)',
        default=0
    )
    progressive_credit_reportlab = fields.Float(
        'Progressive Credit (Reportlab)',
        digits=dp.get_precision('Account'),
        default=0.0
    )
    progressive_debit_reportlab = fields.Float(
        'Progressive Debit (Reportlab)',
        digits=dp.get_precision('Account'),
        default=0.0
    )
