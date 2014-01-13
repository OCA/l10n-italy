# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 Agile Business Group sagl (<http://www.agilebg.com>)
#    Author: Nicola Malcontenti <nicola.malcontenti@agilebg.com>
#    Copyright (C) 2013 Associazione OpenERP Italia
#                 (<http://www.openerp-italia.org>).
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

from openerp.osv import orm
from openerp.osv import fields


class crm_lead(orm.Model):
    _inherit = 'crm.lead'

    def on_change_city(self, cr, uid, ids, city):
        return self.pool.get('res.partner').on_change_city(cr, uid, ids, city)

    def _lead_create_contact(self, cr, uid, lead, name, is_company,
                             parent_id=False, context=None):
        if lead:
            partner_id = super(crm_lead, self)._lead_create_contact(
                cr, uid, lead, name, is_company,
                parent_id=parent_id, context=context
            )
            if partner_id:
                partner = self.pool.get('res.partner')
                vals = {
                    'province': lead.province.id,
                    'region': lead.region.id,
                }
                partner.write(cr, uid, partner_id, vals, context=context)
        return partner_id

    _columns = {
        'province': fields.many2one('res.province', string='Provincia'),
        'region': fields.many2one('res.region', string='Region'),
    }
