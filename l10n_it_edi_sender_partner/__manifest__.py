# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Terzo intermediario per fatturazione elettronica",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Terzo intermediario o soggetto emittete per fatturazione elettronica",
    "author": "Nextev Srl, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_edi_extension",
    ],
    "external_dependencies": {
        "python": ["openupgradelib"],
    },
    "data": [
        "views/l10n_it_sender_partner.xml",
        "views/l10n_it_view.xml",
        "views/account_view.xml",
        "data/invoice_it_template.xml",
    ],
    "installable": True,
    "pre_init_hook": "_l10n_it_fatturapa_pre_migration",
}
