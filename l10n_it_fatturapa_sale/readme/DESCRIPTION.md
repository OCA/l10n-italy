**Italiano**

Questo modulo permette di impostare i documenti correlati e il
riferimento amministrazione nell'ordine di vendita (o le sue righe) e
propagarli alla fattura (o le sue righe) durante la creazione della
fattura.

Inoltre, se il modo di pagamento è RiBa (MP12) e una banca ricevente è impostata nell'ordine di vendita, questa viene automaticamente rimossa durante la creazione della fattura. Questo comportamento è stato implementato per evitare confusione, poiché la banca ricevente per RiBa viene decisa in una fase successiva. Per ulteriori dettagli, consultare la seguente issue su GitHub:
https://github.com/OCA/l10n-italy/issues/4814

**English**

This module allows to set related documents and Admin. Ref. in the sale
order (or its lines) and propagate them to the invoice (or its lines)
during invoice creation.

Additionally, if the payment method is RiBa (MP12) and a recipient bank is set in the sale order, it is automatically removed during invoice creation. This behavior was implemented to avoid confusion, as the recipient bank for RiBa is decided at a later stage. For more details, refer to the following GitHub issue:
https://github.com/OCA/l10n-italy/issues/4814
