# Copyright 2018 Lorenzo Battistini
# Copyright (c) 2019 Matteo Bilotta
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': "ITA - Registro IVA + Scissione dei pagamenti",
    'summary': "Modulo di congiunzione tra registri"
               " IVA e scissione dei pagamenti",
    'version': '12.0.1.0.2',
    'development_status': "Beta",
    'category': "Accounting & Finance",
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_vat_registries_split_payment',
    'author': "Agile Business Group, "
              "Odoo Community Association (OCA)",
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'auto_install': True,
    'depends': [
        'l10n_it_vat_registries',
        'l10n_it_split_payment'
    ]
}
