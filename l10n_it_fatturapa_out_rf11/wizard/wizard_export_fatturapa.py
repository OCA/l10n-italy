from odoo import models, _
from odoo.exceptions import UserError

class WizardExportFatturapa(models.TransientModel):
    _inherit = 'wizard.export.fatturapa'

    def getTemplateValues(self, template_values):
        template_values = super().getTemplateValues(template_values)
        company_fiscal_position = self.env.company.fatturapa_fiscal_position_id.code

        rc_supplier = template_values['invoices'][0].rc_purchase_invoice_id.rc_original_purchase_invoice_ids[0].partner_id

        if rc_supplier.is_74ter_agent and company_fiscal_position == "RF11":
            template_values['codice_destinatario'] = rc_supplier.codice_destinatario

        return template_values

    def saveAttachment(self, fatturapa, number):
        fatturapa_sender_partner = self.env.company.fatturapa_sender_partner
        company_fiscal_position = self.env.company.fatturapa_fiscal_position_id.code
        kind_id = self.env['account.tax.kind'].search([('code', '=', 'N6.9')], limit=1)
        if not kind_id:
            raise UserError(_("Tax kind N6.9 not found."))
        tax_backup = {}
        invoices = fatturapa.invoices
        if invoices:
            for invoice in invoices:
                if invoice.rc_purchase_invoice_id:
                    if len(invoices) > 1:
                        raise UserError(_("You can only export one self invoice at a time."))
                    rc_supplier = invoice.rc_purchase_invoice_id.rc_original_purchase_invoice_ids[0].partner_id
                    if rc_supplier.is_74ter_agent and company_fiscal_position == "RF11":
                        for line in invoice.invoice_line_ids:
                            if line.tax_ids.amount > 0.0:
                                tax_backup[line.id] = {
                                    'tax_amount': line.tax_ids.amount,
                                    'tax_kind_id': line.tax_ids.kind_id,
                                }
                                line.tax_ids.sudo().amount = 0.0
                                line.tax_ids.sudo().kind_id = kind_id
            rc_supplier = invoices[0].rc_purchase_invoice_id.rc_original_purchase_invoice_ids[0].partner_id

        if self.env.company.fatturapa_fiscal_position_id.code == "RF11" and rc_supplier and rc_supplier.is_74ter_agent:
            self.env.company.sudo().fatturapa_sender_partner = self.env.company.partner_id

        res = super().saveAttachment(fatturapa, number)

        self.env.company.sudo().fatturapa_sender_partner = fatturapa_sender_partner
        if invoices:
            for invoice in invoices:
                for line in invoice.invoice_line_ids:
                    if line.id in tax_backup:
                        line.tax_ids.sudo().amount = tax_backup[line.id]['tax_amount']
                        line.tax_ids.sudo().kind_id = tax_backup[line.id]['tax_kind_id']

        return res

    def getAllTaxes(self, invoice):
        res = super().getAllTaxes(invoice)

        # We need to edit only 'Imposta', the other fields are already edited in saveAttachment method
        if invoice.rc_purchase_invoice_id:
            rc_supplier = invoice.rc_purchase_invoice_id.rc_original_purchase_invoice_ids[0].partner_id
            if rc_supplier.is_74ter_agent and self.env.company.fatturapa_fiscal_position_id.code == "RF11":
                for tax_id in res:
                    tax = self.env['account.tax'].browse(tax_id)
                    if tax.amount == 0.0:
                        res[tax_id]['Imposta'] = 0.0

        return res
