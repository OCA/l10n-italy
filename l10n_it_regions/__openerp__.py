# -*- coding: utf-8 -*-
# Copyright 2016 Davide Corio - Abstract srl
# Copyright 2017 Andrea Cometa - Apulia Software srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Italian Regions Import',
    'version': '8.0.1.0.1',
    'category': 'Extra Tools',
    'license': 'AGPL-3',
    'summary': 'Import Italian regions from Geonames',
    'author': "Odoo Community Association (OCA)",
    'website': 'http://odoo-community.org',
    'depends': [
        'base',
        'base_location_geonames_import',
        'l10n_it_base_location_geonames_import'],
    'data': [
        'security/ir.model.access.csv',
        'views/partner_view.xml',
        'views/region_view.xml'],
    'installable': True,
}
