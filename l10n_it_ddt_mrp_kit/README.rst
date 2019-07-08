.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================================
Fatturazione KIT da DDT
==================================================

This module allows for proper invoicing of KIT products
directly from the DDT.

Usage
=====

English
-------

When using a KIT product in PO and SO, in the picking and in the DDT the user will not find the
KIT product but all its components instead. When creating the invoice from DDT,
the base module will invoice all individual components with the same description,
creating some confusion.

This module avoids the invoicing of this components and checks instead all KIT
products that are invoiceable in the related SO and will include them in the
invoice.


Italian
-------

Se si utilizza un prodotto KIT (quindi con una distinta base) negli ordini,
Odoo crea dei trasferimenti e DDT che includono i componenti indicati all'intenro
del KIT, e non quel prodotto stesso. Se si fattura direttamente dal DDT, la
fattura di vendita conterrà una riga per ogni componente, creando un po' di confusione.

Questo modulo evita la fatturazione dei coponenti e verifica invece se ci sono dei
prodotti KIT fatturabili negli ordini associati al DDT, procedendo quindi alla loro
fatturazione.


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
