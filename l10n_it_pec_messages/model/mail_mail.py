# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models, api


class MailMail(models.Model):
    _inherit = "mail.mail"

    @api.model
    def create(self, values):
        """
        when sending a new PEC message,
        use the linked SMTP server and SMTP user
        """
        if self.env.context.get('new_pec_server_id'):
            values['auto_delete'] = False
        mail = super(MailMail, self).create(values)
        if self.env.context.get('new_pec_server_id'):
            in_server_id = self.env.context.get(
                'new_pec_server_id'
            )
            server_pool = self.env['ir.mail_server']
            server_ids = server_pool.search(
                [('in_server_id', '=', in_server_id)])
            if server_ids:
                server = server_ids[0]
                mail.write({
                    'email_from': server.smtp_user,
                    'mail_server_id': server.id,
                    'server_id': in_server_id,
                    'out_server_id': server.id,
                    'pec_type': 'posta-certificata',
                    'direction': 'out'
                })
                mail.mail_message_id.email_from = server.smtp_user
        return mail

    @api.multi
    def send(self, auto_commit=False, raise_exception=False):
        config_parameter = self.env['ir.config_parameter'].sudo()
        bounce_alias = config_parameter.get_param("mail.bounce.alias")
        catchall_domain = config_parameter.get_param("mail.catchall.domain")
        catchall_alias = config_parameter.get_param("mail.catchall.alias")

        for mail in self:
            is_pec = mail.exists() and mail.mail_server_id.pec
            if is_pec:
                # temporary disable email parameters incompatible with PEC
                if bounce_alias:
                    config_parameter.set_param('mail.bounce.alias', False)
                if catchall_domain:
                    config_parameter.set_param('mail.catchall.domain', False)
                if catchall_alias:
                    config_parameter.set_param('mail.catchall.alias', False)

            super(MailMail, mail).send(
                auto_commit=auto_commit, raise_exception=raise_exception)

            if is_pec:
                if bounce_alias:
                    config_parameter.set_param(
                        'mail.bounce.alias', bounce_alias)
                if catchall_domain:
                    config_parameter.set_param(
                        'mail.catchall.domain', catchall_domain)
                if catchall_alias:
                    config_parameter.set_param(
                        'mail.catchall.alias', catchall_alias)
        return True
