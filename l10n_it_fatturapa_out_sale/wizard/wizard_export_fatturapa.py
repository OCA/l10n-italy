# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models

from odoo.addons.l10n_it_account.tools.account_tools import encode_for_export
from odoo.addons.l10n_it_fatturapa.bindings.fatturapa import (
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
            only_one_sale_ref = bool(
                invoice.picking_ids and len(invoice.mapped('picking_ids.sale_id') == 1)
                or len(set(invoice.invoice_line_ids.mapped('origin'))) == 1)
            if invoice.picking_ids and only_one_sale_ref:
                doc_data = self.prepareDatiOrdineAcquisto(
                    invoice, invoice.invoice_line_ids[0])
                if doc_data:
                    documento = DatiDocumentiCorrelatiType()
                    documento.IdDocumento = doc_data['name']
                    documento.Data = doc_data['date']
                    getattr(body.DatiGenerali, doc_type).append(documento)
            else:
                for line in invoice.invoice_line_ids:
                    doc_data = self.prepareDatiOrdineAcquisto(invoice, line)
                    if doc_data:
                        documento = DatiDocumentiCorrelatiType()
                        documento.IdDocumento = doc_data['name']
                        documento.Data = doc_data['date']
                        documento.RiferimentoNumeroLinea.append(
                            line.ftpa_line_number)
                        getattr(body.DatiGenerali, doc_type).append(documento)
        return res

    def prepareDatiOrdineAcquisto(self, invoice, line):
        res = False
        if line.origin:
            orders = invoice.mapped('picking_ids.sale_id')
            orders |= self.env['sale.order'].search([('name', '=', line.origin)])
            for order in orders:
                # get name of internal order if configured in company or if not exists
                # a client order ref
                name = order.name if \
                    self.env.user.company_id.fatturapa_out_sale_internal_ref \
                    or not order.client_order_ref else order.client_order_ref
                res = {
                    'name': encode_for_export(name, 20, 'ascii'),
                    'date': order.date_order.date(),
                }
        return res
