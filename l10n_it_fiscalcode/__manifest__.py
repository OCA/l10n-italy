# Copyright 2014 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2016 Andrea Gallina (Apulia Software)
# Copyright © 2018 Matteo Bilotta (Link IT s.r.l.)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# noinspection PyStatementEffect
{
    'name': 'Italian Localisation - Fiscal Code',
    'version': '11.0.1.1.0',
    'category': 'Localisation/Italy',
    'author': "Link IT s.r.l., "
              "Apulia Software, "
              "Odoo Italia Network, "
              "Odoo Community Association (OCA)",
    'website': 'https://odoo-community.org/',
    'license': 'AGPL-3',
    'depends': ['base_vat'],
    'external_dependencies': {
        'python': ['codicefiscale'],
    },
    'data': [
        "security/ir.model.access.csv",
        'data/res.city.it.code.csv',
        'view/fiscalcode_view.xml',
        'view/report_invoice_document.xml',
        'wizard/compute_fc_view.xml',
        ],
    'installable': True
}
