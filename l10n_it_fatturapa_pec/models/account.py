# -*- coding: utf-8 -*-
# Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
# Copyright © 2018 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from openerp import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    fatturapa_state = fields.Selection(
        [('ready', 'Ready to Send'),
         ('sent', 'Sent'),
         ('delivered', 'Delivered'),
         ('error', 'Error')],
        string='E-invoice State',
        compute='_compute_fatturapa_state',
        store='true',
    )

    @api.multi
    @api.depends('fatturapa_attachment_out_id.state')
    def _compute_fatturapa_state(self):
        mapping = {
            'ready': 'ready',
            'sent': 'sent',
            'validated': 'delivered',
            'sender_error': 'error',
            'recipient_error': 'error',
            'rejected': 'error'
        }
        for record in self:
            record.fatturapa_state = \
                mapping.get(record.fatturapa_attachment_out_id.state)
