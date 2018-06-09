import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo10-addons-oca-l10n-italy",
    description="Meta package for oca-l10n-italy Odoo addons",
    version=version,
    install_requires=[
        'odoo10-addon-account_invoice_report_ddt_group',
        'odoo10-addon-account_vat_period_end_statement',
        'odoo10-addon-l10n_it_abicab',
        'odoo10-addon-l10n_it_account',
        'odoo10-addon-l10n_it_account_tax_kind',
        'odoo10-addon-l10n_it_ateco',
        'odoo10-addon-l10n_it_base_location_geonames_import',
        'odoo10-addon-l10n_it_central_journal',
        'odoo10-addon-l10n_it_codici_carica',
        'odoo10-addon-l10n_it_corrispettivi',
        'odoo10-addon-l10n_it_corrispettivi_sale',
        'odoo10-addon-l10n_it_ddt',
        'odoo10-addon-l10n_it_esigibilita_iva',
        'odoo10-addon-l10n_it_fatturapa',
        'odoo10-addon-l10n_it_fatturapa_out',
        'odoo10-addon-l10n_it_fiscal_document_type',
        'odoo10-addon-l10n_it_fiscalcode',
        'odoo10-addon-l10n_it_fiscalcode_invoice',
        'odoo10-addon-l10n_it_ipa',
        'odoo10-addon-l10n_it_pec',
        'odoo10-addon-l10n_it_rea',
        'odoo10-addon-l10n_it_reverse_charge',
        'odoo10-addon-l10n_it_riba_commission',
        'odoo10-addon-l10n_it_ricevute_bancarie',
        'odoo10-addon-l10n_it_split_payment',
        'odoo10-addon-l10n_it_vat_registries',
        'odoo10-addon-l10n_it_vat_registries_cash_basis',
        'odoo10-addon-l10n_it_website_sale_corrispettivi',
        'odoo10-addon-l10n_it_website_sale_fiscalcode',
        'odoo10-addon-l10n_it_withholding_tax',
        'odoo10-addon-l10n_it_withholding_tax_payment',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
