# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Alessandro Camilli (a.camilli@openforce.it)
#    Copyright (C) 2015
#    Apulia Software srl - info@apuliasoftware.it - www.apuliasoftware.it
#    Openforce di Camilli Alessandro - www.openforce.it
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    of_account_end_vat_statement_interest = fields.Boolean(
        'Interest on End Vat Statement',
        help="Apply interest on end vat statement")
    of_account_end_vat_statement_interest_percent = fields.Float(
        'Interest on End Vat Statement - %',
        help="Apply interest on end vat statement")
    of_account_end_vat_statement_interest_account_id = fields.Many2one(
        'account.account', 'Interest on End Vat Statement - Account',
        help="Apply interest on end vat statement")
