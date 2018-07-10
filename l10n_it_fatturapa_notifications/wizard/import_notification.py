# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
import base64


class ImportNotification(models.TransientModel):
    _name = 'wizard.fatturapa.import.notification'
    name = fields.Binary("XML", help="XML notification file")
    file_name = fields.Char('File Name')
    invoice_type = fields.Selection([
        ('supplier', 'Supplier'),
        ('customer', 'Customer')
    ], string="Invoice type", required=True)

    @api.multi
    def import_file(self, cr, uid, ids, context=None):
        self.ensure_one()
        notification_model = self.env['fatturapa.notification']
        wizard = self
        xml = base64.decodestring(wizard.name)
        file_name = wizard.file_name
        res_id = notification_model.save_notification_xml(
            xml, file_name, invoice_type=wizard.invoice_type)

        return {
            'view_type': 'form',
            'name': "FatturaPA Notification",
            'res_id': res_id,
            'view_mode': 'form',
            'res_model': 'fatturapa.notification',
            'type': 'ir.actions.act_window',
        }
