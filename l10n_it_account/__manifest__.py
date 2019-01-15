# Copyright 2015 Abstract srl (<http://www.abstract.it>)
# Copyright 2015-2017 Agile Business Group (<http://www.agilebg.com>)
# Copyright 2015 Link It Spa (<http://www.linkgroup.it/>)
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Italian Localization - Account',
    'version': '11.0.1.2.2',
    'category': 'Hidden',
    'author': "Agile Business Group, Abstract, "
              "Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/l10n-italy/tree/11.0/l10n_it_account',
    'license': 'AGPL-3',
    "depends": [
        'account_fiscal_year',
        'account_tax_balance',
        'web',
    ],
    "data": [
        'views/account_setting.xml',
        'views/account_menuitem.xml',
        'views/partner_view.xml',
        'views/product_view.xml',
        'views/res_config_settings_views.xml',
        'reports/account_reports_view.xml',
    ],
    'installable': True,
}
