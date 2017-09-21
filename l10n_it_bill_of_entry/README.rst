.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================================
Italian Localization - Bill of Entry: Bolle Doganali
====================================================

This module enables to manage extraUE import purchases, generating a bill of entry
according to the supplier invoice.
It involves three documents:

* Supplier Invoice
* Forwarder Invoice
* Bill of Entry

Here how documents are linked each other:

* N bill of entries --> N supplier invoices
* N bill of entries --> 1 forwarder invoice

Configuration
=============

Mandatory settings:

* An account journal required by the closing transfer account move (e.g. "Bolle Doganali").
* An account journal for extraCEE supplier invoices, apart from 
  ordinary supplier invoices. In this way, extraCEE supplier invoices don't appear in VAT registries;
  in this way, VAT registries have no missing numbers.
* Add a tax mapping on Extra EU fiscal position: purchase taxes (e.g. 22%) should be mapped to
  to no one tax. In this way, every purchase invoice for extra UE fiscal position
  don't show taxes in lines, according to law.
* A virtual supplier (e.g. "Customs" or "Dogana") for the bill of entry.
* The forwarder as a real supplier.
* An expense account where recording the bill of entry net amount (e.g. "ACQUISTO MERCI ExtraCEE").
* An expense account where recording the bill of entry VAT amount,
  paid in advance by the forwarder and declared in the forwarder invoice (e.g. "SPESE DOGANALI ANTICIPATE").

Optional settings:

* An account tax, with the same VAT rate as the ordinary one (i.e. 22% for Italy),
  applied on the bill of entry net amount (e.g. "22% debito ExtraCEE"). In this way,
  bill of entries are highlighted in VAT registries due to this tax code.
* An account for delivery expenses, recorded in the forwarderd invoice (e.g. "SPESE DI TRASPORTO").
* An account for customs duties, recorded in the forwarderd invoice (e.g. "DIRITTI DOGANALI").
* An account for stamp duties, recorded in the forwarderd invoice (e.g. "IMPOSTE DI BOLLO").

Usage
=====

English
-------

Each bill of entry can be manually linked to its corresponding supplier invoice.

The forwarder invoice requires one (or more) line(s) marked as the
advance customs vat.

At the forwarder invoice confirmation, it would be linked to the closing
transfer account move, which closes and reconciles the bill of entry.

Italiano
--------

Dalla bolla doganale è possibile collegare manualmente la (o le) fattura(e)
fornitore corrispondente.

Nella fattura spedizioniere bisogna indicare quale (o quali) riga (righe)
rappresenti(no) l'IVA anticipata alla dogana.

Alla conferma della fattura spedizioniere, verrà generata la scrittura
contabile di giroconto per chiudere la bolla doganale.


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/122/10.0

Workplan and future improvements
================================

Previous releases of this module were able to create bill of entries
through a wizard button, according to a predefined bill of entry invoice template.

This feature requires account_invoice_template module, which is not yet fully available.


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

* Alex Comba <alex.comba@agilebg.com>
* Lorenzo Battistini <lorenzo.battistini@agilebg.com>
* Diego Bruselli <d.bruselli@creativiquadrati.it>

Do not contact contributors directly about support or help with technical issues.

Funders
-------

The development of this module has been financially supported by:

* Odoo Italia Network

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
