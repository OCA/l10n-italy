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
            'p', "http://www.fatturapa.gov.it/sdi/fatturapa/v1.0")
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
                _('Error!'), _('TIN not set.'))

        attach_obj = self.pool['ir.attachment']
        root = tmpl.getroot()
        header = """<?xml version="1.0" encoding="UTF-8"?>\n"""
        attach_data = tostring(root, encoding='utf-8', method='xml')
        attach_data = header+attach_data
        attach_vals = {
            'name': '%s_%s.xml' % (company.vat, str(number)),
            'datas_fname': '%s_%s.xml' % (company.vat, str(number)),
            'datas': base64.encodestring(attach_data),
            'file_type': 'text/xml',
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

    def setIdTrasmittente(self, cr, uid, context=None):
        if not context:
            context = {}

        tmpl = self.template

        user_obj = self.pool['res.users']
        company = user_obj.browse(cr, uid, uid).company_id

        IdTrasmittente = tmpl.find(
            'FatturaElettronicaHeader/DatiTrasmissione/IdTrasmittente')

        if not company.country_id:
            raise orm.except_orm(
                _('Error!'), _('Country not set.'))
        IdPaese = company.country_id.code
        IdTrasmittente.find('IdPaese').text = IdPaese

        if not company.partner_id.fiscalcode:
            # XXX: just for testing purposes, to be resolved asap
            fiscalcode = company.vat
            #raise orm.except_orm(
            #    _('Error!'), _('Fiscalcode not set.'))
        IdCodice = company.partner_id.fiscalcode or fiscalcode
        IdTrasmittente.find('IdCodice').text = IdCodice

        return True

    def setFormatoTrasmissione(self, cr, uid, context=None):
        if not context:
            context = {}

        tmpl = self.template

        user_obj = self.pool['res.users']
        company = user_obj.browse(cr, uid, uid).company_id

        FormatoTrasmissione = tmpl.find(
            'FatturaElettronicaHeader/DatiTrasmissione/FormatoTrasmissione')

        if not company.fatturapa_format_id:
            raise orm.except_orm(
                _('Error!'), _('FatturaPA format not set.'))
        FormatoTrasmissione.text = company.fatturapa_format_id.code

        return True

    def setCodiceDestinatario(self, cr, uid, partner, context=None):
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

        return tmpl

    def setContattiTrasmittente(self, cr, uid, context=None):
        if not context:
            context = {}

        tmpl = self.template

        user_obj = self.pool['res.users']
        company = user_obj.browse(cr, uid, uid).company_id

        ContattiTrasmittente = tmpl.find(
            'FatturaElettronicaHeader/DatiTrasmissione/ContattiTrasmittente')

        if not company.phone:
            raise orm.except_orm(
                _('Error!'), _('Telephone number not set.'))
        Telefono = company.phone
        ContattiTrasmittente.find('Telefono').text = Telefono

        if not company.email:
            raise orm.except_orm(
                _('Error!'), _('Email address not set.'))
        Email = company.email
        ContattiTrasmittente.find('Email').text = Email

        return True

    def setDatiAnagraficiCedente(self, cr, uid, context=None):
        if not context:
            context = {}

        tmpl = self.template

        user_obj = self.pool['res.users']
        company = user_obj.browse(cr, uid, uid).company_id

        DatiAnagrafici = tmpl.find(
            'FatturaElettronicaHeader/CedentePrestatore/DatiAnagrafici')

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
        DatiAnagrafici.find('RegimeFiscale').text = fatturapa_fp.code

        return True

    def setSedeCedente(self, cr, uid, context=None):
        if not context:
            context = {}

        tmpl = self.template

        user_obj = self.pool['res.users']
        company = user_obj.browse(cr, uid, uid).company_id

        Sede = tmpl.find(
            'FatturaElettronicaHeader/CedentePrestatore/Sede')

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

        Sede.find('Indirizzo').text = company.street
        Sede.find('CAP').text = company.zip
        Sede.find('Comune').text = company.city
        Sede.find('Provincia').text = company.partner_id.province.code
        Sede.find('Nazione').text = company.country_id.code

        return True

    def setDatiAnagraficiCessionario(
            self, cr, uid, partner, context=None):
        if not context:
            context = {}

        tmpl = self.template

        DatiAnagrafici = tmpl.find(
            'FatturaElettronicaHeader/CessionarioCommittente/DatiAnagrafici')

        if not partner.fiscalcode:
            raise orm.except_orm(
                _('Error!'), _('Partner fiscalcode not set.'))

        DatiAnagrafici.find('CodiceFiscale').text = partner.fiscalcode
        DatiAnagrafici.find('Anagrafica/Denominazione').text = partner.name

        return True

    def setSedeCessionario(self, cr, uid, partner, context=None):
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

        Sede.find('Indirizzo').text = partner.street
        Sede.find('CAP').text = partner.zip
        Sede.find('Comune').text = partner.city
        Sede.find('Provincia').text = partner.province.code
        Sede.find('Nazione').text = partner.country_id.code

        return True

    def setSoggettoEmittente(self, cr, uid, context=None):
        if not context:
            context = {}

        tmpl = self.template

        SoggettoEmittente = tmpl.find(
            'FatturaElettronicaHeader/SoggettoEmittente')
        # TODO: SoggettoEmittente
        SoggettoEmittente.text = 'CC'

        return True

    def setDatiGeneraliDocumento(self, cr, uid, invoice, body, context=None):
        if not context:
            context = {}

        DatiGeneraliDocumento = body.find('DatiGenerali/DatiGeneraliDocumento')

        # TODO: TipoDocumento
        DatiGeneraliDocumento.find('TipoDocumento').text = 'TD01'
        DatiGeneraliDocumento.find('Divisa').text = invoice.currency_id.name
        DatiGeneraliDocumento.find('Data').text = invoice.date_invoice
        DatiGeneraliDocumento.find('Numero').text = invoice.number
        # TODO: Art73
        DatiGeneraliDocumento.find('Art73').text = 'SI'

        return True

    def setDatiOrdineAcquisto(self, cr, uid, invoice, body, context=None):
        if not context:
            context = {}

        DatiOrdineAcquisto = body.find('DatiGenerali/DatiOrdineAcquisto')

        DatiOrdineAcquisto.find(
            'RiferimentoNumeroLinea').text = str(invoice.fatturapa_po_line_no)
        DatiOrdineAcquisto.find('IdDocumento').text = invoice.fatturapa_po
        DatiOrdineAcquisto.find('CodiceCUP').text = invoice.fatturapa_po_cup
        DatiOrdineAcquisto.find('CodiceCIG').text = invoice.fatturapa_po_cig

        return True

    def setDatiContratto(self, cr, uid, invoice, body, context=None):
        if not context:
            context = {}

        DatiContratto = body.find('DatiGenerali/DatiContratto')

        line_no = str(invoice.fatturapa_contract_line_no)
        DatiContratto.find('RiferimentoNumeroLinea').text = line_no
        DatiContratto.find('IdDocumento').text = invoice.fatturapa_contract
        DatiContratto.find('Data').text = invoice.fatturapa_contract_data
        DatiContratto.find('NumItem').text = invoice.fatturapa_contract_numitem
        DatiContratto.find('CodiceCUP').text = invoice.fatturapa_contract_cup
        DatiContratto.find('CodiceCIG').text = invoice.fatturapa_contract_cig

        return True

    def setDatiConvenzione(self, cr, uid, invoice, body, context=None):
        if not context:
            context = {}

        DatiConvenzione = body.find('DatiGenerali/DatiConvenzione')

        DatiConvenzione.find(
            'RiferimentoNumeroLinea'
            ).text = str(invoice.fatturapa_agreement_line_no)
        DatiConvenzione.find('IdDocumento').text = invoice.fatturapa_agreement
        DatiConvenzione.find('Data').text = invoice.fatturapa_agreement_data
        DatiConvenzione.find(
            'NumItem').text = invoice.fatturapa_agreement_numitem
        DatiConvenzione.find(
            'CodiceCUP').text = invoice.fatturapa_agreement_cup
        DatiConvenzione.find(
            'CodiceCIG').text = invoice.fatturapa_agreement_cig

        return True

    def setDatiRicezione(self, cr, uid, invoice, body, context=None):
        if not context:
            context = {}

        DatiRicezione = body.find('DatiGenerali/DatiRicezione')

        line_no = str(invoice.fatturapa_reception_line_no)
        DatiRicezione.find('RiferimentoNumeroLinea').text = line_no
        DatiRicezione.find('IdDocumento').text = invoice.fatturapa_reception
        DatiRicezione.find('Data').text = invoice.fatturapa_reception_data
        DatiRicezione.find(
            'NumItem').text = invoice.fatturapa_reception_numitem
        DatiRicezione.find(
            'CodiceCUP').text = invoice.fatturapa_reception_cup
        DatiRicezione.find(
            'CodiceCIG').text = invoice.fatturapa_reception_cig

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

        line_no = 1
        for line in invoice.invoice_line:
            el = copy.deepcopy(DettaglioLinee)
            DatiBeniServizi.append(el)
            el.find('NumeroLinea').text = str(line_no)
            el.find('Descrizione').text = line.name
            el.find(
                'PrezzoUnitario').text = str('%.2f' % line.price_unit)
            el.find(
                'PrezzoTotale').text = str('%.2f' % line.price_subtotal)
            # TODO: multiple taxes per line
            el.find(
                'AliquotaIVA').text = str(
                '%.2f' % (line.invoice_line_tax_id[0].amount*100))
            line_no += 1
        DatiBeniServizi.remove(DettaglioLinee)

        return True

    def setDatiRiepilogo(self, cr, uid, invoice, body, context=None):
        if not context:
            context = {}

        DatiRiepilogo = body.find('DatiBeniServizi/DatiRiepilogo')

        # TODO: multiple taxes
        # TODO: improve tax identification
        taxCode = int(re.findall(
            r'\d+', invoice.tax_line[0].tax_code_id.name)[0])

        DatiRiepilogo.find('AliquotaIVA').text = str('%.2f' % taxCode)
        DatiRiepilogo.find(
            'ImponibileImporto').text = str('%.2f' % invoice.amount_untaxed)
        DatiRiepilogo.find(
            'Imposta').text = str('%.2f' % invoice.amount_tax)

        return True

    def setDatiPagamento(self, cr, uid, invoice, body, context=None):
        if not context:
            context = {}

        DatiPagamento = body.find('DatiPagamento')
        DettaglioPagamento = DatiPagamento.find('DettaglioPagamento')
        DatiPagamento.find(
            'CondizioniPagamento'
            ).text = invoice.payment_term.fatturapa_pt_id.code

        # TODO: multiple installments
        DettaglioPagamento.find(
            'ModalitaPagamento'
            ).text = invoice.payment_term.fatturapa_pm_id.code
        DettaglioPagamento.find(
            'DataScadenzaPagamento').text = invoice.date_due
        DettaglioPagamento.find(
            'ImportoPagamento').text = str('%.2f' % invoice.amount_total)

        return True

    def setFatturaElettronicaHeader(self, cr, uid, partner, context=None):
        if not context:
            context = {}

        self.setProgressivoInvio(cr, uid, context=context)
        self.setIdTrasmittente(cr, uid, context=context)
        self.setFormatoTrasmissione(cr, uid, context=context)
        self.setCodiceDestinatario(cr, uid, partner, context=context)
        self.setContattiTrasmittente(cr, uid, context=context)
        self.setDatiAnagraficiCedente(cr, uid, context=context)
        self.setSedeCedente(cr, uid, context=context)
        self.setDatiAnagraficiCessionario(cr, uid, partner, context=context)
        self.setSedeCessionario(cr, uid, partner, context=context)
        self.setSoggettoEmittente(cr, uid, context=context)

    def setFatturaElettronicaBody(self, cr, uid, inv, el, context=None):
        if not context:
            context = {}

        self.setDatiGeneraliDocumento(cr, uid, inv, el, context=context)
        self.setDatiOrdineAcquisto(cr, uid, inv, el, context=context)
        self.setDatiContratto(cr, uid, inv, el, context=context)
        self.setDatiConvenzione(cr, uid, inv, el, context=context)
        self.setDatiRicezione(cr, uid, inv, el, context=context)
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

        content = self.getFile('fatturapa_v1.0.xml').decode('base64')
        self.template = ElementTree(fromstring(content))
        tmpl = self.template
        root = tmpl.getroot()

        invoice_ids = context.get('active_ids', False)
        partner = self.getPartnerId(cr, uid, invoice_ids, context=context)

        self.setFatturaElettronicaHeader(cr, uid, partner, context=context)
        FatturaElettronicaBody = tmpl.find('FatturaElettronicaBody')
        for invoice_id in invoice_ids:
            el = copy.deepcopy(FatturaElettronicaBody)
            root.append(el)
            inv = invoice_obj.browse(cr, uid, invoice_id)
            self.setFatturaElettronicaBody(cr, uid, inv, el, context=context)
        root.remove(FatturaElettronicaBody)

        attach_id = self.saveAttachment(cr, uid, context=context)
        view_rec = model_data_obj.get_object_reference(
            cr, uid, 'base', 'view_attachment_form')
        if view_rec:
            view_id = view_rec and view_rec[1] or False

        return {
            'view_type': 'form',
            'name': "Export FatturaPA",
            'view_id': [view_id],
            'res_id': attach_id,
            'view_mode': 'form',
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'context': context
            }
