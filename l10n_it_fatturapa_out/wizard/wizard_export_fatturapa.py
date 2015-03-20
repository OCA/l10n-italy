# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Davide Corio <davide.corio@lsweb.it>
#    Copyright (C) 2015 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import base64
import tempfile
from pyxb.exceptions_ import SimpleFacetValueError
from unidecode import unidecode
from openerp.osv import orm
from openerp import addons
from openerp.addons.l10n_it_fatturapa.bindings.fatturapa_v_1_1 import (
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
    DatiDocumentiCorrelatiType
    )
from openerp.addons.l10n_it_fatturapa.models.account import (
    RELATED_DOCUMENT_TYPES)
from openerp.tools.translate import _


class WizardExportFatturapa(orm.TransientModel):
    _name = "wizard.export.fatturapa"
    _description = "Export FatturaPA"

    def __init__(self, cr, uid, **kwargs):
        self.fatturapa = False
        self.number = False
        super(WizardExportFatturapa, self).__init__(cr, uid, **kwargs)

    def getFile(self, filename, context=None):
        if context is None:
            context = {}

        path = addons.get_module_resource(
            'l10n_it_fatturapa', 'data', filename)
        with open(path) as test_data:
            with tempfile.TemporaryFile() as out:
                base64.encode(test_data, out)
                out.seek(0)
                return out.read()
    '''
    def setNameSpace(self):
        register_namespace('ds', "http://www.w3.org/2000/09/xmldsig#")
        register_namespace(
            'p', "http://www.fatturapa.gov.it/sdi/fatturapa/v1.1")
        register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    '''
    def saveAttachment(self, cr, uid, context=None):
        if context is None:
            context = {}

        number = self.number

        user_obj = self.pool['res.users']
        company = user_obj.browse(cr, uid, uid).company_id

        if not company.vat:
            raise orm.except_orm(
                _('Error!'), _('Company TIN not set.'))
        attach_obj = self.pool['fatturapa.attachment.out']
        attach_vals = {
            'name': '%s_%s.xml' % (company.vat, str(number)),
            'datas_fname': '%s_%s.xml' % (company.vat, str(number)),
            'datas': base64.encodestring(self.fatturapa.toxml("latin1")),
        }
        attach_id = attach_obj.create(cr, uid, attach_vals, context=context)

        return attach_id

    def setProgressivoInvio(self, cr, uid, context=None):
        if context is None:
            context = {}

        user_obj = self.pool['res.users']
        company = user_obj.browse(cr, uid, uid).company_id
        sequence_obj = self.pool['ir.sequence']
        fatturapa_sequence = company.fatturapa_sequence_id
        if not fatturapa_sequence:
            raise orm.except_orm(
                _('Error!'), _('FatturaPA sequence not configured.'))
        self.number = number = sequence_obj.next_by_id(
            cr, uid, fatturapa_sequence.id, context=context)
        self.fatturapa.FatturaElettronicaHeader.DatiTrasmissione.\
            ProgressivoInvio = number
        return True

    def _setIdTrasmittente(self, cr, uid, company, context=None):
        if context is None:
            context = {}

        if not company.country_id:
            raise orm.except_orm(
                _('Error!'), _('Company Country not set.'))
        IdPaese = company.country_id.code

        IdCodice = company.partner_id.fiscalcode
        if not IdCodice:
            IdCodice = company.vat[2:]
        if not IdCodice:
            raise orm.except_orm(
                _('Error'), _('Company does not have fiscal code or VAT'))

        self.fatturapa.FatturaElettronicaHeader.DatiTrasmissione.\
            IdTrasmittente = IdFiscaleType(
                IdPaese=IdPaese, IdCodice=IdCodice)

        return True

    def _setFormatoTrasmissione(self, cr, uid, company, context=None):
        if context is None:
            context = {}

        if not company.fatturapa_format_id:
            raise orm.except_orm(
                _('Error!'), _('FatturaPA format not set.'))
        self.fatturapa.FatturaElettronicaHeader.DatiTrasmissione.\
            FormatoTrasmissione = company.fatturapa_format_id.code

        return True

    def _setCodiceDestinatario(self, cr, uid, partner, context=None):
        if context is None:
            context = {}
        code = partner.fatturapa_code
        if not code:
            raise orm.except_orm(
                _('Error!'), _('FatturaPA Code not set on partner form.'))
        self.fatturapa.FatturaElettronicaHeader.DatiTrasmissione.\
            CodiceDestinatario = code.upper()

        return True

    def _setContattiTrasmittente(self, cr, uid, company, context=None):
        if context is None:
            context = {}

        if not company.phone:
            raise orm.except_orm(
                _('Error!'), _('Company Telephone number not set.'))
        Telefono = company.phone

        if not company.email:
            raise orm.except_orm(
                _('Error!'), _('Email address not set.'))
        Email = company.email
        self.fatturapa.FatturaElettronicaHeader.DatiTrasmissione.\
            ContattiTrasmittente = ContattiTrasmittenteType(
                Telefono=Telefono, Email=Email)

        return True

    def setDatiTrasmissione(self, cr, uid, company, partner, context=None):
        if context is None:
            context = {}
        self.fatturapa.FatturaElettronicaHeader.DatiTrasmissione = (
            DatiTrasmissioneType())
        self._setIdTrasmittente(cr, uid, company, context=context)
        self._setFormatoTrasmissione(cr, uid, company, context=context)
        self._setCodiceDestinatario(cr, uid, partner, context=context)
        self._setContattiTrasmittente(cr, uid, company, context=context)

    def _setDatiAnagraficiCedente(self, cr, uid, CedentePrestatore,
                                  company, context=None):
        if context is None:
            context = {}

        if not company.vat:
            raise orm.except_orm(
                _('Error!'), _('TIN not set.'))
        CedentePrestatore.DatiAnagrafici = DatiAnagraficiCedenteType()
        fatturapa_fp = company.fatturapa_fiscal_position_id
        if not fatturapa_fp:
            raise orm.except_orm(
                _('Error!'), _('FatturaPA fiscal position not set.'))
        CedentePrestatore.DatiAnagrafici.IdFiscaleIVA = IdFiscaleType(
            IdPaese=company.country_id.code, IdCodice=company.vat[2:])
        CedentePrestatore.DatiAnagrafici.Anagrafica = AnagraficaType(
            Denominazione=company.name)

        # not using for now
        '''
        Anagrafica = DatiAnagrafici.find('Anagrafica')
        Nome = Anagrafica.find('Nome')
        Cognome = Anagrafica.find('Cognome')
        Titolo = Anagrafica.find('Titolo')
        Anagrafica.remove(Nome)
        Anagrafica.remove(Cognome)
        Anagrafica.remove(Titolo)
        '''
        # TODO
        # Anagrafica.remove(Anagrafica.find('CodEORI'))

        if company.partner_id.fiscalcode:
            CedentePrestatore.DatiAnagrafici.CodiceFiscale = (
                company.partner_id.fiscalcode)
        CedentePrestatore.DatiAnagrafici.RegimeFiscale = fatturapa_fp.code
        return True

    def _setAlboProfessionaleCedente(self, cr, uid, CedentePrestatore,
                                     company, context=None):
        if context is None:
            context = {}
        # TODO Albo professionale, for now the main company is considered
        # to be a legal entity and not a single person
        # 1.2.1.4   <AlboProfessionale>
        # 1.2.1.5   <ProvinciaAlbo>
        # 1.2.1.6   <NumeroIscrizioneAlbo>
        # 1.2.1.7   <DataIscrizioneAlbo>

    def _setSedeCedente(self, cr, uid, CedentePrestatore,
                        company, context=None):
        if context is None:
            context = {}

        if not company.street:
            raise orm.except_orm(
                _('Error!'), _('Street not set.'))
        if not company.zip:
            raise orm.except_orm(
                _('Error!'), _('ZIP not set.'))
        if not company.city:
            raise orm.except_orm(
                _('Error!'), _('City not set.'))
        if not company.partner_id.state_id:
            raise orm.except_orm(
                _('Error!'), _('Province not set.'))
        if not company.country_id:
            raise orm.except_orm(
                _('Error!'), _('Country not set.'))
        # FIXME: manage address number in <NumeroCivico>
        # see https://github.com/OCA/partner-contact/pull/96
        CedentePrestatore.Sede = IndirizzoType(
            Indirizzo=company.street,
            CAP=company.zip,
            Comune=company.city,
            Provincia=company.partner_id.state_id.code,
            Nazione=company.country_id.code)

        return True

    def _setStabileOrganizzazione(self, cr, uid, CedentePrestatore,
                                  company, context=None):
        if context is None:
            context = {}
        # TODO: fill this section

    def _setRea(self, cr, uid, CedentePrestatore, company, context=None):
        if context is None:
            context = {}

        if company.fatturapa_rea_office and company.fatturapa_rea_number:
            CedentePrestatore.IscrizioneREA = IscrizioneREAType(
                Ufficio=company.fatturapa_rea_office.name,
                NumeroREA=company.fatturapa_rea_number,
                CapitaleSociale=company.fatturapa_rea_capital,
                SocioUnico=(company.fatturapa_rea_partner or None),
                StatoLiquidazione=company.fatturapa_rea_liquidation
                )

    def _setContatti(self, cr, uid, CedentePrestatore,
                     company, context=None):
        if context is None:
            context = {}
        # TODO: fill this section

    def _setPubAdministrationRef(self, cr, uid, CedentePrestatore,
                                 company, context=None):
        if context is None:
            context = {}
        if company.fatturapa_pub_administration_ref:
            CedentePrestatore.RiferimentoAmministrazione = (
                company.fatturapa_pub_administration_ref)

    def setCedentePrestatore(self, cr, uid, company, context=None):
        self.fatturapa.FatturaElettronicaHeader.CedentePrestatore = (
            CedentePrestatoreType())
        self._setDatiAnagraficiCedente(
            cr, uid, self.fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company, context=context)
        self._setSedeCedente(
            cr, uid, self.fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company, context=context)
        self._setAlboProfessionaleCedente(
            cr, uid, self.fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company, context=context)
        self._setStabileOrganizzazione(
            cr, uid, self.fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company, context=context)
        # FIXME: add Contacts
        self._setRea(
            cr, uid, self.fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company, context=context)
        self._setContatti(
            cr, uid, self.fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company, context=context)
        self._setPubAdministrationRef(
            cr, uid, self.fatturapa.FatturaElettronicaHeader.CedentePrestatore,
            company, context=context)

    def _setDatiAnagraficiCessionario(
            self, cr, uid, partner, context=None):
        if context is None:
            context = {}
        self.fatturapa.FatturaElettronicaHeader.CessionarioCommittente.\
            DatiAnagrafici = DatiAnagraficiCessionarioType()

        if partner.fiscalcode:
            self.fatturapa.FatturaElettronicaHeader.CessionarioCommittente.\
                DatiAnagrafici.CodiceFiscale = partner.fiscalcode
        if not partner.vat:
            raise orm.except_orm(
                _('Error!'), _('Partner VAT not set.'))
        self.fatturapa.FatturaElettronicaHeader.CessionarioCommittente.\
            DatiAnagrafici.IdFiscaleIVA = IdFiscaleType(
                IdPaese=partner.vat[0:2], IdCodice=partner.vat[2:])
        self.fatturapa.FatturaElettronicaHeader.CessionarioCommittente.\
            DatiAnagrafici.Anagrafica = AnagraficaType(
                Denominazione=partner.name)

        # not using for now
        '''
        Anagrafica = DatiAnagrafici.find('Anagrafica')
        Nome = Anagrafica.find('Nome')
        Cognome = Anagrafica.find('Cognome')
        Titolo = Anagrafica.find('Titolo')
        Anagrafica.remove(Nome)
        Anagrafica.remove(Cognome)
        Anagrafica.remove(Titolo)
        '''

        if partner.eori_code:
            self.fatturapa.FatturaElettronicaHeader.CessionarioCommittente.\
                DatiAnagrafici.Anagrafica.CodEORI = partner.eori_code

        return True

    def _setSedeCessionario(self, cr, uid, partner, context=None):
        if context is None:
            context = {}

        if not partner.street:
            raise orm.except_orm(
                _('Error!'), _('Partner street not set.'))
        if not partner.zip:
            raise orm.except_orm(
                _('Error!'), _('Partner ZIP not set.'))
        if not partner.city:
            raise orm.except_orm(
                _('Error!'), _('Partner city not set.'))
        if not partner.state_id:
            raise orm.except_orm(
                _('Error!'), _('Partner province not set.'))
        if not partner.country_id:
            raise orm.except_orm(
                _('Error!'), _('Partner country not set.'))

        # FIXME: manage address number in <NumeroCivico>
        self.fatturapa.FatturaElettronicaHeader.CessionarioCommittente.Sede = (
            IndirizzoType(
                Indirizzo=partner.street,
                CAP=partner.zip,
                Comune=partner.city,
                Provincia=partner.state_id.code,
                Nazione=partner.country_id.code))

        return True

    def setRappresentanteFiscale(
            self, cr, uid, company, context=None):
        if context is None:
            context = {}

        if company.fatturapa_tax_representative:
            # TODO: RappresentanteFiscale should be usefull for foreign
            # companies sending invoices to italian PA only
            raise orm.except_orm(
                _("Error"), _("RappresentanteFiscale not handled"))
        '''
            partner = company.fatturapa_tax_representative

        DatiAnagrafici = RappresentanteFiscale.find('DatiAnagrafici')

        if not partner.fiscalcode:
            raise orm.except_orm(
                _('Error!'), _('RappresentanteFiscale Partner '
                               'fiscalcode not set.'))

        DatiAnagrafici.find('CodiceFiscale').text = partner.fiscalcode

        if not partner.vat:
            raise orm.except_orm(
                _('Error!'), _('RappresentanteFiscale Partner VAT not set.'))
        DatiAnagrafici.find(
            'IdFiscaleIVA/IdPaese').text = partner.vat[0:2]
        DatiAnagrafici.find(
            'IdFiscaleIVA/IdCodice').text = partner.vat[2:]
        DatiAnagrafici.find('Anagrafica/Denominazione').text = partner.name
        if partner.eori_code:
            DatiAnagrafici.find(
                'Anagrafica/CodEORI').text = partner.codiceEORI
        '''
        return True

    def setCessionarioCommittente(self, cr, uid, partner, context=None):
        self.fatturapa.FatturaElettronicaHeader.CessionarioCommittente = (
            CessionarioCommittenteType())
        self._setDatiAnagraficiCessionario(cr, uid, partner, context=context)
        self._setSedeCessionario(cr, uid, partner, context=context)

    def setTerzoIntermediarioOSoggettoEmittente(
            self, cr, uid, company, context=None):
        if context is None:
            context = {}

        if company.fatturapa_sender_partner:
            # TODO
            raise orm.except_orm(
                _("Error"),
                _("TerzoIntermediarioOSoggettoEmittente not handled"))

        '''
        DatiAnagrafici = TerzoIntermediarioOSoggettoEmittente.find(
            'DatiAnagrafici'
            )

        if not partner.fiscalcode:
            raise orm.except_orm(
                _('Error!'), _('TerzoIntermediarioOSoggettoEmittente Partner '
                               'fiscalcode not set.'))

        DatiAnagrafici.find('CodiceFiscale').text = partner.fiscalcode

        if not partner.vat:
            raise orm.except_orm(
                _('Error!'), _('TerzoIntermediarioOSoggettoEmittente '
                               'Partner VAT not set.'))
        DatiAnagrafici.find(
            'IdFiscaleIVA/IdPaese').text = partner.vat[0:2]
        DatiAnagrafici.find(
            'IdFiscaleIVA/IdCodice').text = partner.vat[2:]
        DatiAnagrafici.find('Anagrafica/Denominazione').text = partner.name
        if partner.eori_code:
            DatiAnagrafici.find(
                'Anagrafica/CodEORI').text = partner.codiceEORI
        '''
        return True

    def setSoggettoEmittente(self, cr, uid, context=None):
        if context is None:
            context = {}

        # FIXME: this record is to be checked invoice by invoice
        # so a control is needed to verify that all invoices are
        # of type CC, TZ or internally created by the company

        # SoggettoEmittente.text = 'CC'
        return True

    def setDatiGeneraliDocumento(self, cr, uid, invoice, body, context=None):
        if context is None:
            context = {}

        # TODO DatiSAL

        # TODO DatiDDT

        body.DatiGenerali = DatiGeneraliType()
        if not invoice.number:
            raise orm.except_orm(
                _('Error!'),
                _('Invoice does not have a number.'))

        # TODO: TipoDocumento
        body.DatiGenerali.DatiGeneraliDocumento = DatiGeneraliDocumentoType(
            TipoDocumento='TD01',
            Divisa=invoice.currency_id.name,
            Data=invoice.date_invoice,
            Numero=invoice.number)

        # TODO: DatiRitenuta, DatiBollo, DatiCassaPrevidenziale,
        # ScontoMaggiorazione, ImportoTotaleDocumento, Arrotondamento,
        # Causale

        if invoice.company_id.fatturapa_art73:
            body.DatiGenerali.DatiGeneraliDocumento.Art73 = 'SI'

        return True

    def setRelatedDocumentTypes(self, cr, uid, invoice, body,
                                context=None):
        linecount = 1
        for line in invoice.invoice_line:
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
                eval(
                    "body.DatiGenerali." +
                    doc_type + ".append(documento)")
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
            eval(
                "body.DatiGenerali." +
                doc_type + ".append(documento)")
        return True

    def setDatiTrasporto(self, cr, uid, invoice, body, context=None):
        if context is None:
            context = {}

        return True

    def setDettaglioLinee(self, cr, uid, invoice, body, context=None):
        if context is None:
            context = {}

        body.DatiBeniServizi = DatiBeniServiziType()
        # TipoCessionePrestazione not handled

        # TODO CodiceArticolo

        line_no = 1
        for line in invoice.invoice_line:
            if not line.invoice_line_tax_id:
                raise orm.except_orm(
                    _('Error'),
                    _("Invoice line %s does not have tax") % line.name)
            if len(line.invoice_line_tax_id) > 1:
                raise orm.except_orm(
                    _('Error'),
                    _("Too many taxes for invoice line %s") % line.name)
            aliquota = line.invoice_line_tax_id[0].amount*100
            AliquotaIVA = '%.2f' % (aliquota)
            DettaglioLinea = DettaglioLineeType(
                NumeroLinea=str(line_no),
                Descrizione=line.name,
                PrezzoUnitario='%.2f' % line.price_unit,
                Quantita='%.2f' % line.quantity,
                UnitaMisura=line.uos_id and (
                    unidecode(line.uos_id.name)) or None,
                PrezzoTotale='%.2f' % line.price_subtotal,
                AliquotaIVA=AliquotaIVA)
            if aliquota == 0.0:
                if not line.invoice_line_tax_id[0].non_taxable_nature:
                    raise orm.except_orm(
                        _('Error'),
                        _("No 'nature' field for tax %s") %
                        line.invoice_line_tax_id[0].name)
                DettaglioLinea.Natura = line.invoice_line_tax_id[
                    0
                    ].non_taxable_nature
            line_no += 1

            # not handled
            '''
            el.remove(el.find('DataInizioPeriodo'))
            el.remove(el.find('DataFinePeriodo'))
            el.remove(el.find('ScontoMaggiorazione'))
            el.remove(el.find('Ritenuta'))
            el.remove(el.find('RiferimentoAmministrazione'))
            el.remove(el.find('AltriDatiGestionali'))
            '''

            body.DatiBeniServizi.DettaglioLinee.append(DettaglioLinea)

        return True

    def setDatiRiepilogo(self, cr, uid, invoice, body, context=None):
        if context is None:
            context = {}
        tax_pool = self.pool['account.tax']
        for tax_line in invoice.tax_line:
            tax_id = self.pool['account.tax'].get_tax_by_invoice_tax(
                cr, uid, tax_line.name, context=context)
            tax = tax_pool.browse(cr, uid, tax_id, context=context)
            riepilogo = DatiRiepilogoType(
                AliquotaIVA='%.2f' % tax.amount,
                ImponibileImporto='%.2f' % tax_line.base,
                Imposta='%.2f' % tax_line.amount
                )
            if tax.amount == 0.0:
                if not tax.non_taxable_nature:
                    raise orm.except_orm(
                        _('Error'),
                        _("No 'nature' field for tax %s") % tax.name)
                riepilogo.Natura = tax.non_taxable_nature
            # TODO
            '''
            el.remove(el.find('SpeseAccessorie'))
            el.remove(el.find('Arrotondamento'))
            el.remove(el.find('EsigibilitaIVA'))
            el.remove(el.find('RiferimentoNormativo'))
            '''

            body.DatiBeniServizi.DatiRiepilogo.append(riepilogo)

        return True

    def setDatiPagamento(self, cr, uid, invoice, body, context=None):
        if context is None:
            context = {}

        """ TODO
        DettaglioPagamento = DatiPagamento.find('DettaglioPagamento')
        if (
            invoice.payment_term and invoice.payment_term.fatturapa_pt_id
            and invoice.payment_term.fatturapa_pt_id.code
        ):
            DatiPagamento.find(
                'CondizioniPagamento'
                ).text = invoice.payment_term.fatturapa_pt_id.code
        else:
            raise orm.except_orm(
                _("Error"), _(""))

        # TODO: multiple installments
        if (
            invoice.payment_term and invoice.payment_term.fatturapa_pm_id
            and invoice.payment_term.fatturapa_pm_id.code
        ):
            DettaglioPagamento.find(
                'ModalitaPagamento'
                ).text = invoice.payment_term.fatturapa_pm_id.code
        DettaglioPagamento.find(
            'DataScadenzaPagamento').text = invoice.date_due
        DettaglioPagamento.find(
            'ImportoPagamento').text = unicode(invoice.amount_total)
        """

        return True

    def setFatturaElettronicaHeader(self, cr, uid, company,
                                    partner, context=None):
        if context is None:
            context = {}
        self.fatturapa.FatturaElettronicaHeader = (
            FatturaElettronicaHeaderType())
        self.setDatiTrasmissione(cr, uid, company, partner, context=context)
        self.setCedentePrestatore(cr, uid, company, context=context)
        self.setRappresentanteFiscale(cr, uid, company, context=context)
        self.setCessionarioCommittente(
            cr, uid, partner, context=context)
        self.setTerzoIntermediarioOSoggettoEmittente(
            cr, uid, company, context=context)
        self.setSoggettoEmittente(cr, uid, context=context)

    def setFatturaElettronicaBody(
        self, cr, uid, inv, FatturaElettronicaBody, context=None
    ):
        if context is None:
            context = {}

        self.setDatiGeneraliDocumento(
            cr, uid, inv, FatturaElettronicaBody, context=context)
        self.setRelatedDocumentTypes(cr, uid, inv, FatturaElettronicaBody,
                                     context=context)
        self.setDatiTrasporto(
            cr, uid, inv, FatturaElettronicaBody, context=context)
        self.setDettaglioLinee(
            cr, uid, inv, FatturaElettronicaBody, context=context)
        self.setDatiRiepilogo(
            cr, uid, inv, FatturaElettronicaBody, context=context)
        self.setDatiPagamento(
            cr, uid, inv, FatturaElettronicaBody, context=context)

    def getPartnerId(self, cr, uid, invoice_ids, context=None):
        if context is None:
            context = {}

        invoice_model = self.pool['account.invoice']
        partner = False

        invoices = invoice_model.browse(cr, uid, invoice_ids, context=context)

        for invoice in invoices:
            if not partner:
                partner = invoice.partner_id
            if invoice.partner_id != partner:
                raise orm.except_orm(
                    _('Error!'),
                    _('Invoices must belong to the same partner'))

        return partner

    def exportFatturaPA(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        # self.setNameSpace()

        model_data_obj = self.pool['ir.model.data']
        invoice_obj = self.pool['account.invoice']

        # content = self.getFile('fatturapa_v1.1.xml').decode('base64')
        # self.template = ElementTree(fromstring(content))
        # tmpl = self.template
        # root = tmpl.getroot()

        self.fatturapa = FatturaElettronica(versione='1.1')
        invoice_ids = context.get('active_ids', False)
        partner = self.getPartnerId(cr, uid, invoice_ids, context=context)

        user_obj = self.pool['res.users']
        company = user_obj.browse(cr, uid, uid).company_id
        try:
            self.setFatturaElettronicaHeader(cr, uid, company,
                                             partner, context=context)
            for invoice_id in invoice_ids:
                inv = invoice_obj.browse(cr, uid, invoice_id, context=context)
                if inv.fatturapa_attachment_out_id:
                    raise orm.except_orm(
                        _("Error"),
                        _("Invoice %s has FatturaPA Export File yet") % (
                            inv.number))
                invoice_body = FatturaElettronicaBodyType()
                self.setFatturaElettronicaBody(
                    cr, uid, inv, invoice_body, context=context)
                self.fatturapa.FatturaElettronicaBody.append(invoice_body)
                # TODO DatiVeicoli

            self.setProgressivoInvio(cr, uid, context=context)
        except SimpleFacetValueError as e:
            raise orm.except_orm(
                _("Error"),
                (unicode(e)))

        attach_id = self.saveAttachment(cr, uid, context=context)

        for invoice_id in invoice_ids:
            inv = invoice_obj.browse(cr, uid, invoice_id)
            inv.write({'fatturapa_attachment_out_id': attach_id})

        view_rec = model_data_obj.get_object_reference(
            cr, uid, 'l10n_it_fatturapa_out',
            'view_fatturapa_out_attachment_form')
        if view_rec:
            view_id = view_rec and view_rec[1] or False

        return {
            'view_type': 'form',
            'name': "Export FatturaPA",
            'view_id': [view_id],
            'res_id': attach_id,
            'view_mode': 'form',
            'res_model': 'fatturapa.attachment.out',
            'type': 'ir.actions.act_window',
            'context': context
            }
