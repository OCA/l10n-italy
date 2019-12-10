===================
EPoS Fiscal Printer
===================

This module allow to print receipt of point_of_sale,
on fiscal printer Epson via EPos protocol.

Configuration
=============

- print list departments of your fiscal printer
- mapping odoo sale taxes with group taxes - departments of fiscal printer, for each sale tax on odoo, using field "Department group tax on fiscal printer 1~99"
- In odoo, use taxes included in price
- connect your fiscal printer on network and find IP
- open point_of_sale configuration and fill Printer IP Address field, with printer IP
- that's all, at validation of payment on POS session system print fiscal receipt.


Credits
=======

Contributors
------------

* Leonardo Donelli
* Lorenzo Battistini
* Alessio Gerace

Do not contact contributors directly about support or help with technical issues.
