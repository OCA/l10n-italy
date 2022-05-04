import setuptools

setuptools.setup(
    setup_requires=['setuptools-odoo'],
    odoo_addon={
        'external_dependencies_override': {
            'python': {
                'pyxb': 'PyXB==1.2.6',
                'unidecode': 'Unidecode<1.3.0',
            },
        },
    },
)
