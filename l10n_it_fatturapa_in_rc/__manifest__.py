# Copyright 2018 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'ITA - Fattura elettronica - Inversione contabile',
    "summary": "Modulo ponte tra e-fattura in acquisto e inversione"
               " contabile",
    "version": "12.0.1.1.1",
    "development_status": "Beta",
    "category": "Hidden",
    'website': 'https://github.com/OCA/l10n-italy/tree/10.0/'
               'l10n_it_fatturapa_in_rc',
    "author": "Efatto.it di Sergio Corato, Odoo Community Association (OCA)",
    "maintainers": ["sergiocorato"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "autoinstall": True,
    "depends": [
        "l10n_it_reverse_charge",
        "l10n_it_fatturapa_in",
        "l10n_it_account_tax_kind",
    ],
    "data": [
        "views/rc_type_view.xml",
    ],
}
