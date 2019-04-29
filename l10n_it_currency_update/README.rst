.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================================================
Italian Localization - Tassi di cambio Banca d'Italia
======================================================

Configurazione
--------------

Questo modulo integra il modulo OCA per l'aggiornamento dei cambi in automatico,
disponibile qui: https://github.com/OCA/account-financial-tools/tree/10.0/currency_rate_update.

Viene quindi aggiunta la possibilità di scaricare i tassi di cambio dal sito della
Banca d'Italia: https://tassidicambio.bancaditalia.it/.
Le istruzioni per l'export dei dati sono disponibili
qui: https://tassidicambio.bancaditalia.it/assets/files/Operating_Instructions.pdf.

I tassi di cambio sono esportati in formato JSON.

Non è necessaria alcuna configurazione.

Utilizzo
--------
All'installazione del modulo, al menu "Contabilità > Multi-Valute > Rate Auto-download"
è possibile selezionare tra i "Webservice to use" anche la "Banca d'Italia".

Il modulo per la gestione dei tassi di cambio OCA esegue in automatico l'azione
"Update now". Si suggerisce di verificare i tempi di esecuzione del cron e porlo a fine
giornata, per essere sicuri che la Banca d'Italia abbia aggiornato i dati.

Usage
=====

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/122/10.0


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/l10n-italy/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Giacomo Grasso <giacomo.grasso.82@gmail.com>
* Gabriele Baldessari <gabriele.baldessari@gmail.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
