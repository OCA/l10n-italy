# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2025 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import email
import io
import logging
import zipfile
from datetime import timedelta, timezone
from imaplib import IMAP4

from markupsafe import Markup, escape

from odoo import _, fields, models
from odoo.exceptions import UserError, ValidationError

from .mail_thread import fatturapa_regex, get_attachment_filename

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

    @staticmethod
    def _format_imap_date(date):
        """Format a date for the IMAP SEARCH command.

        Do not rely on the locale, because IMAP always expects
        English month abbreviations.
        """
        return "%02d-%s-%04d" % (date.day, IMAP_MONTHS[date.month - 1], date.year)

    def _get_e_invoice_file_names(self, attachment):
        """Return the e-invoice names contained in an attachment."""
        file_name = get_attachment_filename(attachment)
        if file_name.lower().endswith(".zip"):
            content = attachment.content
            if isinstance(content, str):
                content = content.encode()
            try:
                with zipfile.ZipFile(io.BytesIO(content)) as zip_file:
                    file_names = []
                    for name in zip_file.namelist():
                        inner_name = name.replace("\\", "/").rsplit("/", 1)[-1]
                        inner_name = inner_name.strip().strip('"')
                        if fatturapa_regex.match(inner_name):
                            file_names.append(inner_name)
                if file_names:
                    return file_names
            except (zipfile.BadZipFile, OSError):
                _logger.warning(
                    "Unable to read ZIP attachment %s", file_name, exc_info=True
                )
        return [file_name]

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
        """Return the company linked to this PEC server.

        The search is done using all the companies enabled for the user,
        so that the company can be found even when the server belongs to
        a company different from the current one.
        """
        self.ensure_one()
        company_ids = self.env.user.company_ids.ids or self.env.companies.ids
        company_model = self.env["res.company"].with_context(
            allowed_company_ids=company_ids
        )
        return company_model.search(
            [("l10n_it_edi_pec_fetch_server_id", "=", self.id)], limit=1
        )

    def _is_e_invoice_imported(self, file_name, company):
        """Return whether an e-invoice has already been imported."""
        return bool(
            self.env["ir.attachment"]
            .sudo()
            .search_count(
                [
                    ("name", "=", file_name),
                    ("company_id", "=", company.id),
                    ("res_model", "=", "account.move"),
                    ("res_field", "=", "l10n_it_edi_attachment_file"),
                ],
                limit=1,
            )
        )

    def _check_pec_message(self, raw_message, sdi_email, company):
        """Return the e-invoices found in a single PEC message.

        Each e-invoice is marked with ``is_einvoice_xml_found``,
        depending on whether it is already present as an e-invoice
        attachment for the given company.
        """
        message = email.message_from_bytes(raw_message, policy=email.policy.SMTP)
        mail_thread = self.env["mail.thread"]
        if not mail_thread._is_pec_message(message, sdi_email):
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
        for attachment in fatturapa_attachments:
            for file_name in self._get_e_invoice_file_names(attachment):
                found_e_invoices.append(
                    {
                        "message_id": message_dict.get("message_id"),
                        "subject": message_dict.get("subject"),
                        "date": message_dict.get("date"),
                        "email_from": message_dict.get("email_from"),
                        "file_name": file_name,
                        "is_einvoice_xml_found": self._is_e_invoice_imported(
                            file_name, company
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
            imap_server.select(readonly=True)
            since = self._format_imap_date(datetime_from.date())
            before = self._format_imap_date(datetime_to.date() + timedelta(days=1))
            _result, data = imap_server.search(
                None, '(SINCE "%s" BEFORE "%s")' % (since, before)
            )
            if not data or not data[0]:
                return messages
            for num in data[0].split():
                try:
                    _result, msg_data = imap_server.fetch(num, "(BODY.PEEK[])")
                except Exception:
                    _logger.warning(
                        "Unable to fetch PEC message %s from IMAP server %s",
                        num,
                        self.name,
                        exc_info=True,
                    )
                    continue
                raw_message = self._get_raw_message_from_imap_data(msg_data)
                if not raw_message:
                    continue
                try:
                    message = email.message_from_bytes(
                        raw_message, policy=email.policy.SMTP
                    )
                except Exception:
                    _logger.warning(
                        "Unable to parse PEC message %s from IMAP server %s",
                        num,
                        self.name,
                        exc_info=True,
                    )
                    messages.append(raw_message)
                    continue
                message_date = self._get_message_datetime(message)
                if message_date and not (datetime_from <= message_date <= datetime_to):
                    continue
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
        """Check that all e-invoices received through this PEC server
        in the given period have been imported.

        The PEC mailbox is the source of truth: every incoming e-invoice
        found in the mailbox is returned, and the e-invoice attachment
        is only used to set the ``is_einvoice_xml_found`` flag.
        No Odoo attachment is checked if it does not correspond to a
        PEC message present in the mailbox.

        Note that POP servers usually delete messages after fetching them,
        so only messages still available on the server can be checked.

        :param datetime_from: start of the period (included)
        :param datetime_to: end of the period (included)
        :return: list of dictionaries, one for each e-invoice found,
            with the ``is_einvoice_xml_found`` flag
        """
        self.ensure_one()
        if not self.is_l10n_it_edi_pec:
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
        sdi_email = company.l10n_it_edi_pec_email_exchange_system
        if not sdi_email:
            raise UserError(
                _(
                    "Please configure the SdI email address on the company "
                    "linked to PEC server %s"
                )
                % self.name
            )
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
            found_e_invoices.extend(
                self._check_pec_message(raw_message, sdi_email, company)
            )
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
        if not self.is_l10n_it_edi_pec:
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

    def _import_pec_messages(self, datetime_from, datetime_to, message_ids):
        """Import the selected PEC messages, creating the related e-bills.

        The messages are searched again in the mailbox, because their content
        is not stored by the check wizard.
        """
        self.ensure_one()
        message_ids = set(message_ids)
        company = self._get_pec_company()
        if not company:
            raise UserError(
                _(
                    "No company is linked to PEC server %s, "
                    "so the destination company cannot be determined."
                )
                % self.name
            )
        if company not in self.env.user.company_ids:
            raise UserError(
                _(
                    "You are not allowed to access company %s "
                    "linked to PEC server %s."
                )
                % (company.display_name, self.name)
            )
        raw_messages = {}
        for raw_message in self._get_pec_messages(datetime_from, datetime_to):
            message = email.message_from_bytes(raw_message, policy=email.policy.SMTP)
            message_id = (message.get("Message-Id") or "").strip()
            if message_id in message_ids:
                raw_messages[message_id] = raw_message
        missing_message_ids = message_ids - set(raw_messages)
        if missing_message_ids:
            raise UserError(
                _(
                    "The following PEC messages are no longer available "
                    "on the server: %s"
                )
                % ", ".join(sorted(missing_message_ids))
            )
        mail_thread = self.env["mail.thread"].with_company(company)
        for message_id in sorted(raw_messages):
            mail_thread.with_context(
                default_fetchmail_server_id=self.id
            ).message_process(
                self.object_id.model if self.object_id else False,
                raw_messages[message_id],
                save_original=self.original,
                strip_attachments=(not self.attach),
            )
        return True

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
