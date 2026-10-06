**Italiano**

**Fatture**

Le fatture clienti con termine di pagamento RiBa devono avere il *Conto
bancario RiBa* del cliente, altrimenti non possono essere confermate. Alla
conferma vengono aggiunte le eventuali spese di incasso.

Nella lista delle fatture, la colonna *Valore scoperto* mostra l'esposizione
verso il cliente, cioè l'importo delle scadenze RiBa della fattura non ancora
raggiunte.

**Emissione della distinta**

Il menu RiBa si trova nell'applicazione *Fatturazione*. In *RiBa → Emissione*
sono elencate le scadenze RiBa delle fatture confermate; i filtri predefiniti
mostrano quelle *RiBa da emettere* e *Da riconciliare*. Selezionate le
scadenze, l'azione *Emetti RiBa* chiede la *Configurazione* da usare e crea la
distinta in bozza.

Per i clienti con l'opzione *Raggruppa per cliente*, le scadenze con la stessa
data diventano un'unica riga della distinta. Se però le fatture selezionate
hanno CIG o CUP diversi, nessuna scadenza viene raggruppata e si crea una riga
per ogni scadenza.

In *RiBa → Presentazione RiBa* si può indicare un *Importo presentazione*:
vengono proposte le scadenze in ordine di data fino a raggiungere
quell'importo, così da emettere una distinta entro il limite concordato con la
banca.

**La distinta**

Gli stati della distinta sono *Bozza*, *Accettata*, *Accreditata* (solo per il
*Salvo buon fine*), *Pagata*, *Insoluta* e *Annullata*. Le registrazioni
contabili generate sono riepilogate nella scheda *Contabilità*, sia della
distinta sia delle sue righe. Il pulsante *Righe distinta* apre le righe in una
vista dedicata, disponibile anche in *RiBa → Dettaglio distinte*, per operare
sulle singole righe invece che su tutta la distinta.

Dalla distinta si stampa il documento da consegnare alla banca (*Stampa
distinta*) e si esporta il file RiBa (azione *Esporta RiBa*), che richiede i
dati bancari e fiscali descritti nella configurazione.

**Accettazione**

Quando la banca accetta la distinta si usa *Segna come accettata*. La *Data
accettazione* è obbligatoria ed è la data delle registrazioni di accettazione.
Per ogni riga della distinta viene creata nel *Registro accettazione* una
registrazione con:

- in DARE il *Conto accettazione*, per l'importo della riga, con la data di
  scadenza della RiBa;
- in AVERE il conto crediti della fattura, che viene riconciliato.

In entrambe le modalità, quindi, all'accettazione la fattura risulta pagata:
il credito passa dal cliente al conto effetti, fino all'incasso o
all'insoluto.

**Accredito (Salvo buon fine)**

Quando la banca accredita l'importo della distinta si usa *Segna come
accreditata*: i conti vengono proposti dalla configurazione. L'*Importo
accredito*, in sola lettura, è il totale della distinta; nel *Valore tariffe
banca* si indicano le eventuali spese, che richiedono il *Conto banca C/C* e il
*Conto spese bancarie*. La registrazione viene creata nel *Registro accrediti*
e confermata subito, alla *Data accredito* indicata nel wizard (proposta dalla
distinta o in mancanza oggi, e non precedente alla data di accettazione), che
viene riportata sulla distinta. Contiene:

- in DARE il *Conto RiBa*, con una riga per ogni scadenza della distinta;
- in AVERE il *Conto accettazione*, riconciliato con le registrazioni di
  accettazione;
- se ci sono spese, in DARE il *Conto spese bancarie* e in AVERE il *Conto
  banca C/C*.

L'accredito rappresenta un credito verso la banca su un conto a parte, di cui
l'azienda può disporre fino all'incasso effettivo.

**Incasso della distinta**

Il modulo non genera nessuna registrazione di incasso: la distinta risulta
pagata quando il movimento di conto corrente effettivo, in riconciliazione
bancaria, chiude il credito verso la banca.

Le righe da riconciliare sono elencate nella scheda *Contabilità* della
distinta, sotto *Righe da incassare*:

- *Salvo buon fine*: le righe in DARE del *Conto RiBa* della registrazione di
  accredito, una per scadenza;
- *Al dopo incasso*: le righe in DARE del *Conto accettazione* delle
  registrazioni di accettazione.

Ogni movimento della banca chiude le righe delle scadenze che paga, e i
pagamenti sono gestiti come in fattura: *Importo pagato* e *Importo residuo* mostrano quanto
la banca ha già pagato e quanto deve ancora pagare, e lo *Stato pagamento*
passa a *Parzialmente pagata* e poi a *Pagata*. Quando il residuo è zero la
distinta passa in stato *Pagata*, e la *Data pagamento* riporta la data della
registrazione che l'ha incassata. Se la riconciliazione viene annullata, la
distinta torna in stato *Accreditata* (o *Accettata* nel caso *Al dopo
incasso*).

Le righe della distinta non hanno un pulsante per l'incasso e restano in stato
*Accreditata* (o *Confermata* nel caso *Al dopo incasso*): l'unica operazione
che le riguarda singolarmente è l'insoluto.

**Insoluto**

Nei giorni successivi alla scadenza la banca può comunicare l'insoluto di una
o più ricevute. L'insoluto è un'operazione manuale, da registrare per ogni riga
interessata con il pulsante *Segna come insoluta*, dalla distinta o da *RiBa →
Dettaglio distinte*.

Il wizard propone i conti della configurazione, l'*Importo effetti insoluti*
pari all'importo della riga e, come spese di insoluto, il *Valore tariffa*
della configurazione nel campo *Valore scaduto tariffe dovute*. Con *Addebita
i costi al cliente* le spese vengono registrate con il cliente. La
registrazione viene creata nel *Registro insoluti*, alla *Data* indicata o in
mancanza alla scadenza della riga, e contiene:

- in DARE il *Conto effetti insoluti*, con il cliente;
- in AVERE il *Conto RiBa* (*Salvo buon fine*) o il *Conto accettazione* (*Al
  dopo incasso*), riconciliato con la riga da incassare della sua scadenza
  (*Salvo buon fine*) o della sua accettazione (*Al dopo incasso*): il residuo
  della distinta scende come per un incasso;
- se ci sono spese, in DARE il conto spese proposto dal *Conto spese di
  protesto* e in AVERE il *Conto banca C/C*.

La fattura viene scollegata dall'accettazione, torna da pagare e compare in
*RiBa → Fatture insolute*; la riga e la distinta passano in stato *Insoluta*.
Il pulsante *Salta e conferma insoluto* porta invece la riga in stato
*Insoluta* senza creare la registrazione di insoluto, cancellando quella di
accettazione.

Il movimento di conto corrente con cui la banca addebita l'insoluto e le
relative spese va poi riconciliato manualmente. Per velocizzare l'operazione
conviene creare un modello di riconciliazione (*Fatturazione → Configurazione
→ Banche → Modelli di riconciliazione*) che proponga il *Conto effetti
insoluti* e il conto delle spese.

**Annullamento**

Il pulsante *Annulla* cancella le registrazioni di accettazione, accredito e
insoluto della distinta, dopo averle riportate in bozza: le fatture tornano da
pagare. Le distinte *Salvo buon fine* annullate possono essere riportate in
bozza con *Reimposta a bozza*.

**English**

**Invoices**

Customer invoices with a RiBa payment term need the *RiBa Bank Account* of the
customer, otherwise they cannot be confirmed. When they are confirmed, the
collection fees, if any, are added.

In the invoices list, the *Open Amount* column shows the exposure towards the
customer, that is the amount of the RiBa due dates of the invoice that have not
been reached yet.

**Issuing the slip**

The RiBa menu is in the *Invoicing* app. *RiBa → Issue* lists the RiBa due
dates of confirmed invoices; the default filters show the ones *RiBa To Issue*
and *To Reconcile*. After selecting the due dates, the *Issue RiBa* action asks
for the *Configuration* to be used and creates the slip in draft.

For customers with the *Group RiBa* option, the due dates having the same date
become a single slip line. If the selected invoices have different CIG or CUP,
though, no due date is grouped and a line is created for each due date.

*RiBa → Presentation Riba* accepts a *Presentation Amount*: the due dates are
proposed by date until that amount is reached, to issue a slip within the limit
agreed with the bank.

**The slip**

The states of the slip are *Draft*, *Accepted*, *Credited* (only for *Subject
To Collection*), *Paid*, *Past Due* and *Canceled*. The journal entries created
are summarized in the *Accounting* tab, both of the slip and of its lines. The
*Slip lines* button opens the lines in a dedicated view, available in *RiBa →
Slips Detail* too, to work on single lines instead of the whole slip.

The slip can be printed for the bank (*Print Slip*) and the RiBa file can be
exported (*Export RiBa* action), which requires the bank and fiscal data
described in the configuration.

**Acceptance**

When the bank accepts the slip, use *Mark as Accepted*. The *Acceptance Date*
is required and it is the date of the acceptance entries. For each line of the
slip an entry is created in the *Acceptance Journal*, with:

- in debit the *Acceptance Account*, for the amount of the line, with the due
  date of the RiBa;
- in credit the receivable account of the invoice, that is reconciled.

In both modes, then, the invoice is paid at acceptance: the credit moves from
the customer to the bills account, until the collection or the past due.

**Credit (Subject To Collection)**

When the bank credits the amount of the slip, use *Mark as Credited*: the
accounts are proposed from the configuration. The *Credit Amount*, read only,
is the total of the slip; the *Bank Fees Amount* holds the fees, if any, that
need the *A/C Bank Account* and the *Bank Fees Account*. The entry is created
in the *Credit Journal* and posted right away, at the *Credit Date* set in the
wizard (proposed from the slip or else today, and not before the acceptance
date), that is written on the slip. It has:

- in debit the *RiBa Account*, with a line for each due date of the slip;
- in credit the *Acceptance Account*, reconciled with the acceptance entries;
- if there are fees, the *Bank Fees Account* in debit and the *A/C Bank
  Account* in credit.

The credit is a credit towards the bank on a separate account, that the
company can dispose of until the actual collection.

**Collecting the slip**

The module does not create any collection entry: the slip is paid when the
actual entry of the current account, in the bank reconciliation, closes the
credit towards the bank.

The lines to be reconciled are listed in the *Accounting* tab of the slip,
under *Lines to Collect*:

- *Subject To Collection*: the debit lines of the *RiBa Account* in the credit
  entry, one for each due date;
- *After Collection*: the debit lines of the *Acceptance Account* in the
  acceptance entries.

Each entry of the bank closes the lines of the due dates it pays, and payments
are managed as in invoices: *Paid Amount* and *Amount Due* show how much the bank has
already paid and how much is left, and the *Payment Status* goes to *Partially
Paid* and then to *Paid*. When nothing is left the slip becomes *Paid*, and the
*Payment Date* is the date of the entry that collected it. If the
reconciliation is undone, the slip goes back to *Credited* (or *Accepted* for
*After Collection*).

The lines of the slip have no button to collect them and stay *Credited* (or
*Confirmed* for *After Collection*): the only operation on a single line is the
past due.

**Past due**

In the days after the due date the bank can report that one or more receipts
are past due. The past due is a manual operation, to be recorded for each line
with the *Mark as Past Due* button, from the slip or from *RiBa → Slips
Detail*.

The wizard proposes the accounts of the configuration, the *Past Due Bills
Amount* equal to the amount of the line and, as past due fees, the *Fee Amount*
of the configuration in the *Past Due Fees Amount* field. With *Charge the
customer the costs* the fees are recorded with the customer. The entry is
created in the *Past Due Journal*, at the *Date* set in the wizard or else at
the due date of the line, and has:

- in debit the *Past Due Bills Account*, with the customer;
- in credit the *RiBa Account* (*Subject To Collection*) or the *Acceptance
  Account* (*After Collection*), reconciled with the line to collect of its
  due date (*Subject To Collection*) or of its acceptance (*After
  Collection*): the amount due of the slip decreases as for a collection;
- if there are fees, the fees account proposed from the *Protest Fee Account*
  in debit and the *A/C Bank Account* in credit.

The invoice is unlinked from the acceptance, it is due again and it is listed
in *RiBa → Past Due Invoices*; the line and the slip become *Past Due*. The
*Skip and Confirm Past Due* button instead sets the line as *Past Due* without
creating the past due entry, deleting the acceptance one.

The entry of the current account with which the bank debits the past due and
its fees has to be reconciled manually. A reconciliation model (*Invoicing →
Configuration → Banks → Reconciliation Models*) proposing the *Past Due Bills
Account* and the fees account makes this faster.

**Cancelling**

The *Cancel* button deletes the acceptance, credit and past due entries of the
slip, after resetting them to draft: the invoices are due again. Canceled
*Subject To Collection* slips can be reset to draft with *Reset to Draft*.
