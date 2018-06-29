.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

===============================
Ricevute bancarie & commissioni
===============================

This module extends the functionality of Sales commissions introducing a flag in Commission types: Only paid RiBa.
If this flag is active and the commission type is Payment Based, sale agents having this commission type
have their commissions generated only for paid invoices whose RiBa lines are also paid.

Installation
============

This module is auto-installed by Odoo when *l10n_it_ricevute_bancarie* and
*sale_commission* are installed.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/l10n-italy/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Simone Rubino <simone.rubino@agilebg.com> (www.agilebg.com)

Do not contact contributors directly about support or help with technical issues.

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
