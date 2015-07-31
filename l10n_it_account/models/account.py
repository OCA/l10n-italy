# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Abstract srl (<http://www.abstract.it>)
#    Copyright (C) 2015 Agile Business Group sagl (<http://www.agilebg.com>)
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

from openerp import fields, models


class AccountAccount(models.Model):
    _inherit = 'account.account'

    inverse_user_type = fields.Many2one(
        'account.account.type',
        string='Inverse Account Type',
        help="Used on balance sheet to report this account when its balance is \
        negative")
    inverse_parent_id = fields.Many2one(
        'account.account',
        string='Inverse Parent',
        help="Used on balance sheet to report this account when its balance is \
        negative")
