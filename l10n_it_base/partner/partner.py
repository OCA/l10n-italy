# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2010 OpenERP Italian Community (<http://www.openerp-italia.org>). 
#    All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
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

class res_region(osv.osv):
    _name = 'res.region'
    _description = 'Region'
    _columns = {
        'name': fields.char('Region Name', size=64, help='The full name of the region.', required=True),
        'country_id': fields.many2one('res.country', 'Country'),
    }
res_region()

class res_province(osv.osv):
    _name = 'res.province'
    _description = 'Province'
    _columns = {
        'name': fields.char('Province Name', size=64, help='The full name of the province.', required=True),
        'code': fields.char('Province Code', size=2, help='The province code in two chars.',required=True),
        'region': fields.many2one('res.region','Region'),
    }

res_province()

class res_city(osv.osv):
    _name = 'res.city'
    _description = 'City'
    _columns = {
        'name': fields.char('City', size=64, required=True),
    	'province_id': fields.many2one('res.province','Province'),
        'zip': fields.char('ZIP', size=5),
        'phone_prefix': fields.char('Telephone Prefix' , size=16),
        'istat_code': fields.char('ISTAT code', size=16),
        'cadaster_code': fields.char('Cadaster Code', size=16),
        'web_site': fields.char('Web Site', size=64),
        'region': fields.related('province_id','region',type='many2one', relation='res.region', string='Region', readonly=True),
    }

res_city()


class res_partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
        'city': fields.related('address','city',type='char', string='City'),
    }    
   
res_partner()

class res_partner_address(osv.osv):
    _inherit = 'res.partner.address'

    '''
    def name_get(self, cr, user, ids, context={}):
        if not len(ids):
            return []
        res = []
        for r in self.read(cr, user, ids, ['name','zip','country_id', 'city','partner_id', 'street']):
            if context.get('contact_display', 'contact')=='partner' and r['partner_id']:
                res.append((r['id'], r['partner_id'][1]))
            else:
                addr = r['name'] or ''
                if r['name'] and (r['city'] or r['country_id']):
                    addr += ', '
                addr += (r['country_id'] and r['country_id'][1] or '') + ' ' + (r['city'] and r['city'][1] or '') + ' '  + (r['street'] or '')
                if (context.get('contact_display', 'contact')=='partner_address') and r['partner_id']:
                    res.append((r['id'], "%s: %s" % (r['partner_id'][1], addr.strip() or '/')))
                else:
                    res.append((r['id'], addr.strip() or '/'))
        return res
    '''

    def _get_province(self, cr, uid, context=None):
        result = None
        if 'city' in context:
            city_id = self.pool.get('res.city').search(cr, uid, [('name', '=', context['city'].title())])
            if city_id:
                city_obj = self.pool.get('res.city').browse(cr, uid, city_id[0])
                result = city_obj.province_id.id
        return result

    def _get_region(self, cr, uid, context=None):
        result = None
        if 'city' in context:
            city_id = self.pool.get('res.city').search(cr, uid, [('name', '=', context['city'].title())])
            if city_id:
                city_obj = self.pool.get('res.city').browse(cr, uid, city_id[0])
                result = city_obj.region.id
        return result

    _columns = {
#        'city': fields.many2one('res.city', 'City'),
        'province': fields.many2one('res.province', string='Province'),
        'region': fields.many2one('res.region', string='Region'),
    }

    _defaults = {
        'province': _get_province,
        'region': _get_region,
        }

    def on_change_city(self, cr, uid, ids, city):
        res = {'value':{}}
        if(city):
            city_id = self.pool.get('res.city').search(cr, uid, [('name', '=', city.title())])
            if city_id:
                city_obj = self.pool.get('res.city').browse(cr, uid, city_id[0])
                res = {'value': {
                    'province':city_obj.province_id.id,
                    'region':city_obj.region.id,
                    'zip': city_obj.zip,
                    'country_id': city_obj.region.country_id.id,
                    'city': city.title(),
                    }}
        return res
    
res_partner_address()
