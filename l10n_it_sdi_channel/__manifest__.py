# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Italian Localization - Fattura elettronica - Canale SdI",
    "summary": "Aggiunge il canale di invio/ricezione dei file XML "
               "attraverso lo SdI",
    "version": "12.0.2.2.0",
    "development_status": "Beta",
    "category": "Hidden",
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_sdi_channel',
    "author": "Efatto.it di Sergio Corato, Odoo Community Association (OCA)",
    "maintainers": ["sergiocorato"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account",
        "l10n_it_fatturapa",
        "l10n_it_fatturapa_in",
        "l10n_it_fatturapa_out",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "data/mail_message_subtype_data.xml",
        "views/account_invoice_views.xml",
        "views/sdi_view.xml",
        "views/company_view.xml",
        "views/fatturapa_attachment_views.xml",
        "wizards/send_to_sdi_views.xml",
    ],
}
