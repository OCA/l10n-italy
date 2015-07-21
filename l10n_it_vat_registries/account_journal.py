# -*- coding: utf-8 -*-
#
#    Copyright (C) 2015 Agile Business Group
#    (<http://www.agilebg.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from openerp import models, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'
    tax_registry_id = fields.Many2one(
        'account.tax.registry', 'VAT registry',
        help="You can group several journals within 1 registry. In printing "
             "wizard, you will be able to select the registry in order to load"
             " that group of journals")
