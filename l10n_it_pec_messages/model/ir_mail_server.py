# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class IrMailServer(models.Model):

    _inherit = "ir.mail_server"

    in_server_id = fields.Many2one(
        'fetchmail.server',
        string='Incoming PEC server',
        domain="[('pec', '=', True)]")

    pec = fields.Boolean(
        "Pec Server",
        help="Check if this server is PEC")

    _sql_constraints = [
        ('incomingserver_name_unique', 'unique(in_server_id)',
         'Incoming Server already in use'),
        ]

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if self._context.get('avoid_pec_server'):
            args.append(('pec', '=', False))
        return super(IrMailServer, self).search(
            args=args, offset=offset, limit=limit, order=order, count=count)

    @api.model
    def send_email(
        self, message, mail_server_id=None, smtp_server=None, smtp_port=None,
        smtp_user=None, smtp_password=None, smtp_encryption=None,
        smtp_debug=False
    ):
        if not mail_server_id:
            # if not explicit SMTP, prevent to use PEC server
            return super(IrMailServer, self.with_context(
                avoid_pec_server=True
            )).send_email(
                message=message, mail_server_id=mail_server_id,
                smtp_server=smtp_server, smtp_port=smtp_port,
                smtp_user=smtp_user, smtp_password=smtp_password,
                smtp_encryption=smtp_encryption,
                smtp_debug=smtp_debug)
        else:
            res = super(IrMailServer, self).send_email(
                message=message, mail_server_id=mail_server_id,
                smtp_server=smtp_server, smtp_port=smtp_port,
                smtp_user=smtp_user, smtp_password=smtp_password,
                smtp_encryption=smtp_encryption,
                smtp_debug=smtp_debug)
            return res
