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
        'odoo11-addon-l10n_it_codici_carica',
        'odoo11-addon-l10n_it_esigibilita_iva',
        'odoo11-addon-l10n_it_fiscal_document_type',
        'odoo11-addon-l10n_it_fiscalcode',
        'odoo11-addon-l10n_it_pec',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
