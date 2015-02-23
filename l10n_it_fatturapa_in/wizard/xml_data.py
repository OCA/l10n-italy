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


class XmlData():
    _name = 'Xml Object for data'
    _description = """ The object to store sdi xml datas"""

    content = None
    template = None
    root = None

    # Datas
    # <CedentePrestatore>
    cedentePrestatore = None
    idFiscaleIVA = None
    codiceFiscale = None
    nomeCedentePrestatore = None
    regimeFiscale = None
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

    # <CessionarioCommittente>
    cessionarioCommittente = None
    idFiscaleIVAPA = None
    codiceFiscalePA = None

    # <DatiGeneraliDocumento>
    datiGeneraliDocumento = None
    tipoDocumento = None
    divisa = None
    data = None
    numero = None
    # TODO: datiRitenuta
    # TODO: datiBollo
    # TODO: datiCassaPrevidenza
    # TODO: scontoMaggiorazione
    importoTotaleDocumento = None
    arrotondamento = None
    causale = None
    art73 = False
    # TODO: datiOrdineAcquisto
    # TODO: datiContratto
    # TODO: datiConvenzione
    # TODO: datiRicezione
    # TODO: datiFattureCollegate
    # TODO: datiSal
    # TODO: datiDdt
    # TODO: datiTrasporto

    # <DatiBeniServizi>/<DettaglioLinee>
    dettaglioLinee = None
    lines = {}
    # TODO: tipoCessionePrestazione
    # TODO: codiceArticolo

    # <DettaglioLinee>

    def __init__(self, content):
        self.content = content
        self.template = ElementTree(fromstring(self.content))
        self.root = self.template.getroot()

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

    def parseNomeCedentePrestatore(self):
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
        self.nomeCedentePrestatore = denominazione or '%s %s %s' % (
            titolo, nome, cognome
            )

    def parseRegimeFiscale(self):
        self.regimeFiscale = self.cedentePrestatore.find(
            'DatiAnagrafici/RegimeFiscale').text

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

    def parseIdFiscaleIvaPA(self):
        # XXX: per fare un check sulla PIVA dell'ente
        if self.cessionarioCommittente.find('DatiAnagrafici/IdFiscaleIVA') \
                is not None:
            idPaese = self.cessionarioCommittente.find(
                'DatiAnagrafici/IdFiscaleIVA/IdPaese').text
            idCodice = self.cessionarioCommittente.find(
                'DatiAnagrafici/IdFiscaleIVA/IdCodice').text
            self.idFiscaleIVAPA = idPaese + idCodice

    def parseCodiceFiscalePA(self):
        self.codiceFiscalePA = self.cedentePrestatore.find(
            'DatiAnagrafici/CodiceFiscale') is not None and \
            self.cedentePrestatore.find(
                'DatiAnagrafici/CodiceFiscale').text

    def parseDatiGeneraliDocumento(self):
        self.tipoDocumento = self.datiGeneraliDocumento.\
            find('TipoDocumento').text
        self.divisa = self.datiGeneraliDocumento.find('Divisa').text
        self.data = self.datiGeneraliDocumento.find('Data').text
        self.numero = self.datiGeneraliDocumento.find('Numero').text

    def parseDettaglioLinee(self):
        for line in self.dettaglioLinee:
            numeroLinea = line.find('NumeroLinea').text
            descrizione = line.find('Descrizione').text
            quantita = line.find('Quantita').text
            prezzoUnitario = line.find('PrezzoUnitario').text
            prezzoTotale = line.find('PrezzoTotale').text
            aliquotaIVA = line.find('AliquotaIVA').text
            self.lines[numeroLinea] = {
                     'Descrizione': descrizione,
                     'Quantita': quantita,
                     'PrezzoUnitario': prezzoUnitario,
                     'PrezzoTotale': prezzoTotale,
                     'AliquotaIVA': aliquotaIVA
            }

    def parseXml(self):
        # TODO: RappresentanteFiscale (come trattarlo?)
        # TODO: TerzoIntermediarioOSoggettoEmittente ( ?)
        # Dati CedentePrestatore e CessionarioCommittente
        self.cedentePrestatore = self.template.find(
            'FatturaElettronicaHeader/CedentePrestatore'
            )
        self.parseIdFiscaleIva()
        self.parseCodiceFiscale()
        self.parseNomeCedentePrestatore()
        self.parseRegimeFiscale()
        self.parseSede()
        self.parseContatti()
        self.cessionarioCommittente = self.template.find(
            'FatturaElettronicaHeader/CessionarioCommittente'
            )
        self.parseIdFiscaleIvaPA()
        self.parseCodiceFiscalePA()

        # Dati Fatturazione
        self.datiGeneraliDocumento = self.template.find(
            'FatturaElettronicaBody/DatiGenerali/DatiGeneraliDocumento'
            )
        self.parseDatiGeneraliDocumento()

        # Linee Fatturazione
        datiBeniServizi = self.template.find(
            'FatturaElettronicaBody/DatiBeniServizi'
            )
        self.dettaglioLinee = datiBeniServizi.findall(
            'DettaglioLinee'
            )
        self.parseDettaglioLinee()

if __name__ == '__main__':
        with open('../tests/IT01234567890_11002.xml') as test_data:
            with tempfile.TemporaryFile() as out:
                base64.encode(test_data, out)
                out.seek(0)
                xml_data = XmlData(out.read().decode('base64'))
                xml_data.parseXml()
                for attr in dir(xml_data):
                    if isinstance(getattr(xml_data, attr), str) and attr != 'content':
                        print "xml_data.%s = %s" % (attr, getattr(xml_data, attr))
                for k,v in xml_data.lines.iteritems():
                    print 'line %s -> values %s' % (k, v)
