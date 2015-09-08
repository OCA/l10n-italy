.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Period End VAT Statement
========================

This module helps to register the VAT statement of period end.

In order to load correct amount from tax code, the tax code has to be
associated to account involved in statement, through tax code form.

The 'VAT statement' object allows to specify every amount and relative account
used by the statement.
By default, amounts of debit and credit taxes are automatically loaded
from tax codes of selected periods.
Previous debit or credit is loaded from previous VAT statement, according
to its payments status.
Confirming the statement, the 'account.move' is created. If you select
a payment term, the due date(s) will be set.

The 'tax authority' tab contains information about payment(s).
You can see statement's result ('authority VAT amount') and residual
amount to pay ('Balance').
The statement can be paid like every other debit: by voucher or 'move.line'
reconciliation.

If you need to calculate interest, you can add default information in your
company data (percentage and account).

Specification:
http://wiki.odoo-italia.org/doku.php/moduli/vat_period_end_statement

Credits
=======

Contributors
------------

* Lorenzo Battistini <lorenzo.battistini@agilebg.com>
* Elena Carlesso <ecarlesso@linkgroup.it>
* Marco Marchiori <marcomarkiori@gmail.com>
* Sergio Corato <sergiocorato@gmail.com>
* Andrea Gallina <a.gallina@apuliasoftware.it>
* Alex Comba <alex.comba@agilebg.com>
* Alessandro Camilli <camillialex@gmail.com>

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
