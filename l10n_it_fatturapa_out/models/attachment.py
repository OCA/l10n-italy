# Copyright 2014 Davide Corio
# Copyright 2016-2018 Lorenzo Battistini - Agile Business Group

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class FatturaPAAttachment(models.Model):
    _name = "fatturapa.attachment.out"
    _description = "E-invoice Export File"
    _inherits = {"ir.attachment": "ir_attachment_id"}
    _inherit = ["mail.thread"]
    _order = "id desc"

    ir_attachment_id = fields.Many2one(
        "ir.attachment", "Attachment", required=True, ondelete="cascade"
    )
    att_name = fields.Char(
        string="E-invoice file name", related="ir_attachment_id.name", store=True
    )
    out_invoice_ids = fields.One2many(
        "account.move",
        "fatturapa_attachment_out_id",
        string="Out Invoices",
        readonly=True,
    )
    has_pdf_invoice_print = fields.Boolean(
        help="True if all the invoices have a printed "
        "report attached in the XML, False otherwise.",
        compute="_compute_has_pdf_invoice_print",
        store=True,
    )
    invoice_partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        store=True,
        compute="_compute_invoice_partner_id",
    )
    state = fields.Selection(
        selection=[
            ("ready", "Ready to Send"),
            ("sent", "Sent"),
            ("sender_error", "Sender Error"),
            ("recipient_error", "Not delivered"),
            ("rejected", "Rejected (PA)"),
            ("validated", "Delivered"),
            ("accepted", "Accepted"),
        ],
        string="State",
        default="ready",
        tracking=True,
    )
    sending_date = fields.Datetime("Sent Date", readonly=True)
    delivered_date = fields.Datetime("Delivered Date", readonly=True)

    _sql_constraints = [
        (
            "ftpa_attachment_out_name_uniq",
            "unique(att_name)",
            "The name of the e-invoice file must be unique!",
        )
    ]

    @api.model
    def get_file_vat(self):
        company = self.env.company
        if company.fatturapa_sender_partner:
            if not company.fatturapa_sender_partner.vat:
                raise UserError(
                    _("Partner %s TIN not set.")
                    % company.fatturapa_sender_partner.display_name
                )
            vat = company.fatturapa_sender_partner.vat
        else:
            if not company.vat:
                raise UserError(_("Company %s TIN not set.") % company.display_name)
            vat = company.vat
        vat = vat.replace(" ", "").replace(".", "").replace("-", "")
        return vat

    def file_name_exists(self, file_id):
        vat = self.get_file_vat()
        partial_fname = r"{}\_{}.".format(vat, file_id)  # escaping _ SQL
        # Not trying to perfect match file extension, because user could have
        # downloaded, signed and uploaded again the file, thus having changed
        # file extension
        return bool(self.search([("name", "=like", "%s%%" % partial_fname)]))

    @api.depends("out_invoice_ids")
    def _compute_invoice_partner_id(self):
        for att in self:
            partners = att.mapped("out_invoice_ids.partner_id")
            att.invoice_partner_id = False
            if len(partners) == 1:
                att.invoice_partner_id = partners.id

    @api.constrains("name")
    def _check_name(self):
        for att in self:
            res = self.search([("name", "=", att.name)])
            if len(res) > 1:
                raise UserError(_("File %s already present.") % att.name)

    @api.depends("out_invoice_ids.fatturapa_doc_attachments.is_pdf_invoice_print")
    def _compute_has_pdf_invoice_print(self):
        """Check if all the invoices related to this attachment
        have at least one attachment containing
        the PDF report of the invoice"""
        for attachment_out in self:
            attachment_out.has_pdf_invoice_print = False
            for invoice in attachment_out.out_invoice_ids:
                invoice_attachments = invoice.fatturapa_doc_attachments
                if not any([ia.is_pdf_invoice_print for ia in invoice_attachments]):
                    break
            else:
                # We have examined all the invoices and none of them
                # has caused a break, this means all the invoices have at least
                # one attachment having is_pdf_invoice_print = True
                attachment_out.has_pdf_invoice_print = True

    def reset_to_ready(self):
        for attachment_out in self:
            if attachment_out.state != "sender_error":
                raise UserError(_("You can only reset files in 'Sender Error' state."))
            attachment_out.state = "ready"

    def write(self, vals):
        res = super(FatturaPAAttachment, self).write(vals)
        if "datas" in vals and "message_ids" not in vals:
            for attachment in self:
                attachment.message_post(
                    subject=_("E-invoice attachment changed"),
                    body=_("User %s uploaded a new e-invoice file")
                    % self.env.user.login,
                )
        return res

    def unlink(self):
        for attachment_out in self:
            if attachment_out.state != "ready":
                raise UserError(
                    _("You can only delete files in 'Ready to Send' state.")
                )
            for invoice in attachment_out.out_invoice_ids:
                invoice.fatturapa_doc_attachments.filtered(
                    "is_pdf_invoice_print"
                ).unlink()
        return super(FatturaPAAttachment, self).unlink()


class FatturaAttachments(models.Model):
    _inherit = "fatturapa.attachments"

    is_pdf_invoice_print = fields.Boolean(
        help="This attachment contains the PDF report of the linked invoice"
    )
