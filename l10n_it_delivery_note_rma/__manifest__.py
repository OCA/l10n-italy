{
    "name": "ITA - Creazione RMA da DDT (Delivery Note)",
    "summary": """Add Oportunity to create RMA from DN with wizard
    and smart button to DN view""",
    "version": "14.0.1.1.0",
    "category": "Delivery Note",
    "website": "https://github.com/OCA/l10n-italy",
    "maintainers": ["solo4games", "CetmixGitDrone"],
    "author": "Odoo Community Association (OCA), Cetmix, Ooops",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["rma", "l10n_it_delivery_note"],
    "data": [
        "views/assets.xml",
        "security/ir.model.access.csv",
        "views/rma_views.xml",
        "views/delivery_views.xml",
        "wizard/stock_delivery_note_rma_wizard_views.xml",
        "views/delivery_portal_template.xml",
    ],
}
