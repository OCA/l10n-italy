.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

=====================================
Italian Localization - VAT Registries
=====================================

Law: http://goo.gl/b4y9Hx

Configuration
=============

You need to configure which tax codes are 'base', setting the 'is base' field
and which taxes are partially or totally non deductible, setting the
'non-deductible' field.

Also, you need to configure the 'vat statement type' on every tax code
(debit tax codes already have the default 'debit' value).

Consider using the mass_editing module

.. image:: /l10n_it_vat_registries/static/1-tax_iva22indetraibiel40.png

-------------------------------------------------------------------------------

.. image:: /l10n_it_vat_registries/static/2-taxcode_iva22indetraibile40_imponibile.png

-------------------------------------------------------------------------------

.. image:: /l10n_it_vat_registries/static/3-tax_iva22indetraibile40_parte_indetraibile.png

-------------------------------------------------------------------------------

.. image:: /l10n_it_vat_registries/static/5-tax_iva22indetraibile40_parte_detraibile.png

-------------------------------------------------------------------------------

.. image:: /l10n_it_vat_registries/static/4-taxcode_iva22indetraibile40_parte_indetraibile_.png

-------------------------------------------------------------------------------

.. image:: /l10n_it_vat_registries/static/6-taxcode_iva22indetraibile40_parte_detraibile.png


Usage
=====

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/122/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/l10n-italy/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/l10n-italy/issues/new?body=module:%20l10n_it_vat_registries%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Lorenzo Battistini <lorenzo.battistini@agilebg.com>
* Sergio Corato <sergiocorato@gmail.com>
* Elena Carlesso <ecarlesso@linkgroup.it>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
