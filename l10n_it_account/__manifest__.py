# Copyright 2015 Abstract srl (<http://www.abstract.it>)
# Copyright 2015-2017 Agile Business Group (<http://www.agilebg.com>)
# Copyright 2015 Link It Spa (<http://www.linkgroup.it/>)
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2020 Gianmarco Conte <gconte@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Contabilità base",
    "summary": "Modulo base usato come dipendenza di altri moduli contabili",
    "version": "14.0.1.1.6",
    "development_status": "Production/Stable",
    "category": "Hidden",
    "author": "Agile Business Group, Abstract, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "account_fiscal_year",
        "account_tax_balance",
        "date_range",
        "web",
    ],
    "data": [
        "views/account_setting.xml",
        "views/account_menuitem.xml",
        "views/partner_view.xml",
        "views/product_view.xml",
        "views/res_config_settings_views.xml",
        "reports/account_reports_view.xml",
        "views/account_view.xml",
    ],
    "installable": True,
    "post_init_hook": "_l10n_it_account_post_init",
}
