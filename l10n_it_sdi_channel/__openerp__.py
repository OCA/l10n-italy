# -*- coding: utf-8 -*-
##############################################################################
#
#    Italian Localization - SdI channel
#
#    Author(s): Sergio Corato (https://efatto.it)
#    Copyright © 2018 Sergio Corato (https://efatto.it)
#    Copyright © 2018 Lorenzo Battistini (https://github.com/eLBati)
#    Copyright © 2018 Enrico Ganzaroli (enrico.gz@gmail.com)
#    Copyright © 2018 Ermanno Gnan (ermannognan@gmail.it)
#
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
##############################################################################
{
    "name": "SdI channel",
    "summary": "Add channel to send-receice xml files to SdI.",
    "version": "7.0.1.1.0",
    "development_status": "Beta",
    "category": "Hidden",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Efatto.it di Sergio Corato, Odoo Community Association (OCA)",
    'description': """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License

Italian Localization  - SdI channel
===================================
This module add some useful fields as a pre-requisite to send XML and ZIP
 files of electronic invoices

http://www.fatturapa.gov.it/export/fatturazione/it/normativa/f-2.htm

through mail PEC, WEB API or SFTP from the exchange system (SDI)

http://www.fatturapa.gov.it/export/fatturazione/it/sdi.htm

CONFIG
======
Nel menu: Contabilità > Configurazione > Contabilità

Sotto Fattura elettronica > SDI channels

va creato un nuovo canale di tipo PEC (unico supportato per ora) in cui 
vanno inseriti:

- La mail PEC dello SdI, inizialmente uguale a sdi01@pec.fatturapa.it.

Dopo il primo invio, lo SdI risponderà segnalando l'indirizzo da utilizzare
per i successivi invii, che va quindi inserito nel server PEC dedicato.

- Il server PEC da utilizzare per gli invii/ricezioni verso lo SdI.

Tale
server è preferibile sia dedicato solo a questo utilizzo, in quanto i messaggi
di altro genere non verrebbero gestiti da Odoo, ma risulterebbero comunque
letti.

In questo server va indicata la mail di invio/ricezione, solitamente
uguale all'utente di connessione (potrebbe essere diversa dall'utente di
connessione in casi particolari).

Se si usano altri SMTP server, per l'invio di email non PEC, bisogna dare loro
 priorità maggiore rispetto al server PEC.

Creare infine il mail server in ingresso, impostando 'FatturaPA PEC server'
    """,
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account",
        "fetchmail",
        "l10n_it_fatturapa",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/sdi_view.xml",
        "views/company_view.xml",
        'views/fetchmail_server.xml',
        'views/ir_mail_server.xml',
    ],
}
