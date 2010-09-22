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

class res_region(osv.osv):
    _name = 'res.region'
    _description = 'Region'
    _columns = {
        'name': fields.char('Region Name', size=64, help='The full name of the region.', required=True),
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

class res_municipality(osv.osv):
    _name = 'res.municipality'
    _description = 'Municipality'
    _columns = {
        'name': fields.char('Municipality', size=64, required=True),
    	'province_id': fields.many2one('res.province','Province'),
        'zip': fields.char('ZIP', size=5),
        'phone_prefix': fields.char('Telephone Prefix' , size=16),
        'istat_code': fields.char('ISTAT code', size=16),
        'cadaster_code': fields.char('Cadaster Code', size=16),
        'web_site': fields.char('Web Site', size=64),
        'region': fields.related('province_id','region',type='many2one', relation='res.region', string='Region', readonly=True),
    }

res_municipality()


class res_partner(osv.osv):
    _inherit = 'res.partner'
    _columns = {
#        'province': fields.related('address','province',type='char', string='Province'),
        'municipality': fields.related('address','municipality',type='many2one', relation='res.municipality', string='Municipality'),
    }    
res_partner()

class res_partner_address(osv.osv):
    _inherit = 'res.partner.address'

    _columns = {
        'municipality': fields.many2one('res.municipality', 'City'),
        'province': fields.related('municipality','province_id',type='many2one', relation='res.province', string='Province'),
        'region': fields.related('municipality','region',type='many2one', relation='res.region', string='Region'),
    }

    def on_change_municipality(self, cr, uid, ids, municipality):
        '''
        res = {'value': {
            'country_id': self.pool.get('res.country').search(cr, uid, [('name','=','Italy')])[0],
            }}
        '''
        res = {'value':{}}
        if(municipality):
            municipality = self.pool.get('res.municipality').browse(cr, uid, municipality)
            res = {'value': {
                'province':municipality.province_id.id,
                'region':municipality.region.id,
                'zip': municipality.zip,
                }}
        return res
    
res_partner_address()
