# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from datetime import datetime

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)

MAX_POP_MESSAGES = 50


class Fetchmail(orm.Model):
    _inherit = 'fetchmail.server'

    _columns = {
        'last_pec_error_message': fields.text(
            'Last PEC error message', readonly=True),
    }

    def fetch_mail(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for server in self.browse(cr, uid, ids, context=context):
            if not server.is_fatturapa_pec:
                super(Fetchmail, server).fetch_mail(
                    cr, uid, ids, context=context)
            else:
                mail_thread = self.pool.get('mail.thread')
                _logger.info('start checking for new emails on %s server %s',
                             server.type, server.name)
                context.update({
                        'fetchmail_server_id': server.id,
                        'server_type': server.type,
                        'fetchmail_cron_running': True,
                        })
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
                                mail_thread.message_process(
                                    cr, uid, server.object_id.model,
                                    data[0][1],
                                    save_original=server.original,
                                    strip_attachments=(not server.attach),
                                    context=context)
                                # if message is processed without exceptions
                                server.write({'last_pec_error_message': ''})
                            except Exception as e:
                                _logger.info(
                                    'Failed to process mail from %s server %s.'
                                    ' Resetting server status',
                                    server.type, server.name, exc_info=True)
                                # Here is where we need to intervene.
                                # Setting to draft prevents new e-invoices to
                                # be sent via PEC
                                server.write({
                                        'state': 'draft',
                                        'last_pec_error_message': str(e),
                                    })
                                break
                            imap_server.store(num, '+FLAGS', '\\Seen')
                            # We need to commit because message is processed:
                            # Possible next exceptions, out of try, should not
                            # rollback processed messages
                            cr.commit()
                    except Exception as e:
                        _logger.info(
                            "General failure when trying to fetch mail from %s"
                            " server %s.",
                            server.type, server.name, exc_info=True)
                        server.write({
                                'state': 'draft',
                                'last_pec_error_message': str(e),
                            })
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
                            for num in range(1, min(
                                    MAX_POP_MESSAGES, num_messages) + 1):
                                (header, messages, octets) = pop_server.retr(
                                    num)
                                message = '\n'.join(messages)
                                try:
                                    mail_thread.message_process(
                                        cr, uid, server.object_id.model,
                                        message,
                                        save_original=server.original,
                                        strip_attachments=(not server.attach),
                                        context=context)
                                    pop_server.dele(num)
                                    # See the comments in the IMAP part
                                    server.write(
                                        {'last_pec_error_message': ''})
                                    server.last_pec_error_message = ''
                                except Exception as e:
                                    _logger.info(
                                        'Failed to process mail from %s server'
                                        ' %s. Resetting server status',
                                        server.type, server.name, exc_info=True
                                    )
                                    # See the comments in the IMAP part
                                    server.write({
                                        'state': 'draft',
                                        'last_pec_error_message': str(e),
                                    })
                                    break
                                cr.commit()
                            if num_messages < MAX_POP_MESSAGES:
                                break
                            pop_server.quit()
                    except Exception as e:
                        _logger.info(
                            "General failure when trying to fetch mail from %s"
                            " server %s.",
                            server.type, server.name, exc_info=True)
                        # See the comments in the IMAP part
                        server.write({
                            'state': 'draft',
                            'last_pec_error_message': str(e),
                        })
                    finally:
                        if pop_server:
                            pop_server.quit()
            server.write({'date': datetime.now().strftime(
                DEFAULT_SERVER_DATETIME_FORMAT)})
        return True
