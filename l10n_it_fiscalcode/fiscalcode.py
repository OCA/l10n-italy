# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2010-2012 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
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
#

from osv import fields, osv


class res_partner(osv.osv):
    _inherit = 'res.partner'

    def check_fiscalcode(self, cr, uid, ids, context=None):

        for partner in self.browse(cr, uid, ids):
            if not partner.fiscalcode:
                return True
            elif len(partner.fiscalcode) != 16 and partner.individual:
                return False
            else:
                return True

    _columns = {
        'fiscalcode': fields.char(
            'Fiscal Code', size=16, help="Italian Fiscal Code"),
        'individual': fields.boolean(
            'Individual',
            help="If checked the C.F. is referred to a Individual Person"),
    }
    _defaults = {
        'individual': False,
    }
    _constraints = [(
        check_fiscalcode,
        "The fiscal code doesn't seem to be correct.", ["fiscalcode"])]
    _sql_constraints = [
        ('fiscalcode_uniq', 'unique (fiscalcode, company_id)',
         'The fiscal code must be unique per company !'),
    ]
