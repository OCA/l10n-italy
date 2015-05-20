.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License

DDT Module
==========

This is a total refactoring of the previews module (l10n_it_sale v7).

Usage
=====

With this module we have the possibility to keep pickings and DDTs
separated.

You can create a DDT From a Sale Order, setting True field create_ddt that
automatically create the DDT on Sale Order Confirmation; or by selecting 
pickings and using the "DdT from Pickings" action to automatically create a DdT. 

Yoy can add Pickings to an existing DDT using the "Add Pickings to DdT"
action, and so automatically update lines and tab Pickings on selected DDT

Finally you can create your invoice directly from selected DDTS using the 
"Create Invoice" action that create a new Invoice with the ddt lines as 
invoice lines

For further information, please visit:

* http://www.odoo-italia.org/

Credits
=======

Contributors
------------

* Davide Corio <davide.corio@abstract.it>
* Nicola Malcontenti <nicola.malcontenti@agilebg.com>
* Lorenzo Battistini <lorenzo.battistini@agilebg.com>
* Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
* Andrea Gallina <a.gallina@apuliasoftware.it>
* Alex Comba <alex.comba@agilebg.com>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
