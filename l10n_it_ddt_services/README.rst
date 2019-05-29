.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================================
Fatturazione servizi da DDT
==================================================

This module allows for including services in the invoices created
directly from the DDT.

Usage
=====

English
-------

Once the DDT has been done and is "To be invoices", the default DDT module
allows the user selecting "Action > DDT Create Invoice"; in the wizard
it is possible to select the Invoice Journal and Date.

This modules adds below a list of invoiceable service lines. These lines
are taken from the SO linked to the current DDT. The user can delete
lines which are not required; the remaining lines will be added in the
invoice.

Italian
-------

Il modulo DDT permette di fatturare direttamente la merce spedita a partire
dal DDT. Si tratta però solo di merce "stoccabile/consumabile".

L'obiettivo è quello di poter fatturare anche i servizi. Nel flusso di base,
dal DDT selezionare "Azione > Crea fattura". Compare un wizard per la
selezione del Sezionale e della Data fattura.

Questo modulo aggiunge anche tutte le righe di servizi fatturabili disponibili
ordini di vendita associati al DDT in oggetto. L'utente può cancellare
le righe che non si vogliono fatturare e procedere.



.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/122/10.0

Credits
=======

Contributors
------------

* Giacomo Grasso <giacomo.grasso.82@gmail.com>


Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
