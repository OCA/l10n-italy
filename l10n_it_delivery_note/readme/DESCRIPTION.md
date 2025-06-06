**English**

This module manage the Italian DDT (Delivery note).

From a picking is possible to generate a Delivery Note and group more
picking in one delivery note. It's also possible to invoice directly from the
delivery note form, with configurable options to use DN data (product names, prices)
instead of sale order data when generating invoices.

This is particularly useful when:
- Products are substituted at delivery time
- Prices are negotiated during delivery
- Detailed descriptions need to be added in the DN

This module is alternative to `l10n_it_ddt`, it follows the Odoo way to
process sale orders, pickings and invoices.

You can't have both `l10n_it_ddt` and `l10n_it_delivery_note` installed
together.

There are two available settings:

- Base (default): one picking, one DN.
- Advanced: more picking in one DN.

**Italiano**

Questo modulo consente di gestire i DDT.

Da un prelievo è possibile generare un DDT e raggruppare più prelievi in
un DDT. È anche possibile fatturare direttamente dalla scheda del DDT,
con opzioni configurabili per utilizzare i dati del DDT (nomi prodotti, prezzi)
invece dei dati dell'ordine di vendita nella generazione delle fatture.

Questo è particolarmente utile quando:
- I prodotti vengono sostituiti al momento della consegna
- I prezzi vengono negoziati durante la consegna
- È necessario aggiungere descrizioni dettagliate nel DDT

Questo modulo è un alternativa al modulo `l10n_it_ddt`, segue la
modalità Odoo di gestire ordini di vendita, prelievi e fatture.

Non è possibile avere installati contemporaneamente `l10n_it_ddt` e
`l10n_it_delivery_note`.

Ci sono due impostazioni possibili.

- Base (predefinita): un prelievo, un DDT.
- Avanzata: più prelievi in un DDT.
