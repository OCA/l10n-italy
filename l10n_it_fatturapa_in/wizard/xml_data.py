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

    def __init__(self, cedentePrestatore):
        self.idFiscaleIVA = None
        self.codiceFiscale = None
        self.nomeRappresentanteFiscale = None
        self.codEORI = None
        # <Sede>
        self.indirizzo = None
        self.cap = None
        self.comune = None
        self.provinca = None
        self.nazione = None
        # <Contatti>
        self.telefono = None
        self.fax = None
        self.email = None
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

    def __init__(self, rappresentanteFiscale):

        self.idFiscaleIVA = None
        self.codiceFiscale = None
        self.nomeRappresentanteFiscale = None
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

    def __init__(self, cessionarioCommittente):

        self.idFiscaleIVA = None
        self.codiceFiscale = None
        self.codEORI = None
        # <Sede>
        self.indirizzo = None
        self.cap = None
        self.comune = None
        self.provinca = None
        self.nazione = None
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

    def __init__(self, terzoIntermediarioOSoggettoEmittente):
        self.idFiscaleIVA = None
        self.codiceFiscale = None
        self.nomeRappresentanteFiscale = None
        self.codEORI = None
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

    def __init__(self, scontoMaggiorazione):
        self.tipo = None
        self.percentuale = None
        self.importo = None
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

    def __init__(self, listaDatiGenerali):
        self.riferimentoNumeroLinea = []
        self.idDocumento = None
        self.data = None
        self.numItem = None
        self.codiceCommessaConvenzione = None
        self.codiceCUP = None
        self.codiceCIG = None
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

    def __init__(self, datiSAL):
        self.riferimentoBase = None
        self.datiSAL = datiSAL
        if self.datiSAL is not None:
            self.riferimentoBase = self.datiSAL.find(
                'RiferimentoBase').text


class DatiDDT():
    _name = 'Dati DDT'

    def __init__(self, datiDDT):

        self.numeroDDT = None
        self.dataDDT = None
        self.riferimentoNumeroLinea = []
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

    def __init__(self, datiTrasporto):
        self.datiAnagraficiVettore = None
        self.idFiscaleIva = None
        self.codiceFiscale = None
        self.nomeTrasportatore = None
        self.codEORI = None
        self.numeroFatturaPrincipale = None
        self.dataFatturaPrincipale = None
        self.indirizzo = None
        self.cap = None
        self.comune = None
        self.provinca = None
        self.nazione = None
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

        def __init__(self, codiceArticolo):
            self.codiceTipo = codiceArticolo.find('CodiceTipo').text
            self.codiceValore = codiceArticolo.find('CodiceValore').text

    class ScontoMaggiorazione():
        _name = 'Sconto Maggiorazione'

        def __init__(self, scontoMaggiorazione):
            self.tipo = scontoMaggiorazione.find('Tipo').text
            self.percentuale = scontoMaggiorazione.find(
                'Percentuale') is not None and scontoMaggiorazione.find(
                'Percentuale').text or None
            self.importo = scontoMaggiorazione.find(
                'Importo') is not None and scontoMaggiorazione.find(
                'Importo').text or None

    # TODO: AltriDatiGestionali

    def __init__(self, line):
        self.codiceArticolo = []
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

    class DettaglioPagamento():
        _name = 'Dettaglio Pagamento'

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
        self.dettaglioPagamento = []
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

    def __init__(self, allegato):
        self.nomeAttachment = None
        self.algoritmoCompressione = None
        self.formatoAttachment = None
        self.descrizioneAttachment = None
        self.attachment = None
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

    def __init__(self, fatturaElettronicaBody):

        # datiRitenuta
        self.datiRitenuta = None
        self.tipoRitenuta = None
        self.importoRitenuta = None
        self.aliquotaRitenuta = None
        self.causalePagamento = None

        # datiBollo
        self.datiBollo = None
        self.bolloVirtuale = None
        self.importoBollo = None

        # datiCassaPrevidenza
        self.datiCassaPrevidenzialeList = []
        # contoMaggiorazione
        self.scontoMaggiorazioneList = []

        self.importoTotaleDocumento = None
        self.arrotondamento = None
        self.causaleList = []
        self.art73 = False
        # DatiOrdineAcquisto
        self.datiOrdineAcquisto = None
        self.datiOrdineAcquistoList = []
        # DatiContratto
        self.datiContratto = None
        self.datiContrattoList = []
        # DatiConvenzione
        self.datiConvenzione = None
        self.datiConvenzioneList = []
        # DatiRicezione
        self.datiRicezione = None
        self.datiRicezioneList = []
        # DatiFattureCollegate
        self.datiFattureCollegate = None
        self.datiFattureCollegateList = []
        # DatiSal
        self.datiSAL = None
        self.datiSALList = []
        # DatiDdt
        self.datiDDT = None
        self.datiDDTList = []
        # DatiTrasporto
        self.datiTrasporto = None

        # <DatiBeniServizi>/<DettaglioLinee>
        self.dettaglioLinee = []

        # Dati Riepilogo
        self.datiRiepilogo = []

        # Dati Veicoli
        self.datiVeicoliData = None
        self.datiVeicoliTotalePercorso = None

        # Dati Pagamento
        self.datiPagamento = None
        self.datiPagamentoList = []

        # Allegati
        self.allegati = None
        self.allegatiList = []
        # <DatiGeneraliDocumento>
        self.tipoDocumento = None
        self.divisa = None
        self.data = None
        self.numero = None
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

        for dgcausale in self.datiGeneraliDocumento.findall('Causale'):
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

    def __init__(self, content):
        self.content = content
        self.template = ElementTree(fromstring(self.content))
        self.root = self.template.getroot()

        # Datas
        # Dati Trasmissione
        self.datiTrasmissione = None
        self.idTrasmittente = None
        self.progressivoInvio = None
        self.formatoTrasmissione = None
        self.codiceDestinatario = None
        self.contattiTrasmittente = None

        # <CedentePrestatore>
        self.cedentePrestatore = None

        # <RappresentanteFiscale>
        self.rappresentanteFiscale = None

        # TerzoIntermediarioOSoggettoEmittente
        self.terzoIntermediarioOSoggettoEmittente = None

        # <CessionarioCommittente>
        self.cessionarioCommittente = None

        # SoggettoEmittente
        self.soggettoEmittente = None

        # FatturaElettronicaBody
        self.fatturaElettronicaBody = []

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
