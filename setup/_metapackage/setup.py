import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-oca-l10n-italy",
    description="Meta package for oca-l10n-italy Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-account_invoice_entry_date',
        'odoo8-addon-account_invoice_sequential_dates',
        'odoo8-addon-account_vat_period_end_statement',
        'odoo8-addon-l10n_it_abicab',
        'odoo8-addon-l10n_it_account',
        'odoo8-addon-l10n_it_account_tax_kind',
        'odoo8-addon-l10n_it_ateco',
        'odoo8-addon-l10n_it_base',
        'odoo8-addon-l10n_it_base_location_geonames_import',
        'odoo8-addon-l10n_it_central_journal',
        'odoo8-addon-l10n_it_codici_carica',
        'odoo8-addon-l10n_it_corrispettivi',
        'odoo8-addon-l10n_it_ddt',
        'odoo8-addon-l10n_it_ddt_delivery',
        'odoo8-addon-l10n_it_esigibilita_iva',
        'odoo8-addon-l10n_it_fatturapa',
        'odoo8-addon-l10n_it_fatturapa_out',
        'odoo8-addon-l10n_it_fiscal_document_type',
        'odoo8-addon-l10n_it_fiscalcode',
        'odoo8-addon-l10n_it_ipa',
        'odoo8-addon-l10n_it_pec',
        'odoo8-addon-l10n_it_rea',
        'odoo8-addon-l10n_it_regions',
        'odoo8-addon-l10n_it_reverse_charge',
        'odoo8-addon-l10n_it_ricevute_bancarie',
        'odoo8-addon-l10n_it_sepa_bonifici',
        'odoo8-addon-l10n_it_split_payment',
        'odoo8-addon-l10n_it_vat_registries',
        'odoo8-addon-l10n_it_withholding_tax',
        'odoo8-addon-l10n_it_withholding_tax_payment',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
