# Copyright 2020 Lorenzo Battistini @ TAKOBI
# Copyright 2021 Alex Comba - Agile Business Group
# Copyright 2023 Simone Rubino - TAKOBI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Emissione e-fattura con reverse charge",
    "summary": "Integrazione l10n_it_fatturapa_out e l10n_it_reverse_charge",
    "version": "16.0.1.0.1",
    "development_status": "Beta",
    "category": "Hidden",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "TAKOBI, Odoo Community Association (OCA)",
    "maintainers": ["eLBati"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "l10n_it_fatturapa_out",
        "l10n_it_fatturapa_in",
        "l10n_it_reverse_charge",
    ],
    "data": [
        "views/rc_type_views.xml",
        "views/invoice_it_template.xml",
    ],
}
