#    Copyright (C) 2017 Apulia Software s.r.l. (http://www.apuliasoftware.it)
#    @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
#
#    License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Italian Localisation - Natura delle aliquote IVA',
    'version': '11.0.1.0.1',
    'category': 'Localisation/Italy',
    'author': "Odoo Community Association (OCA), Apulia Software s.r.l",
    'website': 'https://www.odoo-italia.net/',
    'license': 'LGPL-3',
    'depends': [
        'l10n_it_account',
        ],
    'data': [
        'view/account_tax_kind_view.xml',
        'view/account_tax_view.xml',
        'data/account.tax.kind.csv',
        'security/ir.model.access.csv',
        ],
    'installable': True
}
