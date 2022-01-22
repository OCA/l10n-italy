# Copyright 2013-2016 Camptocamp SA (Yannick Vaucher)
# Copyright 2015-2016 Akretion
# (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2020-2022 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-2022 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-2022 Didotech s.r.l. <https://www.didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Payment Term Extension Plus',
    'version': '12.0.0.1.9',
    'category': 'Accounting & Finance',
    'summary': 'Adds rounding, months, weeks and multiple payment days '
               'properties on payment term lines',
    'author': 'Camptocamp,'
              'Tecnativa,'
              'Agile Business Group, '
              'Odoo Community Association (OCA),'
              'powERP enterprise network',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_payment_method',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard_duedates_simulator.xml',
        'views/account_payment_term.xml',
    ],
    'demo': ['demo/account_demo.xml'],
    'maintainer': 'powERP enterprise network',
    'installable': True,
    'pre_init_hook': 'pre_init_hook',
}