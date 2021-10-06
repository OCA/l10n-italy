# Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
# Copyright 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018-2019 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2021 Ciro Urselli <https://github.com/CiroBoxHub>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Fattura elettronica - Integrazione " "ritenuta",
    "summary": "Modulo ponte tra emissione fatture elettroniche e ritenute.",
    "version": "14.0.1.0.0",
    "development_status": "Beta",
    "category": "Hidden",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Sergio Corato, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_fatturapa",
        "l10n_it_fatturapa_out",
        "l10n_it_withholding_tax",
        "l10n_it_withholding_tax_reason",
    ],
    "data": [
        "views/account_invoice_it_dati_ritenuta.xml",
    ],
    "installable": True,
    "auto_install": True,
}
