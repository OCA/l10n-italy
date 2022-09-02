import setuptools

setuptools.setup(
    setup_requires=['setuptools-odoo'],
    odoo_addon={
        'external_dependencies_override': {
            'python': {
                # required for XsdEnumerationFacets.get_annotation()
                'xmlschema': 'xmlschema>=1.7.0',
            },
        },
    },
)
