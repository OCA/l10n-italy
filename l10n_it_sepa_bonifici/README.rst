.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

====================================
Italian Localization - SEPA Bonifici
====================================

This module adds a new payment export types to use in the payment order.
For italian credit transfer, the format code is CBIBdyPaymentRequest.00.04.00 

Configuration
=============

Configure the CUC code and the Issuer code (must be "CBI").

.. image:: /l10n_it_sepa_bonifici/static/company_setting.png

-------------------------------------------------------------------------------

You need to configure a new payment mode 

.. image:: /l10n_it_sepa_bonifici/static/payment_mode1.png

-------------------------------------------------------------------------------

In the new payment mode is important to set the Italian format SEPA CBI

.. image:: /l10n_it_sepa_bonifici/static/payment_mode2.png



Usage
=====

When you create a new order payment, you must select the payment mode above

.. image:: /l10n_it_sepa_bonifici/static/order_payment.png

-------------------------------------------------------------------------------

For get the xml file, first of all you must click on "make payments"

.. image:: /l10n_it_sepa_bonifici/static/make_payment.png

-------------------------------------------------------------------------------

It will show a wizard. Click on "generate" to continue

.. image:: /l10n_it_sepa_bonifici/static/make_payment_wizard.png

-------------------------------------------------------------------------------

The last step is to download the file from link

.. image:: /l10n_it_sepa_bonifici/static/make_payment_download.png


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

* Alessandro Camilli <alessandro.camilli@openforce.it>
* Andrea Colangelo <andrea.colangelo@openforce.it>
* Lorenzo Battistini <lorenzo.battistini@agilebg.com>
* Alex Comba <alex.comba@agilebg.com>

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
