# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Abstract (http://www.abstract.it)
#    Author: Davide Corio <davide.corio@abstract.it>
#    Copyright 2015 Lorenzo Battistini - Agile Business Group
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

from openerp.osv import fields, orm


class ResCompany(orm.Model):
    _inherit = 'res.company'
    _columns = {
        'sp_account_id': fields.many2one(
            'account.account',
            string='Split Payment Write-off Account',
            help='Account used to write off the VAT amount'),
        }


class AccountConfigSettings(orm.TransientModel):
    _inherit = 'account.config.settings'

    _columns = {
        'sp_account_id': fields.related(
            'company_id', 'sp_account_id', type='many2one',
            relation='account.account',
            string='Split Payment Write-off account',
            help='Account used to write off the VAT amount'),
        }
