# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>

import logging

from odoo import _, fields, models

_logger = logging.getLogger(__name__)
MAX_POP_MESSAGES = 50


class Fetchmail(models.Model):
    _inherit = "fetchmail.server"

    def _default_e_inv_notify_partner_ids(self):
        return [(6, 0, [self.env.user.partner_id.id])]

    last_pec_error_message = fields.Text("Last PEC Error Message", readonly=True)
    pec_error_count = fields.Integer("PEC error count", readonly=True)
    e_inv_notify_partner_ids = fields.Many2many(
        "res.partner",
        string="Contacts to notify",
        help="Contacts to notify when PEC message can't be processed",
        domain=[("email", "!=", False)],
        default=_default_e_inv_notify_partner_ids,
    )

    def fetch_mail_server_type_imap(
        self, server, MailThread, error_messages, **additional_context
    ):
        imap_server = None
        try:
            imap_server = server.connect()
            imap_server.select()
            result, data = imap_server.search(None, "(UNSEEN)")
            for num in data[0].split():
                result, data = imap_server.fetch(num, "(RFC822)")
                imap_server.store(num, "-FLAGS", "\\Seen")
                try:
                    MailThread.with_context(**additional_context).message_process(
                        server.object_id.model,
                        data[0][1],
                        save_original=server.original,
                        strip_attachments=(not server.attach),
                    )
                    # if message is processed without exceptions
                    server.last_pec_error_message = ""
                except Exception as e:
                    server.manage_pec_failure(e, error_messages)
                    continue
                imap_server.store(num, "+FLAGS", "\\Seen")
                # We need to commit because message is processed:
                # Possible next exceptions, out of try, should not
                # rollback processed messages
                self._cr.commit()  # pylint: disable=invalid-commit
        except Exception as e:
            server.manage_pec_failure(e, error_messages)
        finally:
            if imap_server:
                imap_server.close()
                imap_server.logout()

    def fetch_mail_server_type_pop(
        self, server, MailThread, error_messages, **additional_context
    ):
        pop_server = None
        try:
            while True:
                pop_server = server.connect()
                (num_messages, total_size) = pop_server.stat()
                pop_server.list()
                for num in range(1, min(MAX_POP_MESSAGES, num_messages) + 1):
                    (header, messages, octets) = pop_server.retr(num)
                    message = "\n".join(messages)
                    try:
                        MailThread.with_context(**additional_context).message_process(
                            server.object_id.model,
                            message,
                            save_original=server.original,
                            strip_attachments=(not server.attach),
                        )
                        pop_server.dele(num)
                        # See the comments in the IMAP part
                        server.last_pec_error_message = ""
                    except Exception as e:
                        server.manage_pec_failure(e, error_messages)
                        continue
                    # pylint: disable=invalid-commit
                    self._cr.commit()
                if num_messages < MAX_POP_MESSAGES:
                    break
                pop_server.quit()
        except Exception as e:
            server.manage_pec_failure(e, error_messages)
        finally:
            if pop_server:
                pop_server.quit()

    def fetch_mail(self):
        for server in self:
            if not server.is_fatturapa_pec:
                super(Fetchmail, server).fetch_mail()
            else:
                additional_context = {"fetchmail_cron_running": True}
                # Setting fetchmail_cron_running to avoid to disable cron while
                # cron is running (otherwise it would be done by setting
                # server.state = 'draft',
                # see _update_cron method)
                server = server.with_context(**additional_context)
                MailThread = self.env["mail.thread"]
                _logger.info(
                    "start checking for new e-invoices on %s server %s",
                    server.server_type,
                    server.name,
                )
                additional_context["fetchmail_server_id"] = server.id
                additional_context["server_type"] = server.server_type
                error_messages = list()
                if server.server_type == "imap":
                    server.fetch_mail_server_type_imap(
                        server, MailThread, error_messages, **additional_context
                    )
                elif server.server_type == "pop":
                    server.fetch_mail_server_type_pop(
                        server, MailThread, error_messages, **additional_context
                    )
                if error_messages:
                    server.notify_or_log(error_messages)
                    server.pec_error_count += 1
                    max_retry = self.env["ir.config_parameter"].get_param(
                        "fetchmail.pec.max.retry"
                    )
                    if server.pec_error_count > int(max_retry):
                        # Setting to draft prevents new e-invoices to
                        # be sent via PEC.
                        # Resetting server state only after N fails.
                        # So that the system can try to fetch again after
                        # temporary connection errors
                        server.state = "draft"
                        server.notify_about_server_reset()
                else:
                    server.pec_error_count = 0
            server.write({"date": fields.Datetime.now()})
        return True

    def manage_pec_failure(self, exception, error_messages):
        self.ensure_one()
        _logger.info(
            "Failure when fetching emails "
            "using {serv_type} server {serv_name}.".format(
                serv_type=self.server_type, serv_name=self.name
            ),
            exc_info=True,
        )

        exception_msg = str(exception)
        # `str` on Odoo exceptions does not return
        # a nice representation of the error
        odoo_exc_string = getattr(exception, "name", None)
        if odoo_exc_string:
            exception_msg = odoo_exc_string

        self.last_pec_error_message = exception_msg
        error_messages.append(exception_msg)
        return True

    def notify_about_server_reset(self):
        self.ensure_one()
        self.notify_or_log(
            _("PEC server %s has been reset. Last error message is '%s'")
            % (self.name, self.last_pec_error_message)
        )

    def notify_or_log(self, message):
        """
        Send an email to partners in
        self.e_inv_notify_partner_ids containing message.

        :param: message
        :type message: list of str, or str
        """
        self.ensure_one()
        if isinstance(message, list):
            message = "<br/>".join(message)

        if self.e_inv_notify_partner_ids:
            self.env["mail.mail"].create(
                {
                    "subject": _("Fetchmail PEC server [%s] error") % self.name,
                    "body_html": message,
                    "recipient_ids": [(6, 0, self.e_inv_notify_partner_ids.ids)],
                }
            ).send()
            _logger.info(
                "Notifying partners %s about PEC server %s error"
                % (self.e_inv_notify_partner_ids.ids, self.name)
            )
        else:
            _logger.error("Can't notify anyone about PEC server %s error" % self.name)
