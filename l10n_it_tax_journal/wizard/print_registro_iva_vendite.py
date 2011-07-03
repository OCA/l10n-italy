# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Associazione OpenERP Italia
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

class wizard_registro_iva_vendite(osv.osv_memory):

    _name = "wizard.registro.iva.vendite"
    _columns = {
        'date_from': fields.date('From date', required=True),
        'date_to': fields.date('To date', required=True),
    }

    def print_registro(self, cr, uid, ids, context=None):
        wizard = self.read(cr, uid, ids)[0]
        inv_obj = self.pool.get('account.invoice')
        inv_ids = inv_obj.search(cr, uid, [
            ('move_id.date', '<=', wizard['date_to']),
            ('move_id.date', '>=', wizard['date_from']),
            '|',
            ('type', '=', 'out_invoice'),
            ('type', '=', 'out_refund'),
            '|',
            ('state', '=', 'open'),
            ('state', '=', 'paid'),
            ])
        if context is None:
            context = {}
        datas = {'ids': inv_ids}
        datas['model'] = 'account.invoice'
        datas['form'] = wizard
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'registro_iva_vendite',
            'datas': datas,
        }

wizard_registro_iva_vendite()
