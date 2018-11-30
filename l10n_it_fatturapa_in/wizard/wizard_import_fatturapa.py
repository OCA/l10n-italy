# -*- coding: utf-8 -*-

import base64
import logging
from odoo import models, api, fields
from odoo.tools import float_is_zero
from odoo.tools.translate import _
from odoo.exceptions import UserError

from odoo.addons.l10n_it_fatturapa.bindings import fatturapa_v_1_2
from odoo.addons.base_iban.models.res_partner_bank import pretty_iban

_logger = logging.getLogger(__name__)


class WizardImportFatturapa(models.TransientModel):
    _name = "wizard.import.fatturapa"
    _description = "Import E-bill"

    e_invoice_detail_level = fields.Selection([
        ('0', 'Minimum'),
        # ('1', 'Aliquote'),
        ('2', 'Maximum'),
    ], string="E-bills Detail Level",
        help="Minimum level: Bill is created with no lines; "
             "User will have to create them, according to what specified in "
             "the electronic bill.\n"
             # "Livello Aliquote: viene creata una riga fattura per ogni "
             # "aliquota presente nella fattura elettronica\n"
             "Maximum level: every line contained in the electronic bill "
             "will create a line in the bill.",
        required=True
    )

    @api.model
    def default_get(self, fields):
        res = super(WizardImportFatturapa, self).default_get(fields)
        res['e_invoice_detail_level'] = '2'
        fatturapa_attachment_ids = self.env.context.get('active_ids', False)
        fatturapa_attachment_obj = self.env['fatturapa.attachment.in']
        partners = self.env['res.partner']
        for fatturapa_attachment_id in fatturapa_attachment_ids:
            fatturapa_attachment = fatturapa_attachment_obj.browse(
                fatturapa_attachment_id)
            if fatturapa_attachment.in_invoice_ids:
                raise UserError(
                    _("File %s is linked to bills yet.")
                    % fatturapa_attachment.name)
            partners |= fatturapa_attachment.xml_supplier_id
            if len(partners) == 1:
                res['e_invoice_detail_level'] = (
                    partners[0].e_invoice_detail_level)
        return res

    def CountryByCode(self, CountryCode):
        country_model = self.env['res.country']
        return country_model.search([('code', '=', CountryCode)])

    def ProvinceByCode(self, provinceCode):
        province_model = self.env['res.country.state']
        return province_model.search([
            ('code', '=', provinceCode),
            ('country_id.code', '=', 'IT')
        ])

    def log_inconsistency(self, message):
        inconsistencies = self.env.context.get('inconsistencies', '')
        if inconsistencies:
            inconsistencies += '\n'
        inconsistencies += message
        # we can't set
        # self = self.with_context(inconsistencies=inconsistencies)
        # because self is a locale variable.
        # We use __dict__ to modify attributes of self
        self.__dict__.update(
            self.with_context(inconsistencies=inconsistencies).__dict__
        )

    def check_partner_base_data(self, partner_id, DatiAnagrafici):
        partner = self.env['res.partner'].browse(partner_id)
        if (
            DatiAnagrafici.Anagrafica.Denominazione and
            partner.name != DatiAnagrafici.Anagrafica.Denominazione
        ):
            self.log_inconsistency(_(
                "Company Name field contains '%s'."
                " Your System contains '%s'"
            ) % (DatiAnagrafici.Anagrafica.Denominazione, partner.name))
        if (
            DatiAnagrafici.Anagrafica.Nome and
            partner.firstname != DatiAnagrafici.Anagrafica.Nome
        ):
            self.log_inconsistency(_(
                "Name field contains '%s'."
                " Your System contains '%s'"
            ) % (DatiAnagrafici.Anagrafica.Nome, partner.firstname))
        if (
            DatiAnagrafici.Anagrafica.Cognome and
            partner.lastname != DatiAnagrafici.Anagrafica.Cognome
        ):
            self.log_inconsistency(
                _(
                    "Surname field contains '%s'."
                    " Your System contains '%s'"
                )
                % (DatiAnagrafici.Anagrafica.Cognome, partner.lastname)
            )

    def getPartnerBase(self, DatiAnagrafici):
        if not DatiAnagrafici:
            return False
        partner_model = self.env['res.partner']
        cf = DatiAnagrafici.CodiceFiscale or False
        vat = False
        if DatiAnagrafici.IdFiscaleIVA:
            vat = "%s%s" % (
                DatiAnagrafici.IdFiscaleIVA.IdPaese,
                DatiAnagrafici.IdFiscaleIVA.IdCodice
            )
        partners = partner_model.search([
            '|',
            ('vat', '=', vat or 0),
            ('fiscalcode', '=', cf or 0),
        ])
        commercial_partner = False
        if len(partners) > 1:
            for partner in partners:
                if (
                    commercial_partner and
                    partner.commercial_partner_id.id != commercial_partner
                ):
                    raise UserError(
                        _("Two distinct partners with "
                          "VAT number %s and Fiscal Code %s already "
                          "present in db." %
                          (vat, cf))
                        )
        if partners:
            commercial_partner_id = partners[0].id
            self.check_partner_base_data(commercial_partner_id, DatiAnagrafici)
            return commercial_partner_id
        else:
            # partner to be created
            country_id = False
            if DatiAnagrafici.IdFiscaleIVA:
                CountryCode = DatiAnagrafici.IdFiscaleIVA.IdPaese
                countries = self.CountryByCode(CountryCode)
                if countries:
                    country_id = countries[0].id
                else:
                    raise UserError(
                        _("Country Code %s not found in system.") % CountryCode
                    )
            vals = {
                'vat': vat,
                'fiscalcode': cf,
                'customer': False,
                'supplier': True,
                'is_company': (
                    DatiAnagrafici.Anagrafica.Denominazione and True or False),
                'eori_code': DatiAnagrafici.Anagrafica.CodEORI or '',
                'country_id': country_id,
            }
            if DatiAnagrafici.Anagrafica.Nome:
                vals['firstname'] = DatiAnagrafici.Anagrafica.Nome
            if DatiAnagrafici.Anagrafica.Cognome:
                vals['lastname'] = DatiAnagrafici.Anagrafica.Cognome
            if DatiAnagrafici.Anagrafica.Denominazione:
                vals['name'] = DatiAnagrafici.Anagrafica.Denominazione

            return partner_model.create(vals).id

    def getCedPrest(self, cedPrest):
        partner_model = self.env['res.partner']
        partner_id = self.getPartnerBase(cedPrest.DatiAnagrafici)
        fiscalPosModel = self.env['fatturapa.fiscal_position']
        if partner_id:
            vals = {
                'street': cedPrest.Sede.Indirizzo,
                'zip': cedPrest.Sede.CAP,
                'city': cedPrest.Sede.Comune,
                'register': cedPrest.DatiAnagrafici.AlboProfessionale or ''
            }
            if cedPrest.DatiAnagrafici.ProvinciaAlbo:
                ProvinciaAlbo = cedPrest.DatiAnagrafici.ProvinciaAlbo
                prov = self.ProvinceByCode(ProvinciaAlbo)
                if not prov:
                    self.log_inconsistency(
                        _('Register Province ( %s ) not present '
                          'in your system')
                        % ProvinciaAlbo
                    )
                else:
                    vals['register_province'] = prov[0].id
            if cedPrest.Sede.Provincia:
                Provincia = cedPrest.Sede.Provincia
                prov_sede = self.ProvinceByCode(Provincia)
                if not prov_sede:
                    self.log_inconsistency(
                        _('Province ( %s ) not present in your system')
                        % Provincia
                    )
                else:
                    vals['state_id'] = prov_sede[0].id

            vals['register_code'] = (
                cedPrest.DatiAnagrafici.NumeroIscrizioneAlbo)
            vals['register_regdate'] = (
                cedPrest.DatiAnagrafici.DataIscrizioneAlbo)

            if cedPrest.DatiAnagrafici.RegimeFiscale:
                rfPos = cedPrest.DatiAnagrafici.RegimeFiscale
                FiscalPos = fiscalPosModel.search(
                    [('code', '=', rfPos)]
                )
                if not FiscalPos:
                    raise UserError(
                        _('Tax Regime %s not present in your system.')
                        % rfPos
                    )
                else:
                    vals['register_fiscalpos'] = FiscalPos[0].id

            if cedPrest.IscrizioneREA:
                REA = cedPrest.IscrizioneREA
                vals['rea_code'] = REA.NumeroREA
                offices = self.ProvinceByCode(REA.Ufficio)
                if not offices:
                    self.log_inconsistency(
                        _(
                            'REA Office Province Code ( %s ) not present in '
                            'your system'
                        ) % REA.Ufficio
                    )
                else:
                    office_id = offices[0].id
                    vals['rea_office'] = office_id
                vals['rea_capital'] = REA.CapitaleSociale or 0.0
                vals['rea_member_type'] = REA.SocioUnico or False
                vals['rea_liquidation_state'] = REA.StatoLiquidazione or False

            if cedPrest.Contatti:
                vals['phone'] = cedPrest.Contatti.Telefono
                vals['email'] = cedPrest.Contatti.Email
                vals['fax'] = cedPrest.Contatti.Fax
            partner_model.browse(partner_id).write(vals)
        return partner_id

    def getCarrirerPartner(self, Carrier):
        partner_model = self.env['res.partner']
        partner_id = self.getPartnerBase(Carrier.DatiAnagraficiVettore)
        if partner_id:
            vals = {
                'license_number':
                Carrier.DatiAnagraficiVettore.NumeroLicenzaGuida or '',
            }
            partner_model.browse(partner_id).write(vals)
        return partner_id

    def _prepare_generic_line_data(self, line):
        retLine = {}
        account_tax_model = self.env['account.tax']
        # check if a default tax exists and generate def_purchase_tax object
        ir_values = self.env['ir.values']
        company_id = self.env['res.company']._company_default_get(
            'account.invoice.line').id
        supplier_taxes_ids = ir_values.get_default(
            'product.product', 'supplier_taxes_id', company_id=company_id)
        def_purchase_tax = False
        if supplier_taxes_ids:
            def_purchase_tax = account_tax_model.browse(supplier_taxes_ids)[0]
        if float(line.AliquotaIVA) == 0.0 and line.Natura:
            account_taxes = account_tax_model.search(
                [
                    ('type_tax_use', '=', 'purchase'),
                    ('kind_id.code', '=', line.Natura),
                    ('amount', '=', 0.0),
                ])
            if not account_taxes:
                raise UserError(
                    _('No tax with percentage '
                      '%s and nature %s found. Please configure this tax.')
                    % (line.AliquotaIVA, line.Natura))
            if len(account_taxes) > 1:
                raise UserError(
                    _('Too many taxes with percentage '
                      '%s and nature %s found.')
                    % (line.AliquotaIVA, line.Natura))
        else:
            account_taxes = account_tax_model.search(
                [
                    ('type_tax_use', '=', 'purchase'),
                    ('amount', '=', float(line.AliquotaIVA)),
                    ('price_include', '=', False),
                    # partially deductible VAT must be set by user
                    ('children_tax_ids', '=', False),
                ]
            )
            if not account_taxes:
                self.log_inconsistency(
                    _(
                        "XML contains tax with percentage '%s' "
                        "but it does not exist in your system"
                    ) % line.AliquotaIVA
                )
            # check if there are multiple taxes with
            # same percentage
            if len(account_taxes) > 1:
                # just logging because this is an usual case: see split payment
                _logger.warning(_(
                    "Line '%s': Too many taxes with percentage equals "
                    "to '%s'.\nFix it if required"
                ) % (line.Descrizione, line.AliquotaIVA))
                # if there are multiple taxes with same percentage
                # and there is a default tax with this percentage,
                # set taxes list equal to supplier_taxes_id, loaded before
                if (
                    def_purchase_tax and
                    def_purchase_tax.amount == (float(line.AliquotaIVA))
                ):
                    account_taxes = def_purchase_tax
        if account_taxes:
            retLine['invoice_line_tax_ids'] = [(6, 0, [account_taxes[0].id])]
        return retLine

    def get_line_product(self, line, partner):
        product = None
        supplier_info = self.env['product.supplierinfo']
        if len(line.CodiceArticolo) == 1:
            supplier_code = line.CodiceArticolo[0].CodiceValore
            supplier_infos = supplier_info.search([
                ('product_code', '=', supplier_code),
                ('name', '=', partner.id)
            ])
            if supplier_infos:
                products = supplier_infos.mapped('product_id')
                if len(products) == 1:
                    product = products[0]
                else:
                    templates = supplier_infos.mapped('product_tmpl_id')
                    if len(templates) == 1:
                        product = templates.product_variant_ids[0]
        if not product and partner.e_invoice_default_product_id:
            product = partner.e_invoice_default_product_id
        return product

    def adjust_accounting_data(self, product, line_vals):
        if product.product_tmpl_id.property_account_expense_id:
            line_vals['account_id'] = (
                product.product_tmpl_id.property_account_expense_id.id)
        elif (
            product.product_tmpl_id.categ_id.property_account_expense_categ_id
        ):
            line_vals['account_id'] = (
                product.product_tmpl_id.categ_id.
                property_account_expense_categ_id.id
            )
        account = self.env['account.account'].browse(line_vals['account_id'])
        new_tax = None
        if len(product.product_tmpl_id.supplier_taxes_id) == 1:
            new_tax = product.product_tmpl_id.supplier_taxes_id[0]
        elif len(account.tax_ids) == 1:
            new_tax = account.tax_ids[0]
        if new_tax:
            line_tax_id = (
                line_vals.get('invoice_line_tax_ids') and
                line_vals['invoice_line_tax_ids'][0][2][0]
            )
            line_tax = self.env['account.tax'].browse(line_tax_id)
            if new_tax.id != line_tax_id:
                if new_tax._get_tax_amount() != line_tax._get_tax_amount():
                    self.log_inconsistency(_(
                        "XML contains tax %s. Product %s has tax %s. Using "
                        "the XML one"
                    ) % (line_tax.name, product.name, new_tax.name))
                else:
                    # If product has the same amount of the one in XML,
                    # I use it. Typical case: 22% det 50%
                    line_vals['invoice_line_tax_ids'] = [
                        (6, 0, [new_tax.id])]

    def _prepareInvoiceLine(self, credit_account_id, line, wt_found=False):
        retLine = self._prepare_generic_line_data(line)
        retLine.update({
            'name': line.Descrizione,
            'sequence': int(line.NumeroLinea),
            'account_id': credit_account_id,
        })
        if line.PrezzoUnitario:
            retLine['price_unit'] = float(line.PrezzoUnitario)
        if line.Quantita:
            retLine['quantity'] = float(line.Quantita)
        if (
            line.PrezzoTotale and line.PrezzoUnitario and line.Quantita and
            line.ScontoMaggiorazione
        ):
            retLine['discount'] = self._computeDiscount(line)
        if line.RiferimentoAmministrazione:
            retLine['admin_ref'] = line.RiferimentoAmministrazione
        if wt_found and line.Ritenuta:
            retLine['invoice_line_tax_wt_ids'] = [(6, 0, [wt_found.id])]

        return retLine

    def _prepareRelDocsLine(self, invoice_id, line, type):
        res = []
        lineref = line.RiferimentoNumeroLinea or False
        IdDoc = line.IdDocumento or 'Error'
        Data = line.Data or False
        NumItem = line.NumItem or ''
        Code = line.CodiceCommessaConvenzione or ''
        Cig = line.CodiceCIG or ''
        Cup = line.CodiceCUP or ''
        invoice_lineid = False
        if lineref:
            for numline in lineref:
                invoice_lineid = False
                invoice_line_model = self.env['account.invoice.line']
                invoice_lines = invoice_line_model.search(
                    [
                        ('invoice_id', '=', invoice_id),
                        ('sequence', '=', int(numline)),
                    ])
                if invoice_lines:
                    invoice_lineid = invoice_lines[0].id
                val = {
                    'type': type,
                    'name': IdDoc,
                    'lineRef': numline,
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

    def _prepareWelfareLine(self, invoice_id, line):
        TipoCassa = line.TipoCassa or False
        AlCassa = line.AlCassa and (float(line.AlCassa)/100) or None
        ImportoContributoCassa = (
            line.ImportoContributoCassa and
            float(line.ImportoContributoCassa) or None)
        ImponibileCassa = (
            line.ImponibileCassa and float(line.ImponibileCassa) or None)
        AliquotaIVA = (
            line.AliquotaIVA and (float(line.AliquotaIVA)/100) or None)
        Ritenuta = line.Ritenuta or ''
        Natura = line.Natura or False
        kind_id = False
        if Natura:
            kind = self.env['account.tax.kind'].search([
                ('code', '=', Natura)
            ])
            if not kind:
                self.log_inconsistency(
                    _("Tax kind %s not found") % Natura
                )
            else:
                kind_id = kind[0].id

        RiferimentoAmministrazione = line.RiferimentoAmministrazione or ''
        WelfareTypeModel = self.env['welfare.fund.type']
        if not TipoCassa:
            raise UserError(
                _('Welfare Fund is not defined.')
            )
        WelfareType = WelfareTypeModel.search(
            [('name', '=', TipoCassa)]
        )

        res = {
            'welfare_rate_tax': AlCassa,
            'welfare_amount_tax': ImportoContributoCassa,
            'welfare_taxable': ImponibileCassa,
            'welfare_Iva_tax': AliquotaIVA,
            'subjected_withholding': Ritenuta,
            'kind_id': kind_id,
            'pa_line_code': RiferimentoAmministrazione,
            'invoice_id': invoice_id,
        }
        if not WelfareType:
            raise UserError(
                _('Welfare Fund %s not present in your system.') % TipoCassa)
        else:
            res['name'] = WelfareType[0].id

        return res

    def _prepareDiscRisePriceLine(self, id, line):
        Tipo = line.Tipo or False
        Percentuale = line.Percentuale and float(line.Percentuale) or 0.0
        Importo = line.Importo and float(line.Importo) or 0.0
        res = {
            'percentage': Percentuale,
            'amount': Importo,
            self.env.context.get('drtype'): id,
        }
        res['name'] = Tipo

        return res

    def _computeDiscount(self, DettaglioLinea):
        line_total = float(DettaglioLinea.PrezzoTotale)
        line_unit = line_total / float(DettaglioLinea.Quantita)
        discount = (
            1 - (line_unit / float(DettaglioLinea.PrezzoUnitario))
            ) * 100.0
        return discount

    def _addGlobalDiscount(self, invoice_id, DatiGeneraliDocumento):
        discount = 0.0
        if (
            DatiGeneraliDocumento.ScontoMaggiorazione and
            self.e_invoice_detail_level == '2'
        ):
            invoice = self.env['account.invoice'].browse(invoice_id)
            for DiscRise in DatiGeneraliDocumento.ScontoMaggiorazione:
                if DiscRise.Percentuale:
                    amount = (
                        invoice.amount_total * (
                            float(DiscRise.Percentuale) / 100))
                    if DiscRise.Tipo == 'SC':
                        discount -= amount
                    elif DiscRise.Tipo == 'MG':
                        discount += amount
                elif DiscRise.Importo:
                    if DiscRise.Tipo == 'SC':
                        discount -= float(DiscRise.Importo)
                    elif DiscRise.Tipo == 'MG':
                        discount += float(DiscRise.Importo)
            journal = self.get_purchase_journal(invoice.company_id)
            credit_account_id = journal.default_credit_account_id.id
            line_vals = {
                'invoice_id': invoice_id,
                'name': _(
                    "Global bill discount from document general data"),
                'account_id': credit_account_id,
                'price_unit': discount,
                'quantity': 1,
                }
            if self.env.user.company_id.sconto_maggiorazione_product_id:
                sconto_maggiorazione_product = (
                    self.env.user.company_id.sconto_maggiorazione_product_id)
                line_vals['product_id'] = sconto_maggiorazione_product.id
                line_vals['name'] = sconto_maggiorazione_product.name
                self.adjust_accounting_data(
                    sconto_maggiorazione_product, line_vals
                )
            self.env['account.invoice.line'].create(line_vals)
        return True

    def add_dati_bollo(self, invoice, DatiGeneraliDocumento):
        # 2.1.1.6
        Stamps = DatiGeneraliDocumento.DatiBollo
        if Stamps:
            invoice.virtual_stamp = Stamps.BolloVirtuale
            invoice.stamp_amount = float(Stamps.ImportoBollo)
            if self.e_invoice_detail_level == '2':
                journal = self.get_purchase_journal(invoice.company_id)
                credit_account_id = journal.default_credit_account_id.id
                line_vals = {
                    'invoice_id': invoice.id,
                    'name': _(
                        "Stamp duty payed under the MEF Decree June 17, "
                        "2014 (art. 6)"
                    ),
                    'account_id': credit_account_id,
                    'price_unit': invoice.stamp_amount,
                    'quantity': 1,
                    }
                if self.env.user.company_id.dati_bollo_product_id:
                    dati_bollo_product = (
                        self.env.user.company_id.dati_bollo_product_id)
                    line_vals['product_id'] = dati_bollo_product.id
                    line_vals['name'] = dati_bollo_product.name
                    self.adjust_accounting_data(
                        dati_bollo_product, line_vals
                    )
                self.env['account.invoice.line'].create(line_vals)

    def _createPayamentsLine(self, payment_id, line, partner_id):
        PaymentModel = self.env['fatturapa.payment.detail']
        PaymentMethodModel = self.env['fatturapa.payment_method']
        details = line.DettaglioPagamento or False
        if details:
            for dline in details:
                BankModel = self.env['res.bank']
                PartnerBankModel = self.env['res.partner.bank']
                method = PaymentMethodModel.search(
                    [('code', '=', dline.ModalitaPagamento)]
                )
                if not method:
                    raise UserError(
                        _(
                            'Payment method %s is not defined in your system.'
                            % dline.ModalitaPagamento
                        )
                    )
                val = {
                    'recipient': dline.Beneficiario,
                    'fatturapa_pm_id': method[0].id,
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
                    banks = BankModel.search(
                        [('bic', '=', dline.BIC.strip())]
                    )
                    if not banks:
                        if not dline.IstitutoFinanziario:
                            self.log_inconsistency(
                                _("Name of Bank with BIC '%s' is not set."
                                  " Can't create bank") % dline.BIC
                            )
                        else:
                            bankid = BankModel.create(
                                {
                                    'name': dline.IstitutoFinanziario,
                                    'bic': dline.BIC,
                                }
                            ).id
                    else:
                        bankid = banks[0].id
                if dline.IBAN:
                    SearchDom = [
                        (
                            'acc_number', '=',
                            pretty_iban(dline.IBAN.strip())
                        ),
                        ('partner_id', '=', partner_id),
                    ]
                    payment_bank_id = False
                    payment_banks = PartnerBankModel.search(SearchDom)
                    if not payment_banks and not bankid:
                        self.log_inconsistency(
                            _(
                                'BIC is required and not exist in Xml\n'
                                'Curr bank data is: \n'
                                'IBAN: %s\n'
                                'Bank Name: %s\n'
                            )
                            % (
                                dline.IBAN.strip() or '',
                                dline.IstitutoFinanziario or ''
                            )
                        )
                    elif not payment_banks and bankid:
                        payment_bank_id = PartnerBankModel.create(
                            {
                                'acc_number': dline.IBAN.strip(),
                                'partner_id': partner_id,
                                'bank_id': bankid,
                                'bank_name': dline.IstitutoFinanziario,
                                'bank_bic': dline.BIC
                            }
                        ).id
                    if payment_banks:
                        payment_bank_id = payment_banks[0].id

                if payment_bank_id:
                    val['payment_bank'] = payment_bank_id
                PaymentModel.create(val)
        return True

    # TODO sul partner?
    def set_StabileOrganizzazione(self, CedentePrestatore, invoice):
        if CedentePrestatore.StabileOrganizzazione:
            invoice.efatt_stabile_organizzazione_indirizzo = (
                CedentePrestatore.StabileOrganizzazione.Indirizzo)
            invoice.efatt_stabile_organizzazione_civico = (
                CedentePrestatore.StabileOrganizzazione.NumeroCivico)
            invoice.efatt_stabile_organizzazione_cap = (
                CedentePrestatore.StabileOrganizzazione.CAP)
            invoice.efatt_stabile_organizzazione_comune = (
                CedentePrestatore.StabileOrganizzazione.Comune)
            invoice.efatt_stabile_organizzazione_provincia = (
                CedentePrestatore.StabileOrganizzazione.Provincia)
            invoice.efatt_stabile_organizzazione_nazione = (
                CedentePrestatore.StabileOrganizzazione.Nazione)

    def get_purchase_journal(self, company):
        journal_model = self.env['account.journal']
        journals = journal_model.search(
            [
                ('type', '=', 'purchase'),
                ('company_id', '=', company.id)
            ],
            limit=1)
        if not journals:
            raise UserError(
                _(
                    "Define a purchase journal "
                    "for this company: '%s' (id: %d)."
                ) % (company.name, company.id)
            )
        return journals[0]

    def create_e_invoice_line(self, line):
        vals = {
            'line_number': int(line.NumeroLinea or 0),
            'service_type': line.TipoCessionePrestazione,
            'name': line.Descrizione,
            'qty': float(line.Quantita or 0),
            'uom': line.UnitaMisura,
            'period_start_date': line.DataInizioPeriodo,
            'period_end_date': line.DataFinePeriodo,
            'unit_price': float(line.PrezzoUnitario or 0),
            'total_price': float(line.PrezzoTotale or 0),
            'tax_amount': float(line.AliquotaIVA or 0),
            'wt_amount': line.Ritenuta,
            'tax_kind': line.Natura,
            'admin_ref': line.RiferimentoAmministrazione,
        }
        einvoiceline = self.env['einvoice.line'].create(vals)
        if line.CodiceArticolo:
            for caline in line.CodiceArticolo:
                self.env['fatturapa.article.code'].create(
                    {
                        'name': caline.CodiceTipo or '',
                        'code_val': caline.CodiceValore or '',
                        'e_invoice_line_id': einvoiceline.id
                    }
                )
        if line.ScontoMaggiorazione:
            for DiscRisePriceLine in line.ScontoMaggiorazione:
                DiscRisePriceVals = self.with_context(
                    drtype='e_invoice_line_id'
                )._prepareDiscRisePriceLine(
                    einvoiceline.id, DiscRisePriceLine
                )
                self.env['discount.rise.price'].create(DiscRisePriceVals)
        if line.AltriDatiGestionali:
            for dato in line.AltriDatiGestionali:
                self.env['einvoice.line.other.data'].create(
                    {
                        'name': dato.TipoDato,
                        'text_ref': dato.RiferimentoTesto,
                        'num_ref': float(dato.RiferimentoNumero or 0),
                        'date_ref': dato.RiferimentoData,
                        'e_invoice_line_id': einvoiceline.id
                    }
                )
        return einvoiceline

    def invoiceCreate(
        self, fatt, fatturapa_attachment, FatturaBody, partner_id
    ):
        partner_model = self.env['res.partner']
        invoice_model = self.env['account.invoice']
        currency_model = self.env['res.currency']
        invoice_line_model = self.env['account.invoice.line']
        ftpa_doctype_model = self.env['fiscal.document.type']
        rel_docs_model = self.env['fatturapa.related_document_type']
        WelfareFundLineModel = self.env['welfare.fund.data.line']
        SalModel = self.env['faturapa.activity.progress']
        DdTModel = self.env['fatturapa.related_ddt']
        PaymentDataModel = self.env['fatturapa.payment.data']
        PaymentTermsModel = self.env['fatturapa.payment_term']
        SummaryDatasModel = self.env['faturapa.summary.data']

        company = self.env.user.company_id
        partner = partner_model.browse(partner_id)
        pay_acc_id = partner.property_account_payable_id.id
        # currency 2.1.1.2
        currency = currency_model.search(
            [
                (
                    'name', '=',
                    FatturaBody.DatiGenerali.DatiGeneraliDocumento.Divisa
                )
            ])
        if not currency:
            raise UserError(
                _(
                    'No currency found with code %s.'
                    % FatturaBody.DatiGenerali.DatiGeneraliDocumento.Divisa
                )
            )
        purchase_journal = self.get_purchase_journal(company)
        credit_account_id = purchase_journal.default_credit_account_id.id
        invoice_lines = []
        comment = ''
        # 2.1.1
        docType_id = False
        invtype = 'in_invoice'
        docType = FatturaBody.DatiGenerali.DatiGeneraliDocumento.TipoDocumento
        if docType:
            docType_record = ftpa_doctype_model.search(
                [
                    ('code', '=', docType)
                ]
            )
            if docType_record:
                docType_id = docType_record[0].id
            else:
                raise UserError(
                    _("Document type %s not handled.")
                    % docType)
            if docType == 'TD04':
                invtype = 'in_refund'
        # 2.1.1.11
        causLst = FatturaBody.DatiGenerali.DatiGeneraliDocumento.Causale
        if causLst:
            for item in causLst:
                comment += item + '\n'

        invoice_data = {
            'fiscal_document_type_id': docType_id,
            'date_invoice':
            FatturaBody.DatiGenerali.DatiGeneraliDocumento.Data,
            'reference':
            FatturaBody.DatiGenerali.DatiGeneraliDocumento.Numero,
            'sender': fatt.FatturaElettronicaHeader.SoggettoEmittente or False,
            'account_id': pay_acc_id,
            'type': invtype,
            'partner_id': partner_id,
            'currency_id': currency[0].id,
            'journal_id': purchase_journal.id,
            # 'origin': xmlData.datiOrdineAcquisto,
            'fiscal_position_id': False,
            'payment_term_id': False,
            'company_id': company.id,
            'fatturapa_attachment_in_id': fatturapa_attachment.id,
            'comment': comment
        }

        # 2.1.1.10
        if FatturaBody.DatiGenerali.DatiGeneraliDocumento.Arrotondamento:
            invoice_data['efatt_rounding'] = float(
                FatturaBody.DatiGenerali.DatiGeneraliDocumento.Arrotondamento
            )
        # 2.1.1.12
        if FatturaBody.DatiGenerali.DatiGeneraliDocumento.Art73:
            invoice_data['art73'] = True

        # 2.1.1.5
        Withholding = FatturaBody.DatiGenerali.\
            DatiGeneraliDocumento.DatiRitenuta
        wt_found = None
        if Withholding:
            wts = self.env['withholding.tax'].search([
                ('causale_pagamento_id.code', '=',
                 Withholding.CausalePagamento)
            ])
            if not wts:
                raise UserError(_(
                    "The bill contains withholding tax with "
                    "payment reason %s, "
                    "but such a tax is not found in your system. Please "
                    "set it."
                ) % Withholding.CausalePagamento)
            wt_found = False
            for wt in wts:
                if wt.tax == float(Withholding.AliquotaRitenuta):
                    wt_found = wt
                    break
            if not wt_found:
                raise UserError(_(
                    "No withholding tax found with "
                    "document payment reason %s and rate %s."
                ) % (
                    Withholding.CausalePagamento, Withholding.AliquotaRitenuta
                ))
            invoice_data['ftpa_withholding_type'] = Withholding.TipoRitenuta
        # 2.2.1
        e_invoice_line_ids = []
        for line in FatturaBody.DatiBeniServizi.DettaglioLinee:
            if self.e_invoice_detail_level == '2':
                invoice_line_data = self._prepareInvoiceLine(
                    credit_account_id, line, wt_found)
                product = self.get_line_product(line, partner)
                if product:
                    invoice_line_data['product_id'] = product.id
                    self.adjust_accounting_data(product, invoice_line_data)
                invoice_line_id = invoice_line_model.create(
                    invoice_line_data).id
                invoice_lines.append(invoice_line_id)
            einvoiceline = self.create_e_invoice_line(line)
            e_invoice_line_ids.append(einvoiceline.id)
        invoice_data['invoice_line_ids'] = [(6, 0, invoice_lines)]
        invoice_data['e_invoice_line_ids'] = [(6, 0, e_invoice_line_ids)]
        invoice = invoice_model.create(invoice_data)
        invoice._onchange_invoice_line_wt_ids()
        invoice.write(invoice._convert_to_write(invoice._cache))
        invoice_id = invoice.id

        self.add_dati_bollo(
            invoice, FatturaBody.DatiGenerali.DatiGeneraliDocumento)

        # 2.1.1.7
        Walfares = FatturaBody.DatiGenerali.\
            DatiGeneraliDocumento.DatiCassaPrevidenziale
        if Walfares and self.e_invoice_detail_level == '2':
            for walfareLine in Walfares:
                WalferLineVals = self._prepareWelfareLine(
                    invoice_id, walfareLine)
                WelfareFundLineModel.create(WalferLineVals)
                line_vals = self._prepare_generic_line_data(walfareLine)
                line_vals.update({
                    'name': _(
                        "Welfare Fund: %s") % walfareLine.TipoCassa,
                    'price_unit': float(walfareLine.ImportoContributoCassa),
                    'invoice_id': invoice.id,
                    'account_id': credit_account_id,
                })
                if walfareLine.Ritenuta:
                    if not wt_found:
                        raise UserError(_(
                            "Welfare Fund data %s has withholding tax but no "
                            "withholding tax was found in the system."
                            % walfareLine.TipoCassa))
                    line_vals['invoice_line_tax_wt_ids'] = [
                        (6, 0, [wt_found.id])]
                if self.env.user.company_id.cassa_previdenziale_product_id:
                    cassa_previdenziale_product = (
                        self.env.user.company_id.
                        cassa_previdenziale_product_id
                    )
                    line_vals['product_id'] = cassa_previdenziale_product.id
                    line_vals['name'] = cassa_previdenziale_product.name
                    self.adjust_accounting_data(
                        cassa_previdenziale_product, line_vals
                    )
                self.env['account.invoice.line'].create(line_vals)
        # 2.1.2
        relOrders = FatturaBody.DatiGenerali.DatiOrdineAcquisto
        if relOrders:
            for order in relOrders:
                doc_datas = self._prepareRelDocsLine(
                    invoice_id, order, 'order')
                if doc_datas:
                    for doc_data in doc_datas:
                        rel_docs_model.create(doc_data)
        # 2.1.3
        relContracts = FatturaBody.DatiGenerali.DatiContratto
        if relContracts:
            for contract in relContracts:
                doc_datas = self._prepareRelDocsLine(
                    invoice_id, contract, 'contract')
                if doc_datas:
                    for doc_data in doc_datas:
                        rel_docs_model.create(doc_data)
        # 2.1.4
        relAgreements = FatturaBody.DatiGenerali.DatiConvenzione
        if relAgreements:
            for agreement in relAgreements:
                doc_datas = self._prepareRelDocsLine(
                    invoice_id, agreement, 'agreement')
                if doc_datas:
                    for doc_data in doc_datas:
                        rel_docs_model.create(doc_data)
        # 2.1.5
        relReceptions = FatturaBody.DatiGenerali.DatiRicezione
        if relReceptions:
            for reception in relReceptions:
                doc_datas = self._prepareRelDocsLine(
                    invoice_id, reception, 'reception')
                if doc_datas:
                    for doc_data in doc_datas:
                        rel_docs_model.create(doc_data)
        # 2.1.6
        RelInvoices = FatturaBody.DatiGenerali.DatiFattureCollegate
        if RelInvoices:
            for invoice in RelInvoices:
                doc_datas = self._prepareRelDocsLine(
                    invoice_id, invoice, 'invoice')
                if doc_datas:
                    for doc_data in doc_datas:
                        rel_docs_model.create(doc_data)
        # 2.1.7
        SalDatas = FatturaBody.DatiGenerali.DatiSAL
        if SalDatas:
            for SalDataLine in SalDatas:
                SalModel.create(
                    {
                        'fatturapa_activity_progress': (
                            SalDataLine.RiferimentoFase or 0),
                        'invoice_id': invoice_id
                    }
                )
        # 2.1.8
        DdtDatas = FatturaBody.DatiGenerali.DatiDDT
        if DdtDatas:
            for DdtDataLine in DdtDatas:
                if not DdtDataLine.RiferimentoNumeroLinea:
                    DdTModel.create(
                        {
                            'name': DdtDataLine.NumeroDDT or '',
                            'date': DdtDataLine.DataDDT or False,
                            'invoice_id': invoice_id
                        }
                    )
                else:
                    for numline in DdtDataLine.RiferimentoNumeroLinea:
                        invoice_lines = invoice_line_model.search(
                            [
                                ('invoice_id', '=', invoice_id),
                                ('sequence', '=', int(numline)),
                            ])
                        invoice_lineid = False
                        if invoice_lines:
                            invoice_lineid = invoice_lines[0].id
                        DdTModel.create(
                            {
                                'name': DdtDataLine.NumeroDDT or '',
                                'date': DdtDataLine.DataDDT or False,
                                'invoice_id': invoice_id,
                                'invoice_line_id': invoice_lineid
                            }
                        )
        # 2.1.9
        Delivery = FatturaBody.DatiGenerali.DatiTrasporto
        if Delivery:
            delivery_id = self.getCarrirerPartner(Delivery)
            delivery_dict = {
                'carrier_id': delivery_id,
                'transport_vehicle': Delivery.MezzoTrasporto or '',
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
                'ftpa_incoterms': Delivery.TipoResa,
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
            invoice.write(delivery_dict)
        # 2.2.2
        Summary_datas = FatturaBody.DatiBeniServizi.DatiRiepilogo
        if Summary_datas:
            for summary in Summary_datas:
                summary_line = {
                    'tax_rate': summary.AliquotaIVA or 0.0,
                    'non_taxable_nature': summary.Natura or False,
                    'incidental_charges': summary.SpeseAccessorie or 0.0,
                    'rounding': summary.Arrotondamento or 0.0,
                    'amount_untaxed': summary.ImponibileImporto or 0.0,
                    'amount_tax': summary.Imposta or 0.0,
                    'payability': summary.EsigibilitaIVA or False,
                    'law_reference': summary.RiferimentoNormativo or '',
                    'invoice_id': invoice_id,
                }
                SummaryDatasModel.create(summary_line)

        # 2.1.10
        ParentInvoice = FatturaBody.DatiGenerali.FatturaPrincipale
        if ParentInvoice:
            parentinv_vals = {
                'related_invoice_code':
                ParentInvoice.NumeroFatturaPrincipale or '',
                'related_invoice_date':
                ParentInvoice.DataFatturaPrincipale or False
            }
            invoice.write(parentinv_vals)
        # 2.3
        Vehicle = FatturaBody.DatiVeicoli
        if Vehicle:
            veicle_vals = {
                'vehicle_registration': Vehicle.Data or False,
                'total_travel': Vehicle.TotalePercorso or '',
            }
            invoice.write(veicle_vals)
        # 2.4
        PaymentsData = FatturaBody.DatiPagamento
        if PaymentsData:
            for PaymentLine in PaymentsData:
                cond = PaymentLine.CondizioniPagamento or False
                if not cond:
                    raise UserError(
                        _('Payment method code not found in document.')
                    )
                terms = PaymentTermsModel.search([('code', '=', cond)])
                if not terms:
                    raise UserError(
                        _('Payment method code %s is incorrect.') % cond
                    )
                else:
                    term_id = terms[0].id
                PayDataId = PaymentDataModel.create(
                    {
                        'payment_terms': term_id,
                        'invoice_id': invoice_id
                    }
                ).id
                self._createPayamentsLine(PayDataId, PaymentLine, partner_id)
        # 2.5
        AttachmentsData = FatturaBody.Allegati
        if AttachmentsData:
            AttachModel = self.env['fatturapa.attachments']
            for attach in AttachmentsData:
                if not attach.NomeAttachment:
                    name = _("Attachment without name")
                else:
                    name = attach.NomeAttachment
                content = attach.Attachment
                _attach_dict = {
                    'name': name,
                    'datas': base64.b64encode(str(content)),
                    'datas_fname': name,
                    'description': attach.DescrizioneAttachment or '',
                    'compression': attach.AlgoritmoCompressione or '',
                    'format': attach.FormatoAttachment or '',
                    'invoice_id': invoice_id,
                }
                AttachModel.create(_attach_dict)

        self._addGlobalDiscount(
            invoice_id, FatturaBody.DatiGenerali.DatiGeneraliDocumento)

        # compute the invoice
        invoice.compute_taxes()
        return invoice_id

    def compute_xml_amount_untaxed(self, DatiRiepilogo):
        amount_untaxed = 0.0
        for Riepilogo in DatiRiepilogo:
            amount_untaxed += float(Riepilogo.ImponibileImporto)
        return amount_untaxed

    def check_invoice_amount(self, invoice, FatturaElettronicaBody):
        if (
            FatturaElettronicaBody.DatiGenerali.DatiGeneraliDocumento.
            ScontoMaggiorazione and
            FatturaElettronicaBody.DatiGenerali.DatiGeneraliDocumento.
            ImportoTotaleDocumento
        ):
            # assuming that, if someone uses
            # DatiGeneraliDocumento.ScontoMaggiorazione, also fills
            # DatiGeneraliDocumento.ImportoTotaleDocumento
            ImportoTotaleDocumento = float(
                FatturaElettronicaBody.DatiGenerali.DatiGeneraliDocumento.
                ImportoTotaleDocumento)
            if not float_is_zero(
                invoice.amount_total-ImportoTotaleDocumento, precision_digits=2
            ):
                self.log_inconsistency(
                    _('Bill total %s is different from '
                      'document total amount %s')
                    % (invoice.amount_total, ImportoTotaleDocumento)
                )
        else:
            # else, we can only check DatiRiepilogo if
            # DatiGeneraliDocumento.ScontoMaggiorazione is not present,
            # because otherwise DatiRiepilogo and odoo invoice total would
            # differ
            amount_untaxed = self.compute_xml_amount_untaxed(
                FatturaElettronicaBody.DatiBeniServizi.DatiRiepilogo)
            if not float_is_zero(
                invoice.amount_untaxed-amount_untaxed, precision_digits=2
            ):
                self.log_inconsistency(
                    _('Computed amount untaxed %s is different from'
                      ' summary data %s')
                    % (invoice.amount_untaxed, amount_untaxed)
                )

    def get_invoice_obj(self, fatturapa_attachment):
        xml_string = fatturapa_attachment.get_xml_string()
        return fatturapa_v_1_2.CreateFromDocument(xml_string)

    @api.multi
    def importFatturaPA(self):
        fatturapa_attachment_obj = self.env['fatturapa.attachment.in']
        fatturapa_attachment_ids = self.env.context.get('active_ids', False)
        invoice_model = self.env['account.invoice']
        new_invoices = []
        for fatturapa_attachment_id in fatturapa_attachment_ids:
            self.__dict__.update(
                self.with_context(inconsistencies='').__dict__
            )
            fatturapa_attachment = fatturapa_attachment_obj.browse(
                fatturapa_attachment_id)
            if fatturapa_attachment.in_invoice_ids:
                raise UserError(
                    _("File is linked to bills yet."))
            fatt = self.get_invoice_obj(fatturapa_attachment)
            cedentePrestatore = fatt.FatturaElettronicaHeader.CedentePrestatore
            # 1.2
            partner_id = self.getCedPrest(cedentePrestatore)
            # 1.3
            TaxRappresentative = fatt.FatturaElettronicaHeader.\
                RappresentanteFiscale
            # 1.5
            Intermediary = fatt.FatturaElettronicaHeader.\
                TerzoIntermediarioOSoggettoEmittente

            generic_inconsistencies = ''
            if self.env.context.get('inconsistencies'):
                generic_inconsistencies = (
                    self.env.context['inconsistencies'] + '\n\n')

            # 2
            for fattura in fatt.FatturaElettronicaBody:

                # reset inconsistencies
                self.__dict__.update(
                    self.with_context(inconsistencies='').__dict__
                )

                invoice_id = self.invoiceCreate(
                    fatt, fatturapa_attachment, fattura, partner_id)
                invoice = invoice_model.browse(invoice_id)
                self.set_StabileOrganizzazione(cedentePrestatore, invoice)
                if TaxRappresentative:
                    tax_partner_id = self.getPartnerBase(
                        TaxRappresentative.DatiAnagrafici)
                    invoice.write(
                        {
                            'tax_representative_id': tax_partner_id
                        }
                    )
                if Intermediary:
                    Intermediary_id = self.getPartnerBase(
                        Intermediary.DatiAnagrafici)
                    invoice.write(
                        {
                            'intermediary': Intermediary_id
                        }
                    )
                new_invoices.append(invoice_id)
                self.check_invoice_amount(invoice, fattura)

                if self.env.context.get('inconsistencies'):
                    invoice_inconsistencies = (
                        self.env.context['inconsistencies'])
                else:
                    invoice_inconsistencies = ''
                invoice.inconsistencies = (
                    generic_inconsistencies + invoice_inconsistencies)

        return {
            'view_type': 'form',
            'name': "Electronic Bills",
            'view_mode': 'tree,form',
            'res_model': 'account.invoice',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', new_invoices)],
        }
