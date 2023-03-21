# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2012 Andrea Cometa.
#    Email: info@andreacometa.it
#    Web site: http://www.andreacometa.it
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2012 Associazione OpenERP Italia
#    (<http://www.odoo-italia.org>).
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

from openerp import models, fields


class AccountConfigSettings(models.TransientModel):

    _inherit = 'account.config.settings'

    due_cost_service_id = fields.Many2one(
        related='company_id.due_cost_service_id',
        help='Default Service for RiBa Due Cost (collection fees) on invoice',
        domain=[('type', '=', 'service')])

    def default_get(self, cr, uid, fields, context=None):
        res = super(AccountConfigSettings, self).default_get(
            cr, uid, fields, context)
        if res:
            user = self.pool['res.users'].browse(cr, uid, uid, context)
            res['due_cost_service_id'] = user.company_id.due_cost_service_id.id
        return res


class ResCompany(models.Model):

    _inherit = 'res.company'

    due_cost_service_id = fields.Many2one('product.product')
