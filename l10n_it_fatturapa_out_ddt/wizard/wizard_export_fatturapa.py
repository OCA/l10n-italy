# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.addons.l10n_it_fatturapa.bindings.fatturapa_v_1_2 import (
    DatiDDTType,
    DatiTrasportoType,
    DatiAnagraficiVettoreType,
    IdFiscaleType,
    AnagraficaType
)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    @api.model
    def default_get(self, fields):
        res = super(WizardExportFatturapa, self).default_get(fields)
        invoice_ids = self.env.context.get('active_ids', False)
        invoices = self.env['account.invoice'].browse(invoice_ids)
        for invoice in invoices:
            for line in invoice.invoice_line_ids:
                if line.ddt_line_id:
                    res['include_ddt_data'] = 'dati_ddt'
                    return res
        return res

    include_ddt_data = fields.Selection([
        ('dati_ddt', 'Include DDT Data'),
        ('dati_trasporto', 'Include transport data'),
        ],
        string="DDT Data",
        help="Include DDT data: The field must be entered when a transport "
             "document associated with a deferred invoice is present\n"
             "Include transport data: The field must be entered when a "
             "shipping invoice to be filled with transport data is present"
    )

    def setDatiDDT(self, invoice, body):
        res = super(WizardExportFatturapa, self).setDatiDDT(
            invoice, body)
        if self.include_ddt_data == 'dati_ddt':
            inv_lines_by_ddt = {}
            for line in invoice.invoice_line_ids:
                if (
                    line.ddt_line_id and
                    line.ddt_line_id.package_preparation_id.ddt_number and
                    line.ddt_line_id.package_preparation_id.date
                ):
                    key = (
                        line.ddt_line_id.package_preparation_id.ddt_number,
                        line.ddt_line_id.package_preparation_id.date[:10]
                    )
                    if key not in inv_lines_by_ddt:
                        inv_lines_by_ddt[key] = []
                    inv_lines_by_ddt[key].append(line.ftpa_line_number)
            for key in sorted(inv_lines_by_ddt.iterkeys()):
                DatiDDT = DatiDDTType(
                    NumeroDDT=key[0],
                    DataDDT=key[1]
                )
                for line_number in inv_lines_by_ddt[key]:
                    DatiDDT.RiferimentoNumeroLinea.append(line_number)
                body.DatiGenerali.DatiDDT.append(DatiDDT)
        elif self.include_ddt_data == 'dati_trasporto':
            body.DatiGenerali.DatiTrasporto = DatiTrasportoType(
                MezzoTrasporto=invoice.transportation_method_id.name or None,
                CausaleTrasporto=invoice.transportation_reason_id.name or None,
                NumeroColli=invoice.parcels or None,
                Descrizione=invoice.goods_description_id.name or None,
                PesoLordo='%.2f' % invoice.gross_weight,
                PesoNetto='%.2f' % invoice.weight,
                TipoResa=invoice.incoterms_id.code or None
            )
            if invoice.carrier_id:
                if not invoice.carrier_id.vat:
                    raise UserError(
                        _('TIN not set for %s.') % invoice.carrier_id.name)
                body.DatiGenerali.DatiTrasporto.DatiAnagraficiVettore = (
                    DatiAnagraficiVettoreType())
                if invoice.carrier_id.fiscalcode:
                    body.DatiGenerali.DatiTrasporto.DatiAnagraficiVettore.\
                        CodiceFiscale = invoice.carrier_id.fiscalcode
                body.DatiGenerali.DatiTrasporto.DatiAnagraficiVettore.\
                    IdFiscaleIVA = IdFiscaleType(
                        IdPaese=invoice.carrier_id.vat[0:2],
                        IdCodice=invoice.carrier_id.vat[2:]
                    )
                body.DatiGenerali.DatiTrasporto.DatiAnagraficiVettore.\
                    Anagrafica = AnagraficaType(
                        Denominazione=invoice.carrier_id.name)
        return res
