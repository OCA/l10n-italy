#  Copyright 2020 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'ITA - Codice fiscale negli scontrini',
    'version': '12.0.1.1.0',
    'category': 'Point of Sale',
    'summary': 'Consente di includere il codice fiscale negli scontrini',
    'author': 'Agile Business Group, '
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/fiscal_epos_print_fiscalcode',
    'depends': [
        'fiscal_epos_print',
        'l10n_it_pos_fiscalcode',
    ],
    'data': [
        'views/assets.xml',
        'views/res_partner_views.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml'
    ],
}
