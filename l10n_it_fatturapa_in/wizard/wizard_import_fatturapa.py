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
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import base64
from openerp.osv import orm
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

from openerp.addons.l10n_it_fatturapa.bindings import fatturapa_v_1_1
from openerp.addons.base_iban import base_iban


class WizardImportFatturapa(orm.TransientModel):
    _name = "wizard.import.fatturapa"
    _description = "Import FatturaPA"

    def saveAttachment(self, cr, uid, context=None):
        if not context:
            context = {}

        return False

    def CountryByCode(self, cr, uid, CountryCode, context=None):
        country_model = self.pool['res.country']
        return country_model.search(
            cr, uid, [('code', '=', CountryCode)], context=context)

    def ProvinceByCode(self, cr, uid, provinceCode, context=None):
        province_model = self.pool['res.province']
        return province_model.search(
            cr, uid, [('code', '=', provinceCode)], context=context)

    def getPartnerBase(self, cr, uid, angrafica, context=None):
        partner_model = self.pool['res.partner']
        cf = angrafica.CodiceFiscale or False
        CountryCode = angrafica.IdFiscaleIVA.IdPaese
        country_ids = self.CountryByCode(
            cr, uid, CountryCode, context=context)
        if country_ids:
            country_id = country_ids[0]
        else:
            raise orm.except_orm(
                _('Error !'),
                _("Country Code %s not found in system") % CountryCode
            )
        vat = "%s%s" % (
            angrafica.IdFiscaleIVA.IdPaese,
            angrafica.IdFiscaleIVA.IdCodice
        )
        partner_ids = partner_model.search(
            cr, uid,
            ['|',
             ('vat', '=', vat or 0),
             ('fiscalcode', '=', cf or 0),
             ],
            context=context)
        if len(partner_ids) > 1:
            raise orm.except_orm(
                _('Error !'),
                _("Two distinct partners with "
                  "Vat %s and Fiscalcode %s already present in db" %
                  (vat, cf))
                )
        if partner_ids:
            return partner_ids[0]
        else:
            vals = {
                'name': angrafica.Anagrafica.Denominazione,
                'firstname': angrafica.Anagrafica.Nome or '',
                'lastname': angrafica.Anagrafica.Cognome or '',
                'vat': vat,
                'fiscalcode': cf,
                'customer': False,
                'supplier': True,
                # TODO: needs verify
                'is_company': vat and True or False,
                'eori_code': angrafica.Anagrafica.CodEORI or '',
                'country_id': country_id,
            }
            return partner_model.create(cr, uid, vals, context=context)

    def getCedPrest(self, cr, uid, cedPrest, context=None):
        partner_model = self.pool['res.partner']
        partner_id = self.getPartnerBase(
            cr, uid, cedPrest.DatiAnagrafici, context=context)
        vals = {}
        if partner_id:
            vals = {
                'street': cedPrest.Sede.Indirizzo,
                'zip': cedPrest.Sede.CAP,
                'city': cedPrest.Sede.Comune,
            }

            if cedPrest.IscrizioneREA:
                REA = cedPrest.IscrizioneREA
                if not REA.NumeroREA:
                    raise orm.except_orm(
                        _('Error !'),
                        _("Xml file not contain REA code")
                        )
                office_id = False
                office_ids = self.ProvinceByCode(
                    cr, uid, REA.NumeroREA, context=context)
                if not office_ids:
                    raise orm.except_orm(
                        _('Error !'),
                        _("Xml file not contain REA Office Code")
                        )
                office_id = office_ids[0]
                vals['rea_office'] = office_id
                vals['rea_code'] = REA.NumeroREA
                vals['rea_capital'] = REA.CapitaleSociale or 0.0
                vals['rea_member_type'] = REA.SocioUnico or False
                vals['rea_liquidation_state'] = REA.StatoLiquidazione or False

            if cedPrest.Contatti:
                vals['phone'] = cedPrest.Contatti.Telefono
                vals['email'] = cedPrest.Contatti.Email
                vals['fax'] = cedPrest.Contatti.Fax
            partner_model.write(cr, uid, partner_id, vals, context=context)
        return partner_id

    def getCarrirerPartner(self, cr, uid, Carrier, context=None):
        partner_model = self.pool['res.partner']
        partner_id = self.getPartnerBase(
            cr, uid, Carrier.DatiAnagraficiVettore, context=context)
        vals = {}
        if partner_id:
            vals = {
                'license_number':
                Carrier.DatiAnagraficiVettore.NumeroLicenzaGuida or '',
            }
            partner_model.write(cr, uid, partner_id, vals, context=context)
        return partner_id

    def _prepareInvoiceLine(
        self, cr, uid, credit_account_id, line, context=None
    ):
        account_tax_model = self.pool['account.tax']
        if float(line.AliquotaIVA) == 0.0 and line.Natura:
            account_tax_ids = account_tax_model.search(
                cr, uid,
                [
                    ('type_tax_use', 'in', ('purchase', 'all')),
                    ('non_taxable_nature', '=', line.Natura),
                    ('amount', '=', 0.0),
                ], context=context)
            if not account_tax_ids:
                raise orm.except_orm(
                    _('Error!'),
                    _('No tax with percentage '
                      '%s and nature %s found')
                    % (line.AliquotaIVA, line.Natura))
            if len(account_tax_ids) > 1:
                raise orm.except_orm(
                    _('Error!'),
                    _('Too many tax with percentage '
                      '%s and nature %s found')
                    % (line.AliquotaIVA, line.Natura))
        else:
            account_tax_ids = account_tax_model.search(
                cr, uid,
                [
                    ('type_tax_use', 'in', ('purchase', 'all')),
                    ('amount', '=', float(line.AliquotaIVA) / 100),
                    ('price_include', '=', False),
                    # partially deductible VAT must be set by user
                    ('child_ids', '=', False),
                ], context=context)
            if not account_tax_ids:
                raise orm.except_orm(
                    _('Error!'),
                    _('Define a tax with percentage '
                      'equals to: "%s"')
                    % line.AliquotaIVA)
            if len(account_tax_ids) > 1:
                raise orm.except_orm(
                    _('Error!'),
                    _('Too many tax with percentage '
                      'equals to: "%s"')
                    % line.AliquotaIVA)
        return {
            'name': line.Descrizione,
            'sequence': int(line.NumeroLinea),
            'account_id': credit_account_id,
            'price_unit': float(line.PrezzoUnitario),
            'quantity': float(line.Quantita),
            'invoice_line_tax_id': [(6, 0, [account_tax_ids[0]])],
        }

    def _prepareRelDocsLine(
        self, cr, uid, invoice_id, line, type, context=None
    ):
        res = []
        lineref = line.RiferimentoNumeroLinea or False
        IdDoc = line.IdDocumento or 'Error'
        Data = line.Data or False
        NumItem = line.NumItem or ''
        Code = line.CodiceCommessaConvenzione or ''
        Cup = line.CodiceCIG or ''
        Cig = line.CodiceCUP or ''
        invoice_lineid = False
        if lineref:
            for numline in lineref:
                invoice_lineid = False
                invoice_line_model = self.pool['account.invoice.line']
                invoice_line_ids = invoice_line_model.search(
                    cr, uid,
                    [
                        ('invoice_id', '=', invoice_id),
                        ('sequence', '=', int(numline)),
                    ], context=context)

                if invoice_line_ids:
                    invoice_lineid = invoice_line_ids[0]
                val = {
                    'type': type,
                    'name': IdDoc,
                    'lineRef': lineref,
                    'invoice_line_id': invoice_lineid,
                    'invoice_id': invoice_id,
                    'date': Data,
                    'numitem': NumItem,
                    'code': Code,
                    'cig': Cig,
                    'cup': Cup,
                }
                res.append(val)

        else:
            val = {
                'type': type,
                'name': IdDoc,
                'lineRef': lineref,
                'invoice_line_id': invoice_lineid,
                'invoice_id': invoice_id,
                'date': Data,
                'numitem': NumItem,
                'code': Code,
                'cig': Cig,
                'cup': Cup
            }
            res.append(val)
        return res

    def _prepareWelfareLine(
        self, cr, uid, invoice_id, line, context=None
    ):
        res = []
        TipoCassa = line.TipoCassa or False
        AlCassa = (float(line.AlCassa)/100) or 0.0
        ImportoContributoCassa = float(line.ImportoContributoCassa) or 0.0
        ImponibileCassa = float(line.ImponibileCassa) or 0.0
        AliquotaIVA = (float(line.AliquotaIVA)/100) or 0.0
        Ritenuta = line.Ritenuta or ''
        Natura = line.Natura or False
        RiferimentoAmministrazione = line.RiferimentoAmministrazione or ''
        WelfareTypeModel = self.pool['welfare.fund.type']
        if not TipoCassa:
            raise orm.except_orm(
                _('Error!'),
                _('TipoCassa is not defined ')
            )
        WelfareTypeId = WelfareTypeModel.search(
            cr, uid,
            [('name', '=', TipoCassa)],
            context=context
        )
        NaturaId = False
        if Natura:
            NaturaIds = WelfareTypeModel.search(
                cr, uid,
                [('name', '=', Natura)],
                context=context
            )
            if NaturaIds:
                NaturaId = NaturaIds[0]
        if not WelfareTypeId:
            raise orm.except_orm(
                _('Error!'),
                _('TipoCassa type is not compatible ')
            )
        res = {
            'name': WelfareTypeId[0],
            'welfare_rate_tax': AlCassa,
            'welfare_amount_tax': ImportoContributoCassa,
            'welfare_taxable': ImponibileCassa,
            'welfare_Iva_tax': AliquotaIVA,
            'subjected_withholding': Ritenuta,
            'fund_fiscalpos': NaturaId,
            'pa_line_code': RiferimentoAmministrazione,
            'invoice_id': invoice_id,
        }
        return res

    def _prepareDiscRisePriceLine(
        self, cr, uid, invoice_id, line, context=None
    ):
        res = []
        Tipo = line.Tipo or False
        Percentuale = (float(line.Percentuale)/100) or 0.0
        Importo = float(line.Importo) or 0.0
        if not Tipo:
            raise orm.except_orm(
                _('Error!'),
                _('Type Discount or Rise price is not defined ')
            )
        res = {
            'name': Tipo,
            'percentage': Percentuale,
            'amount': Importo,
            'invoice_id': invoice_id,
        }
        return res

    def _CreatePayamentsLine(
        self, cr, uid, payment_id, line, partner_id,
        context=None
    ):
        PaymentModel = self.pool['fatturapa.payment.detail']
        PaymentMethodModel = self.pool['fatturapa.payment_method']
        details = line.DettaglioPagamento or False
        if details:
            for dline in details:
                BankModel = self.pool['res.bank']
                PartnerBankModel = self.pool['res.partner.bank']
                method_id = PaymentMethodModel.search(
                    cr, uid,
                    [('code', '=', dline.ModalitaPagamento)],
                    context=context
                )
                if not method_id:
                    raise orm.except_orm(
                        _('Error!'),
                        _(
                            'Xml Incorrect'
                            'ModalitaPagamento in line DettaglioPagamento'
                            'is not defined'
                        )
                    )
                val = {
                    'recipient': dline.Beneficiario,
                    'fatturapa_pm_id': method_id[0],
                    'payment_term_start':
                    dline.DataRiferimentoTerminiPagamento or False,
                    'payment_days':
                    dline.GiorniTerminiPagamento or 0,
                    'payment_due_date':
                    dline.DataScadenzaPagamento or False,
                    'payment_amount':
                    dline.ImportoPagamento or 0.0,
                    'post_office_code':
                    dline.CodUfficioPostale or '',
                    'recepit_surname':
                    dline.CognomeQuietanzante or '',
                    'recepit_name':
                    dline.NomeQuietanzante or '',
                    'recepit_cf':
                    dline.CFQuietanzante or '',
                    'recepit_title':
                    dline.TitoloQuietanzante or '1',
                    'payment_bank_name':
                    dline.IstitutoFinanziario or '',
                    'payment_bank_iban':
                    dline.IBAN or '',
                    'payment_bank_abi':
                    dline.ABI or '',
                    'payment_bank_cab':
                    dline.CAB or '',
                    'payment_bank_bic':
                    dline.BIC or '',
                    'payment_bank': False,
                    'prepayment_discount':
                    dline.ScontoPagamentoAnticipato or 0.0,
                    'max_payment_date':
                    dline.DataLimitePagamentoAnticipato or False,
                    'penalty_amount':
                    dline.PenalitaPagamentiRitardati or 0.0,
                    'penalty_date':
                    dline.DataDecorrenzaPenale or False,
                    'payment_code':
                    dline.CodicePagamento or '',
                    'payment_data_id': payment_id
                }
                bankid = False
                payment_bank_id = False
                if dline.BIC:
                    bankids = BankModel.search(
                        cr, uid,
                        [('bic', '=', dline.BIC.strip())], context=context
                    )
                    if not bankids:
                        if dline.IstitutoFinanziario == '':
                            raise orm.except_orm(
                                _('Error!'),
                                _('Name of Banck is required')
                            )
                        bankid = BankModel.create(
                            cr, uid,
                            {
                                'name': dline.IstitutoFinanziario,
                                'bic': dline.BIC,
                            },
                            context=context
                        )
                    else:
                        bankid = bankids[0]
                if dline.IBAN:
                    SearchDom = [
                        ('state', '=', 'iban'),
                        (
                            'acc_number', '=',
                            base_iban._pretty_iban(dline.IBAN.strip())
                        ),
                        ('partner_id', '=', partner_id),
                    ]
                    payment_bank_id = False
                    payment_bank_ids = PartnerBankModel.search(
                        cr, uid, SearchDom, context=context)
                    if not payment_bank_ids and not bankid:
                        raise orm.except_orm(
                            _('Error!'),
                            _('BIC is required and not exist in Xml')
                        )
                    elif not payment_bank_ids and bankid:
                        payment_bank_id = PartnerBankModel.create(
                            cr, uid,
                            {
                                'state': 'iban',
                                'acc_number': dline.IBAN.strip(),
                                'partner_id': partner_id,
                                'bank': bankid,
                                'bank_name': dline.IstitutoFinanziario,
                                'bank_bic': dline.BIC
                            },
                            context=context
                        )
                    if payment_bank_ids:
                        payment_bank_id = payment_bank_ids[0]
                val['payment_bank'] = payment_bank_id
                PaymentModel.create(cr, uid, val, context=context)
        return True

    def invoiceCreate(
        self, cr, uid, fatt, fatturapa_attachment, FatturaBody,
        partner_id, context=None
    ):
        if context is None:
            context = {}
        partner_model = self.pool['res.partner']
        journal_model = self.pool['account.journal']
        invoice_model = self.pool['account.invoice']
        currency_model = self.pool['res.currency']
        invoice_line_model = self.pool['account.invoice.line']
        rel_docs_model = self.pool['fatturapa.related_document_type']
        WelfareFundLineModel = self.pool['welfare.fund.data.line']
        DiscRisePriceModel = self.pool['discount.rise.price']
        SalModel = self.pool['faturapa.activity.progress']
        DdTModel = self.pool['fatturapa.related_ddt']
        PaymentDataModel = self.pool['fatturapa.payment.data']
        PaymentTermsModel = self.pool['fatturapa.payment_term']

        company = self.pool['res.users'].browse(
            cr, uid, uid, context=context).company_id
        partner = partner_model.browse(cr, uid, partner_id, context=context)
        pay_acc_id = partner.property_account_payable.id
        # FIXME: takes the first purchase journal without any check.
        journal_ids = journal_model.search(
            cr, uid,
            [
                ('type', '=', 'purchase'),
                ('company_id', '=', company.id)
            ],
            limit=1, context=context)
        if not journal_ids:
            raise orm.except_orm(
                _('Error!'),
                _(
                    'Define a purchase journal '
                    'for this company: "%s" (id:%d).'
                ) % (company.name, company.id)
            )
        purchase_journal = journal_model.browse(
            cr, uid, journal_ids[0], context=context)
        # currency 2.1.1.2
        currency_id = currency_model.search(
            cr, uid,
            [
                (
                    'name', '=',
                    FatturaBody.DatiGenerali.DatiGeneraliDocumento.Divisa
                )
            ],
            context=context)
        if not currency_id:
            raise orm.except_orm(
                _('Error!'),
                _(
                    'No currency found with code %s'
                    % FatturaBody.DatiGenerali.DatiGeneraliDocumento.Divisa
                )
            )
        credit_account_id = purchase_journal.default_credit_account_id.id
        invoice_lines = []
        #2.2.1
        for line in FatturaBody.DatiBeniServizi.DettaglioLinee:
            invoice_line_data = self._prepareInvoiceLine(
                cr, uid, credit_account_id, line, context=context)
            invoice_line_id = invoice_line_model.create(
                cr, uid, invoice_line_data, context=context)
            invoice_lines.append(invoice_line_id)
        comment = ''
        #2.1.1.11
        causLst = FatturaBody.DatiGenerali.DatiGeneraliDocumento.Causale
        if causLst:
            for item in causLst:
                comment += item + '\n'
        invoice_data = {
            'name': 'Fattura ' + partner.name,
            'date_invoice':
            FatturaBody.DatiGenerali.DatiGeneraliDocumento.Data,
            'supplier_invoice_number':
            FatturaBody.DatiGenerali.DatiGeneraliDocumento.Numero,
            'sender': fatt.FatturaElettronicaHeader.SoggettoEmittente or False,
            'account_id': pay_acc_id,
            'type': 'in_invoice',
            'partner_id': partner_id,
            'currency_id': currency_id[0],
            'journal_id': len(journal_ids) and journal_ids[0] or False,
            'invoice_line': [(6, 0, invoice_lines)],
            # 'origin': xmlData.datiOrdineAcquisto,
            'fiscal_position': False,
            'payment_term': False,
            'company_id': company.id,
            'fatturapa_attachment_in_id': fatturapa_attachment.id,
            'comment': comment
        }
        #2.1.1.5
        Withholding = FatturaBody.DatiGenerali.\
            DatiGeneraliDocumento.DatiRitenuta
        if Withholding:
            invoice_data['withholding_amount'] = Withholding.ImportoRitenuta
            invoice_data['ftpa_withholding_type'] = Withholding.TipoRitenuta
            invoice_data['ftpa_withholding_rate'] = float(
                Withholding.AliquotaRitenuta)/100
            invoice_data['ftpa_withholding_payment_reason'] = Withholding.\
                CausalePagamento
        #2.1.1.6
        Stamps = FatturaBody.DatiGenerali.\
            DatiGeneraliDocumento.DatiBollo
        if Stamps:
            invoice_data['virtual_stamp'] = Stamps.BolloVirtuale
            invoice_data['stamp_amount'] = float(Stamps.ImportoBollo)
        invoice_id = invoice_model.create(
            cr, uid, invoice_data, context=context)

        invoice = invoice_model.browse(cr, uid, invoice_id, context=context)
        #2.1.1.7
        Walfares = FatturaBody.DatiGenerali.\
            DatiGeneraliDocumento.DatiCassaPrevidenziale
        if Walfares:
            for walfareLine in Walfares:
                WalferLineVals = self._prepareWelfareLine(
                    cr, uid, invoice_id, walfareLine, context=context)
                WelfareFundLineModel.create(
                    cr, uid, WalferLineVals, context=context)
        #2.1.1.8
        DiscountRises = FatturaBody.DatiGenerali.\
            DatiGeneraliDocumento.ScontoMaggiorazione
        if DiscountRises:
            for DiscRisePriceLine in Walfares:
                DiscRisePriceVals = self._prepareDiscRisePriceLine(
                    cr, uid, invoice_id, DiscRisePriceLine, context=context)
                DiscRisePriceModel.create(
                    cr, uid, DiscRisePriceVals, context=context)
        #2.1.2
        relOrders = FatturaBody.DatiGenerali.DatiOrdineAcquisto
        if relOrders:
            for order in relOrders:
                doc_datas = self._prepareRelDocsLine(
                    cr, uid, invoice_id, order, 'order', context=context)
                if doc_datas:
                    for doc_data in doc_datas:
                        rel_docs_model.create(
                            cr, uid, doc_data, context=context)
        #2.1.3
        relContracts = FatturaBody.DatiGenerali.DatiContratto
        if relContracts:
            for contract in relContracts:
                doc_datas = self._prepareRelDocsLine(
                    cr, uid, invoice_id, contract, 'contract', context=context)
                if doc_datas:
                    for doc_data in doc_datas:
                        rel_docs_model.create(
                            cr, uid, doc_data, context=context)
        #2.1.4
        relAgreements = FatturaBody.DatiGenerali.DatiConvenzione
        if relAgreements:
            for agreement in relAgreements:
                doc_datas = self._prepareRelDocsLine(
                    cr, uid, invoice_id, agreement,
                    'agreement', context=context)
                if doc_datas:
                    for doc_data in doc_datas:
                        rel_docs_model.create(
                            cr, uid, doc_data, context=context)
        #2.1.5
        relReceptions = FatturaBody.DatiGenerali.DatiRicezione
        if relReceptions:
            for reception in relReceptions:
                doc_datas = self._prepareRelDocsLine(
                    cr, uid, invoice_id, reception,
                    'reception', context=context)
                if doc_datas:
                    for doc_data in doc_datas:
                        rel_docs_model.create(
                            cr, uid, doc_data, context=context)
        #2.1.6
        RelInvoices = FatturaBody.DatiGenerali.DatiFattureCollegate
        if RelInvoices:
            for invoice in RelInvoices:
                doc_datas = self._prepareRelDocsLine(
                    cr, uid, invoice_id, invoice, 'invoice', context=context)
                if doc_datas:
                    for doc_data in doc_datas:
                        rel_docs_model.create(
                            cr, uid, doc_data, context=context)
        #2.1.7
        SalDatas = FatturaBody.DatiGenerali.DatiSAL
        if SalDatas:
            for SalDataLine in SalDatas:
                SalModel.create(
                    cr, uid,
                    {
                        'fatturapa_activity_progress': (
                            SalDataLine.RiferimentoFase or 0),
                        'invoice_id': invoice_id
                    }, context=context
                )
        #2.1.8
        DdtDatas = FatturaBody.DatiGenerali.DatiDDT
        if DdtDatas:
            for DdtDataLine in DdtDatas:
                if not DdtDataLine.RiferimentoNumeroLinea:
                    DdTModel.create(
                        cr, uid,
                        {
                            'name': DdtDataLine.NumeroDDT or '',
                            'date': DdtDataLine.DataDDT or False,
                            'invoice_id': invoice_id
                        }, context=context
                    )
                else:
                    for numline in DdtDataLine.RiferimentoNumeroLinea:
                        invoice_line_ids = invoice_line_model.search(
                            cr, uid,
                            [
                                ('invoice_id', '=', invoice_id),
                                ('sequence', '=', int(numline)),
                            ], context=context)
                        invoice_lineid = False
                        if invoice_line_ids:
                            invoice_lineid = invoice_line_ids[0]
                        DdTModel.create(
                            cr, uid,
                            {
                                'name': DdtDataLine.NumeroDDT or '',
                                'date': DdtDataLine.DataDDT or False,
                                'invoice_id': invoice_id,
                                'invoice_line_id': invoice_lineid
                            }, context=context
                        )
        #2.1.9
        Delivery = FatturaBody.DatiGenerali.DatiTrasporto
        if Delivery:
            delivery_id = self.getCarrirerPartner(
                cr, uid, Delivery, context=context)
            if delivery_id:
                delivery_dict = {
                    'carrier_id': delivery_id,
                    'transport_vaicle': Delivery.MezzoTrasporto or '',
                    'transport_reason': Delivery.CausaleTrasporto or '',
                    'number_items': Delivery.NumeroColli or 0,
                    'description': Delivery.Descrizione or '',
                    'unit_weight': Delivery.UnitaMisuraPeso or 0.0,
                    'gross_weight': Delivery.PesoLordo or 0.0,
                    'net_weight': Delivery.PesoNetto or 0.0,
                    'pickup_datetime': Delivery.DataOraRitiro or False,
                    'transport_date': Delivery.DataInizioTrasporto or False,
                    'delivery_datetime': Delivery.DataOraConsegna or False,
                    'delivery_address': '',
                }
                if Delivery.IndirizzoResa:
                    delivery_dict['delivery_address'] = (
                        '{0}, {1}\n{2} - {3}\n{4} {5}'.format(
                            Delivery.IndirizzoResa.Indirizzo or '',
                            Delivery.IndirizzoResa.NumeroCivico or '',
                            Delivery.IndirizzoResa.CAP or '',
                            Delivery.IndirizzoResa.Comune or '',
                            Delivery.IndirizzoResa.Provincia or '',
                            Delivery.IndirizzoResa.Nazione or ''
                        )
                    )
                if Delivery.TipoResa:
                    StockModel = self.pool['stock.incoterms']
                    stock_incoterm_id = StockModel.search(
                        cr, uid, [('code', '=', Delivery.TipoResa)],
                        context=context
                    )
                    if stock_incoterm_id:
                        delivery_dict['incoterm'] = stock_incoterm_id
                invoice_model.write(
                    cr, uid, invoice_id, delivery_dict, context=context)
        #2.1.10
        ParentInvoice = FatturaBody.DatiGenerali.FatturaPrincipale
        if ParentInvoice:
            parentinv_vals = {
                'related_invoice_code':
                ParentInvoice.NumeroFatturaPrincipale or '',
                'related_invoice_date':
                ParentInvoice.DataFatturaPrincipale or False
            }
            invoice_model.write(
                cr, uid, invoice_id, parentinv_vals, context=context)
        #2.3
        Veicle = FatturaBody.DatiVeicoli
        if Veicle:
            veicle_vals = {
                'vaicle_registration': Veicle.Data or False,
                'total_travel': Veicle.TotalePercorso or '',
            }
            invoice_model.write(
                cr, uid, invoice_id, veicle_vals, context=context)
        #2.4
        PaymentsData = FatturaBody.DatiPagamento
        if PaymentsData:
            for PaymentLine in PaymentsData:
                cond = PaymentLine.CondizioniPagamento or False
                if not cond:
                    raise orm.except_orm(
                        _('Error!'),
                        _('Payment method Code not found in document')
                    )
                term_id = False
                term_ids = PaymentTermsModel.search(
                    cr, uid, [('code', '=', cond)], context=context)
                if not term_ids:
                    raise orm.except_orm(
                        _('Error!'),
                        _('Payment method Code %s is incorrect') % cond
                    )
                else:
                    term_id = term_ids[0]
                PayDataId = PaymentDataModel.create(
                    cr, uid,
                    {
                        'payment_terms': term_id,
                        'invoice_id': invoice_id
                    },
                    context=context
                )
                self._CreatePayamentsLine(
                    cr, uid, PayDataId, PaymentLine, partner_id,
                    context=context
                )
        #2.5
        AttachmentsData = FatturaBody.Allegati
        if AttachmentsData:
            AttachModel = self.pool['fatturapa.attachments']
            for attach in AttachmentsData:
                if not attach.NomeAttachment:
                    raise orm.except_orm(
                        _('Error!'),
                        _('Attachment Name is Required')
                    )
                content = attach.Attachment
                name = attach.NomeAttachment
                _attach_dict = {
                    'name': name,
                    'datas': base64.b64encode(str(content)),
                    'datas_fname': name,
                    'description': attach.DescrizioneAttachment or '',
                    'compression': attach.AlgoritmoCompressione or '',
                    'format': attach.FormatoAttachment or '',
                    'invoice_id': invoice_id,
                }
                AttachModel.create(
                    cr, uid, _attach_dict, context=context)
#        somedata = {}
        # compute the invoice
        invoice_model.button_compute(
            cr, uid, [invoice_id], context=context,
            set_total=True)
        return invoice_id

    def importFatturaPA(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        fatturapa_attachment_obj = self.pool['fatturapa.attachment.in']
        fatturapa_attachment_ids = context.get('active_ids', False)
        invoice_model = self.pool['account.invoice']
        new_invoices = []
        for fatturapa_attachment in fatturapa_attachment_obj.browse(
                cr, uid, fatturapa_attachment_ids, context=context):
            if fatturapa_attachment.in_invoice_ids:
                raise orm.except_orm(
                    _("Error"), _("File is linked to invoices yet"))
            fatt = fatturapa_v_1_1.CreateFromDocument(
                fatturapa_attachment.datas.decode('base64'))
            cedentePrestatore = fatt.FatturaElettronicaHeader.CedentePrestatore
            #1.2
            partner_id = self.getCedPrest(
                cr, uid, cedentePrestatore, context=context)
            #1.3
            TaxRappresentative = fatt.FatturaElettronicaHeader.\
                RappresentanteFiscale
            #1.5
            Intermediary = fatt.FatturaElettronicaHeader.\
                TerzoIntermediarioOSoggettoEmittente
            #2
            for fattura in fatt.FatturaElettronicaBody:
                #~ fattura = fatt.FatturaElettronicaBody[i]
                # TODO
                if (
                    fattura.DatiGenerali.DatiGeneraliDocumento.TipoDocumento in
                    ('TD04', 'TD05')
                ):
                    raise orm.except_orm(
                        _("Error"),
                        _("tipoDocumento %s not handled")
                        % fattura.tipoDocumento)
                invoice_id = self.invoiceCreate(
                    cr, uid, fatt, fatturapa_attachment, fattura,
                    partner_id, context=context)

                if TaxRappresentative:
                    tax_partner_id = self.getPartnerBase(
                        cr, uid, TaxRappresentative.DatiAnagrafici,
                        context=context)
                    invoice_model.write(
                        cr, uid, invoice_id,
                        {
                            'tax_representative_id': tax_partner_id
                        }, context=context
                    )
                if Intermediary:
                    Intermediary_id = self.getPartnerBase(
                        cr, uid, Intermediary.DatiAnagrafici, context=context)
                    invoice_model.write(
                        cr, uid, invoice_id,
                        {
                            'intermediary': Intermediary_id
                        }, context=context
                    )
                new_invoices.append(invoice_id)
        return {
            'view_type': 'form',
            'name': "PA Supplier Invoices",
            'view_mode': 'tree,form',
            'res_model': 'account.invoice',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', new_invoices)],
            'context': context
        }
