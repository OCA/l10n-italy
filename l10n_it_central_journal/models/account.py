# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2017 Dinamiche Aziendali srl
#                       (<http://www.dinamicheaziendali.it.it>).
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################

from odoo import models, fields
import odoo.addons.decimal_precision as dp


class account_journal(models.Model):
    _inherit = "account.journal"

    central_journal_exclude = fields.Boolean('Exclude from Central \
            Journal')


class account_fiscalyear(models.Model):
    _inherit = "date.range"
    # _inherit = "account.fiscalyear"

    date_last_print = fields.Date('Last printed date')
    progressive_page_number = fields.Integer('Progressive of the page',
                                             default=0)
    progressive_line_number = fields.Integer('Progressive line', default=0)
    progressive_credit = fields.Float(
        'Progressive Credit',
        digits_compute=dp.get_precision('Account'),
        default=lambda *a: float())
    progressive_debit = fields.Float(
        'Progressive Debit',
        digits_compute=dp.get_precision('Account'),
        default=lambda *a: float())
