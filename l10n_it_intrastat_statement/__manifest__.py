{
    'name': 'ITA - Dichiarazione Intrastat',
    'version': '11.0.1.0.0',
    'category': 'Account',
    'summary': 'Dichiarazione Intrastat per l\'Agenzia delle Dogane',
    'author': 'Openforce'
            ', Link IT srl, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy',
    'license': 'LGPL-3',
    "depends": [
        'l10n_it_intrastat',
        'web',
    ],
    "data": [
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'wizard/export_file_view.xml',
        'views/config.xml',
        'views/intrastat.xml',
        'report/report_intrastat_mod1.xml',
        'report/intrastat_mod1_bis.xml',
        'report/report_intrastat_mod2.xml',
        'report/report_intrastat_mod2_bis.xml',
        'report/reports.xml',
    ],
    "demo": [],
    "installable": True
}
