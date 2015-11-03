# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 ISA s.r.l. (<http://www.isa.it>).
#    Copyright (C) 2015 Link It Spa
#    (<http://www.linkgroup.it/>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp

class account_journal(models.Model):
    _inherit = "account.journal"

    central_journal_exclude = fields.Boolean('Exclude from Central \
            Journal')
    
class account_fiscalyear(models.Model):
    _inherit = "account.fiscalyear"
    
    date_last_print = fields.Date('Last printed date')
                                 
    progressive_page_number = fields.Integer('Progressive of the page',
                                             
                                             
                                             default=0)
    progressive_line_number = fields.Integer('Progressive line', default = 0)
    progressive_credit = fields.Float('Progressive Credit',
                                      digits_compute=dp.get_precision('Account'),
                                      
                                      
                                      default=lambda *a: float())
    progressive_debit = fields.Float('Progressive Debit',
                                     digits_compute=dp.get_precision('Account'),
                                     
                                     default=lambda *a: float())
    
                