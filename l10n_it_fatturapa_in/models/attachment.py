# -*- coding: utf-8 -*-

from openerp import fields, models, api


class FatturaPAAttachmentIn(models.Model):
    _name = "fatturapa.attachment.in"
    _description = "FatturaPA import File"
    _inherits = {'ir.attachment': 'ir_attachment_id'}
    _inherit = ['mail.thread']
    _order = 'id desc'

    ir_attachment_id = fields.Many2one(
        'ir.attachment', 'Attachment', required=True, ondelete="cascade")
    in_invoice_ids = fields.One2many(
        'account.invoice', 'fatturapa_attachment_in_id',
        string="In Invoices", readonly=True)
    xml_supplier_id = fields.Many2one(
        "res.partner", string="Supplier", compute="_compute_xml_data",
        store=True)
    invoices_number = fields.Integer(
        "Invoices number", compute="_compute_xml_data", store=True)
    invoices_total = fields.Float(
        "Invoices total", compute="_compute_xml_data", store=True,
        help="Se indicato dal fornitore, Importo totale del documento al "
             "netto dell'eventuale sconto e comprensivo di imposta a debito "
             "del cessionario / committente"
    )
    registered = fields.Boolean(
        "Registered", compute="_compute_registered", store=True)

    @api.onchange('datas_fname')
    def onchagne_datas_fname(self):
        self.name = self.datas_fname

    def get_xml_string(self):
        return self.ir_attachment_id.get_xml_string()

    @api.one
    @api.depends('ir_attachment_id.datas')
    def _compute_xml_data(self):
        fatt = self.env['wizard.import.fatturapa'].get_invoice_obj(self)
        cedentePrestatore = fatt.FatturaElettronicaHeader.CedentePrestatore
        partner_id = self.env['wizard.import.fatturapa'].getCedPrest(
            cedentePrestatore)
        self.xml_supplier_id = partner_id
        self.invoices_number = len(fatt.FatturaElettronicaBody)
        self.invoices_total = 0
        for invoice_body in fatt.FatturaElettronicaBody:
            self.invoices_total += float(
                invoice_body.DatiGenerali.DatiGeneraliDocumento.
                ImportoTotaleDocumento or 0
            )

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
