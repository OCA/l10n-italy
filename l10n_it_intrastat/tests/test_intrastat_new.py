"""
Tests are based on test environment created by module mk_test_env in repository
https://github.com/zeroincombenze/zerobug-test

Each model is declared by a dictionary which name should be "TEST_model",
where model is the upercase model name with dot replaced by '_'
i.e.: res_partner -> TEST_RES_PARTNER

Every record is declared in the model dictionary by a key which is the external
reference used to retrieve the record.
i.e.:
TEST_RES_PARTNER = {
    'z0bug.partner1': {
        'name': 'Alpha',
        'street': '1, First Avenue',
        ...
    }
}

The magic dictionary TEST_SETUP contains data to load at test setup.
TEST_SETUP = {
    'res.partner': TEST_RES_PARTNER,
    ...
}

In setup() function, the following code
    self.setup_records(lang='it_IT')
creates all record declared by above data; lang is an optional parameter.

Final notes:
* Many2one value must be declared as external identifier
* Written on 2022-03-04 16:31:00.321632 by mk_test_env 12.0.0.7.2
"""
import logging
from odoo.tests import common

_logger = logging.getLogger(__name__)

# Record data for base models
TEST_ACCOUNT_ACCOUNT = {
    'external.3202': {
        'code': '3202',
        'name': 'Ricavi da prestazioni di servizio',
        'user_type_id': 'account.data_account_type_revenue',
        'reconcile': False,
    },
    'external.4105': {
        'code': '4105',
        'name': 'Lavorazioni esterne',
        'user_type_id': 'account.data_account_type_expenses',
        'reconcile': False,
    },
    'external.3101': {
        'code': '3101',
        'name': 'Merci c/vendita',
        'user_type_id': 'account.data_account_type_revenue',
        'reconcile': False,
    },
    'external.2601': {
        'code': '2601',
        'name': 'IVA n/debito',
        'user_type_id': 'account.data_account_type_current_liabilities',
        'reconcile': False,
    },
    'external.1601': {
        'code': '1601',
        'name': 'IVA n/credito',
        'user_type_id': 'account.data_account_type_current_assets',
        'reconcile': False,
    },
    'external.3112': {
        'code': '3112',
        'name': 'Ricavi da merci e servizi',
        'user_type_id': 'account.data_account_type_revenue',
        'reconcile': False,
    },
    'external.4102': {
        'code': '4102',
        'name': 'Acq. Materie prime',
        'user_type_id': 'account.data_account_type_direct_costs',
        'reconcile': False,
    },
    'external.4101': {
        'code': '4101',
        'name': 'Acq. Merce',
        'user_type_id': 'account.data_account_type_direct_costs',
        'reconcile': False,
    },
}
TEST_ACCOUNT_FISCAL_POSITION = {
    'z0bug.fiscalpos_eu': {
        'name': 'Regime Intra comunitario',
        'intrastat': True,
        'rc_type': 'local',
    },
}
TEST_ACCOUNT_JOURNAL = {
    'external.INV': {
        'name': 'Fatture di vendita',
        'code': 'INV',
        'type': 'sale',
        'update_posted': True,
    },
    'external.BILL': {
        'name': 'Fatture di acquisto',
        'code': 'BILL',
        'type': 'purchase',
        'update_posted': True,
    },
}
TEST_ACCOUNT_PAYMENT_TERM = {
    'z0bug.payment_5': {
        'name': 'BB 45GG',
        'fatturapa_pt_id': 'l10n_it_fiscal_payment_term.fatturapa_tp02',
        'fatturapa_pm_id': 'l10n_it_fiscal_payment_term.fatturapa_mp05',
    },
}
TEST_ACCOUNT_TAX = {
    'by': 'description',
    'external.00art15v': {
        'description': '00art15v',
        'name': 'Vend.escluso art.15 DPR633',
        'amount': 0,
        'amount_type': 'percent',
        'type_tax_use': 'sale',
        'price_include': True,
        'kind_id': 'l10n_it_account_tax_kind.n1',
    },
    'external.00art15a': {
        'description': '00art15a',
        'name': 'Acq.escluso art.15 DPR633',
        'amount': 0,
        'amount_type': 'percent',
        'type_tax_use': 'purchase',
        'price_include': True,
        'kind_id': 'l10n_it_account_tax_kind.n1',
    },
    'z0bug.tax_a41v': {
        'description': 'a41v',
        'name': 'Vend.N.I. art.41 L.427/93',
        'amount': 0,
        'amount_type': 'percent',
        'type_tax_use': 'sale',
        'price_include': True,
        'kind_id': 'l10n_it_account_tax_kind.n3_2',
    },
    'external.22v': {
        'description': '22v',
        'name': 'IVA 22% su vendite',
        'amount': 22,
        'amount_type': 'percent',
        'type_tax_use': 'sale',
        'price_include': True,
        'account_id': 'external.2601',
        'refund_account_id': 'external.2601',
    },
    'external.22a': {
        'description': '22a',
        'name': 'IVA 22% da acquisti',
        'amount': 22,
        'amount_type': 'percent',
        'type_tax_use': 'purchase',
        'price_include': True,
        'account_id': 'external.1601',
        'refund_account_id': 'external.1601',
    },
    'z0bug.tax_a41a': {
        'description': 'a41a',
        'name': 'Acq.N.I. art.41 L.427/93',
        'amount': 0,
        'amount_type': 'percent',
        'type_tax_use': 'purchase',
        'price_include': True,
        'kind_id': 'l10n_it_account_tax_kind.n3_2',
        'rc_type': 'local',
        'rc_sale_tax_id': 'z0bug.tax_aa41v',
    },
}
TEST_PRODUCT_TEMPLATE = {
    'by': 'default_code',
    'z0bug.product_template_23': {
        'default_code': 'WW',
        'name': 'Special Worldwide service',
        'lst_price': 1.88,
        'standard_price': 0,
        'type': 'service',
        'taxes_id': 'external.00art15v',
        'supplier_taxes_id': 'external.00art15a',
        'property_account_income_id': 'external.3202',
        'property_account_expense_id': 'external.4105',
        'uom_id': 'product.product_uom_unit',
        'uom_po_id': 'product.product_uom_unit',
        'intrastat_type': 'service',
        'intrastat_code_id': 'external.582929',
    },
    'z0bug.product_template_26': {
        'default_code': 'ZZ',
        'name': 'Prodotto Zeta',
        'lst_price': 1.44,
        'standard_price': 0.72,
        'type': 'consu',
        'taxes_id': 'external.22v',
        'supplier_taxes_id': 'external.22a',
        'property_account_income_id': 'external.3112',
        'property_account_expense_id': 'external.4102',
        'uom_id': 'product.product_uom_unit',
        'uom_po_id': 'product.product_uom_unit',
        'weight': 0.35,
        'intrastat_type': 'good',
        'intrastat_code_id': 'external.84439910',
    },
}
TEST_RES_BANK = {
    'z0bug.bank_bct': {
        'name': 'Banca di Credito a Tutti',
        'bic': 'CRTTITMM',
        'country': 'base.it',
    },
}
TEST_RES_PARTNER = {
    'z0bug.res_partner_13': {
        'name': 'Axilor GmbH',
        'street': 'Christophstraße 13',
        'country_id': 'base.de',
        'zip': '55113',
        'city': 'Määnz',
        'customer': True,
        'supplier': True,
        'is_company': True,
        'vat': 'DE812526315',
        'property_account_position_id': 'z0bug.fiscalpos_eu',
        'property_payment_term_id': 'z0bug.payment_5',
        'lang': 'en_US',
    },
    'base.main_partner': {
        'name': 'Test Company',
        'street': 'Via dei Matti, 0',
        'country_id': 'base.it',
        'zip': '20080',
        'city': 'Ozzero',
        'state_id': 'base.state_it_mi',
        'customer': True,
        'supplier': True,
        'is_company': True,
        'email': 'info@testcompany.org',
        'phone': '+39 025551234',
        'vat': 'IT05111810015',
        'website': 'https://www.testcompany.org',
        'lang': 'it_IT',
    },
    'z0bug.res_partner_12': {
        'name': 'Freie Universität Berlin',
        'street': 'Kaiserswerther Straße 12-24',
        'country_id': 'base.de',
        'zip': '14195',
        'city': 'Berlin',
        'customer': True,
        'supplier': True,
        'is_company': True,
        'vat': 'DE123456788',
        'property_account_position_id': 'z0bug.fiscalpos_eu',
        'property_supplier_payment_term_id': 'z0bug.payment_5',
        'lang': 'en_US',
    },
}
TEST_RES_PARTNER_BANK = {
    'z0bug.bank_company_2': {
        'acc_number': 'IT74B0246801011000000024680',
        'partner_id': 'base.main_partner',
        'acc_type': 'iban',
        'bank_id': 'z0bug.bank_bct',
    },
    'z0bug.bank_partner_13': {
        'acc_number': 'DE64500105177324151368',
        'partner_id': 'z0bug.res_partner_13',
        'acc_type': 'iban',
    },
}
TEST_SETUP = {
    'account.account': TEST_ACCOUNT_ACCOUNT,
    'account.fiscal.position': TEST_ACCOUNT_FISCAL_POSITION,
    'account.journal': TEST_ACCOUNT_JOURNAL,
    'account.payment.term': TEST_ACCOUNT_PAYMENT_TERM,
    'account.tax': TEST_ACCOUNT_TAX,
    'product.template': TEST_PRODUCT_TEMPLATE,
    'res.bank': TEST_RES_BANK,
    'res.partner': TEST_RES_PARTNER,
    'res.partner.bank': TEST_RES_PARTNER_BANK,
}

# Record data for child models
TEST_ACCOUNT_INVOICE_LINE = {
    'z0bug.invoice_Z0_4_1': {
        'invoice_id': 'z0bug.invoice_Z0_4',
        'product_id': 'z0bug.product_product_23',
        'name': 'Servizi ad alto valore aggiunto',
        'quantity': 250,
        'account_id': 'external.3101',
        'price_unit': 1,
        'invoice_line_tax_ids': 'z0bug.tax_a41v',
    },
    'z0bug.invoice_Z0_4_2': {
        'invoice_id': 'z0bug.invoice_Z0_4',
        'product_id': 'z0bug.product_product_26',
        'name': 'Prodotto Zeta (versione EU)',
        'quantity': 100,
        'account_id': 'external.3101',
        'price_unit': 1.5,
        'invoice_line_tax_ids': 'z0bug.tax_a41v',
    },
    'z0bug.invoice_ZI_9_1': {
        'invoice_id': 'z0bug.invoice_ZI_9',
        'product_id': 'z0bug.product_product_23',
        'name': 'Servizi ad alto valore aggiunto',
        'quantity': 150,
        'account_id': 'external.4101',
        'price_unit': 0.89,
        'invoice_line_tax_ids': 'z0bug.tax_a41a',
        'rc': True,
    },
    'z0bug.invoice_ZI_9_2': {
        'invoice_id': 'z0bug.invoice_ZI_9',
        'product_id': 'z0bug.product_product_26',
        'name': 'Prodotto Zeta (versione EU)',
        'quantity': 200,
        'account_id': 'external.4101',
        'price_unit': 1.05,
        'invoice_line_tax_ids': 'z0bug.tax_a41a',
        'rc': True,
    },
}

# Record data for models to test
TEST_ACCOUNT_INVOICE = {
    'z0bug.invoice_Z0_4': {
        'partner_id': 'z0bug.res_partner_13',
        'origin': 'IT/21/002',
        'reference': 'IT/21/002',
        'date_invoice': '2022-02-28',
        'type': 'out_invoice',
        'journal_id': 'external.INV',
        'fiscal_position_id': 'z0bug.fiscalpos_eu',
        'currency_id': 'base.EUR',
        'partner_bank_id': 'z0bug.bank_company_2',
        'payment_term_id': 'z0bug.payment_5',
        'company_bank_id': 'z0bug.bank_company_2',
        'counterparty_bank_id': 'z0bug.bank_partner_13',
        'intrastat': True,
    },
    'z0bug.invoice_ZI_9': {
        'partner_id': 'z0bug.res_partner_12',
        'origin': 'Order 12',
        'reference': 'DE/22/9876',
        'date_invoice': '2022-02-28',
        'date': '2022-02-28',
        'type': 'in_invoice',
        'journal_id': 'external.BILL',
        'fiscal_position_id': 'z0bug.fiscalpos_eu',
        'currency_id': 'base.EUR',
        'intrastat': True,
    },
}

TNL_RECORDS = {
    'product.product': {
        # 'type': ['product', 'consu'],
    },
    'product.template': {
        # 'type': ['product', 'consu'],
    },
}

# Test Result
# Items are invoice lines: key is (invoice_id, statement_section)
TRES_INVOICE = {
    '%s~%s' % ('z0bug.invoice_Z0_4', 'sale_s1'): {
        'intrastat_code': '84439910',
    },
    '%s~%s' % ('z0bug.invoice_Z0_4', 'sale_s3'): {
        'intrastat_code': '582929',
    },
    '%s~%s' % ('z0bug.invoice_ZI_9', 'purchase_s1'): {
        'intrastat_code': '84439910',
    },
    '%s~%s' % ('z0bug.invoice_ZI_9', 'purchase_s3'): {
        'intrastat_code': '582929',
    },
}
# Item are invoice intrastat lines: key is (invoice_id, statement_section)
TRES_INTRASTAT = {
    '%s~%s' % ('z0bug.invoice_Z0_4', 'sale_s1'): {
        'intrastat_code': '84439910',
        'amount_currency': 150.0,
    },
    '%s~%s' % ('z0bug.invoice_Z0_4', 'sale_s3'): {
        'intrastat_code': '582929',
        'amount_currency': 250.0,
    },
    '%s~%s' % ('z0bug.invoice_ZI_9', 'purchase_s1'): {
        'intrastat_code': '84439910',
        'amount_currency': 210.0,
    },
    '%s~%s' % ('z0bug.invoice_ZI_9', 'purchase_s3'): {
        'intrastat_code': '582929',
        'amount_currency': 133.5,
    },
}


class TestAccountMove(common.TransactionCase):

    # --------------------------------------- #
    # Common code: may be share among modules #
    # --------------------------------------- #

    def simulate_xref(self, xref, raise_if_not_found=None,
                      model=None, by=None, company=None, case=None):
        """Simulate External Reference
        This function simulates self.env.ref() searching for model record.
        Ordinary xref is formatted as "MODULE.NAME"; when MODULE = "external"
        this function is called.
        Record is searched by <by> parameter, default is 'code' or 'name';
        id NAME is formatted as "FIELD=VALUE", FIELD value is assigned to <by>
        If company is supplied, it is added in search domain;

        Args:
            xref (str): external reference
            raise_if_not_found (bool): raise exception if xref not found or
                                       if more records found
            model (str): external reference model
            by (str): default field to search object record,
            company (obj): default company
            case: apply for uppercase or lowercase

        Returns:
            obj: the model record
        """
        if model not in self.env:
            if raise_if_not_found:
                raise ValueError('Model %s not found in the system' % model)
            return False
        _fields = self.env[model].fields_get()
        if not by:
            if model in self.by:
                by = self.by[model]
            else:
                by = 'code' if 'code' in _fields else 'name'
        module, name = xref.split('.', 1)
        if '=' in name:
            by, name = name.split('=', 1)
        if case == 'upper':
            name = name.upper()
        elif case == 'lower':
            name = name.lower()
        domain = [(by, '=', name)]
        if (model not in ('product.product',
                          'product.template',
                          'res.partner',
                          'res.users') and
                company and 'company_id' in _fields):
            domain.append(('company_id', '=', company.id))
        objs = self.env[model].search(domain)
        if len(objs) == 1:
            return objs[0]
        if raise_if_not_found:
            raise ValueError('External ID not found in the system: %s' % xref)
        return False

    def env_ref(self, xref, raise_if_not_found=None,
                model=None, by=None, company=None, case=None):
        """Get External Reference
        This function is like self.env.ref(); if xref does not exist and
        xref prefix is 'external.', engage simulate_xref

        Args:
            xref (str): external reference, format is "module.name"
            raise_if_not_found (bool): raise exception if xref not found
            model (str): external ref. model; required for "external." prefix
            by (str): field to search for object record (def 'code' or 'name')
            company (obj): default company

        Returns:
            obj: the model record
        """
        if xref is False or xref is None:
            return xref
        obj = self.env.ref(xref, raise_if_not_found=raise_if_not_found)
        if not obj:
            module, name = xref.split('.', 1)
            if module == 'external':
                return self.simulate_xref(xref,
                                          model=model,
                                          by=by,
                                          company=company,
                                          case=case)
        return obj

    def add_xref(self, xref, model, xid):
        """Add external reference that will be used in next tests.
        If xref exist, result ID will be upgraded"""
        module, name = xref.split('.', 1)
        if module == 'external':
            return False
        ir_model = self.env['ir.model.data']
        vals = {
            'module': module,
            'name': name,
            'model': model,
            'res_id': xid,
        }
        xrefs = ir_model.search([('module', '=', module),
                                 ('name', '=', name)])
        if not xrefs:
            return ir_model.create(vals)
        xrefs[0].write(vals)
        return xrefs[0]

    def get_values(self, model, values, by=None, company=None, case=None):
        """Load data values and set them in a dictionary for create function
        * Not existent fields are ignored
        * Many2one field are filled with current record ID
        """
        _fields = self.env[model].fields_get()
        vals = {}
        if model in TNL_RECORDS:
            for item in TNL_RECORDS[model].keys():
                if item in values:
                    (old, new) = TNL_RECORDS[model][item]
                    if values[item] == old:
                        values[item] = new
        for item in values.keys():
            if item not in _fields:
                continue
            if item == 'company_id' and not values[item]:
                vals[item] = company.id
            elif _fields[item]['type'] == 'many2one':
                res = self.env_ref(
                    values[item],
                    model=_fields[item]['relation'],
                    by=by,
                    company=company,
                    case=case,
                )
                if res:
                    vals[item] = res.id
            elif (_fields[item]['type'] == 'many2many' and
                  '.' in values[item] and
                  ' ' not in values[item]):
                res = self.env_ref(
                    values[item],
                    model=_fields[item]['relation'],
                    by=by,
                    company=company,
                    case=case,
                )
                if res:
                    vals[item] = [(6, 0, [res.id])]
            elif values[item] is not None:
                vals[item] = values[item]
        return vals

    def model_create(self, model, values, xref=None):
        """Create a test record and set external ID to next tests"""
        res = self.env[model].create(values)
        if xref and ' ' not in xref:
            self.add_xref(xref, model, res.id)
        return res

    def model_browse(self, model, xid, company=None, by=None,
                     raise_if_not_found=True):
        """Browse a record by external ID"""
        res = self.env_ref(
            xid,
            model=model,
            company=company,
            by=by,
        )
        if res:
            return res
        return self.env[model]

    def model_make(self, model, values, xref, company=None, by=None):
        """Create or write a test record and set external ID to next tests"""
        res = self.model_browse(model,
                                xref,
                                company=company,
                                by=by,
                                raise_if_not_found=False)
        if res:
            res.write(values)
            return res
        return self.model_create(model, values, xref=xref)

    def default_company(self):
        return self.env.user.company_id

    def set_locale(self, locale_name, raise_if_not_found=True):
        modules_model = self.env['ir.module.module']
        modules = modules_model.search([('name', '=', locale_name)])
        if modules and modules[0].state != 'uninstalled':
            modules = []
        if modules:
            modules.button_immediate_install()
            self.env['account.chart.template'].try_loading_for_current_company(
                locale_name
            )
        else:
            if raise_if_not_found:
                raise ValueError(
                    'Module %s not found in the system' % locale_name)

    def install_language(self, iso, overwrite=None, force_translation=None):
        iso = iso or 'en_US'
        overwrite = overwrite or False
        load = False
        lang_model = self.env['res.lang']
        languages = lang_model.search([('code', '=', iso)])
        if not languages:
            languages = lang_model.search([('code', '=', iso),
                                           ('active', '=', False)])
            if languages:
                languages.write({'active': True})
                load = True
        if not languages or load:
            vals = {
                'lang': iso,
                'overwrite': overwrite,
            }
            self.env['base.language.install'].create(vals).lang_install()
        if force_translation:
            vals = {'lang': iso}
            self.env['base.update.translations'].create(vals).act_update()

    def setup_records(
        self, lang=None, locale=None, company=None, save_as_demo=None
    ):
        """Create all record from declared data. See above doc

        Args:
            lang (str): install & load specific language
            locale (str): install locale module with CoA; i.e l10n_it
            company (obj): declare default company for tests
            save_as_demo (bool): commit all test data as they are demo data
            Warning: usa save_as_demo carefully; is used in multiple tests,
            like in travis this option can be cause to failue of tests
            This option can be used in local tests with "run_odoo_debug -T"

        Returns:
            None
        """

        def iter_data(model, model_data, company):
            for item in model_data.keys():
                if isinstance(model_data[item], str):
                    continue
                vals = self.get_values(
                    model,
                    model_data[item],
                    company=company)
                res = self.model_make(
                    model, vals, item,
                    company=company,
                    by=by)
                if model == 'product.template':
                    model2 = 'product.product'
                    vals = self.get_values(
                        model2,
                        model_data[item],
                        company=company)
                    vals['product_tmpl_id'] = res.id
                    self.model_make(
                        model2, vals, item.replace('template', 'product'),
                        company=company,
                        by=by)

        self.save_as_demo = save_as_demo or False
        if locale:
            self.set_locale(locale)
        if lang:
            self.install_language('it_IT')
        if not self.env['ir.module.module'].search(
                [('name', '=', 'stock'), ('state', '=', 'installed')]):
            TNL_RECORDS['product.product']['type'] = ['product', 'consu']
            TNL_RECORDS['product.template']['type'] = ['product', 'consu']
        self.by = {}
        for model, model_data in TEST_SETUP.items():
            by = model_data.get('by')
            if by:
                self.by[model] = by
        company = company or self.default_company()
        for model, model_data in TEST_SETUP.items():
            by = model_data.get('by')
            iter_data(model, model_data, company)

    # ------------------ #
    # Specific test code #
    # ------------------ #
    def setUp(self):
        super().setUp()
        self.setup_records(lang='it_IT', save_as_demo=True)

    def tearDown(self):
        super().tearDown()
        if self.save_as_demo:
            self.env.cr.commit()               # pylint: disable=invalid-commit

    def test_intrastat_invoices(self):
        model = 'account.invoice'
        model_child = 'account.invoice.line'
        for xref in TEST_ACCOUNT_INVOICE:
            _logger.info(
                "🎺 Testing %s[%s]" % (model, xref)
            )
            vals = self.get_values(
                model,
                TEST_ACCOUNT_INVOICE[xref])
            inv = self.model_make(model, vals, xref)

            for xref_child in TEST_ACCOUNT_INVOICE_LINE.values():
                if xref_child['invoice_id'] == xref:
                    vals = self.get_values(model_child, xref_child)
                    vals['invoice_id'] = inv.id
                    self.model_make(model_child, vals, False)
            inv.compute_taxes()
            inv.action_invoice_open()
            # Enable follow statement if fiscal position is not intrastat
            # inv.compute_intrastat_lines()

            self.assertEqual(
                inv.intrastat, True,
                msg='Flag intrastat not set!')

        # There are 4 invoice lines with intrastat:
        # sale-product / sale-service / purchase-product / purchase-service
        invoice_checked = {}
        for hash_code, test_intra in TRES_INVOICE.items():
            (invoice_id, statement_section) = hash_code.split('~', 1)
            if invoice_id not in invoice_checked:
                invoice_checked[invoice_id] = 0
            # intrastat = TRES_INTRASTAT[hash]
            invoice = self.env_ref(invoice_id)
            for line in invoice.invoice_line_ids:
                intrastat_code = line.product_id.intrastat_code_id.name
                if intrastat_code != test_intra['intrastat_code']:
                    continue
                # Count line checked
                invoice_checked[invoice_id] += 1
                if line.product_id.type == 'service':
                    section = '%s_s3' % invoice.journal_id.type
                else:
                    section = '%s_s1' % invoice.journal_id.type
                self.assertEqual(
                    section, statement_section,
                    msg='Wrong intrastat section!'
                )
        for invoice, ctr in invoice_checked.items():
            self.assertEqual(
                ctr, 2,
                msg='Not all invoice lines has been checked!'
            )
        # Now check for intrastat lines
        for hash_code, test_intra in TRES_INTRASTAT.items():
            (invoice_id, statement_section) = hash_code.split('~', 1)
            invoice = self.env_ref(invoice_id)
            intrastat_code = self.env['report.intrastat.code'].search(
                [('name', '=', test_intra['intrastat_code'])]
            )
            intrastat = self.env['account.invoice.intrastat'].search(
                [('invoice_id', '=', invoice.id),
                 ('intrastat_code_id', '=', intrastat_code.id)])
            self.assertEqual(
                intrastat.amount_currency,
                test_intra['amount_currency'],
                msg='Wrong intrastat currency_amount!'
            )
