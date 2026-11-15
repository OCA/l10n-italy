# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>

import email
import logging
from datetime import timedelta, timezone

from odoo import _, fields, models
from odoo.exceptions import UserError

from .mail_thread import get_attachment_filename

_logger = logging.getLogger(__name__)
MAX_POP_MESSAGES = 50
IMAP_MONTHS = (
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)


class Fetchmail(models.Model):
    _inherit = "fetchmail.server"

    is_fatturapa_pec = fields.Boolean("E-invoice PEC server")

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

    @staticmethod
    def _format_imap_date(date):
        """Format a date for the IMAP SEARCH command.

        Do not rely on the locale, because IMAP always expects
        English month abbreviations.
        """
        return "%02d-%s-%04d" % (date.day, IMAP_MONTHS[date.month - 1], date.year)

    @staticmethod
    def _get_message_datetime(message):
        """Return the message date as a naive UTC datetime."""
        message_date = message.get("Date")
        if not message_date:
            return False
        try:
            parsed_date = email.utils.parsedate_to_datetime(message_date)
        except (TypeError, ValueError, IndexError, OverflowError):
            return False
        if parsed_date.tzinfo:
            parsed_date = parsed_date.astimezone(timezone.utc).replace(tzinfo=None)
        return parsed_date

    def _get_pec_company(self):
        """Return the company of the SdI channel linked to this PEC server.

        The search is done using all the companies enabled for the user,
        so that the channel can be found even when the server belongs to
        a company different from the current one.
        """
        self.ensure_one()
        company_ids = self.env.user.company_ids.ids or self.env.companies.ids
        sdi_channel_model = self.env["sdi.channel"].with_context(
            allowed_company_ids=company_ids
        )
        sdi_channel = sdi_channel_model.search(
            [("fetch_pec_server_id", "=", self.id)], limit=1
        )
        return sdi_channel.company_id

    def _check_pec_message(self, raw_message, company):
        """Return the e-invoices found in a single PEC message.

        Each e-invoice is marked with ``is_einvoice_xml_found``,
        depending on whether it is already present as
        ``fatturapa.attachment.in`` for the given company.
        """
        message = email.message_from_bytes(raw_message, policy=email.policy.SMTP)
        mail_thread = self.env["mail.thread"]
        if not mail_thread._is_pec_message(message):
            # Not a message coming from SdI
            return []
        message_dict = mail_thread.message_parse(message)
        fatturapa_attachments, _response_attachments = mail_thread._get_pec_attachments(
            message_dict
        )
        if not fatturapa_attachments:
            # Not an incoming e-invoice (e.g. an SdI response or notification)
            return []
        found_e_invoices = []
        attachment_in_model = self.env["fatturapa.attachment.in"]
        for attachment in fatturapa_attachments:
            file_name = get_attachment_filename(attachment)
            domain = [
                ("name", "=", file_name),
                ("company_id", "=", company.id),
            ]
            found_e_invoices.append(
                {
                    "message_id": message_dict.get("message_id"),
                    "subject": message_dict.get("subject"),
                    "date": message_dict.get("date"),
                    "email_from": message_dict.get("email_from"),
                    "file_name": file_name,
                    "is_einvoice_xml_found": bool(
                        attachment_in_model.search_count(domain)
                    ),
                }
            )
        return found_e_invoices

    def _get_pec_connection(self):
        """Return a connection to the PEC server or raise a clear error."""
        self.ensure_one()
        try:
            connection = self.connect()
        except Exception as error:
            raise UserError(
                _("Unable to connect to PEC server %s: %s") % (self.name, error)
            ) from error
        if not connection:
            raise UserError(
                _(
                    "Unable to connect to PEC server %s. "
                    "Please check the server configuration."
                )
                % self.name
            )
        return connection

    @staticmethod
    def _get_raw_message_from_imap_data(msg_data):
        """Extract the message body from an IMAP FETCH response."""
        if not msg_data:
            return None
        for item in msg_data:
            if isinstance(item, tuple):
                values = [
                    bytes(value)
                    for value in item
                    if isinstance(value, (bytes, bytearray)) and value
                ]
                if values:
                    return max(values, key=len)
        values = [
            bytes(value)
            for value in msg_data
            if isinstance(value, (bytes, bytearray)) and value
        ]
        return max(values, key=len) if values else None

    def _get_pec_messages_imap(self, datetime_from, datetime_to):
        messages = []
        imap_server = None
        try:
            imap_server = self._get_pec_connection()
            status, _data = imap_server.select(readonly=True)
            if status != "OK":
                raise UserError(
                    _("Unable to select IMAP mailbox for PEC server %s") % self.name
                )
            since = self._format_imap_date(datetime_from.date())
            before = self._format_imap_date(datetime_to.date() + timedelta(days=1))
            status, data = imap_server.search(
                None, '(SINCE "%s" BEFORE "%s")' % (since, before)
            )
            if status != "OK":
                raise UserError(
                    _("Unable to search PEC messages on IMAP server %s") % self.name
                )
            if not data or not data[0]:
                return messages
            for num in data[0].split():
                try:
                    status, msg_data = imap_server.fetch(num, "(BODY.PEEK[])")
                except Exception as error:
                    raise UserError(
                        _(
                            "Unable to fetch PEC message %(num)s from IMAP "
                            "server %(server)s: %(error)s",
                            num=num,
                            server=self.name,
                            error=error,
                        )
                    ) from error
                if status != "OK":
                    raise UserError(
                        _(
                            "Unable to fetch PEC message %(num)s from IMAP "
                            "server %(server)s",
                            num=num,
                            server=self.name,
                        )
                    )
                raw_message = self._get_raw_message_from_imap_data(msg_data)
                if not raw_message:
                    raise UserError(
                        _(
                            "Empty PEC message %(num)s received from IMAP "
                            "server %(server)s",
                            num=num,
                            server=self.name,
                        )
                    )
                messages.append(raw_message)
        finally:
            if imap_server:
                imap_server.close()
                imap_server.logout()
        return messages

    def _get_pec_messages_pop(self, datetime_from, datetime_to):
        messages = []
        pop_server = None
        try:
            pop_server = self._get_pec_connection()
            num_messages, _total_size = pop_server.stat()
            for num in range(1, num_messages + 1):
                _header, lines, _octets = pop_server.retr(num)
                raw_message = b"\n".join(lines)
                try:
                    message = email.message_from_bytes(
                        raw_message, policy=email.policy.SMTP
                    )
                except Exception:
                    _logger.warning(
                        "Unable to parse PEC message %s from POP server %s",
                        num,
                        self.name,
                        exc_info=True,
                    )
                    messages.append(raw_message)
                    continue
                # POP has no server-side date search, so filter using the
                # message Date header.
                message_date = self._get_message_datetime(message)
                if message_date and not (datetime_from <= message_date <= datetime_to):
                    continue
                messages.append(raw_message)
        finally:
            if pop_server:
                pop_server.quit()
        return messages

    def _get_pec_messages(self, datetime_from, datetime_to):
        self.ensure_one()
        if self.server_type == "imap":
            return self._get_pec_messages_imap(datetime_from, datetime_to)
        if self.server_type == "pop":
            return self._get_pec_messages_pop(datetime_from, datetime_to)
        raise UserError(_("Server type %s is not supported") % self.server_type)

    def check_received_e_invoices(self, datetime_from, datetime_to):
        """Return the e-invoices received in the period, flagged as imported or not.

        POP servers may delete messages after fetching, so only messages
        still available on the server can be checked.
        """
        self.ensure_one()
        if not self.is_fatturapa_pec:
            raise UserError(
                _("Server %s is not configured as e-invoice PEC server") % self.name
            )
        datetime_from = fields.Datetime.to_datetime(datetime_from)
        datetime_to = fields.Datetime.to_datetime(datetime_to)
        if not datetime_from or not datetime_to:
            raise UserError(_("Both the start and end datetime are required"))
        if datetime_from > datetime_to:
            raise UserError(_("The start datetime cannot be after the end datetime"))
        company = self._get_pec_company()
        if not company:
            raise UserError(_("No company is linked to PEC server %s.") % self.name)
        if company not in self.env.user.company_ids:
            raise UserError(
                _(
                    "You are not allowed to access company %s "
                    "linked to PEC server %s."
                )
                % (company.display_name, self.name)
            )
        self = self.with_company(company)
        found_e_invoices = []
        for raw_message in self._get_pec_messages(datetime_from, datetime_to):
            found_e_invoices.extend(self._check_pec_message(raw_message, company))
        missing_e_invoices = [
            e_invoice
            for e_invoice in found_e_invoices
            if not e_invoice["is_einvoice_xml_found"]
        ]
        if missing_e_invoices:
            _logger.warning(
                "PEC server %s: %s of %s e-invoices received between %s and %s "
                "have not been imported: %s",
                self.name,
                len(missing_e_invoices),
                len(found_e_invoices),
                datetime_from,
                datetime_to,
                ", ".join(missing["file_name"] for missing in missing_e_invoices),
            )
        else:
            _logger.info(
                "PEC server %s: all %s e-invoices received between %s and %s "
                "have been imported",
                self.name,
                len(found_e_invoices),
                datetime_from,
                datetime_to,
            )
        return found_e_invoices

    def action_check_pec_e_invoices(self):
        """Open the wizard to check the e-invoices received via PEC."""
        self.ensure_one()
        if not self.is_fatturapa_pec:
            raise UserError(
                _("Server %s is not configured as e-invoice PEC server") % self.name
            )
        return {
            "type": "ir.actions.act_window",
            "name": _("Check received PEC e-invoices"),
            "res_model": "pec.e_invoice.check.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_fetchmail_server_id": self.id},
        }

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
