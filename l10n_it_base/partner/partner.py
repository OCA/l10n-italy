# -*- encoding: utf-8 -*-
#
#
#    Copyright (C) 2010 OpenERP Italian Community
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2010 Associazione OpenERP Italia.
#    Copyright (C) 2014 Lorenzo Battistini <lorenzo.battistini@agilebg.com>.
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
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from osv import osv
from osv import fields
import logging


class res_region(osv.osv):
    _name = 'res.region'
    _description = 'Region'
    _columns = {
        'name': fields.char(
            'Region Name', size=64, help='The full name of the region.',
            required=True),
        'country_id': fields.many2one('res.country', 'Country'),
    }


res_region()


class res_province(osv.osv):
    _name = 'res.province'
    _description = 'Province'
    _columns = {
        'name': fields.char(
            'Province Name', size=64, help='The full name of the province.',
            required=True),
        'code': fields.char(
            'Province Code', size=2, help='The province code in two chars.',
            required=True),
        'region': fields.many2one('res.region', 'Region'),
    }


res_province()


class res_city(osv.osv):
    _name = 'res.city'
    _description = 'City'
    _columns = {
        'name': fields.char('City', size=64, required=True),
        'province_id': fields.many2one('res.province', 'Province'),
        'zip': fields.char('ZIP', size=5),
        'phone_prefix': fields.char('Telephone Prefix', size=16),
        'istat_code': fields.char('ISTAT code', size=16),
        'cadaster_code': fields.char('Cadaster Code', size=16),
        'web_site': fields.char('Web Site', size=64),
        'region': fields.related(
            'province_id', 'region', type='many2one', relation='res.region',
            string='Region', readonly=True),
    }


class res_partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
        'province': fields.many2one('res.province', string='Province'),
        'region': fields.many2one('res.region', string='Region'),
        'province_code': fields.related(
            'province', 'code', type='char',
            size=2, string='Province code'),
    }

    def on_change_city(self, cr, uid, ids, city):
        res = {'value': {}}
        if(city):
            city_id = self.pool.get('res.city').search(
                cr, uid, [('name', '=ilike', city)])
            if city_id:
                city_obj = self.pool.get('res.city').browse(
                    cr, uid, city_id[0])
                res = {'value': {
                    'province': (
                        city_obj.province_id and city_obj.province_id.id or
                        False
                    ),
                    'region': city_obj.region and city_obj.region.id or False,
                    'zip': city_obj.zip,
                    'country_id': (
                        city_obj.region and
                        city_obj.region.country_id and
                        city_obj.region.country_id.id or False
                    ),
                    'city': city.title(),
                }
                }
        return res

    def _set_vals_city_data(self, cr, uid, vals):
        if 'city' in vals and 'province' not in vals and 'region' not in vals:
            if vals['city']:
                city_obj = self.pool.get('res.city')
                city_ids = city_obj.search(
                    cr, uid, [('name', '=ilike', vals['city'])])
                if city_ids:
                    city = city_obj.browse(cr, uid, city_ids[0])
                    if 'zip' not in vals:
                        vals['zip'] = city.zip
                    if city.province_id:
                        vals['province'] = city.province_id.id
                    try:
                        if city.region:
                            vals['region'] = city.region.id
                            if city.region.country_id:
                                vals['country_id'] = city.region.country_id.id
                    except Exception as ex:
                        logging.error(ex)
        return vals

    def create(self, cr, uid, vals, context=None):
        vals = self._set_vals_city_data(cr, uid, vals)
        return super(res_partner, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        vals = self._set_vals_city_data(cr, uid, vals)
        return super(res_partner, self).write(cr, uid, ids, vals, context)

    def _address_fields(self, cr, uid, context=None):
        return super(res_partner, self)._address_fields(
            cr, uid, context) + ['province_code']
