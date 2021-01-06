# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from openerp import models

from openerp.addons.l10n_it_fatturapa.bindings.fatturapa import (
    DatiDocumentiCorrelatiType,
)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def setRelatedDocumentTypes(self, invoice, body):
        res = super(WizardExportFatturapa, self).setRelatedDocumentTypes(
            invoice, body)
        if invoice.partner_id.fatturapa_sale_order_data or \
                self.env.user.company_id.fatturapa_sale_order_data:
            doc_type = 'DatiOrdineAcquisto'
            # if sale_order refer to the whole invoice create only 1 rel doc
            if invoice.picking_ids and set(self.env['sale.order'].search([
                ('name', 'in', invoice.picking_ids.mapped('origin'))]).mapped(
                'client_order_ref')) == 1 or \
                    len(set(invoice.invoice_line.mapped('origin'))) == 1:
                doc_data = self.prepareRelDocsLine(
                    invoice, invoice.invoice_line[0])
                if doc_data:
                    documento = DatiDocumentiCorrelatiType()
                    documento.IdDocumento = doc_data['name']
                    documento.Data = doc_data['date']
                    getattr(body.DatiGenerali, doc_type).append(documento)
            else:
                for line in invoice.invoice_line:
                    doc_data = self.prepareRelDocsLine(invoice, line)
                    if doc_data:
                        documento = DatiDocumentiCorrelatiType()
                        documento.IdDocumento = doc_data['name']
                        documento.Data = doc_data['date']
                        documento.RiferimentoNumeroLinea.append(
                            line.ftpa_line_number)
                        getattr(body.DatiGenerali, doc_type).append(documento)
        return res

    def prepareRelDocsLine(self, invoice, line):
        res = False
        sale_order_name = False
        if line.origin:
            # if invoiced from picking, get sale_order from picking
            for picking in invoice.picking_ids:
                if picking.name == line.origin:
                    sale_order_name = picking.origin
                    break
            # else use origin directly
            if not sale_order_name:
                sale_order_name = line.origin
            order = self.env['sale.order'].search(
                [('name', '=', sale_order_name)])
            if order:
                company_id = self.env.user.company_id
                name = order.name if company_id.\
                    fatturapa_out_sale_internal_ref \
                    or not order.client_order_ref \
                    else order.client_order_ref
                res = {
                    'name': name[:20].replace('\n', ' ').replace
                    ('\t', ' ').replace('\r', ' ').encode(
                        'latin', 'ignore').decode('latin'),
                    'date': order.date_order[:10],
                }
        return res
