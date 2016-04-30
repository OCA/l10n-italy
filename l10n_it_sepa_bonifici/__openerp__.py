# -*- coding: utf-8 -*-
# © 2016 Alessandro Camilli <alessandro.camilli@openforce.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Banking SEPA Italian Credit Transfer CBI',
    'version': '8.0.1.0.0',
    'category': 'Banking',
    'author':
    'Openforce di Alessandro Camilli, Odoo Community Association (OCA)',
    'website': 'http://www.openforce.it',
    'license': 'AGPL-3',
    'depends': [
        'account_banking_pain_base',
    ],
    'data': [
        'wizard/export_sepa_cbi_view.xml',
        'wizard/export_sepa_cbi_estero_view.xml',
        'data/payment_type_sepa_cbi.xml',
    ],
    'installable': True
}
