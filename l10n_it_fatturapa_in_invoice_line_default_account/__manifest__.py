# Copyright 2018 Lorenzo Battistini
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2019 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'ITA - Fattura elettronica - Conto di costo predefinito su fornitore',
    "summary": "Modulo ponte tra ricezione fatture elettroniche e modulo "
               "\"Account Invoice Line Default Account\"",
    'version': '12.0.1.0.0',
    'category': 'Hidden',
    'author': 'TAKOBI, '
              'Odoo Community Association (OCA)',
    'maintainers': ['eLBati'],
    'website': 'https://github.com/OCA/l10n-italy',
    'license': 'AGPL-3',
    "depends": [
        'l10n_it_fatturapa_in',
        'account_invoice_line_default_account',
    ],
    "data": [
    ],
    "installable": True,
    'auto_install': True,
}
