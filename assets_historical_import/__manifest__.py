# Copyright 2019-TODAY Openforce Srls Unipersonale (www.openforce.it)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    'name': 'Assets Management - Historical Import',
    'version': '12.0.1.1.0',
    'category': 'Accounting',
    'summary': "Assets: import historical data",
    'author': 'Openforce',
    'website': 'www.openforce.it',
    'license': 'LGPL-3',
    'external_dependencies': {
        'python': [
            'xlrd',  # Already in Odoo requirements, but let's be sure
            'xlsxwriter',
        ],
    },
    'depends': [
        'assets_management',
    ],
    'data': [
        'views/asset.xml',
        'views/asset_category.xml',
        'views/asset_depreciation_mode.xml',
        'views/asset_depreciation_type.xml',
        'wizards/asset_historical_import.xml',
    ],
    'installable': True,
    'post_init_hook': 'set_import_codes',
}
