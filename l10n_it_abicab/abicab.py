# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
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

from osv import fields, orm


class res_bank(orm.Model):
    _inherit = "res.bank"
    _columns = {
        'abi': fields.char('ABI', size=5),
        'cab': fields.char('CAB', size=5),
    }


class res_partner_bank(orm.Model):
    _inherit = "res.partner.bank"
    _columns = {
        'bank_abi': fields.char('ABI', size=5),
        'bank_cab': fields.char('CAB', size=5),
    }

    def onchange_bank_id(self, cr, uid, ids, bank_id, context=None):
        result = super(
            res_partner_bank, self).onchange_bank_id(
            cr, uid, ids, bank_id, context=context)
        if bank_id:
            bank = self.pool.get('res.bank').browse(
                cr, uid, bank_id, context=context)
            result['value']['bank_abi'] = bank.abi
            result['value']['bank_cab'] = bank.cab
        return result
