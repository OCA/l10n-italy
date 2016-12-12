# -*- coding: utf-8 -*-
# Copyright 2014 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2016 Andrea Gallina (Apulia Software)
# Copyright 2016 Giuliano Lotta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Italian Localisation - Fiscal Code',
    'version': '10.0.2.0.0',
    'category': 'Localisation/Italy',
    'author': "Odoo Italia Network, Odoo Community Association (OCA)",
    'website': 'https://odoo-community.org/',
    'license': 'AGPL-3',
    'depends': ['base_vat'],
    'external_dependencies': {
        'python': ['codicefiscale', 'stdnum'], },
    'data': [
        'view/fiscalcode_view.xml',
        'view/res_company_view.xml',
        'wizard/compute_fc_view.xml',
        'data/res.city.it.code.csv',
        "security/ir.model.access.csv"
        ],
    'installable': True
}
