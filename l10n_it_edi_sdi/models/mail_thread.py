# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import logging
import re

from lxml import etree

from odoo import api, models

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
METADATI_REGEX = re.compile(
    r"(IT[a-zA-Z0-9]{11,16}|"
    r"(?!IT)[A-Z]{2}[a-zA-Z0-9]{2,28})"
    r"_[a-zA-Z0-9]{1,5}"
    r"_MT_[a-zA-Z0-9]{,3}"
)

NOTIFICATION_TYPE_MAP = {
    "NS": "notificaScarto",
    "RC": "ricevutaConsegna",
    "MC": "notificaMancataConsegna",
    "NE": "notificaEsito",
    "DT": "notificaDecorrenzaTermini",
    # AT (attestazioneTrasmissione) is not mapped here because
    # l10n_it_edi's state_map does not handle it yet.
}


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.model
    def _l10n_it_edi_sdi_process_incoming_invoices(
        self, message, fatturapa_attachments, company
    ):
        """Process incoming electronic invoices received from SdI.

        :param message: the raw email message
        :param fatturapa_attachments: list of attachment objects matching
            the e-invoice filename pattern
        :param company: the res.company to create invoices for
        """
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

            # Parse the XML and populate the move fields
            move._extend_with_attachments(move.l10n_it_edi_attachment_id, new=True)

        _logger.info(
            "Processed incoming FatturaPA with Message-Id: %s",
            message.get("Message-Id"),
        )
        return []

    @api.model
    def _l10n_it_edi_sdi_process_notifications(
        self, message, response_attachments, company=None
    ):
        """Process SDI notifications (RC, NS, MC, NE, DT).

        :param message: the raw email message
        :param response_attachments: list of attachment objects matching
            the notification filename pattern
        :param company: optional res.company to scope the move search
        """
        for att in response_attachments:
            content = att.content
            if isinstance(content, str):
                content = content.encode()
            filename = att.fname

            # Skip ZIP files
            if filename.lower().endswith(".zip"):
                continue

            # Find the original move from the notification XML
            move = self._l10n_it_edi_sdi_find_move_from_notification(
                content, company=company
            )
            if not move:
                _logger.warning("Could not find move for notification %s", filename)
                continue

            # Extract notification type from filename and map to sdi_state
            notification_type = self._l10n_it_edi_sdi_get_type_from_filename(filename)
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
            "Processed SDI notification with Message-Id: %s",
            message.get("Message-Id"),
        )
        return []

    @api.model
    def _l10n_it_edi_sdi_find_move_from_notification(self, xml_content, company=None):
        """Find the account.move related to a notification XML.

        Parses the XML to find <NomeFile>, then searches for the
        corresponding attachment linked to a move.
        """
        try:
            root = etree.fromstring(xml_content)
            nome_file_elem = root.find(".//NomeFile")
            if nome_file_elem is not None and nome_file_elem.text:
                return self._l10n_it_edi_sdi_find_move_by_attachment_name(
                    nome_file_elem.text, company=company
                )
        except etree.XMLSyntaxError:
            _logger.warning("Failed to parse notification XML", exc_info=True)
        return self.env["account.move"]

    @api.model
    def _l10n_it_edi_sdi_find_move_by_attachment_name(self, filename, company=None):
        """Find the account.move whose e-invoice attachment has the given name.

        :param filename: the attachment name to search for
        :param company: optional res.company to scope the search
        """
        domain = [
            ("name", "=", filename),
            ("res_model", "=", "account.move"),
            ("res_field", "=", "l10n_it_edi_attachment_file"),
        ]
        if company:
            domain.append(("company_id", "=", company.id))
        attachment = self.env["ir.attachment"].search(domain, limit=1)
        if attachment and attachment.res_id:
            return self.env["account.move"].browse(attachment.res_id)
        return self.env["account.move"]

    @api.model
    def _l10n_it_edi_sdi_get_type_from_filename(self, filename):
        """Extract the notification type code from a filename.

        SdI notification filenames follow the pattern:
        IT01234567890_12345_XX_001.xml where XX is the type code
        (NS, RC, MC, NE, DT, AT, MT).
        """
        parts = filename.replace(".xml", "").replace(".XML", "").split("_")
        if len(parts) >= 3:
            return parts[2].upper()
        return ""
