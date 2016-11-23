.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================================================
Account Fiscal Year Closing - Chiusura e riapertura fiscale
===========================================================

[![en](http://www.shs-av.com/wp-content/en_US.png)](http://wiki.zeroincombenze.org/it/Odoo/7.0/man)

Generalization of l10n_es_fiscal_year_closing.

This module replaces the default OpenERP end of year wizards
(from account module)
with a more advanced all-in-one wizard that will let the users:
  - Check for unbalanced moves, moves with invalid dates
    or period or draft moves on the fiscal year to be closed.
  - Create the Loss and Profit entry.
  - Create the Net Loss and Profit entry.
  - Create the Closing entry.
  - Create the Opening entry.

Usage
=====

To use this module, you need to:

#. Create new journal entries
#. Create specific accounts in chart of account
#. Execute: accounting -> Periodic processing -> End of period -> Chiudi anno fiscale
#. Check for all values in form
#. Confirm all account operations



[![it](http://www.shs-av.com/wp-content/it_IT.png)](http://wiki.zeroincombenze.org/it/Odoo/7.0/man)

Variante del modulo l10n_es_fiscal_year_closing

Questo modulo sostituisce il modulo standard di apertura di Odoo con alcune
specificità legate alla contabilità italiana:
  - Controllo movimenti sbilanciati o con date non valide
  - Crea il movimento di rilevazione profitti e perdite
  - Crea il movimento di chiusura contabile
  - Crea il movimento di apertura contabile dei soli conti patrimoniali


Uso
===

Per utilizzare questo modulo:

#. Creare nuovi sezionali specifici
#. Creare conti specifici per la chiusura e riapertura
#. Eseguire: Contabilità -> Elaborazione periodica -> Fine del periodo -> Chiudi anno fiscale
#. Controllare i valori risultanti
#. Confermare definitivamente tutte le operazioni



For further information, please visit:

* http://www.odoo-italia.org/

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/122/8.0

Credits
=======

Contributors
------------

* Borja López Soilán <borja@kami.es>
* Lorenzo Battistini <lorenzo.battistini@agilebg.com>
* Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
