{
    "name": "ITA - POS - Fattura elettronica",
    "summary": "Gestione dati fattura elettronica del cliente all'interno "
               "dell'interfaccia del POS",
    "version": "14.0.0.0.1",
    "development_status": "Beta",
    "category": "Point Of Sale",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Roberto Fichera, Air s.r.l., Odoo Community Association (OCA)",
    "maintainers": ["robyf70"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        # "pos_partner_firstname",
        # "l10n_it_pos_fiscalcode",
        "l10n_it_fatturapa",
        'point_of_sale'
    ],
    'data': [
        'templates/assets.xml'
    ],
    "qweb": [
        'static/Screens/ClientDetailsEdit.xml'
    ],
}
