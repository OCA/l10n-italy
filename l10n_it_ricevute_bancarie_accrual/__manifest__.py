# Copyright 2017-2020 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'ITA - Ricevute bancarie con maturazione',
    'version': '12.0.1.0.1',
    'category': 'Accounting',
    'summary': 'Ricevute bancarie con maturazione',
    'author': 'Sergio Corato',
    'website': 'https://github.com/OCA/l10n-italy/tree/'
               '12.0/l10n_it_ricevute_bancarie_accrual',
    'license': 'AGPL-3',
    'depends': [
        'l10n_it_ricevute_bancarie',
    ],
    'data': [
        'views/riba_view.xml',
        'views/wizard_accreditation.xml',
        'views/wizard_unsolved.xml',
        'views/wizard_accrual.xml',
        'views/account_view.xml',
    ],
    'installable': True
}
