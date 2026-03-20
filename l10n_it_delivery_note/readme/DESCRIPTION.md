**English**

This module manage the Italian DDT (Delivery note).

From a picking is possible to generate a Delivery Note and group more
picking in one delivery note. It's also possible to invoice from the
delivery note form.

This module is alternative to `l10n_it_ddt`, it follows the Odoo way to
process sale orders, pickings and invoices.

You can't have both `l10n_it_ddt` and `l10n_it_delivery_note` installed
together.

There are two available settings:

- Base (default): one picking, one DN.
- Advanced: more picking in one DN.

**Electronic Invoicing Integration**

This module integrates with Italian electronic invoicing (`l10n_it_stock_ddt`).

It automatically adds Delivery Note references to the FatturaPA XML, including:
- DDT Number
- DDT Date
- Line references

The module also handles the distinction between immediate and deferred invoices:
- **TD01 (Immediate invoice)**: when the invoice has the same date as the linked DDTs
- **TD24 (Deferred invoice)**: when the invoice is issued on a different day than the DDTs

**Italiano**

Questo modulo consente di gestire i DDT.

Da un prelievo è possibile generare un DDT e raggruppare più prelievi in
un DDT. È anche possibile fatturare dalla scheda del DDT.

Questo modulo è un alternativa al modulo `l10n_it_ddt`, segue la
modalità Odoo di gestire ordini di vendita, prelievi e fatture.

Non è possibile avere installati contemporaneamente `l10n_it_ddt` e
`l10n_it_delivery_note`.

Ci sono due impostazioni possibili.

- Base (predefinita): un prelievo, un DDT.
- Avanzata: più prelievi in un DDT.

**Integrazione Fatturazione Elettronica**

Questo modulo si integra con la fatturazione elettronica italiana (`l10n_it_stock_ddt`).

Aggiunge automaticamente i riferimenti ai DDT nell'XML della FatturaPA, includendo:
- Numero del DDT
- Data del DDT
- Riferimenti alle righe

Il modulo gestisce anche la distinzione tra fatture immediate e differite:
- **TD01 (Fattura immediata)**: quando la fattura ha la stessa data dei DDT collegati
- **TD24 (Fattura differita)**: quando la fattura è emessa in un giorno diverso rispetto ai DDT
