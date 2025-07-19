# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Italy - E-invoicing - Base Feature",
    "version": "18.0.1.0.0",
    "category": "Accounting/Localizations/EDI",
    "development_status": "Beta",
    "summary": "E-invoice base feature",
    "author": "Giuseppe Borruso, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "external_dependencies": {
        "python": [
            "codicefiscale",
            "openupgradelib",
        ],
    },
    "depends": [
        "account",
        "l10n_it_edi",
        "partner_firstname",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/invoice_it_template.xml",
        "data/res.city.it.code.csv",
        "views/l10n_it_view.xml",
        "views/res_partner_view.xml",
        "views/company_view.xml",
        "wizards/compute_fc_view.xml",
        "wizards/l10n_it_edi_import_file_wizard.xml",
    ],
    "installable": True,
    "pre_init_hook": "_l10n_it_edi_extension_pre_init_hook",
    "post_init_hook": "_l10n_it_edi_extension_post_init_hook",
}
