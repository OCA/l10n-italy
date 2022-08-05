# Copyright 2019 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "ITA - Dichiarazione Intrastat",
    'version': '12.0.1.4.0',
    'category': 'Account',
    'summary': 'Dichiarazione Intrastat per l\'Agenzia delle Dogane',
    'author': "Openforce, Link IT srl, Agile Business Group, "
              "Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_intrastat_statement',
    'license': 'AGPL-3',
    'depends': [
        'l10n_it_intrastat',
    ],
    'data': [
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'wizard/export_file_view.xml',
        'views/config.xml',
        'views/intrastat.xml',
        'report/report_intrastat_mod1.xml',
        'report/intrastat_mod1_bis.xml',
        'report/intrastat_mod1_ter.xml',
        'report/report_intrastat_mod2.xml',
        'report/report_intrastat_mod2_bis.xml',
        'report/reports.xml',
    ]
}
