# -*- coding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 ISA s.r.l. (<http://www.isa.it>).
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
#

from osv import fields, orm
import decimal_precision as dp


class account_fiscalyear(orm.Model):
    _inherit = "account.fiscalyear"
    _description = "Fiscal Year"
    _columns = {
        'date_last_print': fields.date('Last printed date', readonly=True),
        'progressive_page_number': fields.integer(
            'Progressive of the page', required=True, readonly=True),
        'progressive_line_number': fields.integer(
            'Progressive line', required=True, readonly=True),
        'progressive_credit': fields.float(
            'Progressive Credit', digits_compute=dp.get_precision('Account'),
            required=True, readonly=True),
        'progressive_debit': fields.float(
            'Progressive Debit', digits_compute=dp.get_precision('Account'),
            required=True, readonly=True),
    }

    _defaults = {
        'progressive_page_number': 0,
        'progressive_line_number': 0,
        'progressive_credit': lambda *a: float(),
        'progressive_debit': lambda *a: float(),
    }
