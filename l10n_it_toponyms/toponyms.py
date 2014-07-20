# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Lorenzo Battistini (<lorenzo.battistini@agilebg.com>)
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
##############################################################################

from openerp.osv import fields, orm


class ResCountryProvince(orm.Model):

    _name = "res.country.province"

    _columns = {
        'name': fields.char(
            'Province Name', size=64, help='The full name of the province',
            required=True),
        'code': fields.char(
            'Province Code', size=2, help='The province code in two chars',
            required=True),
        }


class ResBetterZip(orm.Model):

    _inherit = 'res.better.zip'

    _columns = {
        'province_id': fields.many2one('res.country.province', 'Province'),
        }


class ResPartner(orm.Model):
    _inherit = 'res.partner'
    _columns = {
        'province_id': fields.many2one('res.country.province', 'Province'),
        }

    def onchange_zip_id(self, cr, uid, ids, zip_id, context=None):
        res = super(ResPartner, self).onchange_zip_id(
            cr, uid, ids, zip_id, context=context)
        if 'value' in res:
            bzip = self.pool['res.better.zip'].browse(
                cr, uid, zip_id, context=context)
            res['value'][
                'province_id'
                ] = bzip.province_id.id if bzip.province_id else False,
        return res
