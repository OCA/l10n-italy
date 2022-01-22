Questo modulo replica alcuni campi della fattura nella registrazione contabile.
Il modello account.move ha la stessa struttura di Odoo 13.0 e successive.
Il modulo semplifica il backport da Odoo 13.0+

Strutture comuni con Odoo 13.0+
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* account.move.invoice_date
* account.move.type (deve essere rinominato move_type)
* account.move.fiscal_position_id
* account.move.payment_term_id
* account.move.partner_bank_id

Differenze da Odoo 13.0+
~~~~~~~~~~~~~~~~~~~~~~~~

* Draft and cancelled invoice has no account.move records
* Events are still active on account.invoice model