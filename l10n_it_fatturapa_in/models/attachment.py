#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models
from odoo.tools import format_date

from ..wizard import efattura

_logger = logging.getLogger(__name__)

SELF_INVOICE_TYPES = ("TD16", "TD17", "TD18", "TD19", "TD20", "TD21", "TD27", "TD28")


class FatturaPAAttachmentIn(models.Model):
    _inherit = "fatturapa.attachment"
    _name = "fatturapa.attachment.in"
    _description = "Electronic Invoice"

    in_invoice_ids = fields.One2many(
        "account.move",
        "fatturapa_attachment_in_id",
        string="In Bills",
        readonly=True,
    )
    xml_supplier_id = fields.Many2one(
        "res.partner", string="Supplier", compute="_compute_xml_data", store=True
    )
    invoices_number = fields.Integer(
        "Bills Number", compute="_compute_xml_data", store=True
    )
    invoices_total = fields.Float(
        "Bills Total",
        compute="_compute_xml_data",
        store=True,
        help="If specified by supplier, total amount of the document net of "
        "any discount and including tax charged to the buyer/ordered",
    )
    invoices_date = fields.Char(
        string="Invoices date", compute="_compute_xml_data", store=True
    )
    registered = fields.Boolean(compute="_compute_registered", store=True)

    e_invoice_received_date = fields.Datetime(string="E-Bill Received Date")

    e_invoice_validation_error = fields.Boolean(
        compute="_compute_e_invoice_validation_error"
    )

    e_invoice_validation_message = fields.Text(
        compute="_compute_e_invoice_validation_error"
    )

    e_invoice_parsing_error = fields.Text(
        compute="_compute_e_invoice_parsing_error",
        store=True,
    )

    is_self_invoice = fields.Boolean(
        "Contains self invoices", compute="_compute_is_self_invoice", store=True
    )

    inconsistencies = fields.Text(compute="_compute_xml_data", store=True)

    linked_invoice_id_xml = fields.Char(
        compute="_compute_linked_invoice_id_xml",
        store=True,
    )

    _sql_constraints = [
        (
            "ftpa_attachment_in_name_uniq",
            "unique(att_name)",
            "The name of the e-bill file must be unique!",
        )
    ]

    @api.depends("in_invoice_ids.e_invoice_validation_error")
    def _compute_e_invoice_validation_error(self):
        for att in self:
            att.e_invoice_validation_error = False
            att.e_invoice_validation_message = False
            bills_with_error = att.in_invoice_ids.filtered(
                lambda b: b.e_invoice_validation_error
            )
            if not bills_with_error:
                continue
            att.e_invoice_validation_error = True
            errors_message_template = "{bill}:\n{errors}"
            error_messages = list()
            for bill in bills_with_error:
                error_messages.append(
                    errors_message_template.format(
                        bill=bill.display_name, errors=bill.e_invoice_validation_message
                    )
                )
            att.e_invoice_validation_message = "\n\n".join(error_messages)

    def recompute_xml_fields(self):
        # Pretend the attachment has been modified
        # and trigger a recomputation:
        # this recomputes all fields whose value
        # is extracted from the attachment
        self.modified(["ir_attachment_id"])
        self.recompute()
        self._compute_registered()

    def get_invoice_obj(self):
        """
        Parse the invoice into a lxml.etree.ElementTree object.
        If the parsing goes wrong:
         - log the error
         - save the parsing error in field `e_invoice_parsing_error`
         - return `False`
        :rtype: lxml.etree.ElementTree or bool.
        """
        self.ensure_one()
        invoice_obj = False
        try:
            xml_string = self.get_xml_string()
            invoice_obj = efattura.CreateFromDocument(xml_string)
        except Exception as e:
            error_msg = _("Impossible to parse XML for {att_name}: {error_msg}").format(
                att_name=self.display_name,
                error_msg=e,
            )
            _logger.error(error_msg)
            self.e_invoice_parsing_error = error_msg
        else:
            self.e_invoice_parsing_error = False
        return invoice_obj

    @api.depends("ir_attachment_id.datas")
    def _compute_is_self_invoice(self):
        for att in self:
            att.is_self_invoice = False
            if not att.datas:
                return
            fatt = att.get_invoice_obj()
            if fatt:
                for invoice_body in fatt.FatturaElettronicaBody:
                    document_type = (
                        invoice_body.DatiGenerali.DatiGeneraliDocumento.TipoDocumento
                    )
                    if document_type in SELF_INVOICE_TYPES:
                        att.is_self_invoice = True
                        break

    @api.depends("ir_attachment_id.datas")
    def _compute_e_invoice_parsing_error(self):
        for att in self:
            if not att.datas:
                return
            att.get_invoice_obj()

    @api.depends("ir_attachment_id.datas")
    def _compute_xml_data(self):
        for att in self:
            att.xml_supplier_id = False
            att.invoices_number = False
            att.invoices_total = False
            att.invoices_date = False
            if not att.datas:
                return
            fatt = att.get_invoice_obj()
            if not fatt:
                # Set default values and carry on
                continue
            # Look into each invoice to compute the following values
            invoices_date = []
            for invoice_body in fatt.FatturaElettronicaBody:
                # Assign this directly so that rounding is applied each time
                att.invoices_total += float(
                    invoice_body.DatiGenerali.DatiGeneraliDocumento.ImportoTotaleDocumento
                    or 0
                )

                document_date = invoice_body.DatiGenerali.DatiGeneraliDocumento.Data
                invoice_date = format_date(
                    att.with_context(lang=att.env.user.lang).env,
                    fields.Date.from_string(document_date),
                )
                if invoice_date not in invoices_date:
                    invoices_date.append(invoice_date)

            att.update(
                dict(
                    invoices_date=" ".join(invoices_date),
                )
            )

            # We don't need to look into each invoice
            # for the following fields
            att.invoices_number = len(fatt.FatturaElettronicaBody)

            # Partner creation that may happen in `getCedPrest`
            # triggers a recomputation
            # that messes up the cache of some fields if they are set
            # (more properly, put in cache) afterwards;
            # this happens for `is_self_invoice` for instance.
            # That is why we set it as the last field.
            cedentePrestatore = fatt.FatturaElettronicaHeader.CedentePrestatore
            wiz_obj = self.env["wizard.import.fatturapa"].with_context(
                from_attachment=att
            )
            partner_id = wiz_obj.getCedPrest(cedentePrestatore)
            att.xml_supplier_id = partner_id
            inconsistencies = wiz_obj.env.context.get("inconsistencies", False)
            att.inconsistencies = inconsistencies

    @api.depends("in_invoice_ids")
    def _compute_registered(self):
        for att in self:
            if att.in_invoice_ids and len(att.in_invoice_ids) == att.invoices_number:
                att.registered = True
            else:
                att.registered = False

    def extract_attachments(self, AttachmentsData, invoice_id):
        AttachModel = self.env["fatturapa.attachments"]
        for attach in AttachmentsData:
            if not attach.NomeAttachment:
                name = _("Attachment without name")
            else:
                name = attach.NomeAttachment
            content = attach.Attachment.encode()
            _attach_dict = {
                "name": name,
                "datas": content,
                "description": attach.DescrizioneAttachment or "",
                "compression": attach.AlgoritmoCompressione or "",
                "format": attach.FormatoAttachment or "",
                "invoice_id": invoice_id,
            }
            AttachModel.create(_attach_dict)

    @api.depends("ir_attachment_id.datas")
    def _compute_linked_invoice_id_xml(self):
        for att in self:
            att.linked_invoice_id_xml = ""
            if not att.datas:
                return
            if isinstance(att.id, int):
                att.linked_invoice_id_xml = ""
                fatt = att.get_invoice_obj()
                if fatt:
                    for invoice_body in fatt.FatturaElettronicaBody:
                        if (
                            invoice_body.DatiGenerali.DatiFattureCollegate
                            and len(invoice_body.DatiGenerali.DatiFattureCollegate) == 1
                        ):
                            att.linked_invoice_id_xml = (
                                invoice_body.DatiGenerali.DatiFattureCollegate[
                                    0
                                ].IdDocumento
                            )
