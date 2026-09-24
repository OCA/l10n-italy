**Italiano**

**Termini di pagamento**

Le fatture da incassare con RiBa devono avere un termine di pagamento con
l'opzione *RiBa* attiva. Nello stesso termine si può indicare l'importo delle
*Spese di incasso RiBa* da addebitare al cliente.

**Spese di incasso**

Se il termine di pagamento ha un importo di *Spese di incasso RiBa*, alla
conferma della fattura cliente viene aggiunta una riga di spese per ogni
scadenza, a meno che il cliente non abbia già delle scadenze nello stesso
mese: le spese vengono addebitate una volta al mese per cliente. Le righe di
spese vengono tolte se la fattura viene riportata in bozza o duplicata.

Il prodotto di tipo servizio da usare per queste righe va indicato in
*Impostazioni → Fatturazione*, nella sezione *Spese di incasso RiBa* in fondo
alla pagina.

**Dati bancari e fiscali**

Per esportare il file RiBa servono:

- sul conto bancario aziendale indicato nella configurazione RiBa, l'IBAN e il
  *Codice SIA*, cioè il codice dell'azienda nel sistema interbancario;
- la partita IVA o il codice fiscale dell'azienda;
- per ogni cliente, la partita IVA o il codice fiscale, e un conto bancario
  con IBAN oppure con ABI e CAB della banca.

Nelle fatture clienti con termine di pagamento RiBa il *Conto bancario RiBa*
viene proposto dal primo conto bancario del cliente.

**Clienti e fornitori**

Nella scheda *Fatturazione* del contatto, gruppo *RiBa*, l'opzione *Raggruppa
per cliente* fa confluire in un'unica riga della distinta le scadenze del
cliente con la stessa data.

Per i fornitori con un termine di pagamento RiBa, nella scheda *Vendite e
acquisti*, gruppo *Acquisti*, compare il *Conto bancario aziendale* su cui la
banca addebita le loro RiBa: viene proposto nelle fatture fornitore, nel campo
*Conto bancario aziendale per fornitore*.

**Configurazione RiBa**

In *Fatturazione → Configurazione → Pagamenti online → Configurazione RiBa*
(menu visibile agli amministratori della contabilità) si definiscono una o più
configurazioni. Per ognuna si indicano:

- *Descrizione*, *Modalità emissione* (*Salvo buon fine* o *Al dopo incasso*)
  e *Conto bancario*, cioè il conto aziendale presso cui si presentano le RiBa;
- **Accettazione**, obbligatoria in entrambe le modalità: *Registro
  accettazione* e *Conto accettazione*. Il conto accoglie gli effetti accettati
  dalla banca (ad esempio "Effetti attivi" o "RiBa all'incasso"): di norma è di
  tipo *Crediti*, e deve essere riconciliabile, perché nel caso *Al dopo
  incasso* è il conto che il movimento di conto corrente dell'incasso va a
  chiudere;
- **Accredito**, solo per il *Salvo buon fine*: *Registro accrediti*, *Conto
  RiBa*, *Conto banca C/C* e *Conto spese bancarie*. Il *Conto RiBa* (ad
  esempio "Banche c/RiBa all'incasso") rappresenta il credito verso la banca, di
  cui l'azienda può disporre (ad esempio per andare in negativo sul conto
  corrente con meno costi) fino a quando la banca non paga effettivamente. Deve
  essere riconciliabile, perché è il conto che il movimento di conto corrente
  dell'incasso va a chiudere, e non deve essere di tipo *Banca e cassa*. Gli
  altri due conti servono per le spese di accredito;
- **Insoluto**: *Registro insoluti*, di tipo *Banca*, *Valore tariffa*, cioè le
  spese di insoluto proposte, *Conto effetti insoluti* (ad esempio "Crediti
  insoluti") e *Conto spese di protesto*.

**English**

**Payment terms**

Invoices to be collected with RiBa need a payment term with the *RiBa* option
enabled. The same payment term can have an amount of *RiBa Collection Fees* to
be charged to the customer.

**Collection fees**

If the payment term has an amount of *RiBa Collection Fees*, a fees line is
added for each due date when the customer invoice is confirmed, unless the
customer already has due dates in the same month: fees are charged once a
month per customer. Fees lines are removed when the invoice is reset to draft
or duplicated.

The service product to be used for these lines is set in *Settings →
Invoicing*, in the *RiBa Collection Fees* section at the bottom of the page.

**Bank and fiscal data**

Exporting the RiBa file requires:

- on the company bank account set in the RiBa configuration, the IBAN and the
  *SIA Code*, that is the code of the company in the interbank system;
- the VAT or fiscal code of the company;
- for each customer, the VAT or fiscal code, and a bank account with the IBAN
  or with the ABI and CAB of the bank.

In customer invoices with a RiBa payment term, the *RiBa Bank Account* is
proposed from the first bank account of the customer.

**Customers and suppliers**

In the *Invoicing* tab of the contact, *RiBa* group, the *Group RiBa* option
merges into a single slip line the due dates of the customer having the same
date.

For suppliers with a RiBa payment term, the *Sales & Purchase* tab, *Purchase*
group, shows the *Company Bank Account* where the bank debits their RiBa: it is
proposed in vendor bills, in the *Company Bank Account for Supplier* field.

**RiBa configuration**

In *Invoicing → Configuration → Online Payments → RiBa Configuration* (menu
visible to accounting administrators) one or more configurations are defined.
Each one has:

- *Description*, *Issue Mode* (*Subject To Collection* or *After Collection*)
  and *Bank Account*, that is the company account where the RiBa are presented;
- **Acceptance**, required in both modes: *Acceptance Journal* and *Acceptance
  Account*. The account holds the bills accepted by the bank (for instance
  "Bills receivable"): it is usually a *Receivable* account, and it has to be
  reconcilable, because in *After Collection* mode it is the account closed by
  the collection entry of the current account;
- **Credit**, only for *Subject To Collection*: *Credit Journal*, *RiBa
  Account*, *A/C Bank Account* and *Bank Fees Account*. The *RiBa Account*
  holds the credit towards the bank, that the company can dispose of (for
  instance to go below zero on the current account at a lower cost) until the
  bank actually pays it. It has to be reconcilable, because it is the account
  closed by the collection entry of the current account, and it must not be a
  *Bank and Cash* account. The other two accounts are used for the credit fees;
- **Past Due**: *Past Due Journal*, of type *Bank*, *Fee Amount*, that is the
  proposed past due fees, *Past Due Bills Account* and *Protest Fee Account*.
