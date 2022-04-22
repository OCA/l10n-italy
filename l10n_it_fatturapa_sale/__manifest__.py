#  Copyright 2020 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "ITA - Fattura elettronica - Integrazione vendite",
    "summary": "Aggiunge alcuni dati per la "
    "fatturazione elettronica nell'ordine di vendita",
    "version": "14.0.1.0.1",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Agile Business Group, " "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Hidden",
    "auto_install": True,
    "depends": [
        "l10n_it_fatturapa",
        "sale_management",
    ],
    "data": [
        "views/related_document_type_views.xml",
        "views/sale_order_line_views.xml",
        "views/sale_order_views.xml",
    ],
}
