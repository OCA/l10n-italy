# Copyright 2025 Martin Stecher - IT-S
{
    "name": "PoS - Fattura PA Fields",
    "summary": "Adds the fattura PA fields in the customer edit screen of POS",
    "version": "16.0.0.0.0",
    "category": "Point of sale",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Odoo Community Association (OCA), [IT-S] Martin Stecher",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["point_of_sale", "l10n_it_fatturapa"],
    "assets": {
        "point_of_sale.assets": [
            "l10n_it_pos_partner_edit_fatturapa/static/src/xml/ClientDetailsEdit.xml",
            "l10n_it_pos_partner_edit_fatturapa/static/src/js/ClientDetailsEdit.esm.js",
        ]
    },
}
