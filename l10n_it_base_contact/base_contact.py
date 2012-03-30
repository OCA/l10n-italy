# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2012 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>). 
#    All Rights Reserved
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

from osv import fields,osv

class res_partner_contact(osv.osv):
    _inherit = "res.partner.contact"
    _columns = {
        'fiscalcode': fields.char('Fiscal Code', size=16, help="Italian Fiscal Code"),
        }
res_partner_contact()

class res_partner_location(osv.osv):
    _inherit = 'res.partner.location'
    _columns = {
        'province': fields.many2one('res.province', string='Province'),
        }
        
    def on_change_city(self, cr, uid, ids, city):
        return self.pool.get('res.partner.address').on_change_city(cr, uid, ids, city)
        
res_partner_location()

class res_partner_address(osv.osv):
    _inherit = 'res.partner.address'
    
    def onchange_location_id(self,cr, uid, ids, location_id=False, context={}):
        res = super(res_partner_address, self).onchange_location_id(
            cr, uid, ids, location_id=location_id, context=context)
        if location_id:
            location = self.pool.get('res.partner.location').browse(cr, uid, location_id, context=context)
            res['value'].update({
                'province':location.province and location.province.id or False,
                'region':location.province and location.province.region and location.province.region.id or False,
                })
        return res
res_partner_address()
