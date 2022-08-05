# Copyright 2015 Nicola Malcontenti - Agile Business Group
# Copyright 2016 Andrea Cometa - Apulia Software
# Copyright 2016-2019 Lorenzo Battistini
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "ITA - Stampa fattura raggruppata per DDT",
    'summary': 'Raggruppa le righe fattura per DDT che le ha '
               'generate, mostrando eventualmente i lotti/seriali',
    'version': '12.0.1.0.5',
    'category': 'Localization/Italy',
    'author': 'Agile Business Group, Apulia Software, Openforce,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/account_invoice_report_ddt_group',
    'license': 'AGPL-3',
    'depends': [
        'account', 'l10n_it_ddt',
    ],
    "data": [
        'views/invoice_ddt.xml',
        'views/partner.xml',
        'views/invoice_view.xml',
    ],
    "installable": True
}
