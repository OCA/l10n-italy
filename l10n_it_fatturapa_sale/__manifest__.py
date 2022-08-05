#  Copyright 2020 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "ITA - Fattura elettronica - Integrazione vendite",
    "summary": "Aggiunge alcuni dati per la "
               "fatturazione elettronica nell'ordine di vendita",
    "version": "12.0.1.1.3",
    "website": "https://github.com/OCA/l10n-italy"
               "/tree/12.0/l10n_it_fatturapa_sale",
    "author": "Agile Business Group, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Hidden",
    "auto_install": True,
    "depends": [
        "l10n_it_fatturapa",
        "sale_management",
    ],
    "excludes": ["sale_order_action_invoice_create_hook"],
    "data": [
        "views/related_document_type_views.xml",
        "views/sale_order_line_views.xml",
        "views/sale_order_views.xml",
    ],
}
