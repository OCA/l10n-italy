# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2014-2015 Agile Business Group http://www.agilebg.com
#    @authors
#       Alessio Gerace <alessio.gerace@gmail.com>
#       Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#       Roberto Onnis <roberto.onnis@innoviu.com>
#
#   About license see __openerp__.py
#
##############################################################################

from odoo import models, fields, api


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    def _get_def_server(self):
        res = self.env['fetchmail.server'].search([
            ('user_ids', 'in', self.env.uid),
            ('pec', '=', True),
        ])
        return res and res.id or False

    in_server_id = fields.Many2one(
        'fetchmail.server', 'Server', default=_get_def_server)

    @api.multi
    def send_mail(self, auto_commit=False):
        """ Override of send_mail to duplicate attachments linked to the
        email.template.
            Indeed, basic mail.compose.message wizard duplicates attachments
            in mass
            mailing mode. But in 'single post' mode, attachments of an
            email template
            also have to be duplicated to avoid changing their ownership. """
        self.ensure_one()
        if self.env.context.get('new_pec_mail'):

            if not self.record_name:
                self.record_name = self.subject
            self.email_from = self.in_server_id.user
            res = super(MailComposeMessage, self.with_context(
                new_pec_server_id=self.in_server_id.id
            )).send_mail(
                auto_commit=auto_commit)
            return res
        return super(MailComposeMessage, self).send_mail(
            auto_commit=auto_commit)

    @api.model
    def default_get(self, fields):
        res = super(MailComposeMessage, self).default_get(fields)
        if self.env.context.get('new_pec_mail'):
            if res.get('in_server_id'):
                server = self.env['fetchmail.server'].browse(
                    res['in_server_id'])
                res['email_from'] = server.user
                res['reply_to'] = server.user
        return res
