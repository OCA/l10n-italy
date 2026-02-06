# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2025 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, fields, models, tools

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
    )

    def fetch_mail(self):
        """Override to add PEC-specific error tracking and auto-disable."""
        for server in self:
            if not server.is_l10n_it_edi_pec:
                super(FetchmailServer, server).fetch_mail()
                continue

            additional_context = {
                "fetchmail_cron_running": True,
                "fetchmail_server_id": server.id,
                "server_type": server.server_type,
            }
            server = server.with_context(**additional_context)
            MailThread = self.env["mail.thread"]
            _logger.info(
                "Start checking for new e-invoices on %s server %s",
                server.server_type,
                server.name,
            )
            error_messages = []
            if server.server_type == "imap":
                server._l10n_it_edi_pec_fetch_imap(
                    MailThread, error_messages, additional_context
                )
            elif server.server_type == "pop":
                server._l10n_it_edi_pec_fetch_pop(
                    MailThread, error_messages, additional_context
                )
            if error_messages:
                server._l10n_it_edi_pec_notify_or_log(error_messages)
                server.pec_error_count += 1
                max_retry = int(
                    self.env["ir.config_parameter"]
                    .sudo()
                    .get_param("fetchmail.pec.max.retry", default="5")
                )
                if server.pec_error_count > max_retry:
                    server.state = "draft"
                    server._l10n_it_edi_pec_notify_about_server_reset()
            else:
                server.pec_error_count = 0
            server.write({"date": fields.Datetime.now()})
        return True

    def _l10n_it_edi_pec_fetch_imap(
        self, MailThread, error_messages, additional_context
    ):
        """Fetch PEC emails via IMAP with per-message error handling."""
        connection = None
        try:
            connection = self.connect()
            connection.select()
            result, data = connection.search(None, "(UNSEEN)")
            for num in data[0].split():
                result, data = connection.fetch(num, "(RFC822)")
                connection.store(num, "-FLAGS", "\\Seen")
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
                connection.store(num, "+FLAGS", "\\Seen")
                if not tools.config["test_enable"]:
                    self._cr.commit()  # pylint: disable=invalid-commit
        except Exception as e:
            self._l10n_it_edi_pec_manage_failure(e, error_messages)
        finally:
            if connection:
                try:
                    connection.close()
                    connection.logout()
                except Exception:
                    _logger.debug("Failed to close IMAP connection", exc_info=True)

    def _l10n_it_edi_pec_fetch_pop(
        self, MailThread, error_messages, additional_context
    ):
        """Fetch PEC emails via POP3 with per-message error handling."""
        pop_server = None
        try:
            while True:
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
                        continue
                    if not tools.config["test_enable"]:
                        self._cr.commit()  # pylint: disable=invalid-commit
                if num_messages < MAX_POP_MESSAGES:
                    break
                pop_server.quit()
        except Exception as e:
            self._l10n_it_edi_pec_manage_failure(e, error_messages)
        finally:
            if pop_server:
                try:
                    pop_server.quit()
                except Exception:
                    _logger.debug("Failed to close POP3 connection", exc_info=True)

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
        odoo_exc_string = getattr(exception, "name", None)
        if odoo_exc_string:
            exception_msg = odoo_exc_string
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
            message = "<br/>".join(message)
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
