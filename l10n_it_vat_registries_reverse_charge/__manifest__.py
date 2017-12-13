# -*- coding: utf-8 -*-
# Copyright 2017 Lara Baggio - Link IT srl
# (<http://www.linkgroup.it/>)
# Copyright 2014-2017 Lorenzo Battistini - Agile Business Group
# (<http://www.agilebg.com>)
# © 2017 Alessandro Camilli - Openforce
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Italian Localization - VAT Registries - Reverse Charge',
    'version': '10.0.1.0.0',
    'category': 'Hidden',
    "author": "LinkIt Srl, Agile Business Group"
              ", Openforce di Camilli Alessandro"
              ", Odoo Community Association (OCA)",
    'website': 'http://www.linkgroup.it/',
    'license': 'LGPL-3',
    "depends": [
        'l10n_it_vat_registries',
        'l10n_it_reverse_charge'],
    "data": [
        'report/report_registro_iva.xml'
    ],
    'installable': True,
    'auto_install': True,
}
