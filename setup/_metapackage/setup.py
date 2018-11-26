import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-l10n-italy",
    description="Meta package for oca-l10n-italy Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-l10n_it_abicab',
        'odoo12-addon-l10n_it_account',
        'odoo12-addon-l10n_it_account_tax_kind',
        'odoo12-addon-l10n_it_esigibilita_iva',
        'odoo12-addon-l10n_it_fiscal_document_type',
        'odoo12-addon-l10n_it_fiscal_payment_term',
        'odoo12-addon-l10n_it_fiscalcode',
        'odoo12-addon-l10n_it_ipa',
        'odoo12-addon-l10n_it_rea',
        'odoo12-addon-l10n_it_split_payment',
        'odoo12-addon-l10n_it_withholding_tax',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
