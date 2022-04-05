# Copyright 2017 Alessandro Camilli - Openforce
# Copyright 2017-2021 Lorenzo Battistini
# Copyright 2019 Glauco Prina - Linkit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Comunicazione dati fatture",
    "summary": 'Comunicazione dati fatture (c.d. "nuovo spesometro" o '
    '"esterometro")',
    "version": "14.0.1.0.1",
    "category": "Account",
    "author": "Openforce di Camilli Alessandro, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "account",
        "l10n_it_fiscal_document_type",
        "l10n_it_appointment_code",
        "l10n_it_fiscalcode",
        "l10n_it_vat_payability",
        "l10n_it_account_tax_kind",
        "l10n_it_account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/res_country_data.xml",
        "wizard/compute_fiscal_document_type_view.xml",
        "wizard/split_big_communication_view.xml",
        "views/comunicazione.xml",
        "views/account.xml",
        "views/account_invoice_view.xml",
        "views/res_country_view.xml",
        "wizard/export_file_view.xml",
        "security/security.xml",
    ],
    "installable": True,
}
