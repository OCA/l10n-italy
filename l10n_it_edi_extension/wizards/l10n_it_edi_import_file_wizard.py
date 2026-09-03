# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import io
import logging
import os
import zipfile

from odoo import fields, models
from odoo.exceptions import UserError
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
                            message = f"E-invoice already exists: {filename}"
                            _logger.warning(message)
                            raise UserError(self.env._(message))

                        content = file.read()
                        attachment = attachment_model.create(
                            {
                                "name": filename,
                                "raw": content,
                                "type": "binary",
                            }
                        )

                        if not attachment._is_l10n_it_edi_import_file():
                            _logger.info(f"Skipping {filename}, not an XML/P7M file")
                            skipped_files.append(filename)
                            attachment.unlink()
                            continue

                        # Since odoo@d1759c9, _decode_edi_l10n_it_edi returns
                        # one file data per attachment, so if the e-invoice
                        # contains multiple e-invoices, first its split
                        # then each single invoice content is decoded
                        split_contents = self.env[
                            "account.journal"
                        ]._l10n_it_edi_extension_split_content(attachment)
                        for split_content in split_contents:
                            file_datas = attachment._decode_edi_l10n_it_edi(
                                filename, split_content
                            )
                            for file_data in file_datas:
                                move = (
                                    self.env["account.move"]
                                    .with_company(company)
                                    .create({})
                                )
                                attachment.write(
                                    {
                                        "res_model": "account.move",
                                        "res_id": move.id,
                                        "res_field": "l10n_it_edi_attachment_file",
                                    }
                                )

                                move.with_context(
                                    account_predictive_bills_disable_prediction=True,
                                    no_new_invoice=True,
                                ).message_post(attachment_ids=attachment.ids)

                                move._l10n_it_edi_import_invoice(move, file_data, True)
                                moves |= move
        action = {
            "name": self.env._("E-invoices"),
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "list,form",
            "views": [[False, "list"], [False, "form"]],
            "domain": [("id", "in", moves.ids)],
        }
        if skipped_files:
            skipped_list_html = "".join(
                f"<li>{html_escape(f)}</li>" for f in skipped_files
            )
            skipped_info_html = (
                self.env._(
                    "The following files were skipped (not valid XML/P7M):<ul>%s</ul>"
                )
                % skipped_list_html
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
