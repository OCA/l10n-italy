# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018 Gianmarco Conte, Marco Calcagni - Dinamiche Aziendali srl
# Copyright 2018 Sergio Corato
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from openerp import fields, models, api, _
from openerp.exceptions import Warning as UserError

from openerp.addons.l10n_it_fatturapa.bindings.fatturapa_v_1_2 import (
    ScontoMaggiorazioneType,
    DettaglioLineeType,
    CodiceArticoloType,
    DatiBeniServiziType,
    DatiRiepilogoType,
)

_logger = logging.getLogger(__name__)

try:
    from unidecode import unidecode
except ImportError as err:
    _logger.debug(err)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def setDettaglioLinee(self, invoice, body):

        body.DatiBeniServizi = DatiBeniServiziType()
        # TipoCessionePrestazione not handled

        line_no = 1
        price_precision = self.env['decimal.precision'].precision_get(
            'Product Price')
        if price_precision < 2:
            # XML wants at least 2 decimals always
            price_precision = 2
        uom_precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        if uom_precision < 2:
            uom_precision = 2
        for line in invoice.invoice_line:
            taxes = line.invoice_line_tax_id.filtered(
                lambda x: not x.tax_code_id.exclude_from_registries)
            if not taxes:
                raise UserError(
                    _("Invoice line %s does not have vat tax.") % line.name)
            if len(taxes) > 1:
                raise UserError(
                    _("Too many vat taxes for invoice line %s.") % line.name)
            aliquota = taxes[0].amount
            AliquotaIVA = '%.2f' % (aliquota * 100)
            line.ftpa_line_number = line_no
            prezzo_unitario = self._get_prezzo_unitario(line)
            DettaglioLinea = DettaglioLineeType(
                NumeroLinea=str(line_no),
                # can't insert newline with pyxb
                # see https://tinyurl.com/ycem923t
                # and '&#10;' would not be correctly visualized anyway
                # (for example firefox replaces '&#10;' with space)
                Descrizione=line.name.replace('\n', ' ').encode(
                    'latin', 'ignore').decode('latin'),
                PrezzoUnitario=('%.' + str(
                    price_precision
                ) + 'f') % prezzo_unitario,
                Quantita=('%.' + str(
                    uom_precision
                ) + 'f') % line.quantity,
                UnitaMisura=line.uos_id and (
                    unidecode(line.uos_id.name)) or None,
                PrezzoTotale='%.2f' % line.price_subtotal,
                AliquotaIVA=AliquotaIVA)
            if line.discount:
                ScontoMaggiorazione = ScontoMaggiorazioneType(
                    Tipo='SC',
                    Percentuale='%.2f' % line.discount
                )
                DettaglioLinea.ScontoMaggiorazione.append(ScontoMaggiorazione)
            if aliquota == 0.0:
                if not taxes[0].kind_id:
                    raise UserError(
                        _("No 'nature' field for tax %s") %
                        taxes[0].name)
                DettaglioLinea.Natura = taxes[0].kind_id.code
            if line.admin_ref:
                DettaglioLinea.RiferimentoAmministrazione = line.admin_ref
            if line.product_id:
                if line.product_id.default_code:
                    CodiceArticolo = CodiceArticoloType(
                        CodiceTipo='ODOO',
                        CodiceValore=line.product_id.default_code
                    )
                    DettaglioLinea.CodiceArticolo.append(CodiceArticolo)
                if line.product_id.ean13:
                    CodiceArticolo = CodiceArticoloType(
                        CodiceTipo='EAN',
                        CodiceValore=line.product_id.ean13
                    )
                    DettaglioLinea.CodiceArticolo.append(CodiceArticolo)
            line_no += 1

            body.DatiBeniServizi.DettaglioLinee.append(DettaglioLinea)

        return True

    def setDatiRiepilogo(self, invoice, body):
        model_tax = self.env['account.tax']
        for tax_line in invoice.tax_line.filtered(
            lambda x: not x.tax_code_id.exclude_from_registries
        ):
            tax = model_tax.get_tax_by_invoice_tax(tax_line.name)
            riepilogo = DatiRiepilogoType(
                AliquotaIVA='%.2f' % (tax.amount * 100),
                ImponibileImporto='%.2f' % tax_line.base,
                Imposta='%.2f' % tax_line.amount
                )
            if tax.amount == 0.0:
                if not tax.kind_id:
                    raise UserError(
                        _("No 'nature' field for tax %s.") % tax.name)
                riepilogo.Natura = tax.kind_id.code
                if not tax.law_reference:
                    raise UserError(
                        _("No 'law reference' field for tax %s.") % tax.name)
                riepilogo.RiferimentoNormativo = tax.law_reference.encode(
                    'latin', 'ignore').decode('latin')
            if tax.payability:
                riepilogo.EsigibilitaIVA = tax.payability
            # TODO

            # el.remove(el.find('SpeseAccessorie'))
            # el.remove(el.find('Arrotondamento'))

            body.DatiBeniServizi.DatiRiepilogo.append(riepilogo)

        return True
