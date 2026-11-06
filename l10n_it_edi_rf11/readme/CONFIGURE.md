**English**

To emit 74-ter self-billing electronic invoices:

1. On the company record (*Settings > Users & Companies > Companies > your
   company*), set **Tax System** to `[RF11] Agenzie viaggi e turismo
   (art.74-ter, DPR 633/72)`. The field is shown right after the **Codice
   Fiscale** field and only when the company **Country** is Italy.
2. Configure the purchase taxes used for the agency commissions. Both carry an
   explicit **nature** (`Exoneration`); the nature written in the FatturaPA is
   read from the tax, not hard-coded. The simplest way to create them is to
   **duplicate an existing reverse-charge purchase tax** (*Accounting >
   Configuration > Taxes*, then *Action ▸ Duplicate*):
   - **Extra-EU / non-taxable**: duplicate **`0% S RC`** and set
     **Exoneration** to `N3.6` with its **Law Reference** (e.g. `Art. 74-ter,
     DPR 633/72`). It is exported as-is (Natura N3.6, no VAT).
   - **Intra-EU**: duplicate **`22% S RC`** and set **Exoneration** to `N6.9`
     with its **Law Reference**. The 22% is kept in the purchase and sales VAT
     registers (the reverse-charge repartition of the copied tax); the module
     emits the FatturaPA **without VAT and with Natura N6.9** automatically (the
     22% stays only in the accounting).

   `S` in the tax name stands for *Servizi* (services), which is what agency
   commissions are. If a copied tax's report grids were authored for a
   different case, have your accountant confirm they fit the 74-ter operation.
3. For **each** travel agency you work with, on its contact tick **74ter
   agency** and set its SdI destination code (*Codice Destinatario*); it is used
   as the `CodiceDestinatario` of the invoices issued on its behalf.

The *Terzo Intermediario o Soggetto Emittente* block is filled automatically
with the **company's own data** (the tour operator issues the invoice on behalf
of the agency), together with `SoggettoEmittente` = **CC**. Leave the company
**Third Party/Sender** (`l10n_edi_it_sender_partner`) **empty**: it is only for
ordinary invoices actually transmitted by a third party and is ignored for
74-ter documents.

For the "invoice paid by the agency" feature:

1. In *Settings > Accounting*, set **Journal for agencies payments**.
2. On a customer contact, set **Agency** and, optionally, tick **Invoices
   paid by agency** so it is proposed automatically on invoices.

**Italiano**

Per emettere le fatture elettroniche in autofattura 74-ter:

1. Sull'anagrafica azienda (*Impostazioni > Utenti e aziende > Aziende > la
   propria azienda*), impostare il **Regime fiscale** su `[RF11] Agenzie viaggi
   e turismo (art.74-ter, DPR 633/72)`. Il campo è mostrato subito dopo il
   **Codice Fiscale** e solo se il **Paese** dell'azienda è Italia.
2. Configurare le imposte di acquisto usate per le provvigioni dell'agenzia.
   Entrambe portano una **natura** esplicita (`Esenzione`); la natura scritta
   nella FatturaPA viene letta dall'imposta, non è cablata nel codice. Il modo
   più semplice per crearle è **duplicare un'imposta di acquisto reverse charge
   esistente** (*Contabilità > Configurazione > Imposte*, poi *Azione ▸
   Duplica*):
   - **Extra-UE / non imponibile**: duplicare **`0% S RC`** e impostare
     l'**Esenzione** su `N3.6` con il relativo **Riferimento normativo** (es.
     `Art. 74-ter, DPR 633/72`). Viene esportata così com'è (Natura N3.6, senza
     IVA).
   - **Intra-UE**: duplicare **`22% S RC`** e impostare l'**Esenzione** su
     `N6.9` con il relativo **Riferimento normativo**. Il 22% resta nei registri
     IVA acquisti e vendite (la ripartizione reverse charge dell'imposta
     copiata); il modulo emette la FatturaPA **senza IVA e con Natura N6.9**
     automaticamente (il 22% resta solo in contabilità).

   La `S` nel nome dell'imposta indica *Servizi*, che è la natura delle
   provvigioni d'agenzia. Se le griglie di dichiarazione dell'imposta copiata
   erano pensate per un altro caso, farle verificare al commercialista per
   l'operazione 74-ter.
3. Per **ogni** agenzia viaggi con cui si lavora, sull'anagrafica spuntare
   **Agenzia 74ter** e impostare il suo Codice Destinatario SdI; viene usato
   come `CodiceDestinatario` delle fatture emesse per suo conto.

Il blocco *Terzo Intermediario o Soggetto Emittente* viene valorizzato
automaticamente con i **dati dell'azienda** stessa (il tour operator emette la
fattura per conto dell'agenzia), insieme a `SoggettoEmittente` = **CC**.
Lasciare **vuoto** il **Terzo Intermediario o Soggetto Emittente**
(`l10n_edi_it_sender_partner`) dell'azienda: serve solo per le fatture ordinarie
effettivamente trasmesse da un terzo e viene ignorato per i documenti 74-ter.

Per la funzione "fattura pagata dall'agenzia":

1. In *Impostazioni > Contabilità*, impostare il **Registro pagamenti
   agenzie**.
2. Sull'anagrafica del cliente, impostare l'**Agenzia** e, facoltativamente,
   spuntare **Fatture pagate dall'agenzia** per proporlo automaticamente sulle
   fatture.
