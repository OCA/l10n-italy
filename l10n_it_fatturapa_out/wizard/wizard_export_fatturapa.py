# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Davide Corio <davide.corio@lsweb.it>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import base64
import copy
import re
import tempfile

from openerp.osv import orm
from openerp import addons
from openerp.tools.translate import _
from lxml.etree import fromstring, tostring, ElementTree
from lxml.etree import register_namespace


class WizardExportFatturapa(orm.TransientModel):
    _name = "wizard.export.fatturapa"
    _description = "Export FatturaPA"

    document_type = {
        'order': 'DatiOrdineAcquisto',
        'contract': 'DatiContratto',
        'agreement': 'DatiConvenzione',
        'reception': 'DatiRicezione',
        'invoice': 'DatiFattureCollegate',
    }

    def __init__(self, cr, uid, **kwargs):
        self.template = False
        self.number = False
        self.tree = False
        super(WizardExportFatturapa, self).__init__(cr, uid, **kwargs)

    def getFile(self, filename, context=None):
        if not context:
            context = {}

        path = addons.get_module_resource(
            'l10n_it_fatturapa', 'data', filename)
        with open(path) as test_data:
            with tempfile.TemporaryFile() as out:
                base64.encode(test_data, out)
                out.seek(0)
                return out.read()

    def setNameSpace(self):
        register_namespace('ds', "http://www.w3.org/2000/09/xmldsig#")
        register_namespace(
            'p', "http://www.fatturapa.gov.it/sdi/fatturapa/v1.1")
        register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")

    def saveAttachment(self, cr, uid, context=None):
        if not context:
            context = {}

        tmpl = self.template
        number = self.number

        user_obj = self.pool['res.users']
        company = user_obj.browse(cr, uid, uid).company_id

        if not company.vat:
            raise orm.except_orm(
                _('Error!'), _('Company TIN not set.'))

        attach_obj = self.pool['fatturapa.attachment.out']
        root = tmpl.getroot()
        header = """<?xml version="1.0" encoding="UTF-8"?>\n"""
        attach_data = tostring(root, encoding='utf-8', method='xml')
        attach_data = header+attach_data
        attach_vals = {
            'name': '%s_%s.xml' % (company.vat, str(number)),
            'datas_fname': '%s_%s.xml' % (company.vat, str(number)),
            'datas': base64.encodestring(attach_data),
        }
        attach_id = attach_obj.create(cr, uid, attach_vals, context=context)

        return attach_id

    def setProgressivoInvio(self, cr, uid, context=None):
        if not context:
            context = {}

        tmpl = self.template

        user_obj = self.pool['res.users']
        company = user_obj.browse(cr, uid, uid).company_id
        sequence_obj = self.pool['ir.sequence']
        fatturapa_sequence = company.fatturapa_sequence_id

        if not fatturapa_sequence:
            raise orm.except_orm(
                _('Error!'), _('FatturaPA sequence not configured.'))

        self.number = number = sequence_obj.next_by_id(
            cr, uid, fatturapa_sequence.id, context=context)

        ProgressivoInvio = tmpl.find(
            'FatturaElettronicaHeader/DatiTrasmissione/ProgressivoInvio')
        ProgressivoInvio.text = number

        return True

    def _setIdTrasmittente(self, cr, uid, company, context=None):
        if not context:
            context = {}

        tmpl = self.template

        IdTrasmittente = tmpl.find(
            'FatturaElettronicaHeader/DatiTrasmissione/IdTrasmittente')

        if not company.country_id:
            raise orm.except_orm(
                _('Error!'), _('Company Country not set.'))
        IdPaese = company.country_id.code
        IdTrasmittente.find('IdPaese').text = IdPaese

        IdCodice = company.partner_id.fiscalcode
        if not IdCodice:
            IdCodice = company.vat[2:]
        if not IdCodice:
            raise orm.except_orm(
                _('Error'), _('Company does not have fiscal code or VAT'))
        IdTrasmittente.find('IdCodice').text = IdCodice

        return True

    def _setFormatoTrasmissione(self, cr, uid, company, context=None):
        if not context:
            context = {}

        tmpl = self.template

        FormatoTrasmissione = tmpl.find(
            'FatturaElettronicaHeader/DatiTrasmissione/FormatoTrasmissione')

        if not company.fatturapa_format_id:
            raise orm.except_orm(
                _('Error!'), _('FatturaPA format not set.'))
        FormatoTrasmissione.text = company.fatturapa_format_id.code

        return True

    def _setCodiceDestinatario(self, cr, uid, partner, context=None):
        if not context:
            context = {}

        tmpl = self.template
        code = partner.fatturapa_code

        CodiceDestinatario = tmpl.find(
            'FatturaElettronicaHeader/DatiTrasmissione/CodiceDestinatario')

        if not code:
            raise orm.except_orm(
                _('Error!'), _('FatturaPA Code not set on partner form.'))
        CodiceDestinatario.text = code.upper()

        return True

    def _setContattiTrasmittente(self, cr, uid, company, context=None):
        if not context:
            context = {}

        tmpl = self.template

        ContattiTrasmittente = tmpl.find(
            'FatturaElettronicaHeader/DatiTrasmissione/ContattiTrasmittente')

        if not company.phone:
            raise orm.except_orm(
                _('Error!'), _('Company Telephone number not set.'))
        Telefono = company.phone
        ContattiTrasmittente.find('Telefono').text = Telefono

        if not company.email:
            raise orm.except_orm(
                _('Error!'), _('Email address not set.'))
        Email = company.email
        ContattiTrasmittente.find('Email').text = Email

        return True

    def setDatiTrasmissione(self, cr, uid, company, partner, context=None):
        if not context:
            context = {}
        self._setIdTrasmittente(cr, uid, company, context=context)
        self._setFormatoTrasmissione(cr, uid, company, context=context)
        self._setCodiceDestinatario(cr, uid, partner, context=context)
        self._setContattiTrasmittente(cr, uid, company, context=context)

    def _setDatiAnagraficiCedente(self, cr, uid, CedentePrestatore,
                                  company, context=None):
        if not context:
            context = {}

        DatiAnagrafici = CedentePrestatore.find('DatiAnagrafici')

        if not company.vat:
            raise orm.except_orm(
                _('Error!'), _('TIN not set.'))

        fatturapa_fp = company.fatturapa_fiscal_position_id
        if not fatturapa_fp:
            raise orm.except_orm(
                _('Error!'), _('FatturaPA fiscal position not set.'))
        DatiAnagrafici.find(
            'IdFiscaleIVA/IdPaese').text = company.country_id.code
        DatiAnagrafici.find(
            'IdFiscaleIVA/IdCodice').text = company.vat[2:]
        DatiAnagrafici.find(
            'Anagrafica/Denominazione').text = company.name

        # not using for now
        Anagrafica = DatiAnagrafici.find('Anagrafica')
        Nome = Anagrafica.find('Nome')
        Cognome = Anagrafica.find('Cognome')
        Titolo = Anagrafica.find('Titolo')
        Anagrafica.remove(Nome)
        Anagrafica.remove(Cognome)
        Anagrafica.remove(Titolo)
        # TODO
        Anagrafica.remove(Anagrafica.find('CodEORI'))

        CodiceFiscale = DatiAnagrafici.find('CodiceFiscale')
        if company.partner_id.fiscalcode:
            CodiceFiscale.text = company.partner_id.fiscalcode
        else:
            DatiAnagrafici.remove(CodiceFiscale)
        DatiAnagrafici.find('RegimeFiscale').text = fatturapa_fp.code
        return True

    def _setAlboProfessionaleCedente(self, cr, uid, CedentePrestatore,
                                     company, context=None):
        # TODO Albo professionale, for now the main company is considered
        # to be a legal entity and not a single person
        # 1.2.1.4   <AlboProfessionale>
        # 1.2.1.5   <ProvinciaAlbo>
        # 1.2.1.6   <NumeroIscrizioneAlbo>
        # 1.2.1.7   <DataIscrizioneAlbo>
        DatiAnagrafici = CedentePrestatore.find('DatiAnagrafici')
        AlboProfessionale = DatiAnagrafici.find('AlboProfessionale')
        DatiAnagrafici.remove(AlboProfessionale)
        ProvinciaAlbo = DatiAnagrafici.find('ProvinciaAlbo')
        DatiAnagrafici.remove(ProvinciaAlbo)
        NumeroIscrizioneAlbo = DatiAnagrafici.find('NumeroIscrizioneAlbo')
        DatiAnagrafici.remove(NumeroIscrizioneAlbo)
        DataIscrizioneAlbo = DatiAnagrafici.find('DataIscrizioneAlbo')
        DatiAnagrafici.remove(DataIscrizioneAlbo)

    def _setSedeCedente(self, cr, uid, CedentePrestatore,
                        company, context=None):
        if not context:
            context = {}

        Sede = CedentePrestatore.find('Sede')

        if not company.street:
            raise orm.except_orm(
                _('Error!'), _('Street not set.'))
        if not company.zip:
            raise orm.except_orm(
                _('Error!'), _('ZIP not set.'))
        if not company.city:
            raise orm.except_orm(
                _('Error!'), _('City not set.'))
        if not company.partner_id.province:
            raise orm.except_orm(
                _('Error!'), _('Province not set.'))
        if not company.country_id:
            raise orm.except_orm(
                _('Error!'), _('Country not set.'))
        # FIXME: manage address number in <NumeroCivico>
        # see https://github.com/OCA/partner-contact/pull/96
        NumeroCivico = Sede.find('NumeroCivico')
        Sede.remove(NumeroCivico)
        Sede.find('Indirizzo').text = company.street
        Sede.find('CAP').text = company.zip
        Sede.find('Comune').text = company.city
        Sede.find('Provincia').text = company.partner_id.province.code
        Sede.find('Nazione').text = company.country_id.code

        return True

    def _setStabileOrganizzazione(self, cr, uid, CedentePrestatore,
                                  company, context=None):
        if not context:
            context = {}

        StabileOrganizzazione = CedentePrestatore.find('StabileOrganizzazione')
        # TODO: fill this section
        CedentePrestatore.remove(StabileOrganizzazione)

    def _setRea(self, cr, uid, CedentePrestatore, company, context=None):
        if not context:
            context = {}

        IscrizioneRea = CedentePrestatore.find('IscrizioneREA')
        if company.fatturapa_rea_office and company.fatturapa_rea_number:
            IscrizioneRea.find(
                'Ufficio'
                ).text = company.fatturapa_rea_office.name
            IscrizioneRea.find('NumeroREA').text = company.fatturapa_rea_number
            IscrizioneRea.find(
                'CapitaleSociale'
                ).text = '%.2f' % company.fatturapa_rea_capital
            IscrizioneRea.find('SocioUnico').text = company.\
                fatturapa_rea_partner or None
            IscrizioneRea.find('StatoLiquidazione').text = company.\
                fatturapa_rea_liquidation
        else:
            CedentePrestatore.remove(IscrizioneRea)

    def _setContatti(self, cr, uid, CedentePrestatore,
                     company, context=None):
        if not context:
            context = {}

        Contatti = CedentePrestatore.find('Contatti')
        # TODO: fill this section
        CedentePrestatore.remove(Contatti)

    def _setPubAdministrationRef(self, cr, uid, CedentePrestatore,
                                 company, context=None):
        if not context:
            context = {}
        RiferimentoAmministrazione = CedentePrestatore.find(
            'RiferimentoAmministrazione'
        )
        if company.fatturapa_pub_administration_ref:
            RiferimentoAmministrazione.text = \
                company.fatturapa_pub_administration_ref
        else:
            CedentePrestatore.remove(RiferimentoAmministrazione)

    def setCedentePrestatore(self, cr, uid, company, context=None):
        tmpl = self.template
        CedentePrestatore = tmpl.find(
            'FatturaElettronicaHeader/CedentePrestatore')
        self._setDatiAnagraficiCedente(cr, uid, CedentePrestatore,
                                       company, context=context)
        self._setSedeCedente(cr, uid, CedentePrestatore,
                             company, context=context)
        self._setAlboProfessionaleCedente(cr, uid, CedentePrestatore,
                                          company, context=context)
        self._setStabileOrganizzazione(cr, uid, CedentePrestatore,
                                       company, context=context)
        # FIXME: add Contacts
        self._setRea(cr, uid, CedentePrestatore,
                     company, context=context)
        self._setContatti(cr, uid, CedentePrestatore,
                          company, context=context)
        self._setPubAdministrationRef(cr, uid, CedentePrestatore,
                                      company, context=context)

    def _setDatiAnagraficiCessionario(
            self, cr, uid, partner, context=None):
        if not context:
            context = {}

        tmpl = self.template

        DatiAnagrafici = tmpl.find(
            'FatturaElettronicaHeader/CessionarioCommittente/DatiAnagrafici')

        CodiceFiscale = DatiAnagrafici.find('CodiceFiscale')
        if not partner.fiscalcode:
            DatiAnagrafici.remove(CodiceFiscale)
        else:
            CodiceFiscale.text = partner.fiscalcode
        if not partner.vat:
            raise orm.except_orm(
                _('Error!'), _('Partner fiscalcode not set.'))
        DatiAnagrafici.find(
            'IdFiscaleIVA/IdPaese').text = partner.vat[0:2]
        DatiAnagrafici.find(
            'IdFiscaleIVA/IdCodice').text = partner.vat[2:]
        DatiAnagrafici.find('Anagrafica/Denominazione').text = partner.name

        # not using for now
        Anagrafica = DatiAnagrafici.find('Anagrafica')
        Nome = Anagrafica.find('Nome')
        Cognome = Anagrafica.find('Cognome')
        Titolo = Anagrafica.find('Titolo')
        Anagrafica.remove(Nome)
        Anagrafica.remove(Cognome)
        Anagrafica.remove(Titolo)

        CodiceEORI = DatiAnagrafici.find('Anagrafica/CodEORI')
        if partner.eori_code:
            CodiceEORI.text = partner.eori_code
        else:
            DatiAnagrafici.remove(CodiceEORI)

        return True

    def _setSedeCessionario(self, cr, uid, partner, context=None):
        if not context:
            context = {}

        tmpl = self.template

        Sede = tmpl.find(
            'FatturaElettronicaHeader/CessionarioCommittente/Sede')

        if not partner.street:
            raise orm.except_orm(
                _('Error!'), _('Partner street not set.'))
        if not partner.zip:
            raise orm.except_orm(
                _('Error!'), _('Partner ZIP not set.'))
        if not partner.city:
            raise orm.except_orm(
                _('Error!'), _('Partner city not set.'))
        if not partner.province:
            raise orm.except_orm(
                _('Error!'), _('Partner province not set.'))
        if not partner.country_id:
            raise orm.except_orm(
                _('Error!'), _('Partner country not set.'))

        # FIXME: manage address number in <NumeroCivico>
        NumeroCivico = Sede.find('NumeroCivico')
        Sede.remove(NumeroCivico)
        Sede.find('Indirizzo').text = partner.street
        Sede.find('CAP').text = partner.zip
        Sede.find('Comune').text = partner.city
        Sede.find('Provincia').text = partner.province.code
        Sede.find('Nazione').text = partner.country_id.code

        return True

    def setRappresentanteFiscale(
            self, cr, uid, company, context=None):
        if not context:
            context = {}

        tmpl = self.template

        FatturaElettronicaHeader = tmpl.find('FatturaElettronicaHeader')

        RappresentanteFiscale = FatturaElettronicaHeader.find(
            'RappresentanteFiscale')

        if not company.fatturapa_tax_representative:
            FatturaElettronicaHeader.remove(RappresentanteFiscale)
            return True
        else:
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
        return True

    def setCessionarioCommittente(self, cr, uid, partner, context=None):
        self._setDatiAnagraficiCessionario(cr, uid, partner, context=context)
        self._setSedeCessionario(cr, uid, partner, context=context)

    def setTerzoIntermediarioOSoggettoEmittente(
            self, cr, uid, company, context=None):
        if not context:
            context = {}

        tmpl = self.template

        FatturaElettronicaHeader = tmpl.find('FatturaElettronicaHeader')

        TerzoIntermediarioOSoggettoEmittente = FatturaElettronicaHeader.find(
            'TerzoIntermediarioOSoggettoEmittente')

        if not company.fatturapa_sender_partner:
            FatturaElettronicaHeader.remove(
                TerzoIntermediarioOSoggettoEmittente
            )
            return True
        else:
            partner = company.fatturapa_sender_partner

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
        return True

    def setSoggettoEmittente(self, cr, uid, context=None):
        if not context:
            context = {}

        tmpl = self.template
        # FIXME: this record is to be checked invoice by invoice
        # so a control is needed to verify that all invoices are
        # of type CC, TZ or internally created by the company

        # SoggettoEmittente.text = 'CC'
        FatturaElettronicaHeader = tmpl.find(
            'FatturaElettronicaHeader')
        SoggettoEmittente = FatturaElettronicaHeader.find(
            'SoggettoEmittente')
        FatturaElettronicaHeader.remove(SoggettoEmittente)
        return True

    def setDatiGeneraliDocumento(self, cr, uid, invoice, body, context=None):
        if not context:
            context = {}

        DatiGenerali = body.find('DatiGenerali')
        # TODO DatiSAL
        DatiSAL = DatiGenerali.find('DatiSAL')
        DatiGenerali.remove(DatiSAL)

        # TODO DatiDDT
        DatiDDT = DatiGenerali.find('DatiDDT')
        DatiGenerali.remove(DatiDDT)

        DatiGeneraliDocumento = body.find('DatiGenerali/DatiGeneraliDocumento')

        if not invoice.number:
            raise orm.except_orm(
                _('Error!'),
                _('Invoice does not have a number.'))

        # TODO: TipoDocumento
        DatiGeneraliDocumento.find('TipoDocumento').text = 'TD01'
        DatiGeneraliDocumento.find('Divisa').text = invoice.currency_id.name
        DatiGeneraliDocumento.find('Data').text = invoice.date_invoice
        DatiGeneraliDocumento.find('Numero').text = invoice.number

        # TODO: DatiRitenuta, DatiBollo, DatiCassaPrevidenziale,
        # ScontoMaggiorazione, ImportoTotaleDocumento, Arrotondamento,
        # Causale
        DatiRitenuta = DatiGeneraliDocumento.find('DatiRitenuta')
        DatiGeneraliDocumento.remove(DatiRitenuta)
        DatiBollo = DatiGeneraliDocumento.find('DatiBollo')
        DatiGeneraliDocumento.remove(DatiBollo)
        DatiCassaPrevidenziale = DatiGeneraliDocumento.find(
            'DatiCassaPrevidenziale')
        DatiGeneraliDocumento.remove(DatiCassaPrevidenziale)
        ScontoMaggiorazione = DatiGeneraliDocumento.find(
            'ScontoMaggiorazione')
        DatiGeneraliDocumento.remove(ScontoMaggiorazione)
        ImportoTotaleDocumento = DatiGeneraliDocumento.find(
            'ImportoTotaleDocumento')
        DatiGeneraliDocumento.remove(ImportoTotaleDocumento)
        Arrotondamento = DatiGeneraliDocumento.find(
            'Arrotondamento')
        DatiGeneraliDocumento.remove(Arrotondamento)
        Causale = DatiGeneraliDocumento.find(
            'Causale')
        DatiGeneraliDocumento.remove(Causale)

        Art73 = DatiGeneraliDocumento.find('Art73')
        if invoice.company_id.fatturapa_art73:
            Art73.text = 'SI'
        else:
            DatiGeneraliDocumento.remove(Art73)

        return True

    def setRelatedDocumentTypes(self, cr, uid, invoice, body,
                                context=None):
        written_types = [k for k in self.document_type]
        DatiGenerali = body.find('DatiGenerali')
        for line in invoice.invoice_line:
            for related_document in line.related_documents:
                Dati = DatiGenerali.find(
                    self.document_type[related_document.type]
                )
                Dati.find(
                    'IdDocumento').text = related_document.name
                RiferimentoNumeroLinea = Dati.find(
                    'RiferimentoNumeroLinea'
                )
                if related_document.lineRef:
                    RiferimentoNumeroLinea.text = str(related_document.lineRef)
                else:
                    Dati.remove(RiferimentoNumeroLinea)

                Data = Dati.find(
                    'Data'
                )
                if related_document.date:
                    Data.text = str(related_document.date)
                else:
                    Dati.remove(Data)

                NumItem = Dati.find(
                    'NumItem'
                )
                if related_document.numitem:
                    NumItem.text = str(related_document.numitem)
                else:
                    Dati.remove(NumItem)

                CodiceCommessaConvenzione = Dati.find(
                    'CodiceCommessaConvenzione'
                )
                if related_document.code:
                    CodiceCommessaConvenzione.text = str(related_document.code)
                else:
                    Dati.remove(CodiceCommessaConvenzione)

                CodiceCUP = Dati.find(
                    'CodiceCUP'
                )
                if related_document.cup:
                    CodiceCUP.text = str(related_document.cup)
                else:
                    Dati.remove(CodiceCUP)

                CodiceCIG = Dati.find(
                    'CodiceCIG'
                )
                if related_document.cig:
                    CodiceCIG.text = str(related_document.cig)
                else:
                    Dati.remove(CodiceCIG)

                written_types.pop(related_document.type)
        for typo in written_types:
            Dato = DatiGenerali.find(
                self.document_type[typo]
            )
            DatiGenerali.remove(Dato)
        return True

    def setDatiTrasporto(self, cr, uid, invoice, body, context=None):
        if not context:
            context = {}

        # TODO: DatiTrasporto
        DatiGenerali = body.find('DatiGenerali')
        DatiTrasporto = DatiGenerali.find('DatiTrasporto')

        DatiGenerali.remove(DatiTrasporto)

        return True

    def setDettaglioLinee(self, cr, uid, invoice, body, context=None):
        if not context:
            context = {}

        DatiBeniServizi = body.find('DatiBeniServizi')
        DettaglioLinee = DatiBeniServizi.find('DettaglioLinee')
        # not handled
        DettaglioLinee.remove(DettaglioLinee.find('TipoCessionePrestazione'))

        # TODO CodiceArticolo
        DettaglioLinee.remove(DettaglioLinee.find('CodiceArticolo'))

        line_no = 1
        for line in invoice.invoice_line:
            el = copy.deepcopy(DettaglioLinee)
            DatiBeniServizi.insert(0, el)
            el.find('NumeroLinea').text = str(line_no)
            el.find('Descrizione').text = line.name
            el.find(
                'PrezzoUnitario').text = '%.2f' % line.price_unit
            el.find(
                'Quantita').text = '%.2f' % line.quantity
            if line.uos_id:
                el.find('UnitaMisura').text = line.uos_id.name
            else:
                el.remove(el.find('UnitaMisura'))
            el.find(
                'PrezzoTotale').text = '%.2f' % line.price_subtotal
            if not line.invoice_line_tax_id:
                raise orm.except_orm(
                    _('Error'),
                    _("Invoice line %s does not have tax") % line.name)
            if len(line.invoice_line_tax_id) > 1:
                raise orm.except_orm(
                    _('Error'),
                    _("Too many taxes for invoice line %s") % line.name)
            el.find(
                'AliquotaIVA').text = '%.2f' % (
                    line.invoice_line_tax_id[0].amount*100)
            line_no += 1

            # not handled
            el.remove(el.find('DataInizioPeriodo'))
            el.remove(el.find('DataFinePeriodo'))
            el.remove(el.find('ScontoMaggiorazione'))
            el.remove(el.find('Ritenuta'))
            el.remove(el.find('RiferimentoAmministrazione'))
            el.remove(el.find('AltriDatiGestionali'))

            # TODO: can XML work without this, in case of 'esente IVA'?
            el.remove(el.find('Natura'))
        DatiBeniServizi.remove(DettaglioLinee)

        return True

    def setDatiRiepilogo(self, cr, uid, invoice, body, context=None):
        if not context:
            context = {}

        DatiBeniServizi = body.find('DatiBeniServizi')
        DatiRiepilogo = DatiBeniServizi.find('DatiRiepilogo')

        for tax_line in invoice.tax_line:
            el = copy.deepcopy(DatiRiepilogo)
            DatiBeniServizi.append(el)
            rates = re.findall(r'\d+%', tax_line.name)
            if len(rates) > 1:
                raise orm.except_orm(
                    _('Error'),
                    _("Too many rates found in tax line %s") % tax_line.name)
            if not rates:
                raise orm.except_orm(
                    _('Error'),
                    _("No rates found in tax line %s") % tax_line.name)
            rate = rates[0].replace('%', '')
            el.find('AliquotaIVA').text = '%.2f' % float(rate)
            el.find('ImponibileImporto').text = '%.2f' % tax_line.base
            el.find('Imposta').text = '%.2f' % tax_line.amount

            # TODO
            el.remove(el.find('Natura'))
            el.remove(el.find('SpeseAccessorie'))
            el.remove(el.find('Arrotondamento'))
            el.remove(el.find('EsigibilitaIVA'))
            el.remove(el.find('RiferimentoNormativo'))

        DatiBeniServizi.remove(DatiRiepilogo)

        return True

    def setDatiPagamento(self, cr, uid, invoice, body, context=None):
        if not context:
            context = {}

        DatiPagamento = body.find('DatiPagamento')
        body.remove(DatiPagamento)

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
        if not context:
            context = {}

        self.setDatiTrasmissione(cr, uid, company, partner, context=context)
        self.setCedentePrestatore(cr, uid, company, context=context)
        self.setRappresentanteFiscale(cr, uid, company, context=context)
        self.setCessionarioCommittente(
            cr, uid, partner, context=context)
        self.setTerzoIntermediarioOSoggettoEmittente(
            cr, uid, company, context=context)
        self.setSoggettoEmittente(cr, uid, context=context)

    def setFatturaElettronicaBody(self, cr, uid, inv, el, context=None):
        if not context:
            context = {}

        self.setDatiGeneraliDocumento(cr, uid, inv, el, context=context)
        self.setRelatedDocumentTypes(cr, uid, inv, el,
                                     context=context)
        self.setDatiTrasporto(cr, uid, inv, el, context=context)
        self.setDettaglioLinee(cr, uid, inv, el, context=context)
        self.setDatiRiepilogo(cr, uid, inv, el, context=context)
        self.setDatiPagamento(cr, uid, inv, el, context=context)

    def getPartnerId(self, cr, uid, invoice_ids, context=None):
        if not context:
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
        if not context:
            context = {}

        self.setNameSpace()

        model_data_obj = self.pool['ir.model.data']
        invoice_obj = self.pool['account.invoice']

        content = self.getFile('fatturapa_v1.1.xml').decode('base64')
        self.template = ElementTree(fromstring(content))
        tmpl = self.template
        root = tmpl.getroot()

        invoice_ids = context.get('active_ids', False)
        partner = self.getPartnerId(cr, uid, invoice_ids, context=context)

        user_obj = self.pool['res.users']
        company = user_obj.browse(cr, uid, uid).company_id

        self.setFatturaElettronicaHeader(cr, uid, company,
                                         partner, context=context)
        FatturaElettronicaBody = tmpl.find('FatturaElettronicaBody')
        for invoice_id in invoice_ids:
            el = copy.deepcopy(FatturaElettronicaBody)
            root.append(el)
            inv = invoice_obj.browse(cr, uid, invoice_id)
            self.setFatturaElettronicaBody(cr, uid, inv, el, context=context)

            # not handled
            el.remove(el.find('DatiVeicoli'))

        root.remove(FatturaElettronicaBody)
        self.setProgressivoInvio(cr, uid, context=context)

        attach_id = self.saveAttachment(cr, uid, context=context)

        for invoice_id in invoice_ids:
            inv = invoice_obj.browse(cr, uid, invoice_id)
            inv.write({'fatturapa_attachment_out_id': attach_id})

        view_rec = model_data_obj.get_object_reference(
            cr, uid, 'l10n_it_fatturapa_out', 'view_fatturapa_attachment_form')
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
