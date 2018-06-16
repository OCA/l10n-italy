# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

import logging

_logger = logging.getLogger(__name__)


class MailMessage(models.Model):
    _inherit = "mail.message"

    @api.multi
    def _compute_out_server(self):
        for msg in self:
            msg.out_server_id = False
            if msg.server_id:
                if msg.server_id.out_server_id:
                    msg.out_server_id = msg.server_id.out_server_id[0].id

    server_id = fields.Many2one(
        'fetchmail.server', 'Server Pec', readonly=True)
    out_server_id = fields.Many2one(
        'ir.mail_server', string='Related Outgoing Server',
        compute='_compute_out_server'
    )
    direction = fields.Selection([
        ('in', 'in'),
        ('out', 'out'),
        ], 'Mail direction', default='in', readonly=True)
    pec_type = fields.Selection([
        ('posta-certificata', 'Pec Mail'),
        ('accettazione', 'Reception'),
        ('non-accettazione', 'No Reception'),
        ('presa-in-carico', 'In Progress'),
        ('avvenuta-consegna', 'Delivery'),
        ('errore-consegna', 'Delivery Error'),
        ('preavviso-errore-consegna', 'Notice Delivery Error'),
        ('rilevazione-virus', 'Virus Detected'),
        ], 'Pec Type', readonly=True)
    pec_error = fields.Boolean('Reception Delivery Error', readonly=True)
    err_type = fields.Selection([
        ('nessuno', 'No Error'),
        ('no-dest', 'Recipient Adress Error'),
        ('no-dominio', 'Recipient domain Error'),
        ('virus', 'Virus Detected Error'),
        ('altro', 'Undefined Error'),
        ], 'Pec Error Type', readonly=True)
    cert_datetime = fields.Datetime(
        'Certified Date and Time ', readonly=True)
    pec_msg_id = fields.Char(
        'PEC-Message-Id',
        help='Message unique identifier', index=1, readonly=True)

    recipient_id = fields.Many2one(
        'res.partner', 'Recipient', readonly=True)
    recipient_addr = fields.Char(
        'Recipient Address', readonly=True)
    delivered_recipients = fields.Char("Delivered recipients", readonly=True)

    pec_msg_parent_id = fields.Many2one(
        'mail.message', 'Parent Message', readonly=True)
    pec_notifications_ids = fields.One2many(
        'mail.message', 'pec_msg_parent_id',
        'Related Notifications',  readonly=True)
