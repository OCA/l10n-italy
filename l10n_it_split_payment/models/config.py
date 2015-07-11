# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Abstract (http://www.abstract.it)
#    Author: Davide Corio <davide.corio@abstract.it>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api


class res_company(models.Model):
    _inherit = 'res.company'
    sp_type = fields.Selection(
        (('1-entry', 'Write-off on invoice journal entry'),
            ('2-entries', 'Write-off on dedicated journal entry')),
        string='Split payment write-off method',
        help='Method used to post the split payment journal entry')
    sp_account_id = fields.Many2one(
        'account.account',
        string='Split Payment Write-off Account',
        help='Account used to write off the VAT amount')
    sp_journal_id = fields.Many2one(
        'account.journal',
        string='Split Payment Write-off Journal',
        help='Journal used to write off the VAT amount')


class account_config_settings(models.TransientModel):
    _inherit = 'account.config.settings'

    sp_type = fields.Selection(
        related='company_id.sp_type',
        string="Split payment write-off method",
        help='Method used to post the split payment journal entry')
    sp_account_id = fields.Many2one(
        related='company_id.sp_account_id',
        string='Split Payment Write-off account',
        help='Account used to write off the VAT amount')
    sp_journal_id = fields.Many2one(
        related='company_id.sp_journal_id',
        string='Split Payment Write-off Journal',
        help='Journal used to write off the VAT amount')
