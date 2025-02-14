# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import io
import logging
import os
import zipfile

from odoo import fields, models
from odoo.exceptions import UserError

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
                            attachment.unlink()
                            continue

                        for file_data in attachment._decode_edi_l10n_it_edi(
                            filename, content
                        ):
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

        return {
            "view_type": "form",
            "name": "E-invoices",
            "view_mode": "list,form",
            "res_model": "account.move",
            "type": "ir.actions.act_window",
            "domain": [("id", "in", moves.ids)],
        }
