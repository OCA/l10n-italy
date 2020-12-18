# -*- coding: utf-8 -*-

import logging
from openerp import models, api, fields, _
from openerp.tools import float_is_zero
from openerp.exceptions import Warning as UserError

from openerp.addons.l10n_it_fatturapa.bindings import fatturapa
from openerp.addons.base_iban.base_iban import _pretty_iban

_logger = logging.getLogger(__name__)

WT_CODES_MAPPING = {
    'RT01': 'ritenuta',
    'RT02': 'ritenuta',
    'RT03': 'inps',
    'RT04': 'enasarco',
    'RT05': 'enpam',
    'RT06': 'other',
}


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

    def getPartnerBase(self, DatiAnagrafici, supplier=True):
        if not DatiAnagrafici:
            return False
        partner_model = self.env['res.partner']
        cf = DatiAnagrafici.CodiceFiscale or False
        vat = False
        if DatiAnagrafici.IdFiscaleIVA:
            # Format Italian VAT ID to always have 11 char
            # to avoid validation error when creating the given partner
            if DatiAnagrafici.IdFiscaleIVA.IdPaese.upper() == 'IT':
                vat = "%s%s" % (
                    DatiAnagrafici.IdFiscaleIVA.IdPaese,
                    DatiAnagrafici.IdFiscaleIVA.IdCodice.rjust(11, '0')
                )
            else:
                vat = "%s%s" % (
                    DatiAnagrafici.IdFiscaleIVA.IdPaese,
                    DatiAnagrafici.IdFiscaleIVA.IdCodice
                )
        partners = partner_model
        if vat:
            domain = [('vat', '=', vat)]
            if self.env.context.get('from_attachment'):
                att = self.env.context.get('from_attachment')
                domain.extend([
                    '|',
                    ('company_id', 'child_of', att.company_id.id),
                    ('company_id', '=', False)
                ])
            partners = partner_model.search(domain)
        if not partners and cf:
            domain = [('fiscalcode', '=', cf)]
            if self.env.context.get('from_attachment'):
                att = self.env.context.get('from_attachment')
                domain.extend([
                    '|',
                    ('company_id', 'child_of', att.company_id.id),
                    ('company_id', '=', False)
                ])
            partners = partner_model.search(domain)
        commercial_partner_id = False
        if len(partners) > 1:
            for partner in partners:
                if (
                    commercial_partner_id and
                    partner.commercial_partner_id.id != commercial_partner_id
                ):
                    raise UserError(
                        _("Two distinct partners with "
                          "VAT number %s and Fiscal Code %s already "
                          "present in db." %
                          (vat, cf))
                        )
                commercial_partner_id = partner.commercial_partner_id.id
        if partners:
            if not commercial_partner_id:
                commercial_partner_id = partners[0].commercial_partner_id.id
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
                'supplier': supplier,
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
            else:
                # in v8 name field is not auto-completed
                vals['name'] = vals['lastname'] + ' ' + vals['firstname']

            return partner_model.create(vals).id

    def getCedPrest(self, cedPrest):
        partner_model = self.env['res.partner']
        partner_id = self.getPartnerBase(cedPrest.DatiAnagrafici)
        no_contact_update = False
        if partner_id:
            no_contact_update = partner_model.browse(partner_id).\
                electronic_invoice_no_contact_update
        fiscalPosModel = self.env['fatturapa.fiscal_position']
        if partner_id and not no_contact_update:
            partner_company_id = partner_model.browse(partner_id).company_id.id
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
                offices = self.ProvinceByCode(REA.Ufficio)
                rea_nr = REA.NumeroREA

                if not offices:
                    office_id = False
                    self.log_inconsistency(
                        _(
                            'REA Office Province Code ( %s ) not present in '
                            'your system'
                        ) % REA.Ufficio
                    )
                else:
                    office_id = offices[0].id
                    vals['rea_office'] = office_id

                rea_domain = [
                    ('rea_code', '=', rea_nr),
                    ('company_id', '=', partner_company_id),
                    ('id', '!=', partner_id)
                ]
                if office_id:
                    rea_domain.append(('rea_office', '=', office_id))
                rea_partners = partner_model.search(rea_domain)
                if rea_partners:
                    rea_names = ", ".join(rea_partners.mapped('name'))
                    p_name = partner_model.browse(partner_id).name
                    self.log_inconsistency(
                        _("Current invoice is from {} with REA Code"
                          " {}. Yet it seems that partners {} have the same"
                          " REA Code. This code should be unique; please fix"
                          " it."
                          .format(p_name, rea_nr, rea_names))
                    )
                else:
                    vals['rea_code'] = REA.NumeroREA

                vals['rea_capital'] = REA.CapitaleSociale or 0.0
                vals['rea_member_type'] = REA.SocioUnico or False
                vals['rea_liquidation_state'] = REA.StatoLiquidazione or False

            if cedPrest.Contatti:
                vals['phone'] = cedPrest.Contatti.Telefono
                vals['email'] = cedPrest.Contatti.Email
                vals['fax'] = cedPrest.Contatti.Fax
            # partner_model.browse(partner_id).write(vals)
            partner_model.browse(partner_id).update(vals)
        return partner_id

    def getCarrirerPartner(self, Carrier):
        partner_model = self.env['res.partner']
        partner_id = self.getPartnerBase(Carrier.DatiAnagraficiVettore)
        no_contact_update = False
        if partner_id:
            no_contact_update = partner_model.browse(partner_id).\
                electronic_invoice_no_contact_update
        if partner_id and not no_contact_update:
            vals = {
                'license_number':
                Carrier.DatiAnagraficiVettore.NumeroLicenzaGuida or '',
            }
            partner_model.browse(partner_id).write(vals)
        return partner_id

    def _prepare_generic_line_data(self, line):
        retLine = {}
        account_taxes = self.get_account_taxes(line.AliquotaIVA, line.Natura)
        if account_taxes:
            retLine['invoice_line_tax_id'] = [(6, 0, [account_taxes[0].id])]
        return retLine

    def get_account_taxes(self, AliquotaIVA, Natura):
        account_tax_model = self.env['account.tax']
        # check if a default tax exists and generate def_purchase_tax object
        ir_values = self.env['ir.values']
        company_id = self.env['res.company']._company_default_get(
            'account.invoice.line')
        supplier_taxes_ids = ir_values.get_default(
            'product.product', 'supplier_taxes_id', company_id=company_id)
        def_purchase_tax = False
        if supplier_taxes_ids:
            def_purchase_tax = account_tax_model.browse(supplier_taxes_ids)[0]
        if float(AliquotaIVA) == 0.0 and Natura:
            account_taxes = account_tax_model.search(
                [
                    ('type_tax_use', '=', 'purchase'),
                    ('kind_id.code', '=', Natura),
                    ('amount', '=', 0.0),
                ], order='sequence')
            if not account_taxes:
                self.log_inconsistency(
                    _('No tax with percentage '
                      '%s and nature %s found. Please configure this tax.')
                    % (AliquotaIVA, Natura))
            if len(account_taxes) > 1:
                self.log_inconsistency(
                    _('Too many taxes with percentage '
                      '%s and nature %s found. Tax %s with lower priority has '
                      'been set on invoice lines.')
                    % (AliquotaIVA, Natura,
                       account_taxes[0].description))
        else:
            account_taxes = account_tax_model.search(
                [
                    ('type_tax_use', '=', 'purchase'),
                    ('amount', '=', float(AliquotaIVA) / 100),
                    ('price_include', '=', False),
                    # partially deductible VAT must be set by user
                    ('child_ids', '=', False),
                ], order='sequence')
            if not account_taxes:
                self.log_inconsistency(
                    _(
                        "XML contains tax with percentage '%s' "
                        "but it does not exist in your system"
                    ) % AliquotaIVA
                )
            # check if there are multiple taxes with
            # same percentage
            if len(account_taxes) > 1:
                # just logging because this is an usual case: see split payment
                _logger.warning(_(
                    "Too many taxes with percentage equals "
                    "to '%s'.\nFix it if required"
                ) % AliquotaIVA)
                # if there are multiple taxes with same percentage
                # and there is a default tax with this percentage,
                # set taxes list equal to supplier_taxes_id, loaded before
                if (
                    def_purchase_tax and
                    def_purchase_tax.amount == (float(AliquotaIVA))
                ):
                    account_taxes = def_purchase_tax
        return account_taxes

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
                templates = supplier_infos.mapped('product_tmpl_id')
                if len(templates) == 1:
                    product = templates.product_variant_ids[0]
        if not product and partner.e_invoice_default_product_id:
            product = partner.e_invoice_default_product_id
        return product

    def adjust_accounting_data(self, product, line_vals):
        if product.product_tmpl_id.property_account_expense:
            line_vals['account_id'] = (
                product.product_tmpl_id.property_account_expense.id)
        elif (
            product.product_tmpl_id.categ_id.property_account_expense_categ
        ):
            line_vals['account_id'] = (
                product.product_tmpl_id.categ_id.
                property_account_expense_categ.id
            )
        account = self.env['account.account'].browse(line_vals['account_id'])
        new_tax = None
        if len(product.product_tmpl_id.supplier_taxes_id) == 1:
            new_tax = product.product_tmpl_id.supplier_taxes_id[0]
        elif len(account.tax_ids) == 1:
            new_tax = account.tax_ids[0]
        if new_tax:
            line_tax_id = (
                line_vals.get('invoice_line_tax_id') and
                line_vals['invoice_line_tax_id'][0][2][0]
            )
            line_tax = self.env['account.tax'].browse(line_tax_id)
            if new_tax.id != line_tax_id or not line_tax:
                if line_tax and new_tax.amount != line_tax.amount:
                    self.log_inconsistency(_(
                        "XML contains tax %s. Product %s has tax %s. Using "
                        "the XML one"
                    ) % (line_tax.name, product.name, new_tax.name))
                else:
                    # If product has the same amount of the one in XML,
                    # I use it. Typical case: 22% det 50%
                    line_vals['invoice_line_tax_id'] = [
                        (6, 0, [new_tax.id])]

    def _prepareInvoiceLine(self, credit_account_id, line, wt_founds=False):
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
            float(line.PrezzoUnitario) and
            line.Quantita and float(line.Quantita) and  # Quantita not required
            line.ScontoMaggiorazione
        ):
            retLine['discount'] = self._computeDiscount(line)
        if line.RiferimentoAmministrazione:
            retLine['admin_ref'] = line.RiferimentoAmministrazione

        if wt_founds and line.Ritenuta:
            retLine['invoice_line_tax_wt_ids'] = [(6, 0, [x.id for x in wt_founds])]

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

    def _createPaymentsLine(self, payment_id, line, partner_id):
        details = line.DettaglioPagamento or False
        if details:
            PaymentModel = self.env['fatturapa.payment.detail']
            PaymentMethodModel = self.env['fatturapa.payment_method']
            BankModel = self.env['res.bank']
            PartnerBankModel = self.env['res.partner.bank']
            for dline in details:
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
                            _pretty_iban(dline.IBAN.strip())
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
                                'bank': bankid,
                                'bank_bic': dline.BIC,
                                'state': 'iban',
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
        ftpa_doctype_model = self.env['fiscal.document.type']
        rel_docs_model = self.env['fatturapa.related_document_type']

        company = self.env.user.company_id.with_env(self.env)
        partner = partner_model.browse(partner_id)
        pay_acc_id = partner.property_account_payable.id

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
            for rel_doc in causLst:
                comment += rel_doc + '\n'

        invoice_data = {
            'fiscal_document_type_id': docType_id,
            'sender': fatt.FatturaElettronicaHeader.SoggettoEmittente or False,
            'account_id': pay_acc_id,
            'type': invtype,
            'partner_id': partner_id,
            'currency_id': currency[0].id,
            'journal_id': purchase_journal.id,
            # 'origin': xmlData.datiOrdineAcquisto,
            'fiscal_position': partner.property_account_position.id or False,
            'payment_term': partner.property_payment_term.id or False,
            'company_id': company.id,
            'fatturapa_attachment_in_id': fatturapa_attachment.id,
            'comment': comment
        }

        # 2.1.1.10
        self.set_efatt_rounding(FatturaBody, invoice_data)

        # 2.1.1.12
        self.set_art73(FatturaBody, invoice_data)

        # 2.1.1.5
        wt_founds = self.set_withholding_tax(FatturaBody, invoice_data)

        # 2.2.1
        self.set_invoice_line_ids(
            FatturaBody, credit_account_id, partner, wt_founds, invoice_data)

        self.set_e_invoice_lines(FatturaBody, invoice_data)

        invoice = invoice_model.create(invoice_data)

        # 2.1.1.7
        self.set_welfares_fund(
            FatturaBody, credit_account_id, invoice, wt_founds)

        # invoice._onchange_invoice_line_wt_ids()
        # invoice.compute_all_withholding_tax()
        invoice.write(invoice._convert_to_write(invoice._cache))
        invoice_id = invoice.id

        self.set_vendor_bill_data(FatturaBody, invoice)

        rel_docs_dict = {
            # 2.1.2
            'order': FatturaBody.DatiGenerali.DatiOrdineAcquisto,
            # 2.1.3
            'contract': FatturaBody.DatiGenerali.DatiContratto,
            # 2.1.4
            'agreement': FatturaBody.DatiGenerali.DatiConvenzione,
            # 2.1.5
            'reception': FatturaBody.DatiGenerali.DatiRicezione,
            # 2.1.6
            'invoice': FatturaBody.DatiGenerali.DatiFattureCollegate,
        }

        for rel_doc_key, rel_doc_data in rel_docs_dict.items():
            if not rel_doc_data:
                continue
            for rel_doc in rel_doc_data:
                doc_datas = self._prepareRelDocsLine(
                    invoice_id, rel_doc, rel_doc_key)
                for doc_data in doc_datas:
                    # Note for v12: must take advantage of batch creation
                    rel_docs_model.create(doc_data)

        # 2.1.7
        self.set_activity_progress(FatturaBody, invoice_id)

        # 2.1.8
        self.set_ddt_data(FatturaBody, invoice_id)

        # 2.1.9
        self.set_delivery_data(FatturaBody, invoice)

        # 2.2.2
        self.set_summary_data(FatturaBody, invoice_id)

        # 2.1.10
        self.set_parent_invoice_data(FatturaBody, invoice)

        # 2.3
        self.set_vehicles_data(FatturaBody, invoice)

        # 2.4
        self.set_payments_data(FatturaBody, invoice_id, partner_id)

        # 2.5
        self.set_attachments_data(FatturaBody, invoice_id)

        self._addGlobalDiscount(
            invoice_id, FatturaBody.DatiGenerali.DatiGeneraliDocumento)

        self.set_roundings(FatturaBody, invoice)

        # compute the invoice
        # invoice.compute_taxes()
        invoice.button_reset_taxes()
        # this can happen with refunds with negative amounts
        invoice.process_negative_lines()
        return invoice_id

    def set_vendor_bill_data(self, FatturaBody, invoice):
        if not invoice.date_invoice:
            invoice.update({
                'date_invoice':
                    FatturaBody.DatiGenerali.DatiGeneraliDocumento.Data.date(),
            })
        if not invoice.reference:
            invoice.update({
                'reference':
                    FatturaBody.DatiGenerali.DatiGeneraliDocumento.Numero,
            })

    def set_parent_invoice_data(self, FatturaBody, invoice):
        ParentInvoice = FatturaBody.DatiGenerali.FatturaPrincipale
        if ParentInvoice:
            parentinv_vals = {
                'related_invoice_code':
                    ParentInvoice.NumeroFatturaPrincipale or '',
                'related_invoice_date':
                    ParentInvoice.DataFatturaPrincipale or False
            }
            invoice.write(parentinv_vals)

    def set_vehicles_data(self, FatturaBody, invoice):
        Vehicle = FatturaBody.DatiVeicoli
        if Vehicle:
            veicle_vals = {
                'vehicle_registration': Vehicle.Data or False,
                'total_travel': Vehicle.TotalePercorso or '',
            }
            invoice.write(veicle_vals)

    def set_attachments_data(self, FatturaBody, invoice_id):
        AttachmentsData = FatturaBody.Allegati
        if AttachmentsData:
            self.env['fatturapa.attachment.in'].extract_attachments(
                AttachmentsData, invoice_id)

    def set_ddt_data(self, FatturaBody, invoice_id):
        DdtDatas = FatturaBody.DatiGenerali.DatiDDT
        if not DdtDatas:
            return
        invoice_line_model = self.env['account.invoice.line']
        DdTModel = self.env['fatturapa.related_ddt']
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

    def set_art73(self, FatturaBody, invoice_data):
        if FatturaBody.DatiGenerali.DatiGeneraliDocumento.Art73:
            invoice_data['art73'] = True

    def set_roundings(self, FatturaBody, invoice):
        rounding = 0.0
        if FatturaBody.DatiBeniServizi.DatiRiepilogo:
            for summary in FatturaBody.DatiBeniServizi.DatiRiepilogo:
                rounding += float(summary.Arrotondamento or 0.0)
        if FatturaBody.DatiGenerali.DatiGeneraliDocumento:
            summary = FatturaBody.DatiGenerali.DatiGeneraliDocumento
            rounding += float(summary.Arrotondamento or 0.0)

        if rounding:
            arrotondamenti_attivi_account_id = self.env.user.company_id.\
                arrotondamenti_attivi_account_id
            if not arrotondamenti_attivi_account_id:
                raise UserError(_("Round up account is not set "
                                  "in Accounting Settings"))

            arrotondamenti_passivi_account_id = self.env.user.company_id.\
                arrotondamenti_passivi_account_id
            if not arrotondamenti_passivi_account_id:
                raise UserError(_("Round down account is not set "
                                  "in Accounting Settings"))

            arrotondamenti_tax_id = self.env.user.company_id.\
                arrotondamenti_tax_id
            if not arrotondamenti_tax_id:
                self.log_inconsistency(
                    _('Round up and down tax is not set')
                )

            line_sequence = max(invoice.invoice_line.mapped('sequence'))
            line_vals = {}
            for summary in FatturaBody.DatiBeniServizi.DatiRiepilogo:
                to_round = float(summary.Arrotondamento or 0.0)
                if to_round != 0.0:
                    account_taxes = self.get_account_taxes(
                        summary.AliquotaIVA, summary.Natura)
                    arrotondamenti_account_id = arrotondamenti_passivi_account_id.id\
                        if to_round > 0.0 else arrotondamenti_attivi_account_id.id
                    invoice_line_tax_id = account_taxes[0].id if account_taxes\
                        else arrotondamenti_tax_id.id
                    name = _("Rounding down") if to_round > 0.0 else _(
                        "Rounding up")
                    line_sequence += 1
                    line_vals.update({
                        'sequence': line_sequence,
                        'invoice_id': invoice.id,
                        'name': name,
                        'account_id': arrotondamenti_account_id,
                        'price_unit': to_round,
                        'invoice_line_tax_id':
                            [(6, 0, [invoice_line_tax_id])],
                    })
            if line_vals:
                self.env['account.invoice.line'].create(line_vals)

    def set_efatt_rounding(self, FatturaBody, invoice_data):
        if FatturaBody.DatiGenerali.DatiGeneraliDocumento.Arrotondamento:
            invoice_data['efatt_rounding'] = float(
                FatturaBody.DatiGenerali.DatiGeneraliDocumento.Arrotondamento
            )

    def set_activity_progress(self, FatturaBody, invoice_id):
        SalDatas = FatturaBody.DatiGenerali.DatiSAL
        if SalDatas:
            SalModel = self.env['faturapa.activity.progress']
            for SalDataLine in SalDatas:
                SalModel.create(
                    {
                        'fatturapa_activity_progress':
                            SalDataLine.RiferimentoFase or 0,
                        'invoice_id': invoice_id
                    }
                )

    def set_payments_data(self, FatturaBody, invoice_id, partner_id):
        PaymentsData = FatturaBody.DatiPagamento
        if PaymentsData:
            PaymentDataModel = self.env['fatturapa.payment.data']
            PaymentTermsModel = self.env['fatturapa.payment_term']
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
                self._createPaymentsLine(PayDataId, PaymentLine, partner_id)

    def set_withholding_tax(self, FatturaBody, invoice_data):
        Withholdings = FatturaBody.DatiGenerali. \
            DatiGeneraliDocumento.DatiRitenuta
        if not Withholdings:
            return None
        invoice_data['ftpa_withholding_ids'] = []
        wt_founds = []
        for Withholding in Withholdings:
            wts = self.env['withholding.tax'].search([
                ('causale_pagamento_id.code', '=', Withholding.CausalePagamento)
            ])
            if not wts:
                raise UserError(_(
                    "The bill contains withholding tax with "
                    "payment reason %s, "
                    "but such a tax is not found in your system. Please "
                    "set it."
                ) % Withholding.CausalePagamento)

            for wt in wts:
                if (
                    wt.tax == float(Withholding.AliquotaRitenuta) and
                    WT_CODES_MAPPING[Withholding.TipoRitenuta] == wt.wt_types
                ):
                    wt_founds.append(wt)
                    break
            else:
                raise UserError(_(
                    "No withholding tax found with "
                    "document payment reason %s, rate %s and type %s.")
                    % (
                        Withholding.CausalePagamento,
                        Withholding.AliquotaRitenuta,
                        WT_CODES_MAPPING[Withholding.TipoRitenuta]
                    ))
            invoice_data['ftpa_withholding_ids'].append((
                0, 0, {
                    'name': Withholding.TipoRitenuta,
                    'amount': Withholding.ImportoRitenuta,
                }))
        return wt_founds

    def set_welfares_fund(
        self, FatturaBody, credit_account_id, invoice, wt_founds
    ):
        if not self.e_invoice_detail_level == '2':
            return

        Welfares = FatturaBody.DatiGenerali. \
            DatiGeneraliDocumento.DatiCassaPrevidenziale
        if not Welfares:
            return

        WelfareFundLineModel = self.env['welfare.fund.data.line']
        for welfareLine in Welfares:
            WalfarLineVals = self._prepareWelfareLine(invoice.id, welfareLine)
            WelfareFundLineModel.create(WalfarLineVals)

            if welfareLine.TipoCassa == 'TC07':
                continue

            line_vals = self._prepare_generic_line_data(welfareLine)
            line_vals.update({
                'name': _(
                    "Welfare Fund: %s") % welfareLine.TipoCassa,
                'price_unit': float(welfareLine.ImportoContributoCassa),
                'invoice_id': invoice.id,
                'account_id': credit_account_id,
            })
            if welfareLine.Ritenuta:
                if not wt_founds:
                    raise UserError(_(
                        "Welfare Fund data %s has withholding tax but no "
                        "withholding tax was found in the system."
                    ) % welfareLine.TipoCassa)
                line_vals['invoice_line_tax_wt_ids'] = [
                    (6, 0, [wt.id for wt in wt_founds])]
            if self.env.user.company_id.cassa_previdenziale_product_id:
                cassa_previdenziale_product = self.env.user.company_id \
                    .cassa_previdenziale_product_id
                line_vals['product_id'] = cassa_previdenziale_product.id
                line_vals['name'] = cassa_previdenziale_product.name
                self.adjust_accounting_data(
                    cassa_previdenziale_product, line_vals
                )
            self.env['account.invoice.line'].create(line_vals)

    def set_delivery_data(self, FatturaBody, invoice):
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

    def set_summary_data(self, FatturaBody, invoice_id):
        Summary_datas = FatturaBody.DatiBeniServizi.DatiRiepilogo
        summary_data_model = self.env['faturapa.summary.data']
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
                summary_data_model.create(summary_line)

    def set_e_invoice_lines(self, FatturaBody, invoice_data):
        e_invoice_lines = self.env['einvoice.line'].browse()
        for line in FatturaBody.DatiBeniServizi.DettaglioLinee:
            e_invoice_lines |= self.create_e_invoice_line(line)
        if e_invoice_lines:
            invoice_data['e_invoice_line_ids'] = [(6, 0, e_invoice_lines.ids)]

    def set_invoice_line_ids(
            self, FatturaBody, credit_account_id, partner, wt_founds,
            invoice_data):
        if not self.e_invoice_detail_level == '2':
            return

        invoice_lines = []
        invoice_line_model = self.env['account.invoice.line']
        for line in FatturaBody.DatiBeniServizi.DettaglioLinee:
            invoice_line_data = self._prepareInvoiceLine(
                credit_account_id, line, wt_founds)
            product = self.get_line_product(line, partner)
            if product:
                invoice_line_data['product_id'] = product.id
                self.adjust_accounting_data(product, invoice_line_data)
            invoice_line_id = invoice_line_model.create(
                invoice_line_data).id
            invoice_lines.append(invoice_line_id)
        invoice_data['invoice_line'] = [(6, 0, invoice_lines)]

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
            amount_untaxed = invoice.compute_xml_amount_untaxed(
                FatturaElettronicaBody)
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
        return fatturapa.CreateFromDocument(xml_string)

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

            xmlproblems = getattr(fatt, '_xmldoctor', None)
            if xmlproblems:  # None or []
                generic_inconsistencies += '\n'.join(xmlproblems) + '\n\n'

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
                        TaxRappresentative.DatiAnagrafici, supplier=False)
                    invoice.write(
                        {
                            'tax_representative_id': tax_partner_id
                        }
                    )
                if Intermediary:
                    Intermediary_id = self.getPartnerBase(
                        Intermediary.DatiAnagrafici, supplier=False)
                    invoice.write(
                        {
                            'intermediary': Intermediary_id
                        }
                    )
                new_invoices.append(invoice_id)
                self.check_invoice_amount(invoice, fattura)

                invoice.set_einvoice_data(fattura)

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
