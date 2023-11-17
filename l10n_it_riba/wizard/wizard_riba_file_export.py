# Copyright (C) 2011-2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# Thanks to Antonio de Vincentiis http://www.devincentiis.it/ ,
# GAzie http://gazie.sourceforge.net/
# and Cecchi s.r.l http://www.cecchi.com/
# Copyright 2023 Simone Rubino - Aion Tech


import base64
import datetime
import re

from odoo import _, fields, models
from odoo.exceptions import UserError


class RibaStorage:
    def __init__(self):
        self.sequence = 0
        self.creditor_bank = 0
        self.sia = 0
        self.riba_date = 0
        self.support = 0
        self.riba_total = 0
        self.riba_creditor = 0
        self.riba_description = ""
        self.riba_debtor_city_province = ""
        self.currency = 0


class RibaFileExport(models.TransientModel):
    """
    ***************************************************************************
     Questa classe genera il file RiBa standard ABI-CBI passando alla funzione
     "createFile" i due array di seguito specificati:
    $header = array monodimensionale con i seguenti index:
                  [0] = credit_sia variabile lunghezza 5 alfanumerico
                  [1] = credit_abi assuntrice variabile lunghezza 5 numerico
                  [2] = credit_cab assuntrice variabile lunghezza 5 numerico
                  [3] = credit_account conto variabile lunghezza 10 alfanumerico
                  [4] = creation_date variabile lunghezza 6 numerico formato
                    GGMMAA
                  [5] = support_name variabile lunghezza 20 alfanumerico
                  [6] = currency_code variabile lunghezza 1 alfanumerico
                    opzionale default "E"
                  [7] = company_name nome ragione sociale creditore variabile
                    lunghezza 24 alfanumerico
                  [8] = creditor_address variabile lunghezza 24 alfanumerico
                  [9] = creditor_zip_city variabile lunghezza 24 alfanumerico
                  [10] = ref (definizione attivita) creditore
                  [11] = codice fiscale/partita iva creditore alfanumerico
                    opzionale
    $ribas = array bidimensionale con i seguenti index:
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

    _name = "riba.file.export"
    _description = "RiBa File Export Wizard"
    _ribaStorage = RibaStorage()

    def _RecordIB(
        self,
        sia_creditor_bank,
        abi_creditor_bank,
        creation_date,
        support_name,
        currency_code,
    ):  # record di testa
        self._ribaStorage.sia = sia_creditor_bank.rjust(5, "0")
        self._ribaStorage.creditor_bank = abi_creditor_bank.rjust(5, "0")
        self._ribaStorage.riba_date = creation_date.rjust(6, "0")
        self._ribaStorage.currency = currency_code[0:1]
        self._ribaStorage.support = support_name.ljust(20, " ")
        return (
            " IB"
            + self._ribaStorage.sia
            + self._ribaStorage.creditor_bank
            + self._ribaStorage.riba_date
            + self._ribaStorage.support
            + " " * 74
            + self._ribaStorage.currency
            + " " * 6
            + "\r\n"
        )

    def _Record14(
        self,
        due_date,
        amount,
        abi_creditor_bank,
        cab_creditor_bank,
        account,
        abi_debtor_bank,
        cab_debtor_bank,
        sia_credit,
        customer_code,
    ):
        self._ribaStorage.riba_total += amount
        return (
            " 14"
            + str(self._ribaStorage.sequence).rjust(7, "0")
            + " " * 12
            + due_date
            + "30000"
            + str(int(round(amount * 100))).rjust(13, "0")
            + "-"
            + abi_creditor_bank.rjust(5, "0")
            + cab_creditor_bank.rjust(5, "0")
            + account.ljust(12, "0")
            + abi_debtor_bank.rjust(5, "0")
            + cab_debtor_bank.rjust(5, "0")
            + " " * 12
            + str(sia_credit).rjust(5, "0")
            + "4"
            + customer_code.ljust(16)
            + " " * 6
            + self._ribaStorage.currency
            + "\r\n"
        )

    def _Record20(
        self,
        creditor_company_name,
        creditor_address,
        creditor_zip_city,
        creditor_ref,
    ):
        self._ribaStorage.riba_creditor = creditor_company_name.ljust(24)
        return (
            " 20"
            + str(self._ribaStorage.sequence).rjust(7, "0")
            + self._ribaStorage.riba_creditor[0:24]
            + creditor_address.ljust(24)[0:24]
            + creditor_zip_city.ljust(24)[0:24]
            + creditor_ref.ljust(24)[0:24]
            + " " * 14
            + "\r\n"
        )

    def _Record30(self, debtor_name, debtor_fiscalcode):
        return (
            " 30"
            + str(self._ribaStorage.sequence).rjust(7, "0")
            + debtor_name.ljust(60)[0:60]
            + debtor_fiscalcode.ljust(16, " ")
            + " " * 34
            + "\r\n"
        )

    def _Record40(
        self,
        debtor_address,
        debtor_zip,
        debtor_city,
        debtor_province,
        debtor_bank_description="",
    ):
        self._ribaStorage.riba_debtor_city_province = (
            debtor_city + debtor_province.rjust(25 - len(debtor_city), " ")
        )
        return (
            " 40"
            + str(self._ribaStorage.sequence).rjust(7, "0")
            + debtor_address.ljust(30)[0:30]
            + str(debtor_zip).rjust(5, "0")
            + self._ribaStorage.riba_debtor_city_province
            + debtor_bank_description.ljust(50)[0:50]
            + "\r\n"
        )

    def _Record50(
        self, debit_amount, invoice_ref, invoice_date, creditor_vat_number, cig, cup
    ):
        self._ribaStorage.riba_description = (
            cig
            + cup
            + "PER LA FATTURA N. "
            + invoice_ref
            + " DEL "
            + invoice_date
            + " IMP "
            + str(debit_amount)
        )
        return (
            " 50"
            + str(self._ribaStorage.sequence).rjust(7, "0")
            + self._ribaStorage.riba_description.ljust(80)[0:80]
            + " " * 10
            + creditor_vat_number.ljust(16, " ")
            + " " * 4
            + "\r\n"
        )

    def _Record51(self, creditor_receipt_number):
        return (
            " 51"
            + str(self._ribaStorage.sequence).rjust(7, "0")
            + str(creditor_receipt_number).rjust(10, "0")
            + self._ribaStorage.riba_creditor[0:20]
            + " " * 80
            + "\r\n"
        )

    def _Record70(self):
        return (
            " 70" + str(self._ribaStorage.sequence).rjust(7, "0") + " " * 110 + "\r\n"
        )

    def _RecordEF(self):  # record di coda
        return (
            " EF"
            + self._ribaStorage.sia
            + self._ribaStorage.creditor_bank
            + self._ribaStorage.riba_date
            + self._ribaStorage.support
            + " " * 6
            + str(self._ribaStorage.sequence).rjust(7, "0")
            + str(int(round(self._ribaStorage.riba_total * 100))).rjust(15, "0")
            + "0" * 15
            + str(int(self._ribaStorage.sequence) * 7 + 2).rjust(7, "0")
            + " " * 24
            + self._ribaStorage.currency
            + " " * 6
            + "\r\n"
        )

    def _createFile(self, header, ribas):
        accumulator = self._RecordIB(
            header[0],
            header[1],
            header[4],
            header[5],
            header[6],
        )
        for value in ribas:  # estraggo le ricevute dall'array
            self._ribaStorage.sequence = self._ribaStorage.sequence + 1
            accumulator = accumulator + self._Record14(
                value[1],
                value[2],
                header[1],
                header[2],
                header[3],
                value[9],
                value[10],
                header[0],
                value[12],
            )
            accumulator = accumulator + self._Record20(
                header[7], header[8], header[9], header[10]
            )
            accumulator = accumulator + self._Record30(value[3], value[4])
            accumulator = accumulator + self._Record40(
                value[5], value[6], value[7], value[8], value[11]
            )
            accumulator = accumulator + self._Record50(
                value[2], value[13], value[14], header[11], value[15], value[16]
            )
            accumulator = accumulator + self._Record51(value[0])
            accumulator = accumulator + self._Record70()
        accumulator = accumulator + self._RecordEF()
        self._ribaStorage.sequence = 0
        self._ribaStorage.riba_total = 0
        return accumulator

    def act_getfile(self):
        active_ids = self.env.context.get("active_ids", [])
        order_obj = self.env["riba.slip"].browse(active_ids)[0]
        credit_bank = order_obj.config_id.bank_id
        company_name = order_obj.config_id.company_id.partner_id.name
        if not credit_bank.acc_number:
            raise UserError(_("No IBAN specified."))
        # remove spaces automatically added by odoo
        credit_iban = credit_bank.acc_number.replace(" ", "")
        credit_abi = credit_iban[5:10]
        credit_cab = credit_iban[10:15]
        credit_account = credit_iban[-12:]
        if not credit_bank.codice_sia:
            raise UserError(
                _(
                    "No SIA Code specified for %(company)s",
                    company=company_name,
                )
            )
        credit_sia = credit_bank.codice_sia
        issued_date = datetime.datetime.now().strftime("%d%m%y")
        support_name = datetime.datetime.now().strftime("%d%m%y%H%M%S") + credit_sia
        creditor_address = order_obj.config_id.company_id.partner_id
        creditor_city = creditor_address.city or ""
        if (
            not order_obj.config_id.company_id.partner_id.vat
            and not order_obj.config_id.company_id.partner_id.fiscalcode
        ):
            raise UserError(
                _(
                    "No VAT or Fiscal Code specified for %(company)s",
                    company=company_name,
                )
            )
        array_header = [
            credit_sia,
            credit_abi,
            credit_cab,
            credit_account,
            issued_date,
            support_name,
            "E",
            company_name,
            creditor_address.street or "",
            creditor_address.zip or "" + " " + creditor_city,
            order_obj.config_id.company_id.partner_id.ref or "",
            (
                order_obj.config_id.company_id.partner_id.vat
                and order_obj.config_id.company_id.partner_id.vat[2:]
                or order_obj.config_id.company_id.partner_id.fiscalcode
            ),
        ]
        array_riba = []
        for line in order_obj.line_ids:
            debit_bank = line.bank_id
            debtor_address = line.partner_id
            debtor_street = debtor_address.street or ""
            debtor_zip = debtor_address.zip or ""
            if debit_bank.bank_abi and debit_bank.bank_cab:
                debit_abi = debit_bank.bank_abi
                debit_cab = debit_bank.bank_cab
            elif debit_bank.acc_number:
                debit_iban = debit_bank.acc_number.replace(" ", "")
                debit_abi = debit_iban[5:10]
                debit_cab = debit_iban[10:15]
            else:
                raise UserError(
                    _(
                        "No IBAN or ABI/CAB specified for %(partner)s",
                        partner=line.partner_id.name,
                    )
                )
            debtor_city = (
                debtor_address.city and debtor_address.city.ljust(23)[0:23] or ""
            )
            debtor_province = (
                debtor_address.state_id and debtor_address.state_id.code or ""
            )
            if not line.due_date:  # ??? VERIFICARE
                due_date = "000000"
            else:
                due_date = line.due_date.strftime("%d%m%y")

            if not line.partner_id.vat and not line.partner_id.fiscalcode:
                raise UserError(
                    _(
                        "No VAT or Fiscal Code specified for %(partner)s",
                        partner=line.partner_id.name,
                    )
                )
            riba = [
                line.sequence,
                due_date,
                line.amount,
                # using regex we remove chars outside letters, numbers, space,
                # dot and comma because, special chars cause errors.
                re.sub(r"[^\w\s,.]+", "", line.partner_id.name)[:60],
                line.partner_id.vat
                and line.partner_id.vat[2:]
                or line.partner_id.fiscalcode,
                re.sub(r"[^\w\s,.]+", "", debtor_street)[:30],
                debtor_zip[:5],
                debtor_city[:24],
                debtor_province,
                debit_abi,
                debit_cab,
                debit_bank.bank_name and debit_bank.bank_name[:50] or "",
                line.partner_id.ref and line.partner_id.ref[:16] or "",
                line.invoice_number[:40],
                line.invoice_date,
                "CIG: %s " % line.cig if line.cig else "",
                "CUP: %s " % line.cup if line.cup else "",
            ]
            array_riba.append(riba)

        out = base64.encodebytes(
            self._createFile(array_header, array_riba).encode("utf8")
        )
        self.write(
            {"state": "get", "riba_txt": out, "file_name": "%s.txt" % order_obj.name}
        )

        view_rec = self.env.ref("l10n_it_riba.wizard_riba_file_export")
        view_id = view_rec.id if view_rec else False

        return {
            "view_id": [view_id],
            "view_mode": "form",
            "res_model": "riba.file.export",
            "res_id": self.id,
            "type": "ir.actions.act_window",
            "target": "new",
        }

    state = fields.Selection(
        (
            ("choose", "choose"),  # choose accounts
            ("get", "get"),  # get the file
        ),
        default="choose",
    )
    riba_txt = fields.Binary("File", readonly=True)
    file_name = fields.Char(readonly=True)
