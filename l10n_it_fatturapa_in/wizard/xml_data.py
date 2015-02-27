# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 AgileBG SAGL <http://www.agilebg.com>
#    Copyright (C) 2015 innoviu Srl <http://www.innoviu.com>
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

from lxml.etree import fromstring, ElementTree
import tempfile
import base64


# TODO: use a single class to manage: CedentePrestatore,
# RappresentanteFiscale, CessionarioCommittente,
# TerzoIntermediarioOSoggettoEmittente
class CedentePrestatore():
    _name = 'Cedente Prestatore'

    cedentePrestatore = None
    idFiscaleIVA = None
    codiceFiscale = None
    nomeRappresentanteFiscale = None
    codEORI = None
    alboProfessionale = None
    provinciaAlbo = None
    numeroIscrizioneAlbo = None
    dataIscrizioneAlbo = None
    regimeFiscale = None
    # <Sede>
    indirizzo = None
    cap = None
    comune = None
    provinca = None
    nazione = None
    # <Contatti>
    telefono = None
    fax = None
    email = None

    def __init__(self, cedentePrestatore):
        self.cedentePrestatore = cedentePrestatore
        self.parseIdFiscaleIva()
        self.parseCodiceFiscale()
        self.parseCedentePrestatore()
        self.alboProfessionale = self.cedentePrestatore.find(
            'DatiAnagrafici/AlboProfessionale') is not None and \
            self.cedentePrestatore.find(
            'DatiAnagrafici/AlboProfessionale').text or None
        self.provinciaAlbo = self.cedentePrestatore.find(
            'DatiAnagrafici/ProvinciaAlbo') is not None and \
            self.cedentePrestatore.find(
            'DatiAnagrafici/ProvinciaAlbo').text or None
        self.numeroIscrizioneAlbo = self.cedentePrestatore.find(
            'DatiAnagrafici/NumeroIscrizioneAlbo') is not None and \
            self.cedentePrestatore.find(
            'DatiAnagrafici/NumeroIscrizioneAlbo').text or None
        self.dataIscrizioneAlbo = self.cedentePrestatore.find(
            'DatiAnagrafici/DataIscrizioneAlbo') is not None and \
            self.cedentePrestatore.find(
            'DatiAnagrafici/DataIscrizioneAlbo').text or None
        self.regimeFiscale = self.cedentePrestatore.find(
            'DatiAnagrafici/RegimeFiscale').text
        self.parseSede()
        self.parseContatti()

    def parseIdFiscaleIva(self):
        idPaese = self.cedentePrestatore.find(
            'DatiAnagrafici/IdFiscaleIVA/IdPaese').text
        idCodice = self.cedentePrestatore.find(
            'DatiAnagrafici/IdFiscaleIVA/IdCodice').text
        self.idFiscaleIVA = idPaese + idCodice

    def parseCodiceFiscale(self):
        self.codiceFiscale = self.cedentePrestatore.find(
            'DatiAnagrafici/CodiceFiscale') and \
            self.cedentePrestatore.find(
                'DatiAnagrafici/CodiceFiscale').text

    def parseCedentePrestatore(self):
        anagrafica = self.cedentePrestatore.find(
            'DatiAnagrafici/Anagrafica')
        denominazione = anagrafica.find('Denominazione') is not None and \
            anagrafica.find('Denominazione').text or ''
        nome = anagrafica.find('Nome') is not None and \
            anagrafica.find('Nome').text or ''
        cognome = anagrafica.find('Cognome') is not None and \
            anagrafica.find('Cognome').text or ''
        titolo = anagrafica.find('Titolo') is not None and \
            anagrafica.find('Titolo').text or ''
        self.nomeRappresentanteFiscale = denominazione or '%s %s %s' % (
            titolo, nome, cognome
            )
        self.codEORI = anagrafica.find(
            'CodiceEori') is not None and \
            anagrafica.find(
            'CodiceEori').text or None

    def parseSede(self):
        sede = self.cedentePrestatore.find('Sede')
        address = sede.find('Indirizzo').text
        number = sede.find('NumeroCivico') is not None and \
            sede.find('NumeroCivico').text or ''
        self.indirizzo = '%s %s' % (address, number)
        self.cap = sede.find('CAP').text
        self.comune = sede.find('Comune').text
        self.provinca = sede.find('Provincia').text
        self.nazione = sede.find('Nazione').text

    def parseContatti(self):
        contatti = self.cedentePrestatore.find('Contatti')
        if contatti is not None:
            self.telefono = contatti.find('Telefono') is not None and \
                contatti.find('Telefono').text or ''
            self.fax = contatti.find('Fax') is not None and \
                contatti.find('Fax').text or ''
            self.email = contatti.find('Email') is not None and \
                contatti.find('Email').text or ''


class RappresentanteFiscale():
    _name = 'Rappresentante Fiscale'

    rappresentanteFiscale = None
    idFiscaleIVA = None
    codiceFiscale = None
    nomeRappresentanteFiscale = None
    codEORI = None

    def __init__(self, rappresentanteFiscale):
        self.rappresentanteFiscale = rappresentanteFiscale
        self.parseIdFiscaleIva()
        self.parseCodiceFiscale()
        self.parseRappresentanteFiscale()
        self.codEORI = self.rappresentanteFiscale.find(
            'DatiAnagrafici/Anagrafica/CodiceEori') is not None and \
            self.rappresentanteFiscale.find(
            'DatiAnagrafici/Anagrafica/CodiceEori').text or None

    def parseIdFiscaleIva(self):
        idPaese = self.rappresentanteFiscale.find(
            'DatiAnagrafici/IdFiscaleIVA/IdPaese').text
        idCodice = self.rappresentanteFiscale.find(
            'DatiAnagrafici/IdFiscaleIVA/IdCodice').text
        self.idFiscaleIVA = idPaese + idCodice

    def parseCodiceFiscale(self):
        self.codiceFiscale = self.rappresentanteFiscale.find(
            'DatiAnagrafici/CodiceFiscale') and \
            self.rappresentanteFiscale.find(
                'DatiAnagrafici/CodiceFiscale').text

    def parseRappresentanteFiscale(self):
        anagrafica = self.rappresentanteFiscale.find(
            'DatiAnagrafici/Anagrafica')
        denominazione = anagrafica.find('Denominazione') is not None and \
            anagrafica.find('Denominazione').text or ''
        nome = anagrafica.find('Nome') is not None and \
            anagrafica.find('Nome').text or ''
        cognome = anagrafica.find('Cognome') is not None and \
            anagrafica.find('Cognome').text or ''
        titolo = anagrafica.find('Titolo') is not None and \
            anagrafica.find('Titolo').text or ''
        self.nomeRappresentanteFiscale = denominazione or '%s %s %s' % (
            titolo, nome, cognome
            )
        self.codEORI = anagrafica.find(
            'CodiceEori') is not None and \
            anagrafica.find(
            'CodiceEori').text or None


class CessionarioCommittente():
    _name = 'CessionarioCommittente'

    cessionarioCommittente = None
    idFiscaleIVA = None
    codiceFiscale = None
    nomeCessionarioCommittente = None
    codEORI = None
    # <Sede>
    indirizzo = None
    cap = None
    comune = None
    provinca = None
    nazione = None

    def __init__(self, cessionarioCommittente):
        self.cessionarioCommittente = cessionarioCommittente
        self.parseIdFiscaleIva()
        self.parseCodiceFiscale()
        self.parseCessionarioCommittente()
        self.parseSede()

    def parseIdFiscaleIva(self):
        idPaese = self.cessionarioCommittente.find(
            'DatiAnagrafici/IdFiscaleIVA/IdPaese') is not None and \
            self.cessionarioCommittente.find(
            'DatiAnagrafici/IdFiscaleIVA/IdPaese').text or ''
        idCodice = self.cessionarioCommittente.find(
            'DatiAnagrafici/IdFiscaleIVA/IdCodice') is not None and \
            self.cessionarioCommittente.find(
            'DatiAnagrafici/IdFiscaleIVA/IdCodice').text or ''
        self.idFiscaleIVA = idPaese + idCodice

    def parseCodiceFiscale(self):
        self.codiceFiscale = self.cessionarioCommittente.find(
            'DatiAnagrafici/CodiceFiscale') is not None and \
            self.cessionarioCommittente.find(
                'DatiAnagrafici/CodiceFiscale').text or None

    def parseCessionarioCommittente(self):
        anagrafica = self.cessionarioCommittente.find(
            'DatiAnagrafici/Anagrafica')
        denominazione = anagrafica.find('Denominazione') is not None and \
            anagrafica.find('Denominazione').text or ''
        nome = anagrafica.find('Nome') is not None and \
            anagrafica.find('Nome').text or ''
        cognome = anagrafica.find('Cognome') is not None and \
            anagrafica.find('Cognome').text or ''
        titolo = anagrafica.find('Titolo') is not None and \
            anagrafica.find('Titolo').text or ''
        self.nomeRappresentanteFiscale = denominazione or '%s %s %s' % (
            titolo, nome, cognome
            )
        self.codEORI = anagrafica.find(
            'CodiceEori') is not None and \
            anagrafica.find(
            'CodiceEori').text or None

    def parseSede(self):
        sede = self.cessionarioCommittente.find('Sede')
        address = sede.find('Indirizzo').text
        number = sede.find('NumeroCivico') is not None and \
            sede.find('NumeroCivico').text or ''
        self.indirizzo = '%s %s' % (address, number)
        self.cap = sede.find('CAP').text
        self.comune = sede.find('Comune').text
        self.provinca = sede.find('Provincia').text
        self.nazione = sede.find('Nazione').text


class TerzoIntermediarioOSoggettoEmittente():
    _name = 'Terzo Intermediario O Soggetto Emittente'

    terzoIntermediarioOSoggettoEmittente = None
    idFiscaleIVA = None
    codiceFiscale = None
    nomeRappresentanteFiscale = None
    codEORI = None

    def __init__(self, terzoIntermediarioOSoggettoEmittente):
        self.terzoIntermediarioOSoggettoEmittente = \
            terzoIntermediarioOSoggettoEmittente
        self.parseIdFiscaleIva()
        self.parseCodiceFiscale()
        self.parseRappresentanteFiscale()

    def parseIdFiscaleIva(self):
        idPaese = self.terzoIntermediarioOSoggettoEmittente.find(
            'DatiAnagrafici/IdFiscaleIVA/IdPaese').text
        idCodice = self.terzoIntermediarioOSoggettoEmittente.find(
            'DatiAnagrafici/IdFiscaleIVA/IdCodice').text
        self.idFiscaleIVA = idPaese + idCodice

    def parseCodiceFiscale(self):
        self.codiceFiscale = self.terzoIntermediarioOSoggettoEmittente.find(
            'DatiAnagrafici/CodiceFiscale') and \
            self.terzoIntermediarioOSoggettoEmittente.find(
                'DatiAnagrafici/CodiceFiscale').text

    def parseRappresentanteFiscale(self):
        anagrafica = self.terzoIntermediarioOSoggettoEmittente.find(
            'DatiAnagrafici/Anagrafica')
        denominazione = anagrafica.find('Denominazione') is not None and \
            anagrafica.find('Denominazione').text or ''
        nome = anagrafica.find('Nome') is not None and \
            anagrafica.find('Nome').text or ''
        cognome = anagrafica.find('Cognome') is not None and \
            anagrafica.find('Cognome').text or ''
        titolo = anagrafica.find('Titolo') is not None and \
            anagrafica.find('Titolo').text or ''
        self.nomeRappresentanteFiscale = denominazione or '%s %s %s' % (
            titolo, nome, cognome
            )


class DatiCassaPrevidenziale():
    _name = 'Dati Cassa'

    datiCassaPrevidenziale = None
    tipoCassa = None
    alCassa = None
    importoContributoCassa = None
    imponibileCassa = None
    aliquotaIVA = None
    ritenuta = None
    natura = None
    riferimentoAmministrazione = None

    def __init__(self, datiCassaPrevidenziale):
        self.datiCassaPrevidenziale = datiCassaPrevidenziale
        if self.datiCassaPrevidenziale is not None:
            self.tipoCassa = self.datiCassaPrevidenziale.find(
                'TipoCassa').text
            self.alCassa = self.datiCassaPrevidenziale.find(
                'AlCassa').text
            self.importoContributoCassa = self.datiCassaPrevidenziale.find(
                'ImportoContributoCassa').text
            self.imponibileCassa = self.datiCassaPrevidenziale.find(
                'ImponibileCassa') is not None and \
                self.datiCassaPrevidenziale.find(
                'ImponibileCassa').text or None
            self.aliquotaIVA = self.datiCassaPrevidenziale.find(
                'AliquotaIVA').text
            self.ritenuta = self.datiCassaPrevidenziale.find(
                'Ritenuta') is not None and self.datiCassaPrevidenziale.find(
                'Ritenuta').text or None
            self.natura = self.datiCassaPrevidenziale.find(
                'Natura') is not None and self.datiCassaPrevidenziale.find(
                'Natura').text or None
            self.riferimentoAmministrazione = self.datiCassaPrevidenziale.find(
                'RiferimentoAmministrazione') is not None and \
                self.datiCassaPrevidenziale.find(
                    'RiferimentoAmministrazione').text or None


class ScontoMaggiorazione():
    _name = 'Sconto Maggiorazione'

    scontoMaggiorazione = None
    tipo = None
    percentuale = None
    importo = None

    def __init__(self, scontoMaggiorazione):
        self.scontoMaggiorazione = scontoMaggiorazione
        if self.scontoMaggiorazione is not None:
            self.tipo = self.scontoMaggiorazione.find(
                'Tipo').text
            self.percentuale = self.scontoMaggiorazione.find(
                'Percentuale') is not None and self.scontoMaggiorazione.find(
                'Percentuale').text or None
            self.importo = self.scontoMaggiorazione.find(
                'Importo') is not None and self.scontoMaggiorazione.find(
                'Importo').text or None


class ListaDatiGenerali():
    _name = 'Lista Dati Generali'

    listaDatiGenerali = None
    riferimentoNumeroLinea = []
    idDocumento = None
    data = None
    numItem = None
    codiceCommessaConvenzione = None
    codiceCUP = None
    codiceCIG = None

    def __init__(self, listaDatiGenerali):
        self.listaDatiGenerali = listaDatiGenerali
        if self.listaDatiGenerali is not None:
            self.riferimentoNumeroLinea.extend(
                [numeroLinea.text for numeroLinea in
                    self.listaDatiGenerali.findall('RiferimentoNumeroLinea')]
            )
            self.idDocumento = self.listaDatiGenerali.find(
                'IdDocumento').text
            self.data = self.listaDatiGenerali.find(
                'Data') is not None and self.listaDatiGenerali.find(
                'Data').text or None
            self.numItem = self.listaDatiGenerali.find(
                'NumItem') is not None and self.listaDatiGenerali.find(
                'NumItem').text or None
            self.codiceCommessaConvenzione = self.listaDatiGenerali.find(
                'CodiceCommessaConvenzione') is not None and \
                self.listaDatiGenerali.find(
                'CodiceCommessaConvenzione').text or None
            self.codiceCUP = self.listaDatiGenerali.find(
                'CodiceCUP') is not None and self.listaDatiGenerali.find(
                'CodiceCUP').text or None
            self.codiceCIG = self.listaDatiGenerali.find(
                'CodiceCIG') is not None and self.listaDatiGenerali.find(
                'CodiceCIG').text or None


class DatiSAL():
    _name = 'Dati SAL'

    datiSAL = None
    riferimentoBase = None

    def __init__(self, datiSAL):
        self.datiSAL = datiSAL
        if self.datiSAL is not None:
            self.riferimentoBase = self.datiSAL.find(
                'RiferimentoBase').text


class DatiDDT():
    _name = 'Dati DDT'

    datiDDT = None
    numeroDDT = None
    dataDDT = None
    riferimentoNumeroLinea = []

    def __init__(self, datiDDT):
        self.datiDDT = datiDDT
        if self.datiDDT is not None:
            self.riferimentoNumeroLinea.extend(
                [numeroLinea.text for numeroLinea in
                    self.datiDDT.findall('RiferimentoNumeroLinea')]
            )
            self.numeroDDT = self.datiDDT.find(
                'NumeroDDT').text
            self.dataDDT = self.datiDDT.find(
                'DataDDT').text


class DatiTrasporto():
    _name = 'Dati Trasporto'

    datiAnagraficiVettore = None
    idFiscaleIva = None
    codiceFiscale = None
    nomeTrasportatore = None
    codEORI = None
    numeroLicenzaGuida = None
    mezzoTrasporto = None
    causaleTrasporto = None
    numeroColli = None
    descrizione = None
    unitaMisuraPeso = None
    pesoLordo = None
    pesoNetto = None
    dataOraArrivo = None
    dataInizioTrasporto = None
    tipoResa = None
    indirizzo = None
    cap = None
    comune = None
    provinca = None
    nazione = None
    dataOraConsegna = None
    numeroFatturaPrincipale = None
    dataFatturaPrincipale = None

    def __init__(self, datiTrasporto):
        self.datiTrasporto = datiTrasporto
        self.parseIdFiscaleIva()
        self.parseCodiceFiscale()
        self.parseNomeTrasportatore()
        self.numeroLicenzaGuida = self.datiTrasporto.find(
            'NumeroLicenzaGuida') is not None and self.datiTrasporto.find(
            'NumeroLicenzaGuida').text or None
        self.mezzoTrasporto = self.datiTrasporto.find(
            'MezzoTrasporto') is not None and self.datiTrasporto.find(
            'MezzoTrasporto').text or None
        self.causaleTrasporto = self.datiTrasporto.find(
            'CausaleTrasporto') is not None and self.datiTrasporto.find(
            'CausaleTrasporto').text or None
        self.numeroColli = self.datiTrasporto.find(
            'NumeroColli') is not None and self.datiTrasporto.find(
            'NumeroColli').text or None
        self.descrizione = self.datiTrasporto.find(
            'Descrizione') is not None and self.datiTrasporto.find(
            'Descrizione').text or None
        self.unitaMisuraPeso = self.datiTrasporto.find(
            'UnitaMisuraPeso') is not None and self.datiTrasporto.find(
            'UnitaMisuraPeso').text or None
        self.pesoLordo = self.datiTrasporto.find(
            'PesoLordo') is not None and self.datiTrasporto.find(
            'PesoLordo').text or None
        self.pesoNetto = self.datiTrasporto.find(
            'PesoNetto') is not None and self.datiTrasporto.find(
            'PesoNetto').text or None
        self.dataOraArrivo = self.datiTrasporto.find(
            'DataOraArrivo') is not None and self.datiTrasporto.find(
            'DataOraArrivo').text or None
        self.dataInizioTrasporto = self.datiTrasporto.find(
            'DataInizioTrasporto') is not None and self.datiTrasporto.find(
            'DataInizioTrasporto').text or None
        self.tipoResa = self.datiTrasporto.find(
            'TipoResa') is not None and self.datiTrasporto.find(
            'TipoResa').text or None
        self.parseIndirizzoResa()
        self.dataOraConsegna = self.datiTrasporto.find(
            'DataOraConsegna') is not None and self.datiTrasporto.find(
            'DataOraConsegna').text or None

    def parseIdFiscaleIva(self):
        idPaese = self.datiTrasporto.find(
            'DatiAnagraficiVettore/IdFiscaleIVA/IdPaese').text
        idCodice = self.datiTrasporto.find(
            'DatiAnagraficiVettore/IdFiscaleIVA/IdCodice').text
        self.idFiscaleIVA = idPaese + idCodice

    def parseCodiceFiscale(self):
        if self.datiTrasporto.find('DatiAnagraficiVettore') is not None:
            self.codiceFiscale = self.datiTrasporto.find(
                'DatiAnagraficiVettore/CodiceFiscale') is not None and \
                self.datiTrasporto.find(
                    'DatiAnagraficiVettore/CodiceFiscale').text

    def parseNomeTrasportatore(self):
        anagrafica = self.datiTrasporto.find(
            'DatiAnagraficiVettore/Anagrafica')
        denominazione = anagrafica.find('Denominazione') is not None and \
            anagrafica.find('Denominazione').text or ''
        nome = anagrafica.find('Nome') is not None and \
            anagrafica.find('Nome').text or ''
        cognome = anagrafica.find('Cognome') is not None and \
            anagrafica.find('Cognome').text or ''
        titolo = anagrafica.find('Titolo') is not None and \
            anagrafica.find('Titolo').text or ''
        self.nomeTrasportatore = denominazione or '%s %s %s' % (
            titolo, nome, cognome
            )

    def parseIndirizzoResa(self):
        indirizzoResa = self.datiTrasporto.find('IndirizzoResa')
        if indirizzoResa is not None:
            address = indirizzoResa.find('Indirizzo').text
            number = indirizzoResa.find(
                'NumeroCivico') is not None and indirizzoResa.find(
                'NumeroCivico').text or ''
            self.indirizzo = '%s %s' % (address, number)
            self.cap = indirizzoResa.find('CAP').text
            self.comune = indirizzoResa.find('Comune').text
            self.provinca = indirizzoResa.find('Provincia').text
            self.nazione = indirizzoResa.find('Nazione').text

    def parseFatturaPrincipale(self):
        if self.datiTrasporto.find('FatturaPrincipale') is not None:
            self.numeroFatturaPrincipale = self.datiTrasporto.find(
                'FatturaPrincipale/NumeroFatturaPrincipale').text
            self.dataFatturaPrincipale = self.datiTrasporto.find(
                'FatturaPrincipale/DataFatturaPrincipale').text


class DettaglioLinea():
    _name = 'Dettaglio Linea'

    class CodiceArticolo():
        _name = 'Codice Articolo'

        codiceTipo = None
        codiceValore = None

        def __init__(self, codiceArticolo):
            self.codiceTipo = codiceArticolo.find('CodiceTipo').text
            self.codiceValore = codiceArticolo.find('CodiceValore').text

    class ScontoMaggiorazione():
        _name = 'Sconto Maggiorazione'

        tipo = None
        percentuale = None
        importo = None

        def __init__(self, scontoMaggiorazione):
            self.tipo = scontoMaggiorazione.find('Tipo').text
            self.percentuale = scontoMaggiorazione.find(
                'Percentuale') is not None and scontoMaggiorazione.find(
                'Percentuale').text or None
            self.importo = scontoMaggiorazione.find(
                'Importo') is not None and scontoMaggiorazione.find(
                'Importo').text or None

    numeroLinea = None
    tipoCessionePrestazione = None
    codiceArticolo = []
    descrizione = []
    quantita = None
    unitaMisura = None
    dataInizioPeriodo = None
    dataFinePeriodo = None
    prezzoUnitario = None
    prezzoTotale = None
    aliquotaIVA = None
    ritenuta = None
    natura = None
    riferimentoAmministrazione = None
    # TODO: AltriDatiGestionali

    def __init__(self, line):
            self.numeroLinea = line.find('NumeroLinea').text
            self.tipoCessionePrestazione = line.find(
                'TipoCessionePrestazione') is not None and line.find(
                'TipoCessionePrestazione').text or None
            if line.find('CodiceArticolo') is not None:
                for ca in line.findall('CodiceArticolo'):
                    self.codiceArticolo.append(
                        self.CodiceArticolo(ca)
                    )
            self.descrizione = line.find('Descrizione').text
            self.quantita = line.find(
                'Quantita') is not None and line.find(
                'Quantita').text or None
            self.unitaMisura = line.find(
                'UnitaMisura') is not None and line.find(
                'UnitaMisura').text or None
            self.dataInizioPeriodo = line.find(
                'DataInizioPeriodo') is not None and line.find(
                'DataInizioPeriodo').text or None
            self.dataFinePeriodo = line.find(
                'DataFinePeriodo') is not None and line.find(
                'DataFinePeriodo').text or None
            self.prezzoUnitario = line.find('PrezzoUnitario').text
            if line.find('ScontoMaggiorazione') is not None:
                for scm in line.findall('ScontoMaggiorazione'):
                    self.codiceArticolo.append(
                        self.ScontoMaggiorazione(scm)
                    )
            self.prezzoTotale = line.find('PrezzoTotale').text
            self.aliquotaIVA = line.find('AliquotaIVA').text
            self.ritenuta = line.find(
                'Ritenuta') is not None and line.find(
                'Ritenuta').text or None
            self.natura = line.find(
                'Natura') is not None and line.find(
                'Natura').text or None
            self.riferimentoAmministrazione = line.find(
                'RiferimentoAmministrazione') is not None and line.find(
                'RiferimentoAmministrazione').text or None


class DatiRiepilogo():
    _name = 'Dati Riepilogo'

    aliquotaIVA = None
    natura = None
    speseAccessorie = None
    arrotondamento = None
    imponibileImporto = None
    imposta = None
    esigibilitaIVA = None
    riferimentoNormativo = None

    def __init__(self, datoRiepilogo):
        self.aliquotaIVA = datoRiepilogo.find('AliquotaIVA').text
        self.natura = datoRiepilogo.find(
            'Natura') is not None and datoRiepilogo.find(
            'Natura').text or None
        self.speseAccessorie = datoRiepilogo.find(
            'SpeseAccessorie') is not None and datoRiepilogo.find(
            'SpeseAccessorie').text or None
        self.arrotondamento = datoRiepilogo.find(
            'Arrotondamento') is not None and datoRiepilogo.find(
            'Arrotondamento').text or None
        self.imponibileImporto = datoRiepilogo.find('ImponibileImporto').text
        self.imposta = datoRiepilogo.find('Imposta').text
        self.esigibilitaIVA = datoRiepilogo.find(
            'EsigibilitaIVA') is not None and datoRiepilogo.find(
            'EsigibilitaIVA').text or None
        self.riferimentoNormativo = datoRiepilogo.find(
            'RiferimentoNormativo') is not None and datoRiepilogo.find(
            'RiferimentoNormativo').text or None


class DatiPagamento():
    _name = 'Dati Pagamento'

    datiPagamento = None
    condizioniPagamento = None
    dettaglioPagamento = []

    class DettaglioPagamento():
        _name = 'Dettaglio Pagamento'

        beneficiario = None
        modalitaPagamento = None
        dataRiferimentoTerminiPagamento = None
        giorniTerminiPagamento = None
        dataScadenzaPagamento = None
        importoPagamento = None
        codUfficioPostale = None
        cognomeQuietanzante = None
        nomeQuietanzante = None
        cFQuietanzante = None
        titoloQuietanzante = None
        istitutoFinanziario = None
        iban = None
        abi = None
        cab = None
        bic = None
        scontoPagamentoAnticipato = None
        dataLimitePagamentoAnticipato = None
        penalitaPagamentiRitardati = None
        dataDecorrenzaPenale = None
        codicePagamento = None

        def __init__(self, dettaglioPagamento):
            self.beneficiario = dettaglioPagamento.find(
                'Beneficiario') is not None and dettaglioPagamento.find(
                'Beneficiario').text or None
            self.modalitaPagamento = dettaglioPagamento.find(
                'ModalitaPagamento') is not None and dettaglioPagamento.find(
                'ModalitaPagamento').text or None
            self.dataRiferimentoTerminiPagamento = dettaglioPagamento.find(
                'DataRiferimentoTerminiPagamento') is not None and \
                dettaglioPagamento.find(
                'DataRiferimentoTerminiPagamento').text or None
            self.giorniTerminiPagamento = dettaglioPagamento.find(
                'GiorniTerminiPagamento') is not None and \
                dettaglioPagamento.find(
                'GiorniTerminiPagamento').text or None
            self.dataScadenzaPagamento = dettaglioPagamento.find(
                'DataScadenzaPagamento') is not None and \
                dettaglioPagamento.find(
                'DataScadenzaPagamento').text or None
            self.importoPagamento = dettaglioPagamento.find(
                'ImportoPagamento') is not None and \
                dettaglioPagamento.find(
                'ImportoPagamento').text or None
            self.codUfficioPostale = dettaglioPagamento.find(
                'CodUfficioPostale') is not None and \
                dettaglioPagamento.find(
                'CodUfficioPostale').text or None
            self.cognomeQuietanzante = dettaglioPagamento.find(
                'CognomeQuietanzante') is not None and \
                dettaglioPagamento.find(
                'CognomeQuietanzante').text or None
            self.nomeQuietanzante = dettaglioPagamento.find(
                'NomeQuietanzante') is not None and \
                dettaglioPagamento.find(
                'NomeQuietanzante').text or None
            self.cFQuietanzante = dettaglioPagamento.find(
                'CFQuietanzante') is not None and \
                dettaglioPagamento.find(
                'CFQuietanzante').text or None
            self.titoloQuietanzante = dettaglioPagamento.find(
                'TitoloQuietanzante') is not None and \
                dettaglioPagamento.find(
                'TitoloQuietanzante').text or None
            self.IstitutoFinanziario = dettaglioPagamento.find(
                'istitutoFinanziario') is not None and \
                dettaglioPagamento.find(
                'IstitutoFinanziario').text or None
            self.iban = dettaglioPagamento.find(
                'IBAN') is not None and \
                dettaglioPagamento.find(
                'IBAN').text or None
            self.abi = dettaglioPagamento.find(
                'ABI') is not None and \
                dettaglioPagamento.find(
                'ABI').text or None
            self.cab = dettaglioPagamento.find(
                'CAB') is not None and \
                dettaglioPagamento.find(
                'CAB').text or None
            self.bic = dettaglioPagamento.find(
                'BIC') is not None and \
                dettaglioPagamento.find(
                'BIC').text or None
            self.scontoPagamentoAnticipato = dettaglioPagamento.find(
                'ScontoPagamentoAnticipato') is not None and \
                dettaglioPagamento.find(
                'ScontoPagamentoAnticipato').text or None
            self.dataLimitePagamentoAnticipato = dettaglioPagamento.find(
                'DataLimitePagamentoAnticipato') is not None and \
                dettaglioPagamento.find(
                'DataLimitePagamentoAnticipato').text or None
            self.penalitaPagamentiRitardati = dettaglioPagamento.find(
                'PenalitaPagamentiRitardati') is not None and \
                dettaglioPagamento.find(
                'PenalitaPagamentiRitardati').text or None
            self.dataDecorrenzaPenale = dettaglioPagamento.find(
                'DataDecorrenzaPenale') is not None and \
                dettaglioPagamento.find(
                'DataDecorrenzaPenale').text or None
            self.codicePagamento = dettaglioPagamento.find(
                'CodicePagamento') is not None and \
                dettaglioPagamento.find(
                'CodicePagamento').text or None

    def __init__(self, datiPagamento):
        self.datiPagamento = datiPagamento
        self.condizioniPagamento = self.datiPagamento.find(
            'CondizioniPagamento').text
        if self.datiPagamento.find('DettaglioPagamento') is not None:
                for dp in self.datiPagamento.findall('DettaglioPagamento'):
                    self.dettaglioPagamento.append(
                        self.DettaglioPagamento(dp)
                    )


class Allegati():
    _name = 'Dati Allegati'

    allegato = None
    nomeAttachment = None
    algoritmoCompressione = None
    formatoAttachment = None
    descrizioneAttachment = None
    attachment = None

    def __init__(self, allegato):
        self.allegato = allegato
        if self.allegato is not None:
            self.nomeAttachment = self.allegato.find(
                'NomeAttachment').text
            self.dataDDT = self.datiDDT.find(
                'DataDDT').text
            self.algoritmoCompressione = self.allegato.find(
                'AlgoritmoCompressione') is not None and \
                self.allegato.find(
                'AlgoritmoCompressione').text or None
            self.formatoAttachment = self.allegato.find(
                'FormatoAttachment') is not None and \
                self.allegato.find(
                'FormatoAttachment').text or None
            self.descrizioneAttachment = self.allegato.find(
                'DescrizioneAttachment') is not None and \
                self.allegato.find(
                'DescrizioneAttachment').text or None
            self.attachment = self.allegato.find(
                'Attachment').text


class FatturaElettronicaBody():
    _name = 'Fattura Elettronica Body'

    fatturaElettronicaBody = None
    # <DatiGeneraliDocumento>
    datiGeneraliDocumento = None
    tipoDocumento = None
    divisa = None
    data = None
    numero = None

    # datiRitenuta
    datiRitenuta = None
    tipoRitenuta = None
    importoRitenuta = None
    aliquotaRitenuta = None
    causalePagamento = None

    # datiBollo
    datiBollo = None
    bolloVirtuale = None
    importoBollo = None

    # datiCassaPrevidenza
    datiCassaPrevidenzialeList = []
    # contoMaggiorazione
    scontoMaggiorazioneList = []

    importoTotaleDocumento = None
    arrotondamento = None
    causaleList = []
    art73 = False
    # DatiOrdineAcquisto
    datiOrdineAcquisto = None
    datiOrdineAcquistoList = []
    # DatiContratto
    datiContratto = None
    datiContrattoList = []
    # DatiConvenzione
    datiConvenzione = None
    datiConvenzioneList = []
    # DatiRicezione
    datiRicezione = None
    datiRicezioneList = []
    # DatiFattureCollegate
    datiFattureCollegate = None
    datiFattureCollegateList = []
    # DatiSal
    datiSAL = None
    datiSALList = []
    # DatiDdt
    datiDDT = None
    datiDDTList = []
    # DatiTrasporto
    datiTrasporto = None

    # <DatiBeniServizi>/<DettaglioLinee>
    dettaglioLinee = []

    # Dati Riepilogo
    datiRiepilogo = []

    # Dati Veicoli
    datiVeicoliData = None
    datiVeicoliTotalePercorso = None

    # Dati Pagamento
    datiPagamento = None
    datiPagamentoList = []

    # Allegati
    allegati = None
    allegatiList = []

    def __init__(self, fatturaElettronicaBody):
        self.fatturaElettronicaBody = fatturaElettronicaBody
        # Dati Fatturazione
        self.datiGeneraliDocumento = self.fatturaElettronicaBody.find(
            'DatiGenerali/DatiGeneraliDocumento'
            )
        self.parseDatiGeneraliDocumento()

        # Dati Ordine
        self.datiOrdineAcquisto = self.fatturaElettronicaBody.findall(
            'DatiGenerali/DatiOrdineAcquisto'
            )
        for datoOrdineAcquisto in self.datiOrdineAcquisto:
            self.datiOrdineAcquistoList.append(
                ListaDatiGenerali(datoOrdineAcquisto)
            )

        # Dati Contratto
        self.datiContratto = self.fatturaElettronicaBody.findall(
            'DatiGenerali/DatiContratto'
            )
        for datoContratto in self.datiContratto:
            self.datiContrattoList.append(
                ListaDatiGenerali(datoContratto)
            )

        # Dati Convenzione
        self.datiConvenzione = self.fatturaElettronicaBody.findall(
            'DatiGenerali/DatiConvenzione'
            )
        for datoConvenzione in self.datiConvenzione:
            self.datiConvenzioneList.append(
                ListaDatiGenerali(datoConvenzione)
            )

        # Dati Ricezione
        self.datiRicezione = self.fatturaElettronicaBody.findall(
            'DatiGenerali/DatiRicezione'
            )
        for datoRicezione in self.datiRicezione:
            self.datiRicezioneList.append(
                ListaDatiGenerali(datoRicezione)
            )

        # Dati Fatture Collegate
        self.datiFattureCollegate = self.fatturaElettronicaBody.findall(
            'DatiGenerali/DatiFattureCollegate'
            )
        for datoFattureCollegate in self.datiFattureCollegate:
            self.datiFattureCollegateList.append(
                ListaDatiGenerali(datoFattureCollegate)
            )

        # Dati SAL
        self.datiSAL = self.fatturaElettronicaBody.findall(
            'DatiGenerali/DatiSAL'
            )
        for datoSAL in self.datiSAL:
            self.datiSALList.append(
                DatiSAL(datoSAL)
            )

        # Dati DDT
        self.datiDDT = self.fatturaElettronicaBody.findall(
            'DatiGenerali/DatiDDT'
            )
        for datoDDT in self.datiDDT:
            self.datiDDTList.append(
                DatiDDT(datoDDT)
            )

        # Dati Trasporto
        datoTrasporto = self.fatturaElettronicaBody.find(
            'DatiGenerali/DatiTrasporto'
            )
        if datoTrasporto is not None:
            self.datiTrasporto = DatiTrasporto(datoTrasporto)

        # Dati Beni e Servizi
        datiBeniServizi = self.fatturaElettronicaBody.find(
            'DatiBeniServizi'
            )

        # Linee Fatturazione
        linee = datiBeniServizi.findall(
            'DettaglioLinee'
            )
        self.parseDettaglioLinee(linee)

        # Dati Riepilogo
        riepilogo = datiBeniServizi.findall(
            'DatiRiepilogo'
            )
        self.parseDatiRiepilogo(riepilogo)

        # Dati Veicoli
        datiVeicoli = self.fatturaElettronicaBody.find(
            'DatiVeicoli')
        if datiVeicoli is not None:
            self.datiVeicoliData = datiVeicoli.find(
                'Data').text
            self.datiVeicoliTotalePercorso = datiVeicoli.find(
                'TotalePercorso').text

        # Dati Pagamento
        self.datiPagamento = self.fatturaElettronicaBody.findall(
            'DatiPagamento'
            )
        for datoPagamento in self.datiPagamento:
            self.datiPagamentoList.append(
                DatiPagamento(datoPagamento)
            )

        # Allegati
        self.allegati = self.fatturaElettronicaBody.findall(
            'Allegati'
            )
        for allegato in self.allegati:
            self.allegatiList.append(
                Allegati(allegato)
            )

    def parseDatiGeneraliDocumento(self):
        self.tipoDocumento = self.datiGeneraliDocumento.\
            find('TipoDocumento').text
        self.divisa = self.datiGeneraliDocumento.find('Divisa').text
        self.data = self.datiGeneraliDocumento.find('Data').text
        self.numero = self.datiGeneraliDocumento.find('Numero').text

        # Dati Ritenuta
        self.datiRitenuta = self.datiGeneraliDocumento.\
            find('DatiRitenuta') is not None and self.datiGeneraliDocumento.\
            find('DatiRitenuta').text or None
        if self.datiRitenuta is not None:
            self.tipoRitenuta = self.datiRitenuta.find(
                'TipoRitenuta').text
            self.importoRitenuta = self.datiRitenuta.find(
                'ImportoRitenuta').text
            self.aliquotaRitenuta = self.datiRitenuta.find(
                'AliquotaRitenuta').text
            self.causalePagamento = self.datiRitenuta.find(
                'CausalePagamento').text

        # Dati Bollo
        self.datiBollo = self.datiGeneraliDocumento.\
            find('DatiBollo') is not None and self.datiGeneraliDocumento.\
            find('DatiBollo').text or None
        if self.datiBollo:
            self.bolloVirtuale = self.datiBollo.find(
                'BolloVirtuale').text
            self.importoBollo = self.datiBollo.find(
                'ImportoBollo').text

        # DatiCassaPrevidenziale
        for datiCassaPrevidenziale in \
                self.datiGeneraliDocumento.findall('DatiCassaPrevidenziale'):
            self.datiCassaPrevidenzialeList.append(
                DatiCassaPrevidenziale(datiCassaPrevidenziale)
            )

        # ScontoMaggiorazione
        for scontoMaggiorazione in \
                self.datiGeneraliDocumento.findall('ScontoMaggiorazione'):
            self.scontoMaggiorazioneList.append(
                ScontoMaggiorazione(scontoMaggiorazione)
            )

        self.importoTotaleDocumento = self.datiGeneraliDocumento.find(
            'ImportoTotaleDocumento') is not None and \
            self.datiGeneraliDocumento.find(
            'ImportoTotaleDocumento').text or None

        self.arrotondamento = self.datiGeneraliDocumento.find(
            'Arrotondamento') is not None and self.datiGeneraliDocumento.find(
            'Arrotondamento').text or None

        for dgcausale in self.datiGeneraliDocumento.findall('causale'):
            self.causaleList.append(dgcausale.text)

        self.art73 = self.datiGeneraliDocumento.find(
            'Art73') is not None and self.datiGeneraliDocumento.find(
            'Art73').text or None

    def parseDettaglioLinee(self, linee):
        for line in linee:
            self.dettaglioLinee.append(DettaglioLinea(line))

    def parseDatiRiepilogo(self, riepilogo):
        for datoRiepilogo in riepilogo:
            self.datiRiepilogo.append(DatiRiepilogo(datoRiepilogo))


class XmlData():
    _name = 'Xml Object for data'
    _description = """ The object to store sdi xml datas"""

    content = None
    template = None
    root = None

    # Datas
    # Dati Trasmissione
    datiTrasmissione = None
    idTrasmittente = None
    progressivoInvio = None
    formatoTrasmissione = None
    codiceDestinatario = None
    contattiTrasmittente = None

    # <CedentePrestatore>
    cedentePrestatore = None

    # <RappresentanteFiscale>
    rappresentanteFiscale = None

    # TerzoIntermediarioOSoggettoEmittente
    terzoIntermediarioOSoggettoEmittente = None

    # <CessionarioCommittente>
    cessionarioCommittente = None

    # SoggettoEmittente
    soggettoEmittente = None

    # FatturaElettronicaBody
    fatturaElettronicaBody = []

    def __init__(self, content):
        self.content = content
        self.template = ElementTree(fromstring(self.content))
        self.root = self.template.getroot()

    def parseIdTrasmittente(self):
        idPaese = self.datiTrasmissione.find(
            'IdTrasmittente/IdPaese').text
        idCodice = self.datiTrasmissione.find(
            'IdTrasmittente/IdCodice').text
        self.idTrasmittente = idPaese + idCodice

    def parseXml(self):
        # Dati Spedizione
        self.datiTrasmissione = self.template.find(
            'FatturaElettronicaHeader/DatiTrasmissione'
            )
        self.parseIdTrasmittente()
        self.progressivoInvio = self.datiTrasmissione.find(
            'ProgressivoInvio')
        self.formatoTrasmissione = self.datiTrasmissione.find(
            'FormatoTrasmissione')
        self.codiceDestinatario = self.datiTrasmissione.find(
            'CodiceDestinatario')
        if self.datiTrasmissione.find(
                'ContattiTrasmittente') is not None:
            # FIXME
            pass

        # Dati CedentePrestatore
        cp = self.template.find(
            'FatturaElettronicaHeader/CedentePrestatore'
            )
        self.cedentePrestatore = CedentePrestatore(cp)

        # RappresentanteFiscale
        rf = self.template.find(
            'FatturaElettronicaHeader/RappresentanteFiscale'
            )
        if rf is not None:
            self.rappresentanteFiscale = RappresentanteFiscale(rf)

        # Dati CessionarioCommittente
        cc = self.template.find(
            'FatturaElettronicaHeader/CessionarioCommittente'
            )
        self.cessionarioCommittente = CessionarioCommittente(cc)

        # TerzoIntermediarioOSoggettoEmittente
        tise = self.template.find(
            'FatturaElettronicaHeader/TerzoIntermediarioOSoggettoEmittente'
            )
        if tise is not None:
            self.terzoIntermediarioOSoggettoEmittente = \
                TerzoIntermediarioOSoggettoEmittente(tise)

        self.soggettoEmittente = self.template.find(
            'FatturaElettronicaHeader/SoggettoEmittente'
            ) is not None and self.template.find(
            'FatturaElettronicaHeader/SoggettoEmittente'
            ).text or None

        # Fattura Elettronica Body
        for feb in self.template.findall('FatturaElettronicaBody'):
            self.fatturaElettronicaBody.append(FatturaElettronicaBody(feb))

if __name__ == '__main__':
        with open('../tests/IT01234567890_11002.xml') as test_data:
            with tempfile.TemporaryFile() as out:
                base64.encode(test_data, out)
                out.seek(0)
                # FIXME: when there are more than one invoice in xml document
                xml_data = XmlData(out.read().decode('base64'))
                xml_data.parseXml()
                for attr in dir(xml_data):
                    if isinstance(getattr(xml_data, attr), str) \
                            and attr != 'content':
                        print "xml_data.%s = %s" % (attr,
                                                    getattr(xml_data, attr)
                                                    )
                print "Dettaglio CedentePrestatore"
                for cp in dir(xml_data.cedentePrestatore):
                        if isinstance(getattr(xml_data.cedentePrestatore, cp),
                                      str) and cp != 'content':
                            print "xml_data.%s = %s" % (xml_data.
                                                        cedentePrestatore,
                                                        getattr(
                                                            xml_data.
                                                            cedentePrestatore,
                                                            cp)
                                                        )
                for fatt in xml_data.fatturaElettronicaBody:
                    print "Dettaglio Fatture"
                    for attr in dir(fatt):
                        if isinstance(getattr(fatt, attr), str) \
                                and attr != 'content':
                            print "xml_data.%s = %s" % (attr,
                                                        getattr(fatt, attr)
                                                        )
                    print "Dettaglio Linee Fattura"
                    for line in fatt.dettaglioLinee:
                        for attr in dir(line):
                            if isinstance(getattr(line, attr), str) \
                                    and attr != 'content':
                                print "line.%s = %s" % (attr,
                                                        getattr(line, attr))
                    print "Dettaglio Linee Riepilogo"
                    for line in fatt.datiRiepilogo:
                        for attr in dir(line):
                            if isinstance(getattr(line, attr), str) \
                                    and attr != 'content':
                                print "line.%s = %s" % (attr,
                                                        getattr(line, attr))
