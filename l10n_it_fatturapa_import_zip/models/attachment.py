#  Copyright 2023 Simone Rubino - TAKOBI
#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import logging
import tempfile
import zipfile
from io import BytesIO
from pathlib import Path

import lxml.etree as ET

from odoo import fields, models

from odoo.addons.l10n_it_fatturapa_in.wizard import efattura

_logger = logging.getLogger(__name__)


def _extract_zip_file(directory, datas):
    """Extract the zip file having content `datas` to `directory`."""
    zip_data = base64.b64decode(datas)
    with zipfile.ZipFile(BytesIO(zip_data)) as zip_ref:
        zip_ref.extractall(directory)


def _is_xml_file(file_path):
    """Check if the file at `file_path` is an XML file."""
    try:
        # Attempt to parse the file as XML
        parser = ET.XMLParser(recover=True)
        root = ET.XML(file_path.read_bytes(), parser)
        ET.tostring(root)
        return True  # Successfully parsed, it's an XML file
    except Exception:
        return False  # Failed to parse, not an XML file


def _has_p7m_extension(file_path):
    """Check if the file at `file_path` has a .p7m extension."""
    return file_path.suffix.lower() == ".p7m"


class FatturaPAAttachmentImportZIP(models.Model):
    _name = "fatturapa.attachment.import.zip"
    _description = "E-bill ZIP import"
    _inherits = {"ir.attachment": "ir_attachment_id"}
    _inherit = [
        "mail.thread",
        "mail.activity.mixin",
        "l10n_it_fatturapa.attachment.e_invoice.link",
    ]
    _order = "id desc"

    ir_attachment_id = fields.Many2one(
        "ir.attachment", "Attachment", required=True, ondelete="cascade"
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("done", "Completed"),
        ],
        default="draft",
        required=True,
        readonly=True,
    )
    messages = fields.Text(
        "Error Messages", readonly=True, compute="_compute_invoices_data"
    )
    xml_out_count = fields.Integer(
        string="XML Out Count", compute="_compute_invoices_data", readonly=True
    )
    xml_in_count = fields.Integer(
        string="XML In Count", compute="_compute_invoices_data", readonly=True
    )
    invoices_out_count = fields.Integer(compute="_compute_invoices_data", readonly=True)
    invoices_in_count = fields.Integer(compute="_compute_invoices_data", readonly=True)
    attachment_out_ids = fields.One2many(
        "fatturapa.attachment.out",
        "attachment_import_zip_id",
        string="Attachments Out",
        readonly=True,
    )
    attachment_in_ids = fields.One2many(
        "fatturapa.attachment.in",
        "attachment_import_zip_id",
        string="Attachments In",
        readonly=True,
    )
    invoice_out_ids = fields.One2many(
        "account.move", "attachment_out_import_zip_id", string="Invoices Out"
    )
    invoice_in_ids = fields.One2many(
        "account.move", "attachment_in_import_zip_id", string="Invoices In"
    )

    def action_view_xml(self):
        if self.env.context.get("xml_type") == "out_xml":
            attachments = self.mapped("attachment_out_ids")
            action = self.env.ref(
                "l10n_it_fatturapa_out.action_fatturapa_attachment"
            ).read()[0]
        elif self.env.context.get("xml_type") == "in_xml":
            attachments = self.mapped("attachment_in_ids")
            action = self.env.ref("l10n_it_fatturapa_in.action_fattura_pa_in").read()[0]
        else:
            return {"type": "ir.actions.act_window_close"}
        action["context"] = "{}"
        action["domain"] = [("id", "in", attachments.ids)]
        return action

    def action_view_invoices(self):
        if self.env.context.get("invoice_type") == "out_invoice":
            invoices = self.mapped("invoice_out_ids")
            action = self.env.ref("account.action_move_out_invoice_type").read()[0]
            context = {
                "default_move_type": "out_invoice",
            }
        elif self.env.context.get("invoice_type") == "in_invoice":
            invoices = self.mapped("invoice_in_ids")
            action = self.env.ref("account.action_move_in_invoice_type").read()[0]
            context = {
                "default_move_type": "in_invoice",
            }
        else:
            return {"type": "ir.actions.act_window_close"}
        action["context"] = context
        action["domain"] = [("id", "in", invoices.ids)]
        return action

    def _compute_invoices_data(self):
        for import_zip in self:
            import_zip.xml_out_count = len(import_zip.attachment_out_ids)
            import_zip.xml_in_count = len(import_zip.attachment_in_ids)
            import_zip.invoices_out_count = len(import_zip.invoice_out_ids)
            import_zip.invoices_in_count = len(import_zip.invoice_in_ids)
            import_zip.messages = "{}\n{}".format(
                "\n".join(
                    [
                        i
                        for i in import_zip.invoice_out_ids.mapped("inconsistencies")
                        if i
                    ]
                ),
                "\n".join(
                    [
                        i
                        for i in import_zip.invoice_in_ids.mapped("inconsistencies")
                        if i
                    ]
                ),
            )

    def action_import(self):
        self.ensure_one()
        company_partner = self.env.company.partner_id
        with tempfile.TemporaryDirectory() as tmp_dir_path:
            tmp_dir = Path(tmp_dir_path)
            _extract_zip_file(tmp_dir, self.datas)
            original_in_invoice_registration_date = (
                self.env.company.in_invoice_registration_date
            )
            # we don't have the received date
            self.env.company.in_invoice_registration_date = "inv_date"

            for xml_file in tmp_dir.rglob("*"):
                # Process only files skipping non-XML/P7M files
                if xml_file.is_file() and (
                    _is_xml_file(xml_file) or _has_p7m_extension(xml_file)
                ):
                    content = xml_file.read_bytes()
                    attach_vals = {
                        "name": xml_file.name,
                        "datas": base64.encodebytes(content),
                        "attachment_import_zip_id": self.id,
                    }
                    attachment = self.env["fatturapa.attachment.in"].create(attach_vals)
                    if attachment.xml_supplier_id == company_partner:
                        attachment.unlink()
                        attach_vals["state"] = "validated"
                        attachment = self.env["fatturapa.attachment.out"].create(
                            attach_vals
                        )
                    wizard = (
                        self.env["wizard.import.fatturapa"]
                        .with_context(
                            active_ids=attachment.ids,
                            active_model=attachment._name,
                        )
                        .create({})
                    )
                    _logger.info(f"Importing {xml_file}")
                    wizard.importFatturaPA()
                else:
                    _logger.info(f"Skipping {xml_file}, not an XML/P7M file")
            self.env.company.in_invoice_registration_date = (
                original_in_invoice_registration_date
            )

        self.state = "done"


class FatturaPAAttachmentIn(models.Model):
    _inherit = "fatturapa.attachment.in"

    attachment_import_zip_id = fields.Many2one(
        "fatturapa.attachment.import.zip",
        "E-bill ZIP import",
        readonly=True,
        ondelete="restrict",
    )


class FatturaPAAttachmentOut(models.Model):
    _inherit = "fatturapa.attachment.out"

    attachment_import_zip_id = fields.Many2one(
        "fatturapa.attachment.import.zip",
        "E-bill ZIP import",
        readonly=True,
        ondelete="restrict",
    )

    def get_invoice_obj(self):
        xml_string = self.get_xml_string()
        return efattura.CreateFromDocument(xml_string)
