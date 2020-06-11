.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========
Enasarco
========

Questo modulo consente di generare la scrittura di rilevazione del 
debito verso l'Enasarco al momento della registrazione della fattura
fornitore


Usage
=====

Nella configurazione della contabilità impostare il sezionale e il conto
da usare per la scrittura dell'Enasarco

Nella fattura fornitore, abilitare la sezione Enasarco con l'apposito flag
presente in testata

Specificare la data e l'importo Enasarco in calce alla fattura.
Alla Validazione l'importo inserito andrà a scalare il dovuto al fornitore
e attraverso un'apposita registrazione verrà alimentato il conto debiti
verso Enasarco per gestire gli importi da versare.


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/commission/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.


Credits
=======


Contributors
------------
* Alessandro Camilli <alessandro.camilli@openforce.it>

Images
-------
* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

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
