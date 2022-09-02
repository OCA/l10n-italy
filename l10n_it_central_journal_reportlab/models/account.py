# Copyright 2018 Gianmarco Conte (gconte@dinamicheaziendali.it)

from odoo import fields, models


class AccountJournalInherit(models.Model):
    _inherit = "account.journal"

    central_journal_exclude = fields.Boolean("Exclude from General Journal")


class DateRangeInherit(models.Model):
    _inherit = "date.range"

    date_last_print = fields.Date("Last printed date")
    progressive_page_number = fields.Integer("Progressive of the page")
    progressive_line_number = fields.Integer("Progressive line")
    progressive_credit = fields.Float(
        "Progressive Credit",
        digits="Account",
    )
    progressive_debit = fields.Float(
        "Progressive Debit",
        digits="Account",
    )
