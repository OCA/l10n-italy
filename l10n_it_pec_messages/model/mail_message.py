# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Associazione Odoo Italia
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
##############################################################################

from openerp.osv import fields, orm


class mail_message(orm.Model):
    _inherit = "mail.message"

    _columns = {
        'pec': fields.many2one(
            'fetchmail.server', 'Server Pec', readonly=True),
        'pec_type': fields.selection([
            ('completa', 'Pec Mail'),
            ('accettazione', 'Reception'),
            ('avvenuta-consegna', 'Delivery'),
            ], 'Pec Type', readonly=True),
        'cert_datetime': fields.datetime(
            'Certified Date and Time ', readonly=True),
        'pec_msg_id': fields.char(
            'PEC-Message-Id',
            help='Message unique identifier', select=1, readonly=True),
        'ref_msg_id': fields.char(
            'ref-Message-Id',
            help='Ref Message unique identifier', select=1, readonly=True),
        'delivery_message_id': fields.many2one(
            'mail.message', 'Delivery Message', readonly=True),
        'reception_message_id': fields.many2one(
            'mail.message', 'Reception Message', readonly=True),
    }

    def _search(
        self, cr, uid, args, offset=0, limit=None, order=None,
        context=None, count=False, access_rights_uid=None
    ):
        res = super(mail_message, self)._search(
            cr, uid, args, offset=0, limit=None, order=None,
            context=None, count=False, access_rights_uid=None)
        return res
