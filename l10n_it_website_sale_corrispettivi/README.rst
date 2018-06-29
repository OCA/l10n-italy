.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

=================================================
Italian localization - Website Sale Corrispettivi
=================================================

This module adds the *Want invoice* check in partner's address form of checkout flow,
its value is the opposite of *Use corrispettivi* in partner.

Configuration
=============

For unlogged users, the behavior depends on how the partner associated to the public user is configured  
(note that the public user is an inactive user by default), for instance:

* If the public user has the flag *Use corrispettivi* enabled, the unlogged user will have *Want invoice* disabled;
* If the public user has the flag *Use corrispettivi* disabled, the unlogged user will have *Want invoice* enabled;

Usage
=====

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/113/10.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/l10n_italy/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Simone Rubino <simone.rubino@agilebg.com>

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
