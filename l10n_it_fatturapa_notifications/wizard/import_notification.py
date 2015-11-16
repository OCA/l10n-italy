# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
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
import base64


class ImportNotification(orm.TransientModel):
    _name = 'wizard.fatturapa.import.notification'
    _columns = {
        'name': fields.binary("XML", help="XML notification file"),
        'file_name': fields.char('File Name', size=256),
        'invoice_type': fields.selection([
            ('supplier', 'Supplier'),
            ('customer', 'Customer')
        ], string="Invoice type", required=True),
    }

    def import_file(self, cr, uid, ids, context=None):
        notification_pool = self.pool['fatturapa.notification']
        wizard = self.browse(cr, uid, ids[0], context=context)
        xml = base64.decodestring(wizard.name)
        file_name = wizard.file_name
        res_id = notification_pool.save_notification_xml(
            cr, uid, ids, xml, file_name, invoice_type=wizard.invoice_type,
            context=context)

        return {
            'view_type': 'form',
            'name': "FatturaPA Notification",
            'res_id': res_id,
            'view_mode': 'form',
            'res_model': 'fatturapa.notification',
            'type': 'ir.actions.act_window',
            'context': context
        }
