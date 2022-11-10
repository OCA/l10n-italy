import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-l10n-italy",
    description="Meta package for oca-l10n-italy Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-l10n_it_ipa>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_rea>=16.0dev,<16.1dev',
        'odoo-addon-l10n_it_vat_payability>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
