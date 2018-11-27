# -*- coding: utf-8 -*-
# Copyright 2017 Didotech srl (<http://www.didotech.com>)
#                Andrei Levin <andrei.levin@didotech.com>
#                Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#                Odoo-Italia.org Community
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp.osv import fields, orm
from ..bindings.vat_settlement_v_1_0 import (
    Fornitura,
    # Intestazione,
    Intestazione_IVP_Type,
    # Comunicazione,
    Comunicazione_IVP_Type,
    Frontespizio_IVP_Type,
    DatiContabili_IVP_Type,
    CTD_ANON
)
import base64
import logging
import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

codice_fornitura = 'IVP17'
identificativo_software = 'Odoo.8.0.3.0.3'


class WizardVatSettlement(orm.TransientModel):
    _name = "wizard.vat.settlement"

    _columns = {
        'data': fields.binary("File", readonly=True),
        'name': fields.char('Filename', 32, readonly=True),
        'state': fields.selection((
            ('create', 'create'),  # choose
            ('get', 'get'),  # get the file
        )),
    }

    _defaults = {
        'state': lambda *a: 'create',
    }

    def get_date_start_stop(self, statement, context=None):
        date_start = False
        date_stop = False
        for period in statement.period_ids:
            if not date_start:
                date_start = period.date_start
            else:
                if period.date_start < date_start:
                    date_start = period.date_start
            if not date_stop:
                date_stop = period.date_stop
            else:
                if period.date_stop > date_stop:
                    date_stop = period.date_stop
        date_start = datetime.datetime.strptime(date_start,
                                                DEFAULT_SERVER_DATE_FORMAT)
        date_stop = datetime.datetime.strptime(date_stop,
                                               DEFAULT_SERVER_DATE_FORMAT)
        return date_start, date_stop


    def get_taxable(self, cr, uid, statement, type, context=None):
        """
        :param cr:
        :param uid:
        :param statement:
        :param type: 'credit' or 'debit'
        :param context:
        :return: amount_taxable
        """
        amount_base = 0.0
        if type == 'credit':
            credit_line_pool = self.pool.get('statement.credit.account.line')
            for credit_line in statement.credit_vat_account_line_ids:
                if credit_line.amount <> 0.0:
                    amount_base += credit_line.amount_base
        elif type == 'debit':
            debit_line_pool = self.pool.get('statement.debit.account.line')
            for debit_line in statement.debit_vat_account_line_ids:
                if debit_line.amount <> 0.0:
                    amount_base += debit_line.amount_base
        return amount_base

    @staticmethod
    def italian_number(number):
        return '{:.2f}'.format(number).replace('.', ',')

    @staticmethod
    def italian_date(dt):
        if len(dt) == 8:
            return dt[-2:] + dt[4:6] + dt[0:4]
        elif len(dt) == 10:
            return dt[-2:] + dt[5:7] + dt[0:4]
        else:
            return ''

    def export_vat_settlemet(self, cr, uid, ids, context=None):
        # TODO: insert period verification
        context = {} if context is None else context
        model_data_obj = self.pool['ir.model.data']
        statement_debit_account_line_obj = \
            self.pool['statement.debit.account.line']
        statement_credit_account_line_obj = \
            self.pool['statement.credit.account.line']

        trimestre = {
            '3': '1',
            '6': '2',
            '9': '3',
            '12': '4'
        }
        module_pool = self.pool.get('ir.module.module')
        company_pool = self.pool.get('res.company')
        ids = module_pool.search(
                cr, uid, [('name', '=', 'account_vat_period_end_statement')])
        if len(ids) == 0:
            _logger.info('Invalid software signature.')
            _logger.info('Please contact antoniomaria.vigliotti@gmail.com '
                         'to obtain free valid software')
            identificativo_software = ''
        else:
            ver = module_pool.browse(cr, uid,
                ids[0]).installed_version
            identificativo_software = 'Odoo' + ver
            identificativo_software = identificativo_software.upper()

        statement_pool = self.pool.get('account.vat.period.end.statement')
        statement_ids = context.get('active_ids', False)

        for statement in statement_pool.browse(cr,
                                               uid,
                                               statement_ids,
                                               context=context):
            ids = statement_pool.search(
                cr, uid, [],
                order='progressivo_telematico desc',
                limit=1,
                context=context)
            if len(ids):
                progressivo_telematico = statement_pool.browse(
                    cr, uid,
                    ids[0]).progressivo_telematico + 1
            else:
                progressivo_telematico = 1

            company_id = statement.company_id.id
            company = company_pool.browse(cr, uid, company_id, context=context)
            if company.partner_id.vat[:2].lower() == 'it':
                vat = company.partner_id.vat[2:]
            else:
                vat = company.partner_id.vat
            if company.partner_id.fiscalcode:
                if len(company.partner_id.fiscalcode) == 16:
                    fiscalcode = company.partner_id.fiscalcode
                else:
                    fiscalcode = company.partner_id.fiscalcode[2:]
            else:
                fiscalcode = vat
            settlement = Fornitura()
            settlement.Intestazione = (Intestazione_IVP_Type())
            settlement.Intestazione.CodiceFornitura = codice_fornitura

            _logger.debug(settlement.Intestazione.toDOM().toprettyxml(
                encoding="latin1"))

            settlement.Comunicazione = (Comunicazione_IVP_Type())
            settlement.Comunicazione.Frontespizio = (Frontespizio_IVP_Type())

            settlement.Comunicazione.Frontespizio.FirmaDichiarazione = "1"
            settlement.Comunicazione.Frontespizio.CodiceFiscale = fiscalcode
                #statement.incaricato_trasmissione_codice_fiscale # TODO qui ci va quello dell'azienda!!!
            if statement.incaricato_trasmissione_codice_fiscale:
                settlement.Comunicazione.Frontespizio.CFIntermediario = \
                    statement.incaricato_trasmissione_codice_fiscale
                settlement.Comunicazione.Frontespizio.ImpegnoPresentazione =\
                    "1"
                if statement.incaricato_trasmissione_data_impegno:
                    settlement.Comunicazione.Frontespizio.DataImpegno = \
                        self.italian_date(
                            statement.incaricato_trasmissione_data_impegno)
                settlement.Comunicazione.Frontespizio.FirmaIntermediario = "1"

            if statement.codice_carica:
                if statement.codice_carica != '0':
                    settlement.Comunicazione.Frontespizio.CFDichiarante = \
                        statement.soggetto_codice_fiscale
                    settlement.Comunicazione.Frontespizio.\
                        CodiceCaricaDichiarante = \
                        statement.codice_carica
                elif not statement.incaricato_trasmissione_codice_fiscale:
                    settlement.Comunicazione.Frontespizio.CodiceFiscale = \
                        statement.soggetto_codice_fiscale
            date_start, date_stop = self.get_date_start_stop(statement,
                                                             context=context)
            settlement.Comunicazione.Frontespizio.AnnoImposta = str(
                date_stop.year)
            settlement.Comunicazione.Frontespizio.PartitaIVA = vat

            # settlement.Comunicazione.Frontespizio.PIVAControllante
            # settlement.Comunicazione.Frontespizio.UltimoMese = str(
            # date_period_end.month)
            # settlement.Comunicazione.Frontespizio.LiquidazioneGruppo
            # settlement.Comunicazione.Frontespizio.CodiceFiscaleSocieta
            # settlement.Comunicazione.Frontespizio.FlagConferma
            if identificativo_software:
                settlement.Comunicazione.Frontespizio.\
                    IdentificativoProdSoftware = identificativo_software
            _logger.debug(
                settlement.Comunicazione.Frontespizio.toDOM().toprettyxml(
                    encoding="UTF-8"))

            settlement.Comunicazione.DatiContabili = (DatiContabili_IVP_Type())

            # We may have more than one modulo, but do we want it?
            # modulo_period_end = datetime.datetime.strptime(
            # statement.date, DEFAULT_SERVER_DATE_FORMAT)
            modulo = CTD_ANON()
            # <<<<< quarter_vat_period non esite nella 7.0 >>>>>
            # if statement.period_ids[0].fiscalyear_id.quarter_vat_period:
            #     # trimestrale
            #     modulo.Trimestre = trimestre[str(modulo_period_end.month)]
            # else:
            #     # mensile
            #    modulo.Mese = str(modulo_period_end.month)
            if date_start.month == date_stop.month:
                modulo.Mese = str(date_stop.month)
            else:
                if date_start.month in (1, 4, 7, 10) and \
                        date_stop.month in (3, 6, 9, 12):
                    modulo.Trimestre = trimestre[str(date_stop.month)]
                else:
                    _logger.info(
                        'Undetermined quarter/month!')
                    raise orm.except_orm(
                        'Error!',
                        "Undetermined quarter/month!")

            # TODO: Per aziende supposte al controllo antimafia (i subfornitori), per il momento non valorizziamo
            # modulo.Subfornitura = "0"
            # TODO: facoltativo: Vittime del terremoto, per il momento non
            # valorizziamo
            # modulo.EventiEccezionali =

            modulo.TotaleOperazioniAttive = self.italian_number(
                self.get_taxable(cr, uid, statement, 'debit', context)
            )
            modulo.TotaleOperazioniPassive = self.italian_number(
                self.get_taxable(cr, uid, statement, 'credit', context)
            )

            iva_esigibile = 0
            debit_account_line_ids = statement_debit_account_line_obj.search(
                cr, uid, [('statement_id', '=', statement.id)])
            for debit_account_line in statement_debit_account_line_obj.browse(
                    cr, uid, debit_account_line_ids, context):
                iva_esigibile += debit_account_line.amount
            # NOTE: formato numerico;
            #  i decimali vanno separati con il carattere  ',' (virgola)
            modulo.IvaEsigibile = self.italian_number(iva_esigibile)

            iva_detratta = 0
            credit_account_line_ids = statement_credit_account_line_obj.search(
                cr, uid, [('statement_id', '=', statement.id)])
            for credit_account_line in statement_credit_account_line_obj.\
                    browse(cr, uid, credit_account_line_ids, context):
                iva_detratta += credit_account_line.amount
            # NOTE: formato numerico;
            #  i decimali vanno separati con il carattere  ',' (virgola)
            modulo.IvaDetratta = self.italian_number(iva_detratta)

            if iva_esigibile > iva_detratta:
                iva_dovuta = iva_esigibile - iva_detratta
                modulo.IvaDovuta = self.italian_number(iva_dovuta)
            else:
                iva_credito = iva_detratta - iva_esigibile
                modulo.IvaCredito = self.italian_number(iva_credito)
            # TODO: lasciamo per dopo
            # modulo.IvaDetratta = self.italian_number(iva_detratta)
            # modulo.IvaCredito =

            previous_debit = statement.previous_debit_vat_amount
            if previous_debit:
                modulo.DebitoPrecedente = self.italian_number(previous_debit)

            previous_credit = statement.previous_credit_vat_amount
            if previous_credit:
                if date_start.month == 1:
                    modulo.CreditoAnnoPrecedente = self.italian_number(
                        previous_credit)
                else:
                    modulo.CreditoPeriodoPrecedente = self.italian_number(
                        previous_credit)

            # Chiedere all'utente
            # modulo.CreditoAnnoPrecedente

            # TODO: lasciamo per dopo
            # modulo.VersamentiAutoUE

            # modulo.CreditiImposta
            # modulo.InteressiDovuti
            # modulo.Acconto

            if statement.authority_vat_amount > 0:
                # NOTE: formato numerico; i decimali vanno separati
                # dall'intero con il carattere  ',' (virgola)
                modulo.ImportoDaVersare = self.italian_number(
                    statement.authority_vat_amount)
            elif statement.authority_vat_amount < 0:
                # NOTE: formato numerico; i decimali vanno separati
                # dall'intero con il carattere  ',' (virgola)
                modulo.ImportoACredito = self.italian_number(
                    -statement.authority_vat_amount)

            settlement.Comunicazione.DatiContabili.Modulo.append(modulo)

            _logger.debug(settlement.Comunicazione.DatiContabili.
                          toDOM().toprettyxml(encoding="latin1"))

            settlement.Comunicazione.identificativo = \
                "%05d" % progressivo_telematico

            vat_settlement_xml = settlement.toDOM().toprettyxml(
                encoding="latin1")

            # fn_name = 'LiquidazioneIVA-%05d.xml' % progressivo_telematico
            fn_name = 'IT%s_LI_%05d.xml'  % (vat, progressivo_telematico)
            attach_vals = {
                'name': fn_name,
                'datas_fname': fn_name,
                'datas': base64.encodestring(vat_settlement_xml),
                'res_model': 'account.vat.period.end.statement',
                'res_id': statement.id
            }
            statement_pool.write(cr, uid, [statement.id],
                {'progressivo_telematico': progressivo_telematico})
            vat_settlement_attachment_out_id = self.pool[
                'account.vat.settlement.attachment'].create(cr,
                    uid, attach_vals, context={})

        view_rec = model_data_obj.get_object_reference(
            cr, uid, 'account_vat_period_end_statement_ivp',
            'view_vat_settlement_attachment_form')
        if view_rec:
            view_id = view_rec and view_rec[1] or False
        return {
            'view_type': 'form',
            'name': "Export Liquidazione IVA",
            'view_id': [view_id],
            'res_id': vat_settlement_attachment_out_id,
            'view_mode': 'form',
            'res_model': 'account.vat.settlement.attachment',
            'type': 'ir.actions.act_window',
            'context': context
        }
