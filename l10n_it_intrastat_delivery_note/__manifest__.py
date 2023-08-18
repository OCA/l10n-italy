{
    "name": "ITA - Intrastat Delivery Note",
    "version": "14.0.1.0.0",
    "category": "Hidden",
    "summary": "Aggiunta campi mancanti a stampa DDT",
    "author": "PyTech SRL, Odoo Community Association (OCA)",
    "maintainers": ["aleuffre", "renda-dev", "PicchiSeba"],
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "l10n_it_delivery_note",
        "l10n_it_intrastat",
    ],
    "data": [
        "report/report_delivery_document.xml",
        "report/report_delivery_note.xml",
    ],
    "demo": [],
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
}
