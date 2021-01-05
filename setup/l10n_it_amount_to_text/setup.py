import setuptools

setuptools.setup(
    setup_requires=['setuptools-odoo'],
    odoo_addon={
        'external_dependencies_override': {
            'python': {
                'num2words': 'num2words>=0.5.12',
            },
        },
    },
)
