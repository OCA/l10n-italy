# -*- coding: utf-8 -*-
# Copyright 2015 AgileBG SAGL <http://www.agilebg.com>
# Copyright 2015 innoviu Srl <http://www.innoviu.com>
# Copyright 2018 Lorenzo Battistini

{
    'name': 'Italian Localization - Fattura Elettronica reception',
    'version': '10.0.1.0.0',
    'category': 'Localization/Italy',
    'summary': 'Electronic invoices reception',
    'author': 'Agile Business Group, Innoviu, '
              'Odoo Community Association (OCA)',
    'website': 'http://www.agilebg.com',
    'license': 'LGPL-3',
    "depends": [
        'l10n_it_fatturapa',
        'l10n_it_withholding_tax_causali',
        ],
    "data": [
        'views/account_view.xml',
        'views/partner_view.xml',
        'wizard/wizard_import_fatturapa_view.xml',
        'security/ir.model.access.csv',
        'wizard/link_to_existing_invoice.xml',
        'views/company_view.xml',
    ],
    "installable": True
}
