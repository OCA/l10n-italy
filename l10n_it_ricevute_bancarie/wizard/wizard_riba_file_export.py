# -*- coding: utf-8 -*-
# Copyright (C) 2011-2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# Thanks to Antonio de Vincentiis http://www.devincentiis.it/ ,
# GAzie http://gazie.sourceforge.net/
# and Cecchi s.r.l http://www.cecchi.com/


import base64
from odoo import fields, models, _
from odoo.exceptions import UserError
import datetime
import re


class RibaFileExport(models.TransientModel):
    """
    ***************************************************************************
     Questa classe genera il file RiBa standard ABI-CBI passando alla funzione
     "creaFile" i due array di seguito specificati:
    $intestazione = array monodimensionale con i seguenti index:
                  [0] = credit_sia variabile lunghezza 5 alfanumerico
                  [1] = credit_abi assuntrice variabile lunghezza 5 numerico
                  [2] = credit_cab assuntrice variabile lunghezza 5 numerico
                  [3] = credit_conto conto variabile lunghezza 10 alfanumerico
                  [4] = data_creazione variabile lunghezza 6 numerico formato
                    GGMMAA
                  [5] = nome_supporto variabile lunghezza 20 alfanumerico
                  [6] = codice_divisa variabile lunghezza 1 alfanumerico
                    opzionale default "E"
                  [7] = name_company nome ragione sociale creditore variabile
                    lunghezza 24 alfanumerico
                  [8] = indirizzo_creditore variabile lunghezza 24 alfanumerico
                  [9] = cap_citta_creditore variabile lunghezza 24 alfanumerico
                  [10] = ref (definizione attivita) creditore
                  [11] = codice fiscale/partita iva creditore alfanumerico
                    opzionale

    $ricevute_bancarie = array bidimensionale con i seguenti index:
                       [0] = numero ricevuta lunghezza 10 numerico
                       [1] = data scadenza lunghezza 6 numerico
                       [2] = importo in centesimi di euro
                       [3] = nome debitore lunghezza 60 alfanumerico
                       [4] = codice fiscale/partita iva debitore lunghezza 16
                        alfanumerico
                       [5] = indirizzo debitore lunghezza 30 alfanumerico
                       [6] = cap debitore lunghezza 5 numerico
                       [7] = citta debitore alfanumerico
                       [8] = debitor_province debitore alfanumerico
                       [9] = abi banca domiciliataria lunghezza 5 numerico
                       [10] = cab banca domiciliataria lunghezza 5 numerico
                       [11] = descrizione banca domiciliataria lunghezza 50
                        alfanumerico
                       [12] = codice cliente attribuito dal creditore lunghezza
                        16 numerico
                       [13] = numero fattura lunghezza 40 alfanumerico
                       [14] = data effettiva della fattura

    """
    _progressivo = 0
    _assuntrice = 0
    _sia = 0
    _data = 0
    _valuta = 0
    _supporto = 0
    _totale = 0
    _creditore = 0
    _descrizione = ''
    _codice = ''
    _comune_provincia_debitor = ''

    def _RecordIB(
        self, sia_assuntrice, abi_assuntrice, data_creazione, nome_supporto,
        codice_divisa
    ):  # record di testa
        self._sia = sia_assuntrice.rjust(5, '0')
        self._assuntrice = abi_assuntrice.rjust(5, '0')
        self._data = data_creazione.rjust(6, '0')
        self._valuta = codice_divisa[0:1]
        self._supporto = nome_supporto.ljust(20, ' ')
        return (
            " IB" + self._sia + self._assuntrice + self._data +
            self._supporto +
            " " * 74 + self._valuta + " " * 6 + "\r\n")

    def _Record14(
        self, scadenza, importo, abi_assuntrice, cab_assuntrice, conto,
        abi_domiciliataria, cab_domiciliataria, sia_credit, codice_cliente
    ):
        self._totale += importo
        return (
            " 14" + str(self._progressivo).rjust(7, '0') + " " * 12 +
            scadenza +
            "30000" + str(int(round(importo * 100))).rjust(13, '0') + "-" +
            abi_assuntrice.rjust(5, '0') + cab_assuntrice.rjust(5, '0') +
            conto.ljust(12, '0') + abi_domiciliataria.rjust(5, '0') +
            cab_domiciliataria.rjust(5, '0') + " " * 12 +
            str(sia_credit).rjust(5, '0') + "4" + codice_cliente.ljust(16) +
            " " * 6 + self._valuta + "\r\n")

    def _Record20(
        self, ragione_soc1_creditore, indirizzo_creditore, cap_citta_creditore,
        ref_creditore
    ):
        self._creditore = ragione_soc1_creditore.ljust(24)
        return (
            " 20" + str(self._progressivo).rjust(7, '0') +
            self._creditore[0:24] + indirizzo_creditore.ljust(24)[0:24] +
            cap_citta_creditore.ljust(24)[0:24] +
            ref_creditore.ljust(24)[0:24] +
            " " * 14 + "\r\n")

    def _Record30(self, nome_debitore, codice_fiscale_debitore):
        return (
            " 30" + str(self._progressivo).rjust(7, '0') +
            nome_debitore.ljust(60)[0:60] +
            codice_fiscale_debitore.ljust(16, ' ') + " " * 34 + "\r\n")

    def _Record40(
        self, indirizzo_debitore, cap_debitore, comune_debitore,
        provincia_debitore, descrizione_domiciliataria=""
    ):
        self._comune_provincia_debitor = comune_debitore + \
            provincia_debitore.rjust(25 - len(comune_debitore), ' ')
        return (
            " 40" + str(self._progressivo).rjust(7, '0') +
            indirizzo_debitore.ljust(30)[0:30] +
            str(cap_debitore).rjust(5, '0') + self._comune_provincia_debitor +
            descrizione_domiciliataria.ljust(50)[0:50] + "\r\n")

    def _Record50(
        self, importo_debito, invoice_ref, data_invoice, partita_iva_creditore
    ):
        self._descrizione = 'PER LA FATTURA N. ' + invoice_ref + \
            ' DEL ' + data_invoice + ' IMP ' + str(importo_debito)
        return (
            " 50" + str(self._progressivo).rjust(7, '0') +
            self._descrizione.ljust(80)[0:80] + " " * 10 +
            partita_iva_creditore.ljust(16, ' ') + " " * 4 + "\r\n")

    def _Record51(self, numero_ricevuta_creditore):
        return " 51" + str(self._progressivo).rjust(7, '0') + str(
            numero_ricevuta_creditore).rjust(
                10, '0') + self._creditore[0:20] + " " * 80 + "\r\n"

    def _Record70(self):
        return " 70" + str(self._progressivo).rjust(
            7, '0') + " " * 110 + "\r\n"

    def _RecordEF(self):  # record di coda
        return (
            " EF" + self._sia + self._assuntrice + self._data +
            self._supporto +
            " " * 6 + str(self._progressivo).rjust(7, '0') +
            str(int(round(self._totale * 100))).rjust(15, '0') + "0" * 15 +
            str(int(self._progressivo) * 7 + 2).rjust(7, '0') + " " * 24 +
            self._valuta + " " * 6 + "\r\n")

    def _creaFile(self, intestazione, ricevute_bancarie):
        accumulatore = self._RecordIB(
            intestazione[0], intestazione[1], intestazione[4], intestazione[5],
            intestazione[6])
        for value in ricevute_bancarie:  # estraggo le ricevute dall'array
            self._progressivo = self._progressivo + 1
            accumulatore = accumulatore + self._Record14(
                value[1], value[2], intestazione[1], intestazione[2],
                intestazione[3], value[9], value[10], intestazione[0],
                value[12])
            accumulatore = accumulatore + \
                self._Record20(intestazione[7], intestazione[
                               8], intestazione[9], intestazione[10])
            accumulatore = accumulatore + self._Record30(value[3], value[4])
            accumulatore = accumulatore + \
                self._Record40(
                    value[5], value[6], value[7], value[8], value[11])
            accumulatore = accumulatore + \
                self._Record50(
                    value[2], value[13], value[14], intestazione[11])
            accumulatore = accumulatore + self._Record51(value[0])
            accumulatore = accumulatore + self._Record70()
        accumulatore = accumulatore + self._RecordEF()
        self._progressivo = 0
        self._totale = 0
        return accumulatore

    def act_getfile(self):
        active_ids = self.env.context.get('active_ids', [])
        order_obj = self.env['riba.distinta'].browse(active_ids)[0]
        credit_bank = order_obj.config_id.bank_id
        name_company = order_obj.config_id.company_id.partner_id.name
        if not credit_bank.acc_number:
            raise UserError(_('No IBAN specified'))
        # remove spaces automatically added by odoo
        credit_iban = credit_bank.acc_number.replace(" ", "")
        credit_abi = credit_iban[5:10]
        credit_cab = credit_iban[10:15]
        credit_conto = credit_iban[-12:]
        if not credit_bank.codice_sia:
            raise UserError(
                _('No SIA Code specified for: ') + name_company)
        credit_sia = credit_bank.codice_sia
        dataemissione = datetime.datetime.now().strftime("%d%m%y")
        nome_supporto = datetime.datetime.now().strftime(
            "%d%m%y%H%M%S") + credit_sia
        creditor_address = order_obj.config_id.company_id.partner_id
        creditor_city = creditor_address.city or ''
        if (
            not order_obj.config_id.company_id.partner_id.vat and not
            order_obj.config_id.company_id.partner_id.fiscalcode
        ):
            raise UserError(
                _('No VAT or Fiscalcode specified for: ') + name_company)
        array_testata = [
            credit_sia,
            credit_abi,
            credit_cab,
            credit_conto,
            dataemissione,
            nome_supporto,
            'E',
            name_company,
            creditor_address.street or '',
            creditor_address.zip or '' + ' ' + creditor_city,
            order_obj.config_id.company_id.partner_id.ref or '',
            (
                order_obj.config_id.company_id.partner_id.vat and
                order_obj.config_id.company_id.partner_id.vat[2:] or
                order_obj.config_id.company_id.partner_id.fiscalcode),
        ]
        arrayRiba = []
        for line in order_obj.line_ids:
            debit_bank = line.bank_id
            debitor_address = line.partner_id
            debitor_street = debitor_address.street or ''
            debitor_zip = debitor_address.zip or ''
            if debit_bank.bank_abi and debit_bank.bank_cab:
                debit_abi = debit_bank.bank_abi
                debit_cab = debit_bank.bank_cab
            elif debit_bank.acc_number:
                debit_iban = debit_bank.acc_number.replace(" ", "")
                debit_abi = debit_iban[5:10]
                debit_cab = debit_iban[10:15]
            else:
                raise UserError(
                    _('No IBAN or ABI/CAB specified for ') +
                    line.partner_id.name)
            debitor_city = debitor_address.city and debitor_address.city.ljust(
                23)[0:23] or ''
            debitor_province = (
                debitor_address.state_id and debitor_address.state_id.code or
                '')
            if not line.due_date:  # ??? VERIFICARE
                due_date = '000000'
            else:
                due_date = datetime.datetime.strptime(
                    line.due_date[:10], '%Y-%m-%d').strftime("%d%m%y")

            if not line.partner_id.vat and not line.partner_id.fiscalcode:
                raise UserError(
                    _('No VAT or Fiscal code specified for ') +
                    line.partner_id.name)
            Riba = [
                line.sequence,
                due_date,
                line.amount,
                # using regex we remove chars outside letters, numbers, space,
                # dot and comma because, special chars cause errors.
                re.sub(r'[^\w\s,.]+', '', line.partner_id.name)[:60],
                line.partner_id.vat and line.partner_id.vat[
                    2:] or line.partner_id.fiscalcode,
                re.sub(r'[^\w\s,.]+', '', debitor_street)[:30],
                debitor_zip[:5],
                debitor_city[:24],
                debitor_province,
                debit_abi,
                debit_cab,
                debit_bank.bank_name and debit_bank.bank_name[:50] or '',
                line.partner_id.ref and line.partner_id.ref[:16] or '',
                line.invoice_number[:40],
                line.invoice_date,
            ]
            arrayRiba.append(Riba)

        out = base64.encodestring(
            self._creaFile(array_testata, arrayRiba).encode("utf8"))
        self.write({
            'state': 'get',
            'riba_txt': out,
            'file_name': '%s.txt' % order_obj.name
        })

        model_data_obj = self.env['ir.model.data']
        view_rec = model_data_obj.get_object_reference(
            'l10n_it_ricevute_bancarie', 'wizard_riba_file_export')
        view_id = view_rec and view_rec[1] or False

        return {
            'view_type': 'form',
            'view_id': [view_id],
            'view_mode': 'form',
            'res_model': 'riba.file.export',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    _name = "riba.file.export"

    state = fields.Selection(
        (
            ('choose', 'choose'),   # choose accounts
            ('get', 'get'),         # get the file
        ),
        default='choose')
    riba_txt = fields.Binary('File', readonly=True)
    file_name = fields.Char('File name', readonly=True)
