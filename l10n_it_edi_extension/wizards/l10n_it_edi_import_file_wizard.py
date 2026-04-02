# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import io
import logging
import os
import zipfile

from odoo import fields, models
from odoo.exceptions import UserError
from odoo.fields import Domain
from odoo.tools import html_escape

_logger = logging.getLogger(__name__)


class EInvoiceImportFileWizard(models.TransientModel):
    _name = "l10n_it_edi.import_file_wizard"
    _description = "E-invoice Import Files Wizard"

    l10n_it_edi_attachment = fields.Binary()
    l10n_it_edi_attachment_filename = fields.Char()

    def action_import(self):
        self.ensure_one()
        company = self.env.company
        zip_binary = base64.b64decode(self.l10n_it_edi_attachment)
        zip_io = io.BytesIO(zip_binary)
        moves = self.env["account.move"]
        skipped_files = []

        with zipfile.ZipFile(zip_io, "r") as zip_ref:
            for member in zip_ref.infolist():
                if not member.is_dir():
                    with zip_ref.open(member) as file:
                        filename = os.path.basename(member.filename)
                        attachment_model = (
                            self.env["ir.attachment"].sudo().with_company(company)
                        )
                        existing_attachment = attachment_model.search_count(
                            [
                                ("name", "=", filename),
                                ("res_model", "=", "account.move"),
                                ("res_field", "=", "l10n_it_edi_attachment_file"),
                                ("company_id", "=", company.id),
                            ],
                            limit=1,
                        )

                        if existing_attachment:
                            message = self.env._(
                                "E-invoice already exists: %s", filename
                            )
                            _logger.warning(message)
                            raise UserError(message)

                        content = file.read()
                        attachment = attachment_model.create(
                            {
                                "name": filename,
                                "raw": content,
                                "type": "binary",
                            }
                        )
                        files_data = self.env["account.move"]._to_files_data(attachment)
                        files_data = [
                            file_data
                            for file_data in files_data
                            if self.env["account.move"]._is_l10n_it_edi_import_file(
                                file_data
                            )
                        ]

                        if not files_data:
                            _logger.info(f"Skipping {filename}, not an XML/P7M file")
                            skipped_files.append(filename)
                            attachment.unlink()
                            continue

                        files_data.extend(
                            self.env["account.move"]._unwrap_attachments(files_data)
                        )

                        records = (
                            self.env["account.move"]
                            .with_company(company)
                            .create([{}] * len(files_data))
                        )
                        for record, file_data in zip(records, files_data, strict=False):
                            attachment = file_data["attachment"]
                            record.message_post(
                                body=self.env._(
                                    "This invoice was imported from .zip file"
                                ),
                                attachment_ids=attachment.ids,
                            )

                        # Extend created moves with the related attachments.
                        for record, file_data in zip(records, files_data, strict=False):
                            record._extend_with_attachments([file_data], new=True)
                            if record.is_sale_document():
                                record.l10n_it_edi_attachment_name = file_data.get(
                                    "name", ""
                                )
                                record.l10n_it_edi_attachment_file = base64.b64encode(
                                    file_data.get("raw", b"")
                                )

                        moves |= records
        action = {
            "name": self.env._("E-invoices"),
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "list,form",
            "views": [[False, "list"], [False, "form"]],
            "domain": Domain("id", "in", moves.ids),
        }
        if skipped_files:
            skipped_list_html = "".join(
                f"<li>{html_escape(f)}</li>" for f in skipped_files
            )
            skipped_info_html = self.env._(
                "The following files were skipped (not valid XML/P7M):<ul>%s</ul>",
                skipped_list_html,
            )
            # Create activity for the current user
            self.env["mail.activity"].create(
                {
                    "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,
                    "note": skipped_info_html,
                    "summary": self.env._("Partial import: skipped files"),
                    "user_id": self.env.uid,
                    "res_id": self.env.user.partner_id.id,
                    "res_model_id": self.env["ir.model"]._get_id("res.partner"),
                }
            )
        return action
