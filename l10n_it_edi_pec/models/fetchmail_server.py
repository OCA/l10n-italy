# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2025 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from imaplib import IMAP4

from markupsafe import Markup, escape

from odoo import _, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

MAX_POP_MESSAGES = 50


class FetchmailServer(models.Model):
    _inherit = "fetchmail.server"

    is_l10n_it_edi_pec = fields.Boolean(string="E-invoice PEC server")
    last_pec_error_message = fields.Text(
        string="Last PEC Error Message",
        readonly=True,
    )
    pec_error_count = fields.Integer(
        string="PEC error count",
        readonly=True,
    )
    e_inv_notify_partner_ids = fields.Many2many(
        "res.partner",
        string="Contacts to notify",
        help="Contacts to notify when PEC message can't be processed",
        domain=[("email", "!=", False)],
        default=lambda self: [(6, 0, [self.env.user.partner_id.id])],
    )

    def _l10n_it_edi_pec_fetch_imap(self, error_messages, additional_context):
        """Fetch PEC emails via IMAP, leaving failed messages unread.

        Unlike the standard fetchmail IMAP loop which marks all messages
        as Seen regardless of outcome, this method only marks a message
        as Seen after successful processing.  Failed messages remain
        unread so they can be manually reviewed in the PEC mailbox.
        """
        MailThread = self.env["mail.thread"]
        imap_server = None
        try:
            imap_server = self.connect()
            imap_server.select()
            result, data = imap_server.search(None, "(UNSEEN)")
            for num in data[0].split():
                result, data = imap_server.fetch(num, "(RFC822)")
                imap_server.store(num, "-FLAGS", "\\Seen")
                try:
                    MailThread.with_context(**additional_context).message_process(
                        self.object_id.model if self.object_id else False,
                        data[0][1],
                        save_original=self.original,
                        strip_attachments=(not self.attach),
                    )
                    self.last_pec_error_message = ""
                except Exception as e:
                    self._l10n_it_edi_pec_manage_failure(e, error_messages)
                    continue
                imap_server.store(num, "+FLAGS", "\\Seen")
                self._cr.commit()  # pylint: disable=invalid-commit
        except Exception as e:
            self._l10n_it_edi_pec_manage_failure(e, error_messages)
        finally:
            if imap_server:
                try:
                    imap_server.close()
                    imap_server.logout()
                except (OSError, IMAP4.abort):
                    _logger.warning(
                        "Failed to properly finish imap connection: %s.",
                        self.name,
                        exc_info=True,
                    )

    def _l10n_it_edi_pec_fetch_pop(self, error_messages, additional_context):
        """Fetch PEC emails via POP3 with per-message error handling."""
        MailThread = self.env["mail.thread"]
        pop_server = None
        try:
            while True:
                failed_in_loop = 0
                pop_server = self.connect()
                (num_messages, total_size) = pop_server.stat()
                pop_server.list()
                for num in range(1, min(MAX_POP_MESSAGES, num_messages) + 1):
                    (header, messages, octets) = pop_server.retr(num)
                    message = b"\n".join(messages)
                    try:
                        MailThread.with_context(**additional_context).message_process(
                            self.object_id.model if self.object_id else False,
                            message,
                            save_original=self.original,
                            strip_attachments=(not self.attach),
                        )
                        pop_server.dele(num)
                        self.last_pec_error_message = ""
                    except Exception as e:
                        self._l10n_it_edi_pec_manage_failure(e, error_messages)
                        failed_in_loop += 1
                        continue
                    self._cr.commit()  # pylint: disable=invalid-commit
                if num_messages < MAX_POP_MESSAGES or failed_in_loop == num:
                    break
                pop_server.quit()
        except Exception as e:
            self._l10n_it_edi_pec_manage_failure(e, error_messages)
        finally:
            if pop_server:
                try:
                    pop_server.quit()
                except OSError:
                    _logger.warning(
                        "Failed to properly finish pop connection: %s.",
                        self.name,
                        exc_info=True,
                    )

    def fetch_mail(self, raise_exception=True):
        """Override to add PEC-specific error tracking and auto-disable.

        PEC messages are legally relevant: if a message cannot be processed
        as an electronic invoice, it must NOT be marked as read (IMAP) or
        deleted (POP3) so it can be manually reviewed, and configured
        contacts are notified.

        After repeated failures the server is automatically disabled
        to prevent silent message loss.
        """
        for server in self:
            if not server.is_l10n_it_edi_pec:
                super(FetchmailServer, server).fetch_mail(
                    raise_exception=raise_exception
                )
                continue

            # Setting fetchmail_cron_running to avoid disabling the cron
            # while it is running (otherwise it would be done by setting
            # server.state = 'draft', see _update_cron method)
            additional_context = {
                "fetchmail_cron_running": True,
                "default_fetchmail_server_id": server.id,
            }
            server_ctx = server.with_context(**additional_context)
            _logger.info(
                "Start checking for new e-invoices on %s server %s",
                server.server_type,
                server.name,
            )
            error_messages = []
            if server.server_type == "imap":
                server_ctx._l10n_it_edi_pec_fetch_imap(
                    error_messages, additional_context
                )
            elif server.server_type == "pop":
                server_ctx._l10n_it_edi_pec_fetch_pop(
                    error_messages, additional_context
                )
            if error_messages:
                server_ctx._l10n_it_edi_pec_notify_or_log(error_messages)
                server_ctx.pec_error_count += 1
                max_retry = int(
                    self.env["ir.config_parameter"]
                    .sudo()
                    .get_param("fetchmail.pec.max.retry", default="5")
                )
                if server_ctx.pec_error_count > max_retry:
                    server_ctx.state = "draft"
                    server_ctx._l10n_it_edi_pec_notify_about_server_reset()
                if raise_exception:
                    raise ValidationError("\n".join(error_messages))
            else:
                server_ctx.pec_error_count = 0
            server_ctx.write({"date": fields.Datetime.now()})
        return True

    def _l10n_it_edi_pec_manage_failure(self, exception, error_messages):
        """Track a PEC processing failure."""
        self.ensure_one()
        _logger.info(
            "Failure when fetching emails using %s server %s.",
            self.server_type,
            self.name,
            exc_info=True,
        )
        exception_msg = str(exception)
        self.last_pec_error_message = exception_msg
        error_messages.append(exception_msg)

    def _l10n_it_edi_pec_notify_about_server_reset(self):
        """Notify partners that the PEC server has been disabled."""
        self.ensure_one()
        self._l10n_it_edi_pec_notify_or_log(
            _(
                "PEC server %(name)s has been reset. "
                "Last error message is '%(error_message)s'",
                name=self.name,
                error_message=self.last_pec_error_message,
            )
        )

    def _l10n_it_edi_pec_notify_or_log(self, message):
        """Send an email notification to configured partners, or log.

        :param message: list of str, or str
        """
        self.ensure_one()
        if isinstance(message, list):
            message = Markup("<br/>").join(escape(m) for m in message)
        if self.e_inv_notify_partner_ids:
            self.env["mail.mail"].create(
                {
                    "subject": _("Fetchmail PEC server [%s] error", self.name),
                    "body_html": message,
                    "recipient_ids": [(6, 0, self.e_inv_notify_partner_ids.ids)],
                }
            ).send()
            _logger.info(
                "Notifying partners %s about PEC server %s error",
                self.e_inv_notify_partner_ids.ids,
                self.name,
            )
        else:
            _logger.error(
                "Can't notify anyone about PEC server %s error: %s",
                self.name,
                message,
            )
