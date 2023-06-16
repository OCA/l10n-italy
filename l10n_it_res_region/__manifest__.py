# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Contacts Italian Regions',
    'author': 'Nextev Srl,'
    'Odoo Community Association (OCA)',
    'version': '12.0.1.0.0',
    'category': 'Tools',
    'summary': 'Customers, Vendors, Partners Regions',
    'description': """
This module adds italian region field to contacts and
it imports them with Geonames procedure
""",
    'website': 'https://github.com/OCA/l10n-italy',
    'license': 'AGPL-3',
    'depends': [
        'base_location',
        'base_location_geonames_import'
    ],
    'data': [
        'data/res.it.region.csv',
        'security/ir.model.access.csv',
        'views/res_it_region_views.xml',
        'views/base_location_region_views.xml',
    ],
}
