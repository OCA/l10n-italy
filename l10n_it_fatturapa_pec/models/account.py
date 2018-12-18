# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _

class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    def _get_fatturapa_state(self, cr, uid, ids, name, args, context=None):
        mapping = {
            'ready': 'ready',
            'sent': 'sent',
            'validated': 'delivered',
            'sender_error': 'error',
            'recipient_error': 'error',
            'rejected': 'error'
        }
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = mapping.get(
                record.fatturapa_attachment_out_id.state)
        return res


    def _get_account_invoice_ids_by_fatturapa_attachment_out_ids(
        self, cr, uid, ids, context=None):
        res = {}
        attachments = self.pool.get('fatturapa.attachment.out').browse(
            cr, uid, ids, context=context)
        for attachment in attachments:
            for invoice in attachment.out_invoice_ids:
                res[invoice.id] = True
        return res.keys()

    _columns = {
        'fatturapa_state': fields.function(
            _get_fatturapa_state, type='selection', string='E-invoice State',
            selection=[
                ('ready', 'Ready to Send'),
                ('sent', 'Sent'),
                ('delivered', 'Delivered'),
                ('error', 'Error'),
            ],
            store = {
                'fatturapa.attachment.out':
                    (_get_account_invoice_ids_by_fatturapa_attachment_out_ids,
                     ['state'], 10),
            })
    }

