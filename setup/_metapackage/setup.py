import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo9-addons-oca-l10n-italy",
    description="Meta package for oca-l10n-italy Odoo addons",
    version=version,
    install_requires=[
        'odoo9-addon-l10n_it_abicab',
        'odoo9-addon-l10n_it_base_location_geonames_import',
        'odoo9-addon-l10n_it_ddt',
        'odoo9-addon-l10n_it_rea',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
