# Copyright 2019 Lorenzo Battistini - TAKOBI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Codice fiscale nei contatti/opportunità",
    "summary": "Aggiunge il campo codice fiscale ai contatti/opportunità",
    "version": "12.0.1.0.2",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/l10n-italy"
               "/tree/12.0/l10n_it_fiscalcode_crm",
    "author": "TAKOBI, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm",
        "l10n_it_fiscalcode"
    ],
    "data": [
        "views/crm_lead.xml",
    ],
}
