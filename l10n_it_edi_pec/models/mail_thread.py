# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2025 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import re

from lxml import etree

from odoo import _, api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

FATTURAPA_IN_REGEX = re.compile(
    r"^(IT[a-zA-Z0-9]{11,16}|"
    r"(?!IT)[A-Z]{2}[a-zA-Z0-9]{2,28})"
    r"_[a-zA-Z0-9]{1,5}"
    r"\.(xml|XML|Xml|zip|ZIP|Zip|p7m|P7M|P7m)"
    r"(\.(p7m|P7M|P7m))?$"
)

RESPONSE_MAIL_REGEX = re.compile(
    r"(IT[a-zA-Z0-9]{11,16}|"
    r"(?!IT)[A-Z]{2}[a-zA-Z0-9]{2,28})"
    r"_[a-zA-Z0-9]{1,5}"
    r"_[A-Z]{2}_[a-zA-Z0-9]{,3}"
)

NOTIFICATION_TYPE_MAP = {
    "NS": "notificaScarto",
    "RC": "ricevutaConsegna",
    "MC": "notificaMancataConsegna",
    "NE": "notificaEsito",
    "DT": "notificaDecorrenzaTermini",
    "AT": "attestazioneTrasmissione",
}


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.model
    def message_route(
        self, message, message_dict, model=None, thread_id=None, custom_values=None
    ):
        # Check if the email comes from the SDI PEC system
        if any(
            "@pec.fatturapa.it" in x
            for x in [
                message.get("Reply-To", ""),
                message.get("From", ""),
                message.get("Return-Path", ""),
            ]
        ):
            _logger.info(
                "Processing FatturaPA PEC with Message-Id: %s",
                message.get("Message-Id"),
            )
            attachments = message_dict.get("attachments", [])
            fatturapa_attachments = [
                x for x in attachments if FATTURAPA_IN_REGEX.match(x.fname)
            ]
            response_attachments = [
                x for x in attachments if RESPONSE_MAIL_REGEX.match(x.fname)
            ]
            if fatturapa_attachments:
                return self._l10n_it_edi_pec_process_incoming_invoices(
                    message, message_dict, fatturapa_attachments
                )
            if response_attachments:
                return self._l10n_it_edi_pec_process_notifications(
                    message, message_dict, response_attachments
                )
            _logger.warning(
                "SDI PEC email with no matching attachments: %s",
                message_dict.get("subject"),
            )
            return []

        # Check if this is a PEC delivery receipt (CONSEGNA/ACCETTAZIONE)
        # from a PEC server that is configured for e-invoicing
        fetchmail_server_id = self._context.get("fetchmail_server_id")
        if fetchmail_server_id:
            fetchmail_server = self.env["fetchmail.server"].browse(fetchmail_server_id)
            if fetchmail_server.is_l10n_it_edi_pec:
                move = self._l10n_it_edi_pec_find_move_by_subject(
                    message_dict.get("subject", "")
                )
                if move:
                    return self._l10n_it_edi_pec_process_delivery_receipt(
                        move, message_dict
                    )
                raise UserError(
                    _(
                        'PEC message "%(subject)s" has been read '
                        "but not processed, as not related to an "
                        "e-invoice.\n"
                        "Please check PEC mailbox %(fetchmail_name)s, "
                        "at server %(fetchmail_server)s, "
                        "with user %(fetchmail_user)s.",
                        subject=message_dict.get("subject"),
                        fetchmail_name=fetchmail_server.name,
                        fetchmail_server=fetchmail_server.server,
                        fetchmail_user=fetchmail_server.user,
                    )
                )

        return super().message_route(
            message,
            message_dict,
            model=model,
            thread_id=thread_id,
            custom_values=custom_values,
        )

    @api.model
    def _l10n_it_edi_pec_process_incoming_invoices(
        self, message, message_dict, fatturapa_attachments
    ):
        """Process incoming electronic invoices received from SdI via PEC."""
        company = self._l10n_it_edi_pec_get_company()
        AccountMove = self.env["account.move"]

        for att in fatturapa_attachments:
            content = att.content
            if isinstance(content, str):
                content = content.encode()
            filename = att.fname

            # Check for duplicates
            existing = (
                self.env["ir.attachment"]
                .sudo()
                .search_count(
                    [
                        ("name", "=", filename),
                        ("res_model", "=", "account.move"),
                        ("res_field", "=", "l10n_it_edi_attachment_file"),
                        ("company_id", "=", company.id),
                    ],
                    limit=1,
                )
            )
            if existing:
                _logger.info("Invoice %s already exists, skipping", filename)
                continue

            # Create empty move and attachment
            move = AccountMove.with_company(company).create({})
            attachment = (
                self.env["ir.attachment"]
                .sudo()
                .with_company(company)
                .create(
                    {
                        "name": filename,
                        "raw": content,
                        "type": "binary",
                        "res_model": "account.move",
                        "res_id": move.id,
                        "res_field": "l10n_it_edi_attachment_file",
                    }
                )
            )
            move.with_context(
                account_predictive_bills_disable_prediction=True,
                no_new_invoice=True,
            ).message_post(attachment_ids=attachment.ids)

            # Validate XML before parsing (for .xml files only;
            # .p7m signed files are unwrapped by _extend_with_attachments)
            if filename.lower().endswith(".xml"):
                try:
                    etree.fromstring(content)
                except etree.XMLSyntaxError as e:
                    raise UserError(
                        _(
                            "Cannot parse e-invoice XML %(filename)s: %(error)s",
                            filename=filename,
                            error=e,
                        )
                    ) from e

            # Parse the XML and populate the move fields
            move.invalidate_recordset(
                fnames=["l10n_it_edi_attachment_id", "l10n_it_edi_attachment_file"]
            )
            move._extend_with_attachments(move.l10n_it_edi_attachment_id, new=True)

        _logger.info(
            "Processed incoming FatturaPA PEC with Message-Id: %s",
            message.get("Message-Id"),
        )
        return []

    @api.model
    def _l10n_it_edi_pec_process_notifications(
        self, message, message_dict, response_attachments
    ):
        """Process SDI notifications (RC, NS, MC, NE, DT, AT) via PEC."""
        for att in response_attachments:
            content = att.content
            if isinstance(content, str):
                content = content.encode()
            filename = att.fname

            # Skip ZIP files
            if filename.lower().endswith(".zip"):
                continue

            # Find the original move from the notification XML
            move = self._l10n_it_edi_pec_find_move_from_notification(content)
            if not move:
                _logger.warning("Could not find move for notification %s", filename)
                continue

            # Extract notification type from filename and map to sdi_state
            notification_type = self._l10n_it_edi_pec_get_type_from_filename(filename)
            sdi_state = NOTIFICATION_TYPE_MAP.get(notification_type)
            if not sdi_state:
                _logger.warning(
                    "Unknown notification type %s in %s",
                    notification_type,
                    filename,
                )
                continue

            # Process through core notification chain
            notification = {"state": sdi_state, "xml_content": content}
            parsed = move._l10n_it_edi_parse_notification(notification)
            transformed = move._l10n_it_edi_transform_notification(parsed)
            msg = move._l10n_it_edi_get_message(transformed)
            move._l10n_it_edi_write_send_state(transformed, msg)

        _logger.info(
            "Processed SDI notification PEC with Message-Id: %s",
            message.get("Message-Id"),
        )
        return []

    @api.model
    def _l10n_it_edi_pec_process_delivery_receipt(self, move, message_dict):
        """Process a PEC delivery/acceptance receipt (CONSEGNA/ACCETTAZIONE).

        These are from the PEC provider confirming email delivery,
        not from SdI. They are informational only (no state change).
        """
        move.with_context(no_new_invoice=True).sudo().message_post(
            body=message_dict.get("body", ""),
            subject=message_dict.get("subject", ""),
        )
        return []

    @api.model
    def _l10n_it_edi_pec_find_move_from_notification(self, xml_content):
        """Find the account.move related to a notification XML.

        Parses the XML to find <NomeFile>, then searches for the
        corresponding attachment linked to a move.
        """
        try:
            root = etree.fromstring(xml_content)
            nome_file_elem = root.find(".//NomeFile")
            if nome_file_elem is not None and nome_file_elem.text:
                original_filename = nome_file_elem.text
                # Handle .p7m signed files
                unsigned_filename = original_filename.replace(".p7m", "")
                attachment = (
                    self.env["ir.attachment"]
                    .sudo()
                    .search(
                        [
                            (
                                "name",
                                "in",
                                [original_filename, unsigned_filename],
                            ),
                            ("res_model", "=", "account.move"),
                            ("res_field", "=", "l10n_it_edi_attachment_file"),
                        ],
                        limit=1,
                    )
                )
                if attachment and attachment.res_id:
                    return self.env["account.move"].browse(attachment.res_id)
        except etree.XMLSyntaxError:
            _logger.warning("Failed to parse notification XML", exc_info=True)
        return self.env["account.move"]

    @api.model
    def _l10n_it_edi_pec_find_move_by_subject(self, subject):
        """Find a move from a PEC delivery receipt subject.

        PEC delivery receipts have subjects like:
        - "CONSEGNA: IT01234567890_12345.xml"
        - "ACCETTAZIONE: IT01234567890_12345.xml"
        """
        for prefix in ("CONSEGNA: ", "ACCETTAZIONE: "):
            if prefix in subject:
                filename = subject.replace(prefix, "").strip()
                attachment = (
                    self.env["ir.attachment"]
                    .sudo()
                    .search(
                        [
                            ("name", "=", filename),
                            ("res_model", "=", "account.move"),
                            ("res_field", "=", "l10n_it_edi_attachment_file"),
                        ],
                        limit=1,
                    )
                )
                if attachment and attachment.res_id:
                    return self.env["account.move"].browse(attachment.res_id)
        return self.env["account.move"]

    @api.model
    def _l10n_it_edi_pec_get_type_from_filename(self, filename):
        """Extract the notification type code from a filename.

        SdI notification filenames follow the pattern:
        IT01234567890_12345_XX_001.xml where XX is the type code
        (NS, RC, MC, NE, DT, AT, MT).
        """
        try:
            parts = filename.replace(".xml", "").replace(".XML", "").split("_")
            if len(parts) >= 3:
                return parts[2].upper()
        except Exception:
            _logger.debug("Failed to parse notification type from %s", filename)
        return ""

    @api.model
    def _l10n_it_edi_pec_get_company(self):
        """Get the company associated with the current PEC fetchmail server."""
        fetchmail_server_id = self._context.get("fetchmail_server_id")
        if fetchmail_server_id:
            companies = self.env["res.company"].search(
                [
                    ("l10n_it_edi_pec_fetch_server_id", "=", fetchmail_server_id),
                ],
                limit=1,
            )
            if companies:
                return companies
        return self.env.company
