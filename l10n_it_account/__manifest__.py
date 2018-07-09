# Copyright 2015 Abstract srl (<http://www.abstract.it>)
# Copyright 2015-2017 Agile Business Group (<http://www.agilebg.com>)
# Copyright 2015 Link It Spa (<http://www.linkgroup.it/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Italian Localization - Account',
    'version': '11.0.1.0.0',
    'category': 'Hidden',
    'author': "Agile Business Group,Abstract,Odoo Community Association (OCA)",
    'website': 'http://www.odoo-italia.net',
    'license': 'AGPL-3',
    "depends": [
        'account',
        'date_range',
        'web',
    ],
    "data": [
        'views/account_setting.xml',
        'views/account_view.xml',
        'reports/account_reports_view.xml',
    ],
    'installable': True,
}
