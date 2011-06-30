##############################################################################
#    
#    Copyright (C) 2010 OpenERP Italian Community (<http://www.openerp-italia.org>). 
#    Thanks to Antonio de Vincentiis http://www.devincentiis.it/
#    and GAzie http://gazie.sourceforge.net/
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

'''
*****************************************************************************************
 Questa classe genera il file RiBa standard ABI-CBI passando alla funzione "creaFile" i due array di seguito specificati:
$intestazione = array monodimensionale con i seguenti index:
              [0] = abi_assuntrice variabile lunghezza 5 numerico
              [1] = cab_assuntrice variabile lunghezza 5 numerico
              [2] = conto variabile lunghezza 12 alfanumerico
              [3] = data_creazione variabile lunghezza 6 numerico formato GGMAA
              [4] = nome_supporto variabile lunghezza 20 alfanumerico
              [5] = codice_divisa variabile lunghezza 1 alfanumerico opzionale default "E"
              [6] = ragione_soc1_creditore variabile lunghezza 24 alfanumerico
              [7] = ragione_soc2_creditore variabile lunghezza 24 alfanumerico
              [8] = indirizzo_creditore variabile lunghezza 24 alfanumerico
              [9] = cap_citta_prov_creditore variabile lunghezza 24 alfanumerico
              [10] = codice_fiscale_creditore variabile lunghezza 16 alfanumerico opzionale default ""
$ricevute_bancarie = array bidimensionale con i seguenti index:
                   [0] = numero ricevuta lunghezza 10 numerico
                   [1] = scadenza lunghezza 6 numerico
                   [2] = importo in centesimi di euro lunghezza 13 numerico
                   [3] = nome debitore lunghezza 60 alfanumerico
                   [4] = codice fiscale/partita iva debitore lunghezza 16 alfanumerico
                   [5] = indirizzo debitore lunghezza 30 alfanumerico
                   [6] = cap debitore lunghezza 5 numerico
                   [7] = comune provincia debitore lunghezza 25 alfanumerico
                   [8] = abi banca domiciliataria lunghezza 5 numerico
                   [9] = cab banca domiciliataria lunghezza 5 numerico
                   [10] = descrizione banca domiciliataria lunghezza 50 alfanumerico
                   [11] = codice cliente attribuito dal creditore lunghezza 16 numerico
                   [12] = descrizione del debito lunghezza 40 alfanumerico
'''

import tools
import base64
from osv import fields,osv
from tools.translate import _
import datetime

class riba_file_export(osv.osv_memory):

    _progressivo = 0
    _assuntrice = 0
    _data = 0
    _valuta = 0
    _supporto = 0
    _totale = 0
    _creditore = 0

    def _RecordIB(self, abi_assuntrice, data_creazione, nome_supporto, codice_divisa): #record di testa
        self._assuntrice = abi_assuntrice.rjust(5, '0')
        self._data = data_creazione.ljust(6, '0')
        self._valuta = codice_divisa[0:1]
        self._supporto = nome_supporto.rjust(20, '*')
        return " IB     " + self._assuntrice + self._data + self._supporto + " " * 74 + self._valuta + " " * 6 + "\r\n"

    def _Record14(self, scadenza, importo, abi_assuntrice, cab_assuntrice, conto, abi_domiciliataria, cab_domiciliataria, codice_cliente):
        self._totale += importo
        return " 14" + str(self._progressivo).rjust(7,'0') + " " * 12 + scadenza + "30000" + str(importo).rjust(13,'0') + "-" + abi_assuntrice.rjust(5,'0') + cab_assuntrice.rjust(5,'0') + conto.ljust(12) + abi_domiciliataria.rjust(5,'0') + cab_domiciliataria.rjust(5,'0') + " " * 12 + " " * 5 + "4" + codice_cliente.ljust(16) + " " * 6 + self._valuta + "\r\n"

    def _Record20(self, ragione_soc1_creditore, ragione_soc2_creditore, indirizzo_creditore, cap_citta_prov_creditore):
        self._creditore =  ragione_soc1_creditore.ljust(24)
        return " 20" + str(self._progressivo).rjust(7,'0') + self._creditore[0:24] + ragione_soc2_creditore.ljust(24)[0:24] + indirizzo_creditore.ljust(24)[0:24] + cap_citta_prov_creditore.ljust(24)[0:24] + " " * 14 + "\r\n"

    def _Record30(self, nome_debitore, codice_fiscale_debitore):
        return " 30" + str(self._progressivo).rjust(7,'0') + nome_debitore.ljust(60)[0:60] + codice_fiscale_debitore.ljust(16,' ') + " " * 34 + "\r\n"

    def _Record40(self, indirizzo_debitore, cap_debitore, comune_provincia_debitore, descrizione_domiciliataria=""):
        return " 40" + str(self._progressivo).rjust(7,'0') + indirizzo_debitore.ljust(30)[0:30] + str(cap_debitore).rjust(5,'0') + comune_provincia_debitore.ljust(25)[0:25] + descrizione_domiciliataria.ljust(50)[0:50] + "\r\n"

    def _Record50(self, descrizione_debito, codice_fiscale_creditore):
        return " 50" + str(self._progressivo).rjust(7,'0') + descrizione_debito.ljust(40)[0:40] + " " * 50 + codice_fiscale_creditore.ljust(16,' ') + " " * 4 + "\r\n"

    def _Record51(self, numero_ricevuta_creditore):
        return " 51" + str(self._progressivo).rjust(7,'0') + str(numero_ricevuta_creditore).rjust(10,'0') + self._creditore[0:20] + " " * 80 + "\r\n"

    def _Record70(self):
        return " 70" + str(self._progressivo).rjust(7,'0') + " " * 110 + "\r\n"

    def _RecordEF(self): #record di coda
        return " EF     " + self._assuntrice + self._data + self._supporto + " " * 6 + str(self._progressivo).rjust(7,'0') + str(self._totale).rjust(15,'0') + "0" * 15 + str(int(self._progressivo)*7+2).rjust(7,'0') + " " * 24 + self._valuta + " " * 6 + "\r\n"

    def _creaFile(self, intestazione, ricevute_bancarie):
        accumulatore = self._RecordIB(intestazione[0], intestazione[3], intestazione[4], intestazione[5])
        for value in ricevute_bancarie: #estraggo le ricevute dall'array
            self._progressivo =self._progressivo + 1
            accumulatore = accumulatore + self._Record14(
                value[1], value[2], intestazione[0], intestazione[1], intestazione[2], value[8], value[9], value[11])
            accumulatore = accumulatore + self._Record20(intestazione[6], intestazione[7], intestazione[8], intestazione[9])
            accumulatore = accumulatore + self._Record30(value[3], value[4])
            accumulatore = accumulatore + self._Record40(value[5], value[6], value[7], value[10])
            accumulatore = accumulatore + self._Record50(value[12], intestazione[10])
            accumulatore = accumulatore + self._Record51(value[0])
            accumulatore = accumulatore + self._Record70()
        accumulatore = accumulatore + self._RecordEF()
        return accumulatore

    def act_getfile(self, cr, uid, ids, context=None):
        active_ids = context and context.get('active_ids', [])
        voucher = self.pool.get('account.voucher').browse(cr, uid, active_ids, context)[0]
        wizard = self.browse(cr, uid, ids, context)[0]
        credit_bank = self.pool.get('res.partner.bank').browse(cr, uid, wizard.credit_bank_id, context)
        debit_bank = self.pool.get('res.partner.bank').browse(cr, uid, wizard.debit_bank_id, context)
        if not debit_bank.iban or not credit_bank.iban:
            raise osv.except_osv('Error', _('No IBAN specified'))
        credit_abi = credit_bank.iban[5:10]
        debit_abi = debit_bank.iban[5:10]
        credit_cab = credit_bank.iban[10:15]
        debit_cab = debit_bank.iban[10:15]
        credit_account = credit_bank.iban[15:27]
        dataemissione = datetime.datetime.now().strftime("%d%m%y")
        nome_supporto = voucher.partner_id.name[0:6] + datetime.datetime.now().strftime("%d%m%Y%H%M%S")
        if not voucher.company_id.partner_id.address:
            raise osv.except_osv('Error', _('No address specified for ') + voucher.company_id.partner_id.name)
        creditor_address = voucher.company_id.partner_id.address
        if not voucher.partner_id.address:
            raise osv.except_osv('Error', _('No address specified for ') + voucher.partner_id.name)
        debitor_address = voucher.partner_id.address

        creditor_city = ''
        if creditor_address[0].city:
            creditor_city = creditor_address[0].city
        creditor_province = ''
        if creditor_address[0].province:
            creditor_province = creditor_address[0].province.code

        debitor_city = ''
        if debitor_address[0].city:
            debitor_city = debitor_address[0].city
        debitor_province = ''
        if debitor_address[0].province:
            debitor_province = debitor_address[0].province.code

        array_testata = [
            credit_abi,
            credit_cab,
            credit_account,
            dataemissione,
            nome_supporto,
            'E',
            voucher.company_id.partner_id.name,
            creditor_address[0].name or '',
            creditor_address[0].street or '',
            creditor_address[0].zip or '' + ' ' + creditor_city + ' ' + creditor_province,
            voucher.company_id.partner_id.vat or voucher.company_id.partner_id.fiscalcode or '',
            ]
        arrayRiba = []
        for line in voucher.line_ids:
            if not line.date_due:
                due_date =  '000000'
            else:
                due_date = datetime.datetime.strptime(line.date_due[:10], '%Y-%m-%d').strftime("%d%m%y")
            if not voucher.partner_id.vat and not voucher.partner_id.fiscalcode:
                raise osv.except_osv('Error', _('No VAT or Fiscal code specified for ') + voucher.partner_id.name)
            Riba = [
                line.id,
                due_date,
                int(line.amount_unreconciled * 100),
                voucher.partner_id.name,
                voucher.partner_id.vat or voucher.partner_id.fiscalcode,
                debitor_address[0].street or '',
                debitor_address[0].zip or '',
                debitor_city + ' ' + debitor_province,
                debit_abi,
                debit_cab,
                debit_bank.bank.name,
                voucher.partner_id.ref or '',
                line.name or '',
                ]

            arrayRiba.append(Riba)

        out=base64.encodestring(self._creaFile(array_testata, arrayRiba))

        return self.write(cr, uid, ids, {'state':'get', 'data':out}, context=context)

    def _get_debitor_banks(self, cr, uid, fields, context=None):
        voucher_pool = self.pool.get('account.voucher')
        res = []
        if fields.has_key('active_ids'):
            for voucher in voucher_pool.browse(cr, uid, fields['active_ids'], context=context):
                for bank in voucher.partner_id.bank_ids:
                    res.append((bank.id, bank.bank.name))
        return res

    def _get_creditor_banks(self, cr, uid, fields, context=None):
        voucher_pool = self.pool.get('account.voucher')
        res = []
        if fields.has_key('active_ids'):
            for voucher in voucher_pool.browse(cr, uid, fields['active_ids'], context=context):
                for bank in voucher.company_id.partner_id.bank_ids:
                    res.append((bank.id, bank.bank.name))
        return res

    _name = "riba.file.export"
    _columns = {
        'credit_bank_id': fields.selection(_get_creditor_banks, 'Creditor\'s Bank', required=True),
        'debit_bank_id': fields.selection(_get_debitor_banks, 'Debitor\'s Bank', required=True),
        'state': fields.selection( ( ('choose','choose'),   # choose accounts
                                     ('get','get'),         # get the file
                                   ) ),
        'data': fields.binary('File', readonly=True),
    }
    _defaults = { 
        'state': lambda *a: 'choose',
        }

riba_file_export()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
