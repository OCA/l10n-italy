import base64
import os
import shutil
import zipfile
from datetime import datetime

from odoo import fields, models

from odoo.addons.l10n_it_fatturapa_in.wizard import efattura


class FatturaPAAttachmentImportZIP(models.Model):
    _name = "fatturapa.attachment.import.zip"
    _description = "E-bill ZIP import"
    _inherits = {"ir.attachment": "ir_attachment_id"}
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    ir_attachment_id = fields.Many2one(
        "ir.attachment", "Attachment", required=True, ondelete="cascade"
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("done", "Completed"),
        ],
        string="State",
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
    invoices_out_count = fields.Integer(
        string="Invoices Out Count", compute="_compute_invoices_data", readonly=True
    )
    invoices_in_count = fields.Integer(
        string="Invoices In Count", compute="_compute_invoices_data", readonly=True
    )
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
        tmp_dir_name = "/tmp/{}_{}".format(
            self.env.cr.dbname, datetime.now().timestamp()
        )
        if os.path.isdir(tmp_dir_name):
            shutil.rmtree(tmp_dir_name)
        os.mkdir(tmp_dir_name)
        zip_data = base64.b64decode(self.datas)
        zip_file_path = "%s/e_bills_to_import.zip" % tmp_dir_name
        with open(zip_file_path, "wb") as writer:
            writer.write(zip_data)
        tmp_dir_name_xml = tmp_dir_name + "/XML"
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(tmp_dir_name_xml)
        for xml_filename in os.listdir(tmp_dir_name_xml):
            with open("{}/{}".format(tmp_dir_name_xml, xml_filename), "rb") as reader:
                content = reader.read()
            attach_vals = {
                "name": xml_filename,
                "datas": base64.encodebytes(content),
            }
            att_in = self.env["fatturapa.attachment.in"].create(attach_vals)
            if att_in.xml_supplier_id.id == self.env.company.partner_id.id:
                att_in.unlink()
                attach_vals["state"] = "validated"
                att_out = self.env["fatturapa.attachment.out"].create(attach_vals)
                wizard = (
                    self.env["wizard.import.fatturapa"]
                    .with_context(
                        active_ids=[att_out.id], active_model="fatturapa.attachment.out"
                    )
                    .create({})
                )
                wizard.importFatturaPA(invoice_type="sale")
                att_out.attachment_import_zip_id = self.id
            else:
                in_invoice_registration_date = (
                    self.env.company.in_invoice_registration_date
                )
                # we don't have the received date
                self.env.company.in_invoice_registration_date = "inv_date"
                att_in.attachment_import_zip_id = self.id
                wizard = (
                    self.env["wizard.import.fatturapa"]
                    .with_context(
                        active_ids=[att_in.id], active_model="fatturapa.attachment.in"
                    )
                    .create({})
                )
                wizard.importFatturaPA()
                att_in.attachment_import_zip_id = self.id
                self.env.company.in_invoice_registration_date = (
                    in_invoice_registration_date
                )
        if os.path.isdir(tmp_dir_name):
            shutil.rmtree(tmp_dir_name)
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

    def get_invoice_obj(self, fatturapa_attachment):
        xml_string = fatturapa_attachment.get_xml_string()
        return efattura.CreateFromDocument(xml_string)
