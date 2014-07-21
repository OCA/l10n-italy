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

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    province_id = fields.Many2one('res.country.province', 'Province')

    @api.multi
    def onchange_zip_id(self, zip_id):
        res = super(ResPartner, self).onchange_zip_id(zip_id)
        if 'value' in res:
            bzip = self.env['res.better.zip'].browse(zip_id)
            res['value'][
                'province_id'
                ] = bzip.province_id.id if bzip.province_id else False,
        return res
