**Italiano**

Se si utilizza un prodotto KIT (quindi con una distinta base) negli ordini,
Odoo crea dei trasferimenti e DdT che includono i componenti indicati all'intenro
del KIT, e non quel prodotto stesso. Se si fattura direttamente dal DdT, la
fattura di vendita conterrà una riga per ogni componente, creando un po' di confusione.

Questo modulo evita la fatturazione dei coponenti e verifica invece se ci sono dei
prodotti KIT fatturabili negli ordini associati al DdT, procedendo quindi alla loro
fatturazione.

**English**

When using a KIT product in PO and SO, in the picking and in the TD the user will not find the
KIT product but all its components instead. When creating the invoice from TD,
the base module will invoice all individual components with the same description,
creating some confusion.

This module avoids the invoicing of this components and checks instead all KIT
products that are invoiceable in the related SO and will include them in the
invoice.
