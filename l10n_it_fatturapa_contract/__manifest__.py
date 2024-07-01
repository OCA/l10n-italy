#  Copyright 2024 Roberto Fichera - Level Prime Srl
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "ITA - Fattura elettronica - Integrazione Contratti",
    "summary": "Aggiunge alcuni dati per la fatturazione elettronica da Contratti",
    "version": "14.0.1.0.0",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Level Prime Srl, " "Odoo Community Association (OCA)",
    "maintainers": ["Robyf70"],
    "license": "AGPL-3",
    "category": "Hidden",
    "auto_install": True,
    "depends": [
        "l10n_it_fatturapa",
        "contract",
    ],
    "data": [
        "views/contract_views.xml",
        "views/contract_line_views.xml",
        "views/related_document_type_views.xml",
    ],
}
