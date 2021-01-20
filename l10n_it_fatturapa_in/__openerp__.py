# -*- coding: utf-8 -*-
# Copyright 2015 AgileBG SAGL <http://www.agilebg.com>
# Copyright 2015 innoviu Srl <http://www.innoviu.com>
# Copyright 2018-2019 Lorenzo Battistini
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2018 Gianmarco Conte, Marco Calcagni - Dinamiche Aziendali srl
# Copyright 2018-2019 Sergio Corato

{
    'name': 'Italian Localization - Fattura elettronica - Ricezione',
    'version': '8.0.2.0.3',
    'development_status': 'Beta',
    'category': 'Localization/Italy',
    'summary': 'Electronic invoices reception',
    'author': 'Agile Business Group, Innoviu, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy/tree/8.0/'
               'l10n_it_fatturapa_in',
    'license': 'LGPL-3',
    'depends': [
        'l10n_it_fatturapa',
        'l10n_it_withholding_tax_causali',
        ],
    'data': [
        'security/ir.model.access.csv',
        'security/rules.xml',
        'wizard/wizard_import_fatturapa_view.xml',
        'wizard/link_to_existing_invoice.xml',
        'views/account_view.xml',
        'views/partner_view.xml',
        'views/company_view.xml',
    ],
    'installable': True
}
