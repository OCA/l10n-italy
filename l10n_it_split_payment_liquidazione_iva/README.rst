.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

========================================================
Italian Localization - Split payment su liquidazione iva
========================================================

Modulo per considerare l'iva dello split payment in fase di liquidazione IVA.
L'iva a debito derivante dalle fatture di vendita soggette a split payment verrà stornata
nella liquidazione iva con un movimento di storno che verrà messo nella sezione altri
debiti e crediti.

Configuration
=============

Nella configurazione della contabilità è possibile personalizzare la dicitura che verrà
riportata nella liquidazione iva relativamente allo storno.

Usage
=====

Il modulo si integra nel calcolo della liquidazione.
Tutte le funzionalità del modulo verranno attivate insieme al calcolo della liquidazione



Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/l10n-italy/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Alessandro Camilli <alessandrocamilli@openforce.it>
* Silvio Gregorini <silviogregorini@openforce.it>

Funders
-------

The development of this module has been financially supported by:

* Openforce http://openforce.it
* Odoo Italia Network http://odoo-italia.net

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
