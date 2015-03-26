# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2015
#    Associazione Odoo Italia (<http://www.odoo-italia.org>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from openerp import models, fields, api


class ResBank(models.Model):

    _inherit = "res.bank"

    abi = fields.Char(size=5, string='ABI')
    cab = fields.Char(size=5, string='CAB')


class ResPartnerBank(models.Model):

    _inherit = "res.partner.bank"

    bank_abi = fields.Char(size=5, string='ABI')
    bank_cab = fields.Char(size=5, string='CAB')

    @api.onchange('bank')
    @api.cr_uid_ids_context
    def onchange_bank_id(self, cr, uid, ids, bank_id, context=None):
        result = super(
            ResPartnerBank, self).onchange_bank_id(
            cr, uid, ids, bank_id, context=context)
        if bank_id:
            bank = self.pool.get('res.bank').browse(
                cr, uid, bank_id, context=context)
            result['value']['bank_abi'] = bank.abi
            result['value']['bank_cab'] = bank.cab
        return result
