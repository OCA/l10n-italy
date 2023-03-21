# -*- coding: utf-8 -*-
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import logging
from odoo import models, api, fields, _

_logger = logging.getLogger(__name__)
MAX_POP_MESSAGES = 50


class Fetchmail(models.Model):
    _inherit = 'fetchmail.server'

    def _default_e_inv_notify_partner_ids(self):
        return [(6, 0, [self.env.user.partner_id.id])]

    last_pec_error_message = fields.Text(
        "Last PEC Error Message", readonly=True)
    pec_error_count = fields.Integer("PEC error count", readonly=True)
    e_inv_notify_partner_ids = fields.Many2many(
        "res.partner", string="Contacts to notify",
        help="Contacts to notify when PEC message can't be processed",
        domain=[('email', '!=', False)],
        default=_default_e_inv_notify_partner_ids
    )

    @api.multi
    def fetch_mail(self):
        for server in self:
            if not server.is_fatturapa_pec:
                super(Fetchmail, server).fetch_mail()
            else:
                additional_context = {
                    'fetchmail_cron_running': True
                }
                # Setting fetchmail_cron_running to avoid to disable cron while
                # cron is running (otherwise it would be done by setting
                # server.state = 'draft',
                # see _update_cron method)
                server = server.with_context(**additional_context)
                MailThread = self.env['mail.thread']
                _logger.info(
                    'start checking for new e-invoices on %s server %s',
                    server.type, server.name)
                additional_context['fetchmail_server_id'] = server.id
                additional_context['server_type'] = server.type
                imap_server = None
                pop_server = None
                error_raised = False
                if server.type == 'imap':
                    try:
                        imap_server = server.connect()
                        imap_server.select()
                        result, data = imap_server.search(None, '(UNSEEN)')
                        for num in data[0].split():
                            result, data = imap_server.fetch(num, '(RFC822)')
                            imap_server.store(num, '-FLAGS', '\\Seen')
                            try:
                                MailThread.with_context(
                                    **additional_context
                                ).message_process(
                                    server.object_id.model, data[0][1],
                                    save_original=server.original,
                                    strip_attachments=(not server.attach)
                                )
                                # if message is processed without exceptions
                                server.last_pec_error_message = ''
                            except Exception as e:
                                _logger.info(
                                    'Failed to process mail from %s server '
                                    '%s. Resetting server status',
                                    server.type, server.name, exc_info=True
                                )
                                # Here is where we need to intervene.
                                server.last_pec_error_message = str(e)
                                error_raised = True
                                continue
                            imap_server.store(num, '+FLAGS', '\\Seen')
                            # We need to commit because message is processed:
                            # Possible next exceptions, out of try, should not
                            # rollback processed messages
                            self._cr.commit()  # pylint: disable=invalid-commit
                    except Exception as e:
                        _logger.info(
                            "General failure when trying to fetch mail from "
                            "%s server %s.",
                            server.type, server.name, exc_info=True)
                        server.last_pec_error_message = str(e)
                        error_raised = True
                    finally:
                        if imap_server:
                            imap_server.close()
                            imap_server.logout()
                elif server.type == 'pop':
                    try:
                        while True:
                            pop_server = server.connect()
                            (num_messages, total_size) = pop_server.stat()
                            pop_server.list()
                            for num in range(
                                    1, min(MAX_POP_MESSAGES, num_messages) + 1
                            ):
                                (header, messages, octets) = pop_server.retr(
                                    num)
                                message = '\n'.join(messages)
                                try:
                                    MailThread.with_context(
                                        **additional_context
                                    ).message_process(
                                        server.object_id.model, message,
                                        save_original=server.original,
                                        strip_attachments=(not server.attach)
                                    )
                                    pop_server.dele(num)
                                    # See the comments in the IMAP part
                                    server.last_pec_error_message = ''
                                except Exception as e:
                                    _logger.info(
                                        'Failed to process mail from %s server'
                                        '%s. Resetting server status',
                                        server.type, server.name, exc_info=True
                                    )
                                    # See the comments in the IMAP part
                                    error_raised = True
                                    server.last_pec_error_message = str(e)
                                    continue
                                # pylint: disable=invalid-commit
                                self._cr.commit()
                            if num_messages < MAX_POP_MESSAGES:
                                break
                            pop_server.quit()
                    except Exception as e:
                        _logger.info(
                            "General failure when trying to fetch mail from %s"
                            " server %s.",
                            server.type, server.name, exc_info=True)
                        # See the comments in the IMAP part
                        error_raised = True
                        server.last_pec_error_message = str(e)
                    finally:
                        if pop_server:
                            pop_server.quit()
                if error_raised:
                    server.pec_error_count += 1
                    max_retry = self.env['ir.config_parameter'].get_param(
                        'fetchmail.pec.max.retry')
                    if server.pec_error_count > int(max_retry):
                        # Setting to draft prevents new e-invoices to
                        # be sent via PEC.
                        # Resetting server state only after N fails.
                        # So that the system can try to fetch again after
                        # temporary connection errors
                        server.state = 'draft'
                        server.notify_about_server_reset()
                else:
                    server.pec_error_count = 0
            server.write({'date': fields.Datetime.now()})
        return True

    def notify_about_server_reset(self):
        if self.e_inv_notify_partner_ids:
            self.env['mail.mail'].create({
                'subject': _(
                    "Fetchmail PEC server [%s] reset"
                ) % self.name,
                'body_html': _(
                    "<p>"
                    "PEC server %s has been reset. Last error message is</p>"
                    "<p><strong>%s</strong></p>"
                ) % (self.name, self.last_pec_error_message),
                'recipient_ids': [(
                    6, 0,
                    self.e_inv_notify_partner_ids.ids
                )]
            })
            _logger.info(
                'Notifying partners %s about PEC server %s reset'
                % (self.e_inv_notify_partner_ids.ids, self.name)
            )
        else:
            _logger.error(
                "Can't notify anyone about PEC server %s reset" % self.name)
