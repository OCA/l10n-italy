# Copyright 2017 Apulia Software s.r.l. (http://www.apuliasoftware.it)
# @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# Copyright 2017 Alex Comba - Agile Business Group
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Italian Localisation - Natura delle aliquote IVA',
    'version': '12.0.2.1.0',
    'development_status': 'Production/Stable',
    'category': 'Localisation/Italy',
    'author': "Odoo Community Association (OCA), Apulia Software s.r.l",
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_account_tax_kind',
    'license': 'AGPL-3',
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
