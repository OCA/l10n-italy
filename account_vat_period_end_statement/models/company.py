# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Apulia Software srl (<http://www.apuliasoftware.it>).
#                               Andrea Cometa (<a.cometa@apuliasoftware.it>).
#    Copyright (C) 2014 Associazione ODOO Italia
#    (<http://www.odoo-italia.org>).
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

from openerp.osv import fields, orm


class res_company(orm.Model):
    _inherit = 'res.company'
    _columns = {
        'quarterly_vat': fields.boolean(
            'Quarterly vat',
            help="Check for quarterly vat period end statement, "
            "also if monthly periods are set"),
        'amount_interest': fields.float(
            'Amount interest (%)',
            help="Amount in percent of the interest concerning qaurterly"
            "vat period end statement"),
        }

    _sql_constraints = [
        ('amount_interest_percent1', 'CHECK (amount_interest>=0)', 'Amount interest must >= 0!'),
        ('amount_interest_percent2', 'CHECK (amount_interest<=100)', 'Amount interest must be <= 100!'),
    ]
