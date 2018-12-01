# -*- coding: utf-8 -*-
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import logging
from odoo import models, api, fields

_logger = logging.getLogger(__name__)
MAX_POP_MESSAGES = 50


class Fetchmail(models.Model):
    _inherit = 'fetchmail.server'
    last_pec_error_message = fields.Text(
        "Last PEC Error Message", readonly=True)

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
                                # Setting to draft prevents new e-invoices to
                                # be sent via PEC
                                server.state = 'draft'
                                server.last_pec_error_message = str(e)
                                break
                            imap_server.store(num, '+FLAGS', '\\Seen')
                            # We need to commit because message is processed:
                            # Possible next exceptions, out of try, should not
                            # rollback processed messages
                            self._cr.commit()
                    except Exception as e:
                        _logger.info(
                            "General failure when trying to fetch mail from "
                            "%s server %s.",
                            server.type, server.name, exc_info=True)
                        server.state = 'draft'
                        server.last_pec_error_message = str(e)
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
                                    server.state = 'draft'
                                    server.last_pec_error_message = str(e)
                                    break
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
                        server.state = 'draft'
                        server.last_pec_error_message = str(e)
                    finally:
                        if pop_server:
                            pop_server.quit()
            server.write({'date': fields.Datetime.now()})
        return True
