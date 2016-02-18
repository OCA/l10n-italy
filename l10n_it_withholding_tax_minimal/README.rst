.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

=========================
Italian withholding taxes
=========================


Configuration
=============

In accounting configuration you have to set

 - Withholding tax payment term
 - Payable account for withholding taxes to pay
 - Withholding tax journal

You have to set the flag 'Withholding Tax' in tax codes related to
withholding taxes

Configure withholding tax like the following

.. image:: /l10n_it_withholding_tax/static/description/images/tax_configuration.png
   :alt: withholding tax


Usage
=====

To use this module, you need to add the withholding tax to subjected invoice lines

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/122/8.0

Known issues / Roadmap
======================

This module is incompatible with 'l10n_it_withholding_tax'.

Please use this module only if 'l10n_it_withholding_tax' is excessive in your case.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/l10n-italy/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/l10n-italy/issues/new?body=module:%20l10n_it_withholding_tax%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Contributors
------------

* Lorenzo Battistini <lorenzo.battistini@agilebg.com>
* Paolo Chiara <p.chiara@isa.it>


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
