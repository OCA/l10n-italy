
from odoo import models, api, fields
from odoo.tools.translate import _
from odoo.exceptions import UserError
from odoo.addons.l10n_it_fatturapa.bindings import fatturapa


def get_invoice_obj(fatturapa_attachment):
    xml_string = fatturapa_attachment.get_xml_string()
    return fatturapa.CreateFromDocument(xml_string)


class WizardLinkToInvoiceLine(models.TransientModel):
    _name = 'wizard.link.to.invoice.line'
    _description = "Link e-bill to bill"

    wizard_id = fields.Many2one(
        comodel_name='wizard.link.to.invoice',
    )
    e_invoice_nbr = fields.Integer(
        string="Bill number in XML",
        readonly=True,
    )
    e_invoice_descr = fields.Text(
        string="E-bill description",
        readonly=True,
    )
    invoice_id = fields.Many2one(
        comodel_name='account.invoice',
    )

    @api.multi
    def link(self):
        self.ensure_one()
        if not self.invoice_id:
            return True
        fatturapa_attachment = self.wizard_id.attachment_id
        import_wiz = self.env['wizard.import.fatturapa'] \
            .with_context(
            active_ids=fatturapa_attachment.ids,
            linked_invoice=self.invoice_id,) \
            .new({
                'e_invoice_detail_level': '2',
            })
        fatt = get_invoice_obj(fatturapa_attachment)
        FatturaBody = fatt.FatturaElettronicaBody[self.e_invoice_nbr]
        cedentePrestatore = fatt.FatturaElettronicaHeader.CedentePrestatore

        self.invoice_id.fatturapa_attachment_in_id = fatturapa_attachment

        self.invoice_id.set_einvoice_data(FatturaBody)

        import_wiz.set_vendor_bill_data(FatturaBody, self.invoice_id)

        import_wiz.set_e_invoice_lines(FatturaBody, self.invoice_id)

        import_wiz.set_summary_data(FatturaBody, self.invoice_id.id)

        import_wiz.set_delivery_data(FatturaBody, self.invoice_id)

        import_wiz.set_payments_data(
            FatturaBody, self.invoice_id.id, self.invoice_id.partner_id.id)

        import_wiz.set_activity_progress(FatturaBody, self.invoice_id.id)

        import_wiz.set_StabileOrganizzazione(
            cedentePrestatore, self.invoice_id)

        import_wiz.set_efatt_rounding(FatturaBody, self.invoice_id)

        import_wiz.set_art73(FatturaBody, self.invoice_id)

        import_wiz.set_attachments_data(FatturaBody, self.invoice_id.id)

        return True


class WizardLinkToInvoice(models.TransientModel):
    _name = "wizard.link.to.invoice"
    _description = "Link to Bill"

    attachment_id = fields.Many2one(
        comodel_name='fatturapa.attachment.in',
    )
    line_ids = fields.One2many(
        comodel_name='wizard.link.to.invoice.line',
        inverse_name='wizard_id',)

    @api.model
    def _get_default_lines_vals(self, attachment):
        fatt = get_invoice_obj(attachment)
        invoice_model = self.env['account.invoice']
        line_vals = list()
        descr_template = _("Bill number {bill_nbr} of {bill_date}.\n"
                           "Total no tax: {bill_no_tax}\n"
                           "Total tax: {bill_tax}")
        for nbr, FatturaBody in enumerate(fatt.FatturaElettronicaBody):
            dati_generali_documento = \
                FatturaBody.DatiGenerali.DatiGeneraliDocumento
            dati_riepilogo = FatturaBody.DatiBeniServizi.DatiRiepilogo
            line_vals.append({
                'e_invoice_nbr': nbr,
                'e_invoice_descr': descr_template.format(
                    bill_nbr=dati_generali_documento.Numero,
                    bill_date=dati_generali_documento.Data,
                    bill_no_tax=invoice_model.compute_xml_amount_untaxed(
                        FatturaBody),
                    bill_tax=invoice_model.compute_xml_amount_tax(
                        dati_riepilogo)
                ),
            })
        return line_vals

    @api.model
    def _get_default_attachment(self):
        fatturapa_attachment_id = self.env.context.get('active_ids', [])
        if len(fatturapa_attachment_id) != 1:
            raise UserError(_("You can select only one XML file to link."))
        fatturapa_attachment_obj = self.env['fatturapa.attachment.in']
        attachment = fatturapa_attachment_obj.browse(fatturapa_attachment_id)
        return attachment

    @api.model
    def default_get(self, fields_list):
        res = super(WizardLinkToInvoice, self).default_get(fields_list)
        attachment = self._get_default_attachment()
        lines_vals = self._get_default_lines_vals(attachment)
        res.update({
            'attachment_id': attachment.id,
            'line_ids': [(0, 0, line_vals)
                         for line_vals in lines_vals],
        })
        return res

    @api.multi
    def link(self):
        self.ensure_one()
        for line in self.line_ids:
            line.link()
