# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013-2017 Agile Business Group sagl (http://www.agilebg.com)
#    @author Alex Comba <alex.comba@agilebg.com>
#    @author Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#    Copyright (C) 2017 CQ Creativi Quadrati (http://www.creativiquadrati.it)
#    @author Diego Bruselli <d.bruselli@creativiquadrati.it>
#    Copyright (C) 2013
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################

from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    bill_of_entry_journal_id = fields.Many2one(
        'account.journal', 'Bill of entry Storno journal',
        help="Journal used for reconciliation of customs supplier",
    )


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    bill_of_entry_journal_id = fields.Many2one(
        'account.journal', related='company_id.bill_of_entry_journal_id',
        string="Bill of entry Storno journal",
        help="Journal used for reconciliation of customs supplier",
    )
