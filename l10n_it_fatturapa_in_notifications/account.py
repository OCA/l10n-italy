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
from openerp.tools.translate import _
import netsvc


class AccountInvoice(orm.Model):
    _inherit = "account.invoice"
    _columns = {
        'result_notification_id': fields.many2one(
            'fatturapa.notification', "Result notification", readonly=True),
        'rejected': fields.boolean('Rejected')
        }

    _defaults = {
        'rejected': False
    }

    def action_cancel_draft(self, cr, uid, ids, *args):
        if not hasattr(ids, '__iter__'):
            ids = [ids]
        for inv_id in ids:
            invoice = self.browse(cr, uid, inv_id)
            if invoice.rejected:
                raise orm.except_orm(
                    _('Attention'),
                    _('It is not possible to activate a rejected invoice')
                )
        return super(
            AccountInvoice, self).action_cancel_draft(
                cr, uid, ids, *args)

    def action_cancel_reject(self, cr, uid, ids, context=None):
        wf_service = netsvc.LocalService("workflow")
        for inv_id in ids:
            self.write(cr, uid, inv_id, {'rejected': True}, context=context)
            wf_service.trg_validate(
                uid, 'account.invoice', inv_id, 'invoice_cancel', cr
            )
        return True
