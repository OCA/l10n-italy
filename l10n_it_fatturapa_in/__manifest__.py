# Copyright 2015 AgileBG SAGL <http://www.agilebg.com>
# Copyright 2015 innoviu Srl <http://www.innoviu.com>
# Copyright 2018 Lorenzo Battistini
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Fattura elettronica - Ricezione",
    "version": "14.0.1.0.6",
    "development_status": "Alpha",
    "category": "Localization/Italy",
    "summary": "Ricezione fatture elettroniche",
    "author": "Agile Business Group, Innoviu, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy" "l10n_it_fatturapa_in",
    "license": "AGPL-3",
    "depends": [
        "base_vat",
        "l10n_it_fatturapa",
        "l10n_it_fiscal_document_type",
        "l10n_it_withholding_tax_reason",
    ],
    "data": [
        "views/account_view.xml",
        "views/partner_view.xml",
        "wizard/wizard_import_fatturapa_view.xml",
        "wizard/link_to_existing_invoice.xml",
        "views/company_view.xml",
        "security/ir.model.access.csv",
        "security/rules.xml",
    ],
    "installable": True,
    "external_dependencies": {
        "python": ["elementpath", "xmlschema", "asn1crypto"],
    },
}
