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
from openerp.addons.l10n_it_fatturapa_notifications.bindings.\
    MessaggiTypes_v_1_1 import NotificaEsitoCommittente_Type
from openerp.addons.l10n_it_fatturapa_notifications.bindings import (
    MessaggiTypes_v_1_1)
from openerp.tools.translate import _


class FatturaPANotification(orm.Model):
    _inherit = "fatturapa.notification"

    _columns = {
        'fatturapa_in_attachment_id': fields.many2one(
            'fatturapa.attachment.in', "FatturaPA received", readonly=True),
        }

    def save_notification_xml(
        self, cr, uid, ids, xml, file_name, invoice_type="supplier",
        context=None
    ):
        res = super(FatturaPANotification, self).save_notification_xml(
            cr, uid, ids, xml, file_name, context)
        if invoice_type == 'supplier':
            fattPA_attach_pool = self.pool['fatturapa.attachment.in']
            notification = self.browse(cr, uid, res, context=context)
            sender_id, sequence = file_name.split("_")[:2]
            file_identifier = sender_id + "_" + sequence
            fatt_ids = fattPA_attach_pool.search(cr, uid, [
                ('file_identifier', '=', file_identifier),
                ], context=context)
            if not fatt_ids:
                raise orm.except_orm(
                    _("Error"), _("No fatturaPA found with ID %s") %
                    file_identifier)
            if len(fatt_ids) > 1:
                raise orm.except_orm(
                    _("Error"), _("Too many fatturaPA found with ID %s") %
                    file_identifier)
            notification.write(
                {'fatturapa_in_attachment_id': fatt_ids[0]}, context=context)
        return res

    def create_notifica_esito_committente(
        self, cr, uid, ids, invoice, esito='EC01',
        description=False, context=None
    ):
        """
        It creates 'notifica di esito committente' notification and links it to
        fatturaPA.
        'esito' can be
         - EC01 (vale Accettazione)
         - EC02 (vale Rifiuto)
        """
        notifica = NotificaEsitoCommittente_Type()


class FatturaPAAttachmentIn(orm.Model):
    _inherit = "fatturapa.attachment.in"

    def _get_file_identifier(
        self, cr, uid, ids, field_name, arg, context=None
    ):
        res = {}
        notification_pool = self.pool['fatturapa.notification']
        for attachment in self.browse(cr, uid, ids, context=context):
            res[attachment.id] = notification_pool.get_file_identifier(
                attachment.datas_fname)
        return res

    def _get_meta_data(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for attachment in self.browse(cr, uid, ids, context=context):
            for notification in attachment.notification_ids:
                if notification.message_type == 'MT':
                    if attachment.id in res:
                        raise orm.except_orm(
                            _("Error"),
                            _("Too many MT notifications for fatturaPA %s") %
                            attachment.file_identifier)
                    res[attachment.id] = notification.id
        return res

    def _get_sdi_identifier(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for attachment in self.browse(cr, uid, ids, context=context):
            if attachment.meta_data_notification_id:
                pass

    _columns = {
        'notification_ids': fields.one2many(
            'fatturapa.notification', 'fatturapa_in_attachment_id',
            "Notifications"),
        'file_identifier': fields.function(
            _get_file_identifier, type="char", size=512,
            string="File identifier", store=True),
        'meta_data_notification_id': fields.function(
            _get_meta_data, type='many2one', relation='fatturapa.notification',
            string="Meta data file"),
        'sdi_identifier': fields.function(
            _get_sdi_identifier, type="char", size=512,
            string="SDI identifier"),
        }
