# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
import logging

from odoo import models
from odoo.tools.translate import _
from odoo.exceptions import UserError

from odoo.addons.l10n_it_fatturapa.bindings.fatturapa_v_1_2 import (
    FatturaElettronica,
    FatturaElettronicaHeaderType,
    DatiTrasmissioneType,
    IdFiscaleType,
    ContattiTrasmittenteType,
    CedentePrestatoreType,
    AnagraficaType,
    IndirizzoType,
    IscrizioneREAType,
    CessionarioCommittenteType,
    DatiAnagraficiCedenteType,
    DatiAnagraficiCessionarioType,
    FatturaElettronicaBodyType,
    DatiGeneraliType,
    DettaglioLineeType,
    DatiBeniServiziType,
    DatiRiepilogoType,
    DatiGeneraliDocumentoType,
    DatiDocumentiCorrelatiType,
    ContattiType,
    DatiPagamentoType,
    DettaglioPagamentoType,
    AllegatiType,
    ScontoMaggiorazioneType
)
from odoo.addons.l10n_it_fatturapa.models.account import (
    RELATED_DOCUMENT_TYPES)

_logger = logging.getLogger(__name__)

try:
    from unidecode import unidecode
    from pyxb.exceptions_ import SimpleFacetValueError, SimpleTypeValueError
except ImportError as err:
    _logger.debug(err)


class WizardExportFatturapa(models.TransientModel):
    _name = "wizard.export.fatturapa"
    _description = "Export FatturaPA"

    def saveAttachment(self, fatturapa, number):

        company = self.env.user.company_id

        if not company.vat:
            raise UserError(
                _('Company TIN not set.'))
        attach_obj = self.env['fatturapa.attachment.out']
        attach_vals = {
            'name': '%s_%s.xml' % (company.vat, str(number)),
            'datas_fname': '%s_%s.xml' % (company.vat, str(number)),
            'datas': base64.encodestring(fatturapa.toxml("UTF-8")),
        }
        return attach_obj.create(attach_vals)

    def setProgressivoInvio(self, fatturapa):

        company = self.env.user.company_id
        fatturapa_sequence = company.fatturapa_sequence_id
        if not fatturapa_sequence:
            raise UserError(
                _('FatturaPA sequence not configured.'))
        number = fatturapa_sequence.next_by_id()
        fatturapa.FatturaElettronicaHeader.DatiTrasmissione.\
            ProgressivoInvio = number
        return number

    def _setIdTrasmittente(self, company, fatturapa):

        if not company.country_id:
            raise UserError(
                _('Company Country not set.'))
        IdPaese = company.country_id.code

        IdCodice = company.partner_id.fiscalcode
        if not IdCodice:
            if company.vat:
                IdCodice = company.vat[2:]
        if not IdCodice:
            raise UserError(
                _('Company does not have fiscal code or VAT'))

        fatturapa.FatturaElettronicaHeader.DatiTrasmissione.\
            IdTrasmittente = IdFiscaleType(
                IdPaese=IdPaese, IdCodice=IdCodice)

        return True

    def _setFormatoTrasmissione(self, fatturapa):

        # TODO: gestire i privati
        fatturapa.FatturaElettronicaHeader.DatiTrasmissione.\
            FormatoTrasmissione = 'FPA12'

        return True

    def _setCodiceDestinatario(self, partner, fatturapa):
        code = partner.ipa_code
        if not code:
            raise UserError(
                _('IPA Code not set on partner form.'))
        fatturapa.FatturaElettronicaHeader.DatiTrasmissione.\
            CodiceDestinatario = code.upper()

        return True

    def _setContattiTrasmittente(self, company, fatturapa):

        if not company.phone:
            raise UserError(
                _('Company Telephone number not set.'))
        Telefono = company.phone

        if not company.email:
            raise UserError(
                _('Email address not set.'))
        Email = company.email
        fatturapa.FatturaElettronicaHeader.DatiTrasmissione.\
            ContattiTrasmittente = ContattiTrasmittenteType(
                Telefono=Telefono, Email=Email)

        return True

    def setDatiTrasmissione(self, company, partner, fatturapa):
        fatturapa.FatturaElettronicaHeader.DatiTrasmissione = (
            DatiTrasmissioneType())
        self._setIdTrasmittente(company, fatturapa)
        self._setFormatoTrasmissione(fatturapa)
        self._setCodiceDestinatario(partner, fatturapa)
        self._setContattiTrasmittente(company, fatturapa)

    def _setDatiAnagraficiCedente(self, CedentePrestatore, company):

        if not company.vat:
            raise UserError(
                _('TIN not set.'))
        CedentePrestatore.DatiAnagrafici = DatiAnagraficiCedenteType()
        fatturapa_fp = company.fatturapa_fiscal_position_id
        if not fatturapa_fp:
            raise UserError(
                _('FatturaPA fiscal position not set.'))
        CedentePrestatore.DatiAnagrafici.IdFiscaleIVA = IdFiscaleType(
            IdPaese=company.country_id.code, IdCodice=company.vat[2:])
        CedentePrestatore.DatiAnagrafici.Anagrafica = AnagraficaType(
            Denominazione=company.name)

        # not using for now
        #
        # Anagrafica = DatiAnagrafici.find('Anagrafica')
        # Nome = Anagrafica.find('Nome')
        # Cognome = Anagrafica.find('Cognome')
        # Titolo = Anagrafica.find('Titolo')
        # Anagrafica.remove(Nome)
        # Anagrafica.remove(Cognome)
        # Anagrafica.remove(Titolo)

        if company.partner_id.fiscalcode:
            CedentePrestatore.DatiAnagrafici.CodiceFiscale = (
                company.partner_id.fiscalcode)
        CedentePrestatore.DatiAnagrafici.RegimeFiscale = fatturapa_fp.code
        return True

    def _setAlboProfessionaleCedente(self, CedentePrestatore, company):
        # TODO Albo professionale, for now the main company is considered
        # to be a legal entity and not a single person
        # 1.2.1.4   <AlboProfessionale>
        # 1.2.1.5   <ProvinciaAlbo>
        # 1.2.1.6   <NumeroIscrizioneAlbo>
        # 1.2.1.7   <DataIscrizioneAlbo>
        return True

    def _setSedeCedente(self, CedentePrestatore, company):

        if not company.street:
            raise UserError(
                _('Street not set.'))
        if not company.zip:
            raise UserError(
                _('ZIP not set.'))
        if not company.city:
            raise UserError(
                _('City not set.'))
        if not company.partner_id.state_id:
            raise UserError(
                _('Province not set.'))
        if not company.country_id:
            raise UserError(
                _('Country not set.'))
        # TODO: manage address number in <NumeroCivico>
        # see https://github.com/OCA/partner-contact/pull/96
        CedentePrestatore.Sede = IndirizzoType(
            Indirizzo=company.street,
            CAP=company.zip,
            Comune=company.city,
            Provincia=company.partner_id.state_id.code,
            Nazione=company.country_id.code)

        return True

    def _setStabileOrganizzazione(self, CedentePrestatore, company):
        # not handled
        return True

    def _setRea(self, CedentePrestatore, company):

        if company.fatturapa_rea_office and company.fatturapa_rea_number:
            CedentePrestatore.IscrizioneREA = IscrizioneREAType(
                Ufficio=(
                    company.fatturapa_rea_office and
                    company.fatturapa_rea_office.code or None),
                NumeroREA=company.fatturapa_rea_number or None,
                CapitaleSociale=(
                    company.fatturapa_rea_capital and
                    '%.2f' % company.fatturapa_rea_capital or None),
                SocioUnico=(company.fatturapa_rea_partner or None),
                StatoLiquidazione=company.fatturapa_rea_liquidation or None
                )

    def _setContatti(self, CedentePrestatore, company):
        CedentePrestatore.Contatti = ContattiType(
            Telefono=company.partner_id.phone or None,
            Fax=company.partner_id.fax or None,
            Email=company.partner_id.email or None
            )

    def _setPubAdministrationRef(self, CedentePrestatore, company):
        if company.fatturapa_pub_administration_ref:
            CedentePrestatore.RiferimentoAmministrazione = (
                company.fatturapa_pub_administration_ref)

    def setCedentePrestatore(self, company, fatturapa):
        fatturapa.FatturaElettronicaHeader.CedentePrestatore = (
            CedentePrestatoreType())
        self._setDatiAnagraficiCedente(
            fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company)
        self._setSedeCedente(
            fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company)
        self._setAlboProfessionaleCedente(
            fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company)
        self._setStabileOrganizzazione(
            fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company)
        # TODO: add Contacts
        self._setRea(
            fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company)
        self._setContatti(
            fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company)
        self._setPubAdministrationRef(
            fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company)

    def _setDatiAnagraficiCessionario(self, partner, fatturapa):
        fatturapa.FatturaElettronicaHeader.CessionarioCommittente.\
            DatiAnagrafici = DatiAnagraficiCessionarioType()
        if not partner.vat and not partner.fiscalcode:
            raise UserError(
                _('Partner VAT and Fiscalcode not set.'))
        if partner.fiscalcode:
            fatturapa.FatturaElettronicaHeader.CessionarioCommittente.\
                DatiAnagrafici.CodiceFiscale = partner.fiscalcode
        if partner.vat:
            fatturapa.FatturaElettronicaHeader.CessionarioCommittente.\
                DatiAnagrafici.IdFiscaleIVA = IdFiscaleType(
                    IdPaese=partner.vat[0:2], IdCodice=partner.vat[2:])
        fatturapa.FatturaElettronicaHeader.CessionarioCommittente.\
            DatiAnagrafici.Anagrafica = AnagraficaType(
                Denominazione=partner.name)

        # not using for now
        #
        # Anagrafica = DatiAnagrafici.find('Anagrafica')
        # Nome = Anagrafica.find('Nome')
        # Cognome = Anagrafica.find('Cognome')
        # Titolo = Anagrafica.find('Titolo')
        # Anagrafica.remove(Nome)
        # Anagrafica.remove(Cognome)
        # Anagrafica.remove(Titolo)

        if partner.eori_code:
            fatturapa.FatturaElettronicaHeader.CessionarioCommittente.\
                DatiAnagrafici.Anagrafica.CodEORI = partner.eori_code

        return True

    def _setSedeCessionario(self, partner, fatturapa):

        if not partner.street:
            raise UserError(
                _('Customer street not set.'))
        if not partner.zip:
            raise UserError(
                _('Customer ZIP not set.'))
        if not partner.city:
            raise UserError(
                _('Customer city not set.'))
        if not partner.state_id:
            raise UserError(
                _('Customer province not set.'))
        if not partner.country_id:
            raise UserError(
                _('Customer country not set.'))

        # TODO: manage address number in <NumeroCivico>
        fatturapa.FatturaElettronicaHeader.CessionarioCommittente.Sede = (
            IndirizzoType(
                Indirizzo=partner.street,
                CAP=partner.zip,
                Comune=partner.city,
                Provincia=partner.state_id.code,
                Nazione=partner.country_id.code))

        return True

    def setRappresentanteFiscale(self, company):

        if company.fatturapa_tax_representative:
            # TODO: RappresentanteFiscale should be usefull for foreign
            # companies sending invoices to italian PA only
            raise UserError(
                _("RappresentanteFiscale not handled"))
            # partner = company.fatturapa_tax_representative

        # DatiAnagrafici = RappresentanteFiscale.find('DatiAnagrafici')

        # if not partner.fiscalcode:
            # raise UserError(
            # _('RappresentanteFiscale Partner '
            # 'fiscalcode not set.'))

        # DatiAnagrafici.find('CodiceFiscale').text = partner.fiscalcode

        # if not partner.vat:
            # raise UserError(
            # _('RappresentanteFiscale Partner VAT not set.'))
        # DatiAnagrafici.find(
            # 'IdFiscaleIVA/IdPaese').text = partner.vat[0:2]
        # DatiAnagrafici.find(
            # 'IdFiscaleIVA/IdCodice').text = partner.vat[2:]
        # DatiAnagrafici.find('Anagrafica/Denominazione').text = partner.name
        # if partner.eori_code:
            # DatiAnagrafici.find(
            # 'Anagrafica/CodEORI').text = partner.codiceEORI
        return True

    def setCessionarioCommittente(self, partner, fatturapa):
        fatturapa.FatturaElettronicaHeader.CessionarioCommittente = (
            CessionarioCommittenteType())
        self._setDatiAnagraficiCessionario(partner, fatturapa)
        self._setSedeCessionario(partner, fatturapa)

    def setTerzoIntermediarioOSoggettoEmittente(self, company):
        if company.fatturapa_sender_partner:
            # TODO
            raise UserError(
                _("TerzoIntermediarioOSoggettoEmittente not handled"))
        return True

    def setSoggettoEmittente(self):

        # TODO: this record is to be checked invoice by invoice
        # so a control is needed to verify that all invoices are
        # of type CC, TZ or internally created by the company

        # SoggettoEmittente.text = 'CC'
        return True

    def setDatiGeneraliDocumento(self, invoice, body):

        # TODO DatiSAL

        # TODO DatiDDT

        body.DatiGenerali = DatiGeneraliType()
        if not invoice.number:
            raise UserError(
                _('Invoice does not have a number.'))

        TipoDocumento = 'TD01'
        if invoice.type == 'out_refund':
            TipoDocumento = 'TD04'
        ImportoTotaleDocumento = invoice.amount_total
        if invoice.split_payment:
            ImportoTotaleDocumento += invoice.amount_sp
        body.DatiGenerali.DatiGeneraliDocumento = DatiGeneraliDocumentoType(
            TipoDocumento=TipoDocumento,
            Divisa=invoice.currency_id.name,
            Data=invoice.date_invoice,
            Numero=invoice.number,
            ImportoTotaleDocumento='%.2f' % ImportoTotaleDocumento)

        # TODO: DatiRitenuta, DatiBollo, DatiCassaPrevidenziale,
        # ScontoMaggiorazione, Arrotondamento,

        if invoice.comment:
            # max length of Causale is 200
            caus_list = invoice.comment.split('\n')
            for causale in caus_list:
                # Remove non latin chars, but go back to unicode string,
                # as expected by String200LatinType
                causale = causale.encode(
                    'latin', 'ignore').decode('latin')
                body.DatiGenerali.DatiGeneraliDocumento.Causale.append(causale)

        if invoice.company_id.fatturapa_art73:
            body.DatiGenerali.DatiGeneraliDocumento.Art73 = 'SI'

        return True

    def setRelatedDocumentTypes(self, invoice, body):
        linecount = 1
        for line in invoice.invoice_line_ids:
            for related_document in line.related_documents:
                doc_type = RELATED_DOCUMENT_TYPES[related_document.type]
                documento = DatiDocumentiCorrelatiType()
                if related_document.name:
                    documento.IdDocumento = related_document.name
                if related_document.lineRef:
                    documento.RiferimentoNumeroLinea.append(linecount)
                if related_document.date:
                    documento.Data = related_document.date
                if related_document.numitem:
                    documento.NumItem = related_document.numitem
                if related_document.code:
                    documento.CodiceCommessaConvenzione = related_document.code
                if related_document.cup:
                    documento.CodiceCUP = related_document.cup
                if related_document.cig:
                    documento.CodiceCIG = related_document.cig
                getattr(body.DatiGenerali, doc_type).append(documento)
            linecount += 1
        for related_document in invoice.related_documents:
            doc_type = RELATED_DOCUMENT_TYPES[related_document.type]
            documento = DatiDocumentiCorrelatiType()
            if related_document.name:
                documento.IdDocumento = related_document.name
            if related_document.date:
                documento.Data = related_document.date
            if related_document.numitem:
                documento.NumItem = related_document.numitem
            if related_document.code:
                documento.CodiceCommessaConvenzione = related_document.code
            if related_document.cup:
                documento.CodiceCUP = related_document.cup
            if related_document.cig:
                documento.CodiceCIG = related_document.cig
            getattr(body.DatiGenerali, doc_type).append(documento)
        return True

    def setDatiTrasporto(self, invoice, body):
        return True

    def setDettaglioLinee(self, invoice, body):

        body.DatiBeniServizi = DatiBeniServiziType()
        # TipoCessionePrestazione not handled

        # TODO CodiceArticolo

        line_no = 1
        for line in invoice.invoice_line_ids:
            if not line.invoice_line_tax_ids:
                raise UserError(
                    _("Invoice line %s does not have tax") % line.name)
            if len(line.invoice_line_tax_ids) > 1:
                raise UserError(
                    _("Too many taxes for invoice line %s") % line.name)
            aliquota = line.invoice_line_tax_ids[0].amount
            AliquotaIVA = '%.2f' % (aliquota)
            DettaglioLinea = DettaglioLineeType(
                NumeroLinea=str(line_no),
                Descrizione=line.name,
                PrezzoUnitario='%.2f' % line.price_unit,
                Quantita='%.2f' % line.quantity,
                UnitaMisura=line.uom_id and (
                    unidecode(line.uom_id.name)) or None,
                PrezzoTotale='%.2f' % line.price_subtotal,
                AliquotaIVA=AliquotaIVA)
            if line.discount:
                ScontoMaggiorazione = ScontoMaggiorazioneType(
                    Tipo='SC',
                    Percentuale='%.2f' % line.discount
                )
                DettaglioLinea.ScontoMaggiorazione.append(ScontoMaggiorazione)
            if aliquota == 0.0:
                if not line.invoice_line_tax_ids[0].kind_id:
                    raise UserError(
                        _("No 'nature' field for tax %s") %
                        line.invoice_line_tax_ids[0].name)
                DettaglioLinea.Natura = line.invoice_line_tax_ids[
                    0
                ].kind_id.code
            if line.admin_ref:
                DettaglioLinea.RiferimentoAmministrazione = line.admin_ref
            line_no += 1

            # not handled

            # el.remove(el.find('DataInizioPeriodo'))
            # el.remove(el.find('DataFinePeriodo'))
            # el.remove(el.find('Ritenuta'))
            # el.remove(el.find('AltriDatiGestionali'))

            body.DatiBeniServizi.DettaglioLinee.append(DettaglioLinea)

        return True

    def setDatiRiepilogo(self, invoice, body):
        for tax_line in invoice.tax_line_ids:
            tax = tax_line.tax_id
            riepilogo = DatiRiepilogoType(
                AliquotaIVA='%.2f' % tax.amount,
                ImponibileImporto='%.2f' % tax_line.base,
                Imposta='%.2f' % tax_line.amount
                )
            if tax.amount == 0.0:
                if not tax.kind_id:
                    raise UserError(
                        _("No 'nature' field for tax %s") % tax.name)
                riepilogo.Natura = tax.kind_id.code
                if not tax.law_reference:
                    raise UserError(
                        _("No 'law reference' field for tax %s") % tax.name)
                riepilogo.RiferimentoNormativo = tax.law_reference
            if tax.payability:
                riepilogo.EsigibilitaIVA = tax.payability
            # TODO

            # el.remove(el.find('SpeseAccessorie'))
            # el.remove(el.find('Arrotondamento'))

            body.DatiBeniServizi.DatiRiepilogo.append(riepilogo)

        return True

    def setDatiPagamento(self, invoice, body):
        if invoice.payment_term_id:
            DatiPagamento = DatiPagamentoType()
            if not invoice.payment_term_id.fatturapa_pt_id:
                raise UserError(
                    _('Payment term %s does not have a linked fatturaPA '
                      'payment term') % invoice.payment_term_id.name)
            if not invoice.payment_term_id.fatturapa_pm_id:
                raise UserError(
                    _('Payment term %s does not have a linked fatturaPA '
                      'payment method') % invoice.payment_term_id.name)
            DatiPagamento.CondizioniPagamento = (
                invoice.payment_term_id.fatturapa_pt_id.code)
            move_line_pool = self.env['account.move.line']
            payment_line_ids = invoice.get_receivable_line_ids()
            for move_line_id in payment_line_ids:
                move_line = move_line_pool.browse(move_line_id)
                ImportoPagamento = '%.2f' % move_line.debit
                DettaglioPagamento = DettaglioPagamentoType(
                    ModalitaPagamento=(
                        invoice.payment_term_id.fatturapa_pm_id.code),
                    DataScadenzaPagamento=move_line.date_maturity,
                    ImportoPagamento=ImportoPagamento
                    )
                if invoice.partner_bank_id:
                    DettaglioPagamento.IstitutoFinanziario = (
                        invoice.partner_bank_id.bank_name)
                    if invoice.partner_bank_id.acc_number:
                        DettaglioPagamento.IBAN = (
                            ''.join(invoice.partner_bank_id.acc_number.split())
                            )
                    if invoice.partner_bank_id.bank_bic:
                        DettaglioPagamento.BIC = (
                            invoice.partner_bank_id.bank_bic)
                DatiPagamento.DettaglioPagamento.append(DettaglioPagamento)
            body.DatiPagamento.append(DatiPagamento)
        return True

    def setAttachments(self, invoice, body):
        if invoice.fatturapa_doc_attachments:
            for doc_id in invoice.fatturapa_doc_attachments:
                AttachDoc = AllegatiType(
                    NomeAttachment=doc_id.datas_fname,
                    Attachment=doc_id.datas
                )
                body.Allegati.append(AttachDoc)
        return True

    def setFatturaElettronicaHeader(self, company, partner, fatturapa):
        fatturapa.FatturaElettronicaHeader = (
            FatturaElettronicaHeaderType())
        self.setDatiTrasmissione(company, partner, fatturapa)
        self.setCedentePrestatore(company, fatturapa)
        self.setRappresentanteFiscale(company)
        self.setCessionarioCommittente(partner, fatturapa)
        self.setTerzoIntermediarioOSoggettoEmittente(company)
        self.setSoggettoEmittente()

    def setFatturaElettronicaBody(self, inv, FatturaElettronicaBody):

        self.setDatiGeneraliDocumento(inv, FatturaElettronicaBody)
        self.setRelatedDocumentTypes(inv, FatturaElettronicaBody)
        self.setDatiTrasporto(inv, FatturaElettronicaBody)
        self.setDettaglioLinee(inv, FatturaElettronicaBody)
        self.setDatiRiepilogo(inv, FatturaElettronicaBody)
        self.setDatiPagamento(inv, FatturaElettronicaBody)
        self.setAttachments(inv, FatturaElettronicaBody)

    def getPartnerId(self, invoice_ids):

        invoice_model = self.env['account.invoice']
        partner = False

        invoices = invoice_model.browse(invoice_ids)

        for invoice in invoices:
            if not partner:
                partner = invoice.partner_id
            if invoice.partner_id != partner:
                raise UserError(
                    _('Invoices must belong to the same partner'))

        return partner

    def exportFatturaPA(self):

        # self.setNameSpace()

        model_data_obj = self.env['ir.model.data']
        invoice_obj = self.env['account.invoice']

        fatturapa = FatturaElettronica(versione='FPA12')
        invoice_ids = self.env.context.get('active_ids', False)
        partner = self.getPartnerId(invoice_ids)

        company = self.env.user.company_id
        context_partner = self.env.context.copy()
        context_partner.update({'lang': partner.lang})
        try:
            self.with_context(context_partner).setFatturaElettronicaHeader(
                company, partner, fatturapa)
            for invoice_id in invoice_ids:
                inv = invoice_obj.with_context(context_partner).browse(
                    invoice_id)
                if inv.fatturapa_attachment_out_id:
                    raise UserError(
                        _("Invoice %s has FatturaPA Export File yet") % (
                            inv.number))
                invoice_body = FatturaElettronicaBodyType()
                self.with_context(context_partner).setFatturaElettronicaBody(
                    inv, invoice_body)
                fatturapa.FatturaElettronicaBody.append(invoice_body)
                # TODO DatiVeicoli

            number = self.setProgressivoInvio(fatturapa)
        except (SimpleFacetValueError, SimpleTypeValueError) as e:
            raise UserError(
                (unicode(e)))

        attach = self.saveAttachment(fatturapa, number)

        for invoice_id in invoice_ids:
            inv = invoice_obj.browse(invoice_id)
            inv.write({'fatturapa_attachment_out_id': attach.id})

        view_id = model_data_obj.xmlid_to_res_id(
            'l10n_it_fatturapa_out.view_fatturapa_out_attachment_form')

        return {
            'view_type': 'form',
            'name': "Export FatturaPA",
            'view_id': [view_id],
            'res_id': attach.id,
            'view_mode': 'form',
            'res_model': 'fatturapa.attachment.out',
            'type': 'ir.actions.act_window',
            }
