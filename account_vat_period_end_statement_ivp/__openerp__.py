# -*- coding: utf-8 -*-
#    Copyright (C) 2011-12 Domsense s.r.l. <http://www.domsense.com>.
#    Copyright (C) 2012-15 Agile Business Group sagl <http://www.agilebg.com>
#    Copyright (C) 2012-15 LinkIt Spa <http://http://www.linkgroup.it>
#    Copyright (C) 2015-17 Associazione Odoo Italia
#                          <http://www.odoo-italia.org>
#    Copyright (C) 2017    SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# [2011: domsense] First version
# [2012: agilebg] Various enhancements
# [2013: openerp-italia] Various enhancements
# [2017: odoo-italia] Electronic VAT statement
{
    'name': 'IVP 2017',
    'version': '8.0.1.1.0',
    'category': 'other',
    'author': "Agile Business Group, Odoo Italia Associazione,"
              " Odoo Community Association (OCA), Sergio Corato",
    'description': 'IVP 2017 export xml file',
    'website': 'https://efatto.it',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'account',
        'account_vat_period_end_statement',
        'l10n_it_vat_registries',
        'l10n_it_fiscalcode',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_view.xml',
        'wizard/vat_settlement.xml',
    ],
    'external_dependencies': {
        'python': ['pyxb'],
    },
    'installable': True
}
