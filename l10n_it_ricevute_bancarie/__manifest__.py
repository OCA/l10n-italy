# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# Copyright (C) 2019 Sergio Zanchetta - Associazione PNLUG
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "ITA - Ricevute bancarie",
    'version': "12.0.1.8.0",
    'author': "Odoo Community Association (OCA)",
    'category': 'Localization/Italy',
    'summary': 'Ricevute bancarie',
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_ricevute_bancarie',
    'license': "AGPL-3",
    'depends': [
        'account',
        'account_group_menu',
        'l10n_it_fatturapa_out',
        'l10n_it_fiscalcode',
        'base_iban',
        'l10n_it_abicab',
        'account_due_list'],
    'data': [
        "data/riba_sequence.xml",
        "report/report.xml",
        "security/ir.model.access.csv",
        "security/riba_security.xml",
        "views/wizard_accreditation.xml",
        "views/wizard_unsolved.xml",
        "views/riba_view.xml",
        "views/account_view.xml",
        "views/configuration_view.xml",
        "views/partner_view.xml",
        "views/wizard_riba_issue.xml",
        "views/wizard_riba_file_export.xml",
        "views/account_config_view.xml",
        "views/distinta_report.xml",
        "views/riba_detail_view.xml",
    ],
    'demo': ["demo/riba_demo.xml"],
    'installable': True,
}
