**English**

Mandatory settings:

- An account journal required by the closing transfer account move (e.g.
  "Bolle Doganali").
- An account journal for extraUE supplier invoices, apart from ordinary
  supplier invoices. In this way, extraUE supplier invoices don't appear
  in VAT registries; in this way, VAT registries have no missing
  numbers.
- Create the "Extra UE goods purchases" and add a tax mapping: purchase
  taxes (e.g. 22%) should be mapped to to no one tax. In this way, every
  purchase invoice for extra UE fiscal position don't show taxes in
  lines, according to law.
- A virtual supplier (e.g. "Customs" or "Dogana") for the bill of entry.
- The forwarder as a real supplier.

Optional settings:

- An expense account where recording the bill of entry net amount (e.g.
  "ACQUISTO MERCI ExtraUE").
- An expense account where recording the bill of entry VAT amount, paid
  in advance by the forwarder and declared in the forwarder invoice
  (e.g. "SPESE DOGANALI ANTICIPATE").
- An account tax, with the same VAT rate as the ordinary one (i.e. 22%
  for Italy), applied on the bill of entry net amount (e.g. "22% debito
  ExtraUE"). In this way, bill of entries are highlighted in VAT
  registries due to this tax code.
- An account for delivery expenses, recorded in the forwarder invoice
  (e.g. "SPESE DI TRASPORTO").
- An account for customs duties, recorded in the forwarder invoice (e.g.
  "DIRITTI DOGANALI").
- An account for stamp duties, recorded in the forwarder invoice (e.g.
  "IMPOSTE DI BOLLO").

**Italiano**

Impostazioni obbligatorie:

- Un registro utilizzato per la registrazione di giroconto (ad es.
  "Bolle Doganali" o "Varie") da impostare in configurazione
  contabilità.
- Un imposta con aliquota standard da applicare alla bolla doganale (ad
  es. "22% credito ExtraUE") da impostare in configurazione contabilità.
  In questo modo questa imposta viene evidenziata nei registri IVA.
- Un fornitore "Dogana" per le bolle doganali, da impostare in
  configurazione contabilità.
- Un registro per le fatture dei fornitori extra UE, distinto da quello
  delle fatture passive ordinarie. In questo modo, le fatture dei
  fornitori extra non appariranno nei registri IVA ed i registri IVA non
  avranno numeri mancanti.
- Una posizione fiscale "Acquisti beni extra UE" e aggiungere la
  mappatura: l'imposta d'acquisto (ad es. 22%) deve essere mappata a
  nessuna imposta. In questo modo, ogni fattura passive per questa
  posizione fiscale non avrà imposte sulle righe.
- Il fornitore spedizioniere

Impostazioni opzionali:

- Un conto di costo dove registrare l'importo netto della bolla doganale
  (ad es. "ACQUISTO MERCI ExtraUE"), da associare eventualmente ai
  prodotti acquistati extra UE
- Un conto di costo dove registrare l'importo dell'IVA della bolla
  doganale, pagata in anticipo dello spedizioniere e evidenziata nella
  fattura dello spedizioniere (ad es. "SPESE DOGANALI ANTICIPATE").
- Un conto per le spese di consegna, registrate nella fattura
  spedizioniere (ad es. "SPESE DI TRASPORTO")
- Un conto per i diritti doganali, registrati nella fattura
  spedizioniere (ad es. "DIRITTI DOGANALI")
- Un conto per le imposte di bollo, registrate nella fattura
  spedizioniere (ad es. "IMPOSTE DI BOLLO")
