import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-l10n-italy",
    description="Meta package for oca-l10n-italy Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-l10n_it_abicab',
        'odoo14-addon-l10n_it_fiscal_payment_term',
        'odoo14-addon-l10n_it_fiscalcode',
        'odoo14-addon-l10n_it_ipa',
        'odoo14-addon-l10n_it_rea',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
