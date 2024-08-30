# Copyright 2020 Lorenzo Battistini
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Fattura elettronica - Import ZIP",
    "summary": "Permette di importare in uno ZIP diversi file XML di "
    "fatture elettroniche",
    "version": "16.0.1.2.0",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "TAKOBI, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "l10n_it_account",
        "l10n_it_fiscal_document_type",
        "l10n_it_fatturapa_out",
        "l10n_it_fatturapa_in",
        "l10n_it_withholding_tax_reason",
    ],
    "data": [
        "views/account_invoice_views.xml",
        "views/attachment_views.xml",
        "security/ir.model.access.csv",
        "security/rules.xml",
    ],
}
