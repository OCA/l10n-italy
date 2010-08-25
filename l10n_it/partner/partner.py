# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2010 OpenERP Italian Community (<http://www.openerp-italia.org>). 
#    All Rights Reserved
#    $Id$
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

from osv import osv
from osv import fields

class res_province(osv.osv):
    _name = 'res.province'
    _description = 'Province'
    _columns = {
        'name': fields.char('Province Name', size=64, help='The full name of the province.', required=True, translate=True),
        'code': fields.char('Province Code', size=2, help='The province code in two chars.',required=True),
    }

res_province()


class res_partner(osv.osv):
    _inherit = 'res.partner'

    def check_fiscalcode(self, cr, uid, ids, context={}):
        
        for partner in self.browse(cr, uid, ids):
            if not partner.fiscalcode:
                return True
            if len(partner.fiscalcode) != 16:
                return False

        return True

    _columns = {
        'fiscalcode': fields.char('Fiscal Code', size=16, help="Italian Fiscal Code"),
	    'province': fields.related('address','province_id',type='many2one', relation='res.province', string='Province'),
    }
    #_constraints = [(check_fiscalcode, "The fiscal code doesn't seem to be correct.", ["fiscalcode"])]
    
    def check_fiscalcode(self, fiscalcode):
        import re
        pattern = r'^[A-Za-z]{6}[0-9]{2}[A-Za-z]{1}[0-9]{2}[A-Za-z]{1}[0-9]{3}[A-Za-z]{1}$'
        #if len(fiscalcode) == 16 and re.findall(regexp,fiscalcode):
        #if len(fiscalcode) == 16:
        return True
        #else:
        #    return False
    
res_partner()

class res_partner_address(osv.osv):
    _inherit = 'res.partner.address'

    _columns = {
	'province_id': fields.many2one('res.province','Province'),
    }
    
res_partner_address()
