# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Integrazione tra RiBa e provvigioni su vendite",
    "summary": "Modulo ponte tra provvigioni agenti e RiBa",
    "version": "14.0.1.1.2",
    "development_status": "Alpha",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Nextev Srl, Odoo Community Association (OCA)",
    "maintainers": ["odooNextev", "aleuffre", "renda-dev", "PicchiSeba"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale_commission_partial_settlement",
        "l10n_it_ricevute_bancarie",
    ],
    "data": [
        "views/invoice_no_commission.xml",
        "views/configuration_riba_view.xml",
    ],
}
