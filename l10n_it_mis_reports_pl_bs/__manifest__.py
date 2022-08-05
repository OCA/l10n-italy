# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'ITA - MIS builder - Bilancio civilistico',
    'summary': 'Modelli "MIS Builder" per il conto economico e lo stato patrimoniale',
    'author': 'Dinamiche Aziendali srl,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_mis_reports_pl_bs',
    'category': 'Reporting',
    'version': '12.0.1.0.1',
    'license': 'AGPL-3',
    'depends': [
        'mis_builder',
    ],
    'data': [
        'data/mis_report_styles.xml',
        'data/mis_report_pl.xml',
        'data/mis_report_bs.xml',
    ],
    'installable': True,
}
