**Italiano**

Questo modulo permette di impostare i documenti correlati e il
riferimento amministrazione nell'ordine di vendita (o le sue righe) e
propagarli alla fattura (o le sue righe) durante la creazione della
fattura.

Rispetto al modulo standard `l10n_it_edi_sale`, che riporta in fattura
solo il documento di origine indicato nella testata dell'ordine (tipo,
numero, data, CIG e CUP), questo modulo permette di:

- indicare sull'ordine un numero qualsiasi di documenti correlati
  (ordini, contratti, convenzioni, ricezioni, fatture collegate), gestiti
  dal modulo `l10n_it_edi_related_document`;
- indicare documenti correlati anche sulle singole righe dell'ordine
  (`RiferimentoNumeroLinea`);
- indicare sulle righe dell'ordine il riferimento amministrazione
  (`RiferimentoAmministrazione`), gestito dal modulo
  `l10n_it_edi_extension`.

Alla creazione della fattura i documenti correlati vengono copiati
dall'ordine (e dalle sue righe) alla fattura (e alle sue righe): in caso
di fatturazione parziale ogni fattura riceve la propria copia.

**English**

This module allows to set related documents and Admin. Ref. in the sale
order (or its lines) and propagate them to the invoice (or its lines)
during invoice creation.

Compared to the standard `l10n_it_edi_sale` module, which only
propagates to the invoice the origin document set in the sale order
header (type, number, date, CIG and CUP), this module allows to:

- set any number of related documents on the sale order (orders,
  contracts, agreements, receptions, related invoices), as managed by
  the `l10n_it_edi_related_document` module;
- set related documents on the single order lines too
  (`RiferimentoNumeroLinea`);
- set the Admin. Ref. (`RiferimentoAmministrazione`) on the order
  lines, as managed by the `l10n_it_edi_extension` module.

When the invoice is created, the related documents are copied from the
sale order (and its lines) to the invoice (and its lines): with partial
invoicing, each invoice gets its own copy.
