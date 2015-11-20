# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Supplier FatturaPA - Notifications',
    'version': '7.0.1.0.0',
    'category': 'Localization/Italy',
    'summary': 'Supplier electronic invoices notifications',
    'author': 'Agile Business Group, Odoo Community Association (OCA)',
    'website': 'http://www.agilebg.com',
    'description': """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================
Supplier FatturaPA Notifications
================================

This module handles SDI notifications related to supplier invoices (fatturaPA).
See http://fatturapa.gov.it/export/fatturazione/it/b-2.htm


Usage
=====

Within 'fatturaPA' tab of supplier invoice form, you can click on 2 buttons:
 - Accept fatturaPA
 - Reject fatturaPA
This allows to generate the 'notifica esito committente' message
http://fatturapa.gov.it/export/fatturazione/sdi/messaggi/v1.0/IT01234567890_11111_EC_001.xml

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/l10n-italy/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed `feedback
<https://github.com/OCA/
l10n-italy/issues/new?body=module:%20
l10n_it_fatturapa_in_notifications%0Aversion:%20
7.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Contributors
------------

* Lorenzo Battistini <lorenzo.battistini@agilebg.com>

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
""",
    'license': 'AGPL-3',
    "depends": [
        'l10n_it_fatturapa_in',
        'l10n_it_fatturapa_notifications',
    ],
    "data": [
        'attachment_view.xml',
        'wizard/send_notification_view.xml',
        'account_view.xml',
    ],
    "installable": True
}
