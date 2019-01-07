import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-l10n-italy",
    description="Meta package for oca-l10n-italy Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-l10n_it_abicab',
        'odoo11-addon-l10n_it_account',
        'odoo11-addon-l10n_it_account_tax_kind',
        'odoo11-addon-l10n_it_causali_pagamento',
        'odoo11-addon-l10n_it_codici_carica',
        'odoo11-addon-l10n_it_corrispettivi',
        'odoo11-addon-l10n_it_corrispettivi_sale',
        'odoo11-addon-l10n_it_ddt',
        'odoo11-addon-l10n_it_ddt_delivery',
        'odoo11-addon-l10n_it_esigibilita_iva',
        'odoo11-addon-l10n_it_fatturapa',
        'odoo11-addon-l10n_it_fatturapa_out',
        'odoo11-addon-l10n_it_fiscal_document_type',
        'odoo11-addon-l10n_it_fiscal_payment_term',
        'odoo11-addon-l10n_it_fiscalcode',
        'odoo11-addon-l10n_it_ipa',
        'odoo11-addon-l10n_it_pec',
        'odoo11-addon-l10n_it_rea',
        'odoo11-addon-l10n_it_split_payment',
        'odoo11-addon-l10n_it_website_sale_corrispettivi',
        'odoo11-addon-l10n_it_withholding_tax',
        'odoo11-addon-l10n_it_withholding_tax_causali',
        'odoo11-addon-l10n_it_withholding_tax_payment',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
