# Copyright 2014 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Copyright 2020 Francesco Apruzzese <francesco.apruzzese@openforce.it>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Base Location Provinces Import',
    'version': '11.0.1.0.0',
    'category': 'Extra Tools',
    'license': 'AGPL-3',
    'summary': 'Import base_location entries (provinces) from Geonames',
    'description': """
This module extends base_location_geonames_import in order to correctly import
Italian provinces
""",
    'author': "Agile Business Group,Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/l10n-italy/',
    'depends': [
        'base_location_geonames_import',
        ],
    'test': [
        'test/import.yml',
        ],
    'installable': True,
}
