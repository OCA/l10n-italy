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
import os
import shlex
import subprocess
from openerp.osv import orm
from openerp.tools.translate import _
from openerp.osv import fields
import logging

from openerp.addons.l10n_it_fatturapa.bindings import fatturapa
from openerp.addons.base_iban import base_iban
from openerp.osv.osv import except_osv
from lxml import etree

_logger = logging.getLogger(__name__)


class WizardImportFatturapa(orm.TransientModel):
    _name = "wizard.import.fatturapa"
    _description = "Import FatturaPA"

    _columns = {
        'e_invoice_detail_level': fields.selection([
            ('0', 'Minimo'),
            # ('1', 'Aliquote'),
            ('2', 'Massimo'), ],
            string="Livello di dettaglio Fatture elettroniche",
            help="Livello minimo: La fattura passiva viene creata senza righe; "
                 "sara' l'utente a doverle creare in base a quanto indicato dal "
                 "fornitore nella fattura elettronica\n"
                 # "Livello Aliquote: viene creata una riga fattura per ogni "
                 # "aliquota presente nella fattura elettronica\n"
                 "Livello Massimo: tutte le righe presenti nella fattura "
                 "elettronica vengono create come righe della fattura passiva",
            required=True)
        }

    def default_get(self, cr, uid, fields, context={}):
        logging.info('Calling default get for wizard import fatturaPA')
        res = super(WizardImportFatturapa, self).default_get(
            cr, uid, fields, context)
        res['e_invoice_detail_level'] = '2'
        fatturapa_attachment_ids = context.get('active_ids', [])
        fatturapa_attachment_obj = self.pool.get('fatturapa.attachment.in')
        partnerList = []
        for fatturapa_attachment_id in fatturapa_attachment_ids:
            fatturapa_attachment = fatturapa_attachment_obj.browse(
                cr, uid, fatturapa_attachment_id)
            logging.info('Going to get detail level from partner, fattura_pa_id %r, context %r' % (fatturapa_attachment_id, context))
            if fatturapa_attachment.in_invoice_ids:
                raise except_osv(
                    _('Error'), _("File %s is linked to invoices yet"
                                  ) % fatturapa_attachment.name)
            if fatturapa_attachment.xml_supplier_id not in partnerList:
                partnerList.append(fatturapa_attachment.xml_supplier_id)
            if len(partnerList) == 1:
                partner_detail_level = partnerList[0].e_invoice_detail_level
                logging.info(
                    'Going to setup partner detail level %r for partner %r' % (
                        partner_detail_level, partnerList[0]))
                if partner_detail_level:
                    res['e_invoice_detail_level'] = (partner_detail_level)
        return res

    def CountryByCode(self, cr, uid, CountryCode, context=None):
        logging.info('Get CountryCode %r' % (CountryCode))
        country_model = self.pool['res.country']
        return country_model.search(
            cr, uid, [('code', '=', CountryCode)], context=context)

    def ProvinceByCode(self, cr, uid, provinceCode, context=None):
        logging.info('Get provinceCode %r' % (provinceCode))
        province_model = self.pool['res.province']
        return province_model.search(
            cr, uid, [('code', '=', provinceCode)], context=context)

    def check_partner_base_data(
        self, cr, uid, partner_id, DatiAnagrafici, context=None
    ):
        if context is None:
            context = {}
        context['inconsistencies'] = ''
        partner = self.pool['res.partner'].browse(
            cr, uid, partner_id, context=context)
        if (
            DatiAnagrafici.Anagrafica.Denominazione and
            partner.name != DatiAnagrafici.Anagrafica.Denominazione
        ):
            if context.get('inconsistencies'):
                context['inconsistencies'] += '\n'
            context['inconsistencies'] += (
                _(
                    "DatiAnagrafici.Anagrafica.Denominazione contains \"%s\"."
                    " Your System contains \"%s\""
                )
                % (DatiAnagrafici.Anagrafica.Denominazione, partner.name)
            )
        if (
            DatiAnagrafici.Anagrafica.Nome and
            partner.firstname != DatiAnagrafici.Anagrafica.Nome
        ):
            if context.get('inconsistencies'):
                context['inconsistencies'] += '\n'
            context['inconsistencies'] += (
                _(
                    "DatiAnagrafici.Anagrafica.Nome contains \"%s\"."
                    " Your System contains \"%s\""
                )
                % (DatiAnagrafici.Anagrafica.Nome, partner.firstname)
            )
        if (
            DatiAnagrafici.Anagrafica.Cognome and
            partner.lastname != DatiAnagrafici.Anagrafica.Cognome
        ):
            if context.get('inconsistencies'):
                context['inconsistencies'] += '\n'
            context['inconsistencies'] += (
                _(
                    "DatiAnagrafici.Anagrafica.Cognome contains \"%s\"."
                    " Your System contains \"%s\""
                )
                % (DatiAnagrafici.Anagrafica.Cognome, partner.lastname)
            )

    def getPartnerBase(self, cr, uid, DatiAnagrafici, context=None):
        if not DatiAnagrafici:
            return False
        partner_model = self.pool['res.partner']
        cf = DatiAnagrafici.CodiceFiscale or False
        vat = False
        if DatiAnagrafici.IdFiscaleIVA:
            vat = "%s%s" % (
                DatiAnagrafici.IdFiscaleIVA.IdPaese,
                DatiAnagrafici.IdFiscaleIVA.IdCodice
            )
        partner_ids = partner_model.search(
            cr, uid,
            ['|',
             ('vat', '=', vat or 0),
             ('fiscalcode', '=', cf or 0),
             ],
            context=context)
        commercial_partner = False
        if len(partner_ids) > 1:
            for partner in partner_model.browse(
                cr, uid, partner_ids, context=context
            ):
                if (
                    commercial_partner and
                    partner.commercial_partner_id.id != commercial_partner
                ):
                    raise orm.except_orm(
                        _('Error !'),
                        _("Two distinct partners with "
                          "Vat %s and Fiscalcode %s already present in db" %
                          (vat, cf))
                        )
                commercial_partner = partner.commercial_partner_id.id
        if not partner_ids:
            if DatiAnagrafici.Anagrafica.Denominazione:
                partner_ids = partner_model.search(
                    cr, uid,
                    [('name', '=', DatiAnagrafici.Anagrafica.Denominazione)],
                    context=context)
            elif (
                DatiAnagrafici.Anagrafica.Nome and
                DatiAnagrafici.Anagrafica.Cognome
            ):
                partner_ids = partner_model.search(
                    cr, uid,
                    [
                        ('firstname', '=', DatiAnagrafici.Anagrafica.Nome),
                        ('lastname', '=', DatiAnagrafici.Anagrafica.Cognome),
                    ],
                    context=context)
        if partner_ids:
            if not commercial_partner:
                commercial_partner = partner_ids[0]
            self.check_partner_base_data(
                cr, uid, commercial_partner, DatiAnagrafici, context=context)
            return commercial_partner
        else:
            # partner to be created
            country_id = False
            if DatiAnagrafici.IdFiscaleIVA:
                CountryCode = DatiAnagrafici.IdFiscaleIVA.IdPaese
                country_ids = self.CountryByCode(
                    cr, uid, CountryCode, context=context)
                if country_ids:
                    country_id = country_ids[0]
                else:
                    raise orm.except_orm(
                        _('Error !'),
                        _("Country Code %s not found in system") % CountryCode
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

            return partner_model.create(cr, uid, vals, context=context)

    def getCedPrest(self, cr, uid, cedPrest, context=None):
        if not context:
            context = {}
        partner_model = self.pool['res.partner']
        partner_id = self.getPartnerBase(
            cr, uid, cedPrest.DatiAnagrafici, context=context)
        fiscalPosModel = self.pool['fatturapa.fiscal_position']
        vals = {}
        if partner_id:
            if cedPrest.StabileOrganizzazione:
                vals = {
                    'street': cedPrest.StabileOrganizzazione.Indirizzo,
                    'zip': cedPrest.StabileOrganizzazione.CAP,
                    'city': cedPrest.StabileOrganizzazione.Comune,
                    'register': cedPrest.DatiAnagrafici.AlboProfessionale or ''
                }
            else:
                vals = {
                    'street': cedPrest.Sede.Indirizzo,
                    'zip': cedPrest.Sede.CAP,
                    'city': cedPrest.Sede.Comune,
                    'register': cedPrest.DatiAnagrafici.AlboProfessionale or ''
                }
            if cedPrest.DatiAnagrafici.ProvinciaAlbo:
                ProvinciaAlbo = cedPrest.DatiAnagrafici.ProvinciaAlbo
                prov_ids = self.ProvinceByCode(
                    cr, uid, ProvinciaAlbo, context=context)
                if not prov_ids:
                    if context.get('inconsistencies'):
                        context['inconsistencies'] += '\n'
                    context['inconsistencies'] += (
                        _('ProvinciaAlbo ( %s ) not present in system') %
                        ProvinciaAlbo
                        )
                vals['register_province'] = prov_ids[0]
            if cedPrest.Sede.Provincia:
                Provincia = cedPrest.Sede.Provincia
                prov_sede = self.ProvinceByCode(cr, uid, Provincia, context)
                if not prov_sede:
                    self.log_inconsistency(
                        _('Provincia ( %s ) not present in system')
                        % Provincia
                    )
                else:
                    vals['province'] = prov_sede[0]
            vals['register_code'] = (
                cedPrest.DatiAnagrafici.NumeroIscrizioneAlbo)
            vals['register_regdate'] = (
                cedPrest.DatiAnagrafici.DataIscrizioneAlbo)

            if cedPrest.DatiAnagrafici.RegimeFiscale:
                rfPos = cedPrest.DatiAnagrafici.RegimeFiscale
                FiscalPosIds = fiscalPosModel.search(
                    cr, uid,
                    [('code', '=', rfPos)],
                    context=context
                )
                if not FiscalPosIds:
                    raise orm.except_orm(
                        _('Error!'),
                        _('RegimeFiscale %s is not present in your system')
                        % rfPos
                    )
                else:
                    vals['register_fiscalpos'] = FiscalPosIds[0]

            if cedPrest.IscrizioneREA:
                REA = cedPrest.IscrizioneREA
                vals['rea_code'] = REA.NumeroREA
                office_id = False
                office_ids = self.ProvinceByCode(
                    cr, uid, REA.Ufficio, context=context)
                if not office_ids:
                    if context.get('inconsistencies'):
                        context['inconsistencies'] += '\n'
                    context['inconsistencies'] += (
                        _('REA Office Code ( %s ) not present in system') %
                        REA.Ufficio
                        )
                else:
                    office_id = office_ids[0]
                    vals['rea_office'] = office_id
                vals['rea_capital'] = REA.CapitaleSociale or 0.0
                vals['rea_member_type'] = REA.SocioUnico or False
                vals['rea_liquidation_state'] = REA.StatoLiquidazione or False

            if cedPrest.Contatti:
                vals['phone'] = cedPrest.Contatti.Telefono
                vals['email'] = cedPrest.Contatti.Email
                vals['fax'] = cedPrest.Contatti.Fax
            partner_model.write(cr, uid, partner_id, vals, context=context)
        return partner_id

    def getCarrier(self, cr, uid, partner_id, context={}):
        carrier_model = self.pool['delivery.carrier']
        carrier_ids = carrier_model.search(
            cr, uid, [('partner_id', '=', partner_id), ('active', '=', True)])
        if len(carrier_ids) > 1:
            logging.warning(
                'Found more than one carrier for partner %r, carriers %r' % (
                    partner_id, carrier_ids))
        for carrier_id in carrier_ids:
            return carrier_id
        return False

    def getCarrirerPartner(self, cr, uid, Carrier, context=None):
        carrier_id = False
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
            carrier_id = self.getCarrier(cr, uid, partner_id, context)
        return carrier_id

    def _prepareInvoiceLine(
        self, cr, uid, credit_account_id, line, context=None
    ):
        account_tax_model = self.pool['account.tax']
        # check if a default tax exists and generate def_purchase_tax object
        ir_values = self.pool.get('ir.values')
        company_id = self.pool.get('res.company')._company_default_get(
            cr, uid, 'account.invoice.line', context=context
        )
        supplier_taxes_ids = ir_values.get_default(
            cr, uid, 'product.product', 'supplier_taxes_id',
            company_id=company_id
        )
        def_purchase_tax = False
        if supplier_taxes_ids:
            def_purchase_tax = account_tax_model.browse(
                cr, uid, supplier_taxes_ids, context=context)[0]
        if float(line.AliquotaIVA) == 0.0 and line.Natura:
            account_tax_ids = account_tax_model.search(
                cr, uid,
                [
                    ('type_tax_use', 'in', ('purchase', 'all')),
                    ('non_taxable_nature', '=', line.Natura),
                    ('amount', '=', 0.0),
                ], context=context)
            if not account_tax_ids:
                if context.get('inconsistencies'):
                    context['inconsistencies'] += '\n'
                context['inconsistencies'] += (
                    _('No tax with percentage '
                      '%s and nature %s found')
                    % (line.AliquotaIVA, line.Natura))
            if len(account_tax_ids) > 1:
                if context.get('inconsistencies'):
                    context['inconsistencies'] += '\n'
                context['inconsistencies'] += (
                    _('Too many taxes with percentage '
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
                if context.get('inconsistencies'):
                    context['inconsistencies'] += '\n'
                context['inconsistencies'] += (
                    _(
                        'XML contains tax with percentage "%s" '
                        'but it does not exist in your system'
                    ) % line.AliquotaIVA
                )
            # check if there are multiple taxes with
            # same percentage
            if len(account_tax_ids) > 1:
                # just logging because this is an usual case: see split payment
                _logger.warning(_(
                    "Line '%s': Too many taxes with percentage equals "
                    "to \"%s\"\nfix it if required"
                ) % (line.Descrizione, line.AliquotaIVA))
                # if there are multiple taxes with same percentage
                # and there is a default tax with this percentage,
                # set taxes list equal to supplier_taxes_id, loaded before
                if (
                    def_purchase_tax and
                    def_purchase_tax.amount == (float(line.AliquotaIVA) / 100)
                ):
                    account_tax_ids = supplier_taxes_ids
        retLine = {
            'name': line.Descrizione,
            'sequence': int(line.NumeroLinea),
            'account_id': credit_account_id,
        }
        if account_tax_ids:
            retLine['invoice_line_tax_id'] = [(6, 0, [account_tax_ids[0]])]
        if line.PrezzoUnitario:
            retLine['price_unit'] = float(line.PrezzoUnitario)
        if line.Quantita:
            retLine['quantity'] = float(line.Quantita)
        if line.TipoCessionePrestazione:
            retLine['service_type'] = line.TipoCessionePrestazione
        if line.UnitaMisura:
            retLine['ftpa_uom'] = line.UnitaMisura
        if line.DataInizioPeriodo:
            retLine['service_start'] = line.DataInizioPeriodo
        if line.DataFinePeriodo:
            retLine['service_end'] = line.DataFinePeriodo
        if (
            line.PrezzoTotale and line.PrezzoUnitario and line.Quantita and
            line.ScontoMaggiorazione
        ):
            retLine['discount'] = self._computeDiscount(
                cr, uid, line, context=context)
        if line.RiferimentoAmministrazione:
            retLine['admin_ref'] = line.RiferimentoAmministrazione

        return retLine

    def get_line_product(self, cr, uid, line, partner):
        product = None
        supplier_info = self.pool['product.supplierinfo']
        if len(line.CodiceArticolo) == 1:
            supplier_code = line.CodiceArticolo[0].CodiceValore
            supplier_infos = supplier_info.search(cr, uid, [
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

    def adjust_accounting_data(self, cr, uid, product, line_vals, context={}):
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
        account = self.pool['account.account'].browse(
            cr, uid, line_vals['account_id'])
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
            line_tax = self.pool['account.tax'].browse(cr, uid, line_tax_id)
            if new_tax.id != line_tax_id:
                if new_tax._get_tax_amount() != line_tax._get_tax_amount():
                    if context.get('inconsistencies'):
                        context['inconsistencies'] += '\n'
                    context['inconsistencies'] += (
                        _("XML contains tax %s. Product %s has tax %s. Using "
                          "the XML one") % (
                            line_tax.name, product.name, new_tax.name))
                else:
                    # If product has the same amount of the one in XML,
                    # I use it. Typical case: 22% det 50%
                    line_vals['invoice_line_tax_id'] = [
                        (6, 0, [new_tax.id])]

    def _prepareRelDocsLine(
        self, cr, uid, invoice_id, line, type, context=None
    ):
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

    def _prepareWelfareLine(
        self, cr, uid, invoice_id, line, context=None
    ):
        res = []
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
            kind = self.pool['account.tax.kind'].search(cr, uid, [
                ('code', '=', Natura)
            ])
            if not kind:
                self.log_inconsistency(
                    _("Tax kind %s not found") % Natura
                )
            else:
                kind_id = kind[0]
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

        res = {
            'welfare_rate_tax': AlCassa,
            'welfare_amount_tax': ImportoContributoCassa,
            'welfare_taxable': ImponibileCassa,
            'welfare_Iva_tax': AliquotaIVA,
            'subjected_withholding': Ritenuta,
            'fund_nature': Natura or False,
            'kind_id': kind_id,
            'pa_line_code': RiferimentoAmministrazione,
            'invoice_id': invoice_id,
        }
        if not WelfareTypeId:
            raise orm.except_orm(
                _('Error'),
                _('TipoCassa %s is not present in your system') % TipoCassa)
        else:
            res['name'] = WelfareTypeId[0]

        return res

    def _prepareDiscRisePriceLine(
        self, cr, uid, id, line, context=None
    ):
        res = []
        Tipo = line.Tipo or False
        Percentuale = line.Percentuale and float(line.Percentuale) or 0.0
        Importo = line.Importo and float(line.Importo) or 0.0
        res = {
            'percentage': Percentuale,
            'amount': Importo,
            context.get('drtype'): id,
        }
        res['name'] = Tipo

        return res

    def _computeDiscount(self, cr, uid, DettaglioLinea, context=None):
        line_total = float(DettaglioLinea.PrezzoTotale)
        if not line_total or not DettaglioLinea.Quantita:
            return 0
        line_unit = line_total / float(DettaglioLinea.Quantita)
        discount = (
            1 - (line_unit / float(DettaglioLinea.PrezzoUnitario))
            ) * 100.0
        return discount

    def _addGlobalDiscount(
        self, cr, uid, invoice_id, DatiGeneraliDocumento, context=None
    ):
        discount = 0.0
        if DatiGeneraliDocumento.ScontoMaggiorazione:
            invoice = self.pool['account.invoice'].browse(
                cr, uid, invoice_id, context=context)
            invoice.button_compute(context=context, set_total=True)
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
            journal = self.get_purchase_journal(
                cr, uid, invoice.company_id, context=context)
            credit_account_id = journal.default_credit_account_id.id
            line_vals = {
                'invoice_id': invoice_id,
                'name': _(
                    "Global invoice discount from DatiGeneraliDocumento"),
                'account_id': credit_account_id,
                'price_unit': discount,
                'quantity': 1,
                }
            self.pool['account.invoice.line'].create(
                cr, uid, line_vals, context=context)
        return True

    def _createPayamentsLine(
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
                            'ModalitaPagamento %s not defined in your system'
                            % dline.ModalitaPagamento
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
                        if not dline.IstitutoFinanziario:
                            if context.get('inconsistencies'):
                                context['inconsistencies'] += '\n'
                            context['inconsistencies'] += (
                                _("Name of Bank with BIC \"%s\" is not set."
                                  " Can't create bank") % dline.BIC
                            )
                        else:
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
                        if context.get('inconsistencies'):
                            context['inconsistencies'] += '\n'
                        context['inconsistencies'] += (
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

                if payment_bank_id:
                    val['payment_bank'] = payment_bank_id
                PaymentModel.create(cr, uid, val, context=context)
        return True

    def get_purchase_journal(self, cr, uid, company, context=None):
        journal_model = self.pool['account.journal']
        journal_ids = journal_model.search(
            cr, uid,
            [
                ('type', '=', 'purchase'),
                ('company_id', '=', company.id),
                ('default_credit_account_id', '!=', False)
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
        return purchase_journal

    def invoiceCreate(
        self, cr, uid, ids, fatt, fatturapa_attachment, FatturaBody,
        partner_id, context=None
    ):
        if context is None:
            context = {}
        wizardObj = self.browse(cr, uid, ids[0])
        partner_model = self.pool['res.partner']
        invoice_model = self.pool['account.invoice']
        currency_model = self.pool['res.currency']
        invoice_line_model = self.pool['account.invoice.line']
        ftpa_doctype_poll = self.pool['fiscal.document.type']
        rel_docs_model = self.pool['fatturapa.related_document_type']
        WelfareFundLineModel = self.pool['welfare.fund.data.line']
        DiscRisePriceModel = self.pool['discount.rise.price']
        SalModel = self.pool['faturapa.activity.progress']
        DdTModel = self.pool['fatturapa.related_ddt']
        PaymentDataModel = self.pool['fatturapa.payment.data']
        PaymentTermsModel = self.pool['fatturapa.payment_term']
        SummaryDatasModel = self.pool['faturapa.summary.data']

        company = self.pool['res.users'].browse(
            cr, uid, uid, context=context).company_id
        partner = partner_model.browse(cr, uid, partner_id, context=context)
        pay_acc_id = partner.property_account_payable.id
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
        purchase_journal = self.get_purchase_journal(
            cr, uid, company, context=context)
        credit_account_id = purchase_journal.default_credit_account_id.id
        invoice_lines = []
        comment = ''
        # 2.1.1
        docType_id = False
        invtype = 'in_invoice'
        docType = FatturaBody.DatiGenerali.DatiGeneraliDocumento.TipoDocumento
        if docType:
            docType_ids = ftpa_doctype_poll.search(
                cr, uid,
                [
                    ('code', '=', docType)
                ],
                context=context
            )
            if docType_ids:
                docType_id = docType_ids[0]
            else:
                raise orm.except_orm(
                    _("Error"),
                    _("tipoDocumento %s not handled")
                    % docType)
            if docType == 'TD04' or docType == 'TD05':
                invtype = 'in_refund'
        # 2.1.1.11
        causLst = FatturaBody.DatiGenerali.DatiGeneraliDocumento.Causale
        if causLst:
            for item in causLst:
                comment += item + '\n'
        # 2.2.1
        e_invoice_line_ids = []
        CodeArts = self.pool['fatturapa.article.code']
        for line in FatturaBody.DatiBeniServizi.DettaglioLinee:
            if wizardObj.e_invoice_detail_level == '2':
                invoice_line_data = self._prepareInvoiceLine(
                    cr, uid, credit_account_id, line, context=context)
                invoice_line_id = invoice_line_model.create(
                    cr, uid, invoice_line_data, context=context)
    
                if line.CodiceArticolo:
                    for caline in line.CodiceArticolo:
                        CodeArts.create(
                            cr, uid,
                            {
                                'name': caline.CodiceTipo or '',
                                'code_val': caline.CodiceValore or '',
                                'invoice_line_id': invoice_line_id
                            },
                            context=context
                        )
                if line.ScontoMaggiorazione:
                    context['drtype'] = 'invoice_line_id'
                    for DiscRisePriceLine in line.ScontoMaggiorazione:
                        DiscRisePriceVals = self._prepareDiscRisePriceLine(
                            cr, uid, invoice_line_id, DiscRisePriceLine,
                            context=context
                        )
                        DiscRisePriceModel.create(
                            cr, uid, DiscRisePriceVals, context=context)
                invoice_lines.append(invoice_line_id)
            einvoiceline = self.create_e_invoice_line(cr, uid, line)
            e_invoice_line_ids.append(einvoiceline.id)
            
        invoice_data = {
            'date_invoice': FatturaBody.DatiGenerali.DatiGeneraliDocumento.Data,
            'supplier_invoice_number':
                FatturaBody.DatiGenerali.DatiGeneraliDocumento.Numero,
            'sender': fatt.FatturaElettronicaHeader.SoggettoEmittente or False,
            'account_id': pay_acc_id, 'type': invtype, 'partner_id': partner_id,
            'currency_id': currency_id[0], 'journal_id': purchase_journal.id,
            'invoice_line': [(6, 0, invoice_lines)],
            'fiscal_position': (partner.property_account_position.id or False),
            'payment_term': (
                        partner.property_supplier_payment_term.id or False),
            'company_id': company.id,
            'fatturapa_attachment_in_id': fatturapa_attachment.id,
            'comment': comment, 'fiscal_document_type_id': docType_id,
            'e_invoice_line_ids': [(6, 0, e_invoice_line_ids)]}
        # 2.1.1.5
        Withholdings = FatturaBody.DatiGenerali.\
            DatiGeneraliDocumento.DatiRitenuta
        if Withholdings:
            invoice_data['ftpa_withholding_ids'] = []
            for Withholding in Withholdings:
                invoice_data['ftpa_withholding_ids'].append((
                    0, 0, {
                        'name': Withholding.TipoRitenuta,
                        'amount': Withholding.ImportoRitenuta,
                        'rate': float(Withholding.AliquotaRitenuta)/100,
                        'reason': Withholding.CausalePagamento,
                    })
                )
        # 2.1.1.6
        Stamps = FatturaBody.DatiGenerali.\
            DatiGeneraliDocumento.DatiBollo
        if Stamps:
            invoice_data['virtual_stamp'] = Stamps.BolloVirtuale
            invoice_data['stamp_amount'] = float(Stamps.ImportoBollo)
        invoice_id = invoice_model.create(
            cr, uid, invoice_data, context=context)

        self.add_dati_bollo(
            cr, uid, ids, invoice_id,
            FatturaBody.DatiGenerali.DatiGeneraliDocumento)

        invoice = invoice_model.browse(cr, uid, invoice_id, context=context)
        # 2.1.1.7
        Walfares = FatturaBody.DatiGenerali.\
            DatiGeneraliDocumento.DatiCassaPrevidenziale
        if Walfares:
            for walfareLine in Walfares:
                WalferLineVals = self._prepareWelfareLine(
                    cr, uid, invoice_id, walfareLine, context=context)
                WelfareFundLineModel.create(
                    cr, uid, WalferLineVals, context=context)
        # 2.1.1.8
        DiscountRises = FatturaBody.DatiGenerali.\
            DatiGeneraliDocumento.ScontoMaggiorazione
        if DiscountRises:
            context['drtype'] = 'invoice_id'
            for DiscRisePriceLine in DiscountRises:
                DiscRisePriceVals = self._prepareDiscRisePriceLine(
                    cr, uid, invoice_id, DiscRisePriceLine, context=context)
                DiscRisePriceModel.create(
                    cr, uid, DiscRisePriceVals, context=context)
        # 2.1.2
        relOrders = FatturaBody.DatiGenerali.DatiOrdineAcquisto
        if relOrders:
            for order in relOrders:
                doc_datas = self._prepareRelDocsLine(
                    cr, uid, invoice_id, order, 'order', context=context)
                if doc_datas:
                    for doc_data in doc_datas:
                        rel_docs_model.create(
                            cr, uid, doc_data, context=context)
        # 2.1.3
        relContracts = FatturaBody.DatiGenerali.DatiContratto
        if relContracts:
            for contract in relContracts:
                doc_datas = self._prepareRelDocsLine(
                    cr, uid, invoice_id, contract, 'contract', context=context)
                if doc_datas:
                    for doc_data in doc_datas:
                        rel_docs_model.create(
                            cr, uid, doc_data, context=context)
        # 2.1.4
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
        # 2.1.5
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
        # 2.1.6
        RelInvoices = FatturaBody.DatiGenerali.DatiFattureCollegate
        if RelInvoices:
            for invoice in RelInvoices:
                doc_datas = self._prepareRelDocsLine(
                    cr, uid, invoice_id, invoice, 'invoice', context=context)
                if doc_datas:
                    for doc_data in doc_datas:
                        rel_docs_model.create(
                            cr, uid, doc_data, context=context)
        # 2.1.7
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
        # 2.1.8
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
        # 2.1.9
        Delivery = FatturaBody.DatiGenerali.DatiTrasporto
        if Delivery:
            delivery_id = self.getCarrirerPartner(
                cr, uid, Delivery, context=context)
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
                    delivery_dict['incoterm'] = stock_incoterm_id[0]
            invoice_model.write(
                cr, uid, [invoice_id], delivery_dict, context=context)
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
                SummaryDatasModel.create(
                    cr, uid, summary_line, context=context)

        # 2.1.10
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
        # 2.3
        Vehicle = FatturaBody.DatiVeicoli
        if Vehicle:
            veicle_vals = {
                'vehicle_registration': Vehicle.Data or False,
                'total_travel': Vehicle.TotalePercorso or '',
            }
            invoice_model.write(
                cr, uid, invoice_id, veicle_vals, context=context)
        # 2.4
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
                self._createPayamentsLine(
                    cr, uid, PayDataId, PaymentLine, partner_id,
                    context=context
                )
        # 2.5
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

        self._addGlobalDiscount(
            cr, uid, invoice_id,
            FatturaBody.DatiGenerali.DatiGeneraliDocumento, context=context)

        # compute the invoice
        invoice_model.button_compute(
            cr, uid, [invoice_id], context=context,
            set_total=True)
        return invoice_id

    def create_e_invoice_line(self, cr, uid, line):
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
        einvoiceline = self.pool['einvoice.line'].create(cr, uid, vals)
        if line.CodiceArticolo:
            for caline in line.CodiceArticolo:
                self.pool['fatturapa.article.code'].create(
                    cr, uid, {
                        'name': caline.CodiceTipo or '',
                        'code_val': caline.CodiceValore or '',
                        'e_invoice_line_id': einvoiceline})
        if line.ScontoMaggiorazione:
            for DiscRisePriceLine in line.ScontoMaggiorazione:
                DiscRisePriceVals = self._prepareDiscRisePriceLine(
                    cr, uid, einvoiceline, DiscRisePriceLine,
                    context={'drtype': 'e_invoice_line_id'}
                )
                self.pool['discount.rise.price'].create(
                    cr, uid, DiscRisePriceVals)
        if line.AltriDatiGestionali:
            for dato in line.AltriDatiGestionali:
                self.pool['einvoice.line.other.data'].create(cr, uid, 
                    {
                        'name': dato.TipoDato,
                        'text_ref': dato.RiferimentoTesto,
                        'num_ref': float(dato.RiferimentoNumero or 0),
                        'date_ref': dato.RiferimentoData,
                        'e_invoice_line_id': einvoiceline
                    }
                )
        return self.pool['einvoice.line'].browse(cr, uid, einvoiceline)

    def add_dati_bollo(self, cr, uid, ids, invoice, DatiGeneraliDocumento,
                       context={}):
        # 2.1.1.6
        Stamps = DatiGeneraliDocumento.DatiBollo
        if Stamps:
            invoice = self.pool['account.invoice'].browse(cr, uid, invoice)
            invoice.virtual_stamp = Stamps.BolloVirtuale
            invoice.stamp_amount = float(Stamps.ImportoBollo)
            for wizardBrws in self.browse(cr, uid, ids):
                if wizardBrws.e_invoice_detail_level == '2':
                    journal = self.get_purchase_journal(
                        cr, uid, invoice.company_id, context)
                    credit_account_id = journal.default_credit_account_id.id
                    line_vals = {
                        'invoice_id': invoice.id,
                        'name': _(
                            "Bollo assolto ai sensi del decreto MEF 17 giugno "
                            "2014 (art. 6)"
                        ),
                        'account_id': credit_account_id,
                        'price_unit': invoice.stamp_amount,
                        'quantity': 1,
                        }
                    if self.pool['res.users'].browse(
                            cr, uid, uid).company_id.dati_bollo_product_id:
                        dati_bollo_product = (
                            self.pool.user.company_id.dati_bollo_product_id)
                        line_vals['product_id'] = dati_bollo_product.id
                        line_vals['name'] = dati_bollo_product.name
                        self.adjust_accounting_data(
                            cr, uid, dati_bollo_product, line_vals, context)
                    self.pool['account.invoice.line'].create(
                        cr, uid, line_vals)

    def check_CessionarioCommittente(
        self, cr, uid, company, FatturaElettronicaHeader, context=None
    ):
        if (
            company.partner_id.ipa_code !=
            FatturaElettronicaHeader.DatiTrasmissione.CodiceDestinatario
        ):
            raise orm.except_orm(
                _('Error'),
                _('XML IPA code (%s) different from company IPA code (%s)')
                % (
                    FatturaElettronicaHeader.DatiTrasmissione.
                    CodiceDestinatario, company.partner_id.ipa_code))

    def compute_xml_amount_untaxed(self, cr, uid, DatiRiepilogo, context=None):
        amount_untaxed = 0.0
        for Riepilogo in DatiRiepilogo:
            amount_untaxed += float(Riepilogo.ImponibileImporto)
        return amount_untaxed

    def check_invoice_amount(
        self, cr, uid, invoice, FatturaElettronicaBody, context=None
    ):
        if context is None:
            context = {}

        invoice.write(
            {
                'check_total': FatturaElettronicaBody.DatiGenerali.
                DatiGeneraliDocumento.ImportoTotaleDocumento
            }, context=context)
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
            if invoice.amount_total != ImportoTotaleDocumento:
                if context.get('inconsistencies'):
                    context['inconsistencies'] += '\n'
                context['inconsistencies'] += (
                    _('Invoice total %s is different from '
                      'ImportoTotaleDocumento %s')
                    % (invoice.amount_total, ImportoTotaleDocumento)
                )
        else:
            # else, we can only check DatiRiepilogo if
            # DatiGeneraliDocumento.ScontoMaggiorazione is not present,
            # because otherwise DatiRiepilogo and openerp invoice total would
            # differ
            amount_untaxed = self.compute_xml_amount_untaxed(
                cr, uid,
                FatturaElettronicaBody.DatiBeniServizi.DatiRiepilogo,
                context=context)
            if invoice.amount_untaxed != amount_untaxed:
                if context.get('inconsistencies'):
                    context['inconsistencies'] += '\n'
                context['inconsistencies'] += (
                    _('Computed amount untaxed %s is different from'
                      ' DatiRiepilogo %s')
                    % (invoice.amount_untaxed, amount_untaxed)
                )

    def strip_xml_content(self, xml):
        root = etree.XML(xml)
        for elem in root.iter('*'):
            if elem.text is not None:
                elem.text = elem.text.strip()
        return etree.tostring(root)

    def remove_xades_sign(self, xml):
        root = etree.XML(xml)
        for elem in root.iter('*'):
            if elem.tag.find('Signature') > -1:
                elem.getparent().remove(elem)
                break
        return etree.tostring(root)

    def check_file_is_pem(self, p7m_file):
        file_is_pem = True
        strcmd = (
            'openssl asn1parse  -inform PEM -in %s'
        ) % (p7m_file)
        cmd = shlex.split(strcmd)
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            stdoutdata, stderrdata = proc.communicate()
            if proc.wait() != 0:
                file_is_pem = False
        except Exception as e:
            raise orm.except_orm(
                _('Errore'),
                _(
                    'Check PEM file %s'
                ) % e.args
            )
        return file_is_pem

    def parse_pem_2_der(self, pem_file, tmp_der_file):
        strcmd = (
            'openssl asn1parse -in %s -out %s'
        ) % (pem_file, tmp_der_file)
        cmd = shlex.split(strcmd)
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            stdoutdata, stderrdata = proc.communicate()
            if proc.wait() != 0:
                _logger.warning(stdoutdata)
                raise Exception(stderrdata)
        except Exception as e:
            raise orm.except_orm(
                _('Errore'),
                _(
                    'Parsing PEM to DER  file %s'
                ) % e.args
            )
        if not os.path.isfile(tmp_der_file):
            raise orm.except_orm(
                _('Errore'),
                _(
                    'ASN.1 structure is not parsable in DER'
                )
            )
        return tmp_der_file

    def decrypt_to_xml(self, signed_file, xml_file):
        strcmd = (
            'openssl smime -decrypt -verify -inform'
            ' DER -in %s -noverify -out %s'
        ) % (signed_file, xml_file)
        cmd = shlex.split(strcmd)
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            stdoutdata, stderrdata = proc.communicate()
            if proc.wait() != 0:
                _logger.warning(stdoutdata)
                raise Exception(stderrdata)
        except Exception as e:
            raise orm.except_orm(
                _('Errore'),
                _(
                    'Signed Xml file %s'
                ) % e.args
            )
        if not os.path.isfile(xml_file):
            raise orm.except_orm(
                _('Errore'),
                _(
                    'Signed Xml file not decryptable'
                )
            )
        return xml_file

    def importFatturaPA(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        context['inconsistencies'] = ''
        fatturapa_attachment_obj = self.pool['fatturapa.attachment.in']
        fatturapa_attachment_ids = context.get('active_ids', False)
        invoice_model = self.pool['account.invoice']
        new_invoices = []
        for fatturapa_attachment_id in fatturapa_attachment_ids:
            ctx = context.copy()
            fatturapa_attachment = fatturapa_attachment_obj.browse(
                cr, uid, fatturapa_attachment_id, context=ctx)
            if fatturapa_attachment.in_invoice_ids:
                raise orm.except_orm(
                    _("Error"), _("File is linked to invoices yet"))
            fatt = self.get_invoice_obj(cr, uid, fatturapa_attachment)
            
            cedentePrestatore = fatt.FatturaElettronicaHeader.CedentePrestatore
            # 1.2
            partner_id = self.getCedPrest(
                cr, uid, cedentePrestatore, context=ctx)
            # 1.3
            TaxRappresentative = fatt.FatturaElettronicaHeader.\
                RappresentanteFiscale
            # 1.5
            Intermediary = fatt.FatturaElettronicaHeader.\
                TerzoIntermediarioOSoggettoEmittente
            # 2
            for fattura in fatt.FatturaElettronicaBody:
                invoice_id = self.invoiceCreate(
                    cr, uid, ids, fatt, fatturapa_attachment, fattura,
                    partner_id, context=ctx)
                self.set_StabileOrganizzazione(
                    cr, uid, cedentePrestatore, invoice_id)
                if TaxRappresentative:
                    tax_partner_id = self.getPartnerBase(
                        cr, uid, TaxRappresentative.DatiAnagrafici,
                        context=ctx)
                    invoice_model.write(
                        cr, uid, invoice_id,
                        {
                            'tax_representative_id': tax_partner_id
                        }, context=ctx
                    )
                if Intermediary:
                    Intermediary_id = self.getPartnerBase(
                        cr, uid, Intermediary.DatiAnagrafici, context=ctx)
                    invoice_model.write(
                        cr, uid, invoice_id,
                        {
                            'intermediary': Intermediary_id
                        }, context=ctx
                    )
                new_invoices.append(invoice_id)
                invoice = invoice_model.browse(cr, uid, invoice_id, ctx)
                self.check_invoice_amount(
                    cr, uid, invoice,
                    fattura,
                    context=ctx)

            if ctx.get('inconsistencies'):
                invoice.write(
                    {'inconsistencies': ctx['inconsistencies']},
                    context=ctx)

        return {
            'view_type': 'form',
            'name': "PA Supplier Invoices",
            'view_mode': 'tree,form',
            'res_model': 'account.invoice',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', new_invoices)],
            'context': context
        }

    def set_StabileOrganizzazione(self, cr, uid, CedentePrestatore, invoice):
        vals = {}
        if CedentePrestatore.StabileOrganizzazione:
            vals['efatt_stabile_organizzazione_indirizzo'] = (
                CedentePrestatore.StabileOrganizzazione.Indirizzo)
            vals['efatt_stabile_organizzazione_civico'] = (
                CedentePrestatore.StabileOrganizzazione.NumeroCivico)
            vals['efatt_stabile_organizzazione_cap'] = (
                CedentePrestatore.StabileOrganizzazione.CAP)
            vals['efatt_stabile_organizzazione_comune'] = (
                CedentePrestatore.StabileOrganizzazione.Comune)
            vals['efatt_stabile_organizzazione_provincia'] = (
                CedentePrestatore.StabileOrganizzazione.Provincia)
            vals['efatt_stabile_organizzazione_nazione'] = (
                CedentePrestatore.StabileOrganizzazione.Nazione)
            self.pool.get('account.invoice').write(cr, uid, invoice, vals)

    def get_invoice_obj(self, cr, uid, fatturapa_attachment):
        xml_string = self.pool.get('ir.attachment').get_xml_string(
            cr, uid, fatturapa_attachment.ir_attachment_id.id)
        for num in range(1, 24):
            to_replace = '+0%s:00' % (num)
            xml_string = xml_string.replace(to_replace, '')
        return fatturapa.CreateFromDocument(xml_string)
