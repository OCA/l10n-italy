# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013-2017 Agile Business Group sagl (http://www.agilebg.com)
#    @author Alex Comba <alex.comba@agilebg.com>
#    @author Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#    Copyright (C) 2017 CQ Creativi Quadrati (http://www.creativiquadrati.it)
#    @author Diego Bruselli <d.bruselli@creativiquadrati.it>
#    Copyright (C) 2013
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################

{
    'name': 'Italian Localisation - Bill of Entry',
    'version': '10.0.1.0.0',
    'category': 'Localization/Italy',
    'summary': 'Bolle Doganali',
    'author': "Odoo Community Association (OCA), "
              "Agile Business Group, CQ Creativi Quadrati",
    'website': "https://odoo-community.org/",
    'license': 'AGPL-3',
    # account dependency should be replaced with account_invoice_template
    # when this PR will be merged:
    # https://github.com/OCA/account-invoicing/pull/250
    'depends': [
        'base',
        'account',
        # 'account_invoice_template',
    ],
    'data': [
        'views/company_view.xml',
        'views/account_invoice_view.xml',
    ],
    'demo': [
        'demo/bill_of_entry_demo.xml',
    ],
    'installable': True,
}
