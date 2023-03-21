
import base64
import logging

from odoo import fields, models, api, _
from odoo.tools import format_date

from odoo.addons.l10n_it_fatturapa.bindings import fatturapa

_logger = logging.getLogger(__name__)

SELF_INVOICE_TYPES = ("TD16", "TD17", "TD18", "TD19", "TD20", "TD21")


class FatturaPAAttachmentIn(models.Model):
    _inherit = "fatturapa.attachment"
    _name = "fatturapa.attachment.in"

    in_invoice_ids = fields.One2many(
        'account.invoice', 'fatturapa_attachment_in_id',
        string="In Bills", readonly=True)
    xml_supplier_id = fields.Many2one(
        "res.partner", string="Supplier", compute="_compute_xml_data",
        store=True)
    invoices_number = fields.Integer(
        "Bills Number", compute="_compute_xml_data", store=True)
    invoices_total = fields.Float(
        "Bills Total", compute="_compute_xml_data", store=True,
        help="If specified by supplier, total amount of the document net of "
             "any discount and including tax charged to the buyer/ordered"
    )
    invoices_date = fields.Char(
        string="Invoices date", compute="_compute_xml_data", store=True)
    registered = fields.Boolean(
        "Registered", compute="_compute_registered", store=True)

    e_invoice_received_date = fields.Datetime(string='E-Bill Received Date')

    e_invoice_validation_error = fields.Boolean(
        compute='_compute_e_invoice_validation_error')

    e_invoice_validation_message = fields.Text(
        compute='_compute_e_invoice_validation_error')

    e_invoice_parsing_error = fields.Text(
        compute="_compute_e_invoice_parsing_error",
        store=True,
    )
    is_self_invoice = fields.Boolean(
        "Contains self invoices", compute="_compute_is_self_invoice", store=True
    )

    _sql_constraints = [(
        'ftpa_attachment_in_name_uniq',
        'unique(att_name)',
        'The name of the e-bill file must be unique!')]

    @api.depends('in_invoice_ids.e_invoice_validation_error')
    def _compute_e_invoice_validation_error(self):
        for att in self:
            bills_with_error = att.in_invoice_ids.filtered(
                lambda b: b.e_invoice_validation_error
            )
            if not bills_with_error:
                continue
            att.e_invoice_validation_error = True
            errors_message_template = u"{bill}:\n{errors}"
            error_messages = list()
            for bill in bills_with_error:
                error_messages.append(
                    errors_message_template.format(
                        bill=bill.display_name,
                        errors=bill.e_invoice_validation_message))
            att.e_invoice_validation_message = "\n\n".join(error_messages)

    @api.onchange('datas_fname')
    def onchagne_datas_fname(self):
        self.name = self.datas_fname

    @api.multi
    def recompute_xml_fields(self):
        # Pretend the attachment has been modified
        # and trigger a recomputation:
        # this recomputes all fields whose value
        # is extracted from the attachment
        self.modified(['ir_attachment_id'])
        self.recompute()

        self._compute_registered()

    @api.multi
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
            invoice_obj = fatturapa.CreateFromDocument(xml_string)
        except Exception as e:
            error_msg = \
                _("Impossible to parse XML for {att_name}: {error_msg}") \
                .format(
                    att_name=self.display_name,
                    error_msg=e,
                )
            _logger.error(error_msg)
            self.e_invoice_parsing_error = error_msg
        else:
            self.e_invoice_parsing_error = False
        return invoice_obj

    @api.multi
    @api.depends('ir_attachment_id.datas')
    def _compute_is_self_invoice(self):
        for att in self:
            fatt = att.get_invoice_obj()
            att.is_self_invoice = False
            if fatt:
                for invoice_body in fatt.FatturaElettronicaBody:
                    document_type = invoice_body.DatiGenerali \
                        .DatiGeneraliDocumento.TipoDocumento
                    if document_type in SELF_INVOICE_TYPES:
                        # If at least one invoice is a self invoice,
                        # then the whole attachment is flagged
                        att.is_self_invoice = True
                        break

    @api.multi
    @api.depends('ir_attachment_id.datas')
    def _compute_e_invoice_parsing_error(self):
        for att in self:
            att.get_invoice_obj()

    @api.multi
    @api.depends('ir_attachment_id.datas')
    def _compute_xml_data(self):
        for att in self:
            fatt = att.get_invoice_obj()
            if not fatt:
                # Set default values and carry on
                att.update({
                    'xml_supplier_id': False,
                    'invoices_number': 0,
                    'invoices_total': 0,
                    'invoices_date': False,
                })
                continue

            # Look into each invoice to compute the following values
            invoices_date = []
            for invoice_body in fatt.FatturaElettronicaBody:
                # Assign this directly so that rounding is applied each time
                att.invoices_total += float(
                    invoice_body.DatiGenerali.DatiGeneraliDocumento.
                    ImportoTotaleDocumento or 0
                )

                document_date = invoice_body \
                    .DatiGenerali.DatiGeneraliDocumento.Data
                invoice_date = format_date(
                    att.with_context(lang=att.env.user.lang).env,
                    fields.Date.from_string(document_date),
                )
                if invoice_date not in invoices_date:
                    invoices_date.append(invoice_date)

            att.update(dict(
                invoices_date=' '.join(invoices_date),
            ))

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
            wiz_obj = self.env['wizard.import.fatturapa'] \
                .with_context(from_attachment=att)
            partner_id = wiz_obj.getCedPrest(cedentePrestatore)
            att.xml_supplier_id = partner_id

    @api.multi
    @api.depends('in_invoice_ids')
    def _compute_registered(self):
        for att in self:
            if (
                att.in_invoice_ids and
                len(att.in_invoice_ids) == att.invoices_number
            ):
                att.registered = True
            else:
                att.registered = False

    def extract_attachments(self, AttachmentsData, invoice_id):
        AttachModel = self.env['fatturapa.attachments']
        for attach in AttachmentsData:
            if not attach.NomeAttachment:
                name = _("Attachment without name")
            else:
                name = attach.NomeAttachment
            content = attach.Attachment
            _attach_dict = {
                'name': name,
                'datas': base64.b64encode(content),
                'datas_fname': name,
                'description': attach.DescrizioneAttachment or '',
                'compression': attach.AlgoritmoCompressione or '',
                'format': attach.FormatoAttachment or '',
                'invoice_id': invoice_id,
            }
            AttachModel.create(_attach_dict)
