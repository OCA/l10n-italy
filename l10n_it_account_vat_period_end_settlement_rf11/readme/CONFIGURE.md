**Italiano**

Prima di poter liquidare l'IVA 74-ter occorre configurare le imposte
usate per le operazioni a margine. Servono **due imposte** allo 0%: una
di vendita e una di acquisto.

In *Contabilità → Configurazione → Imposte* creare (o modificare) le due
imposte con:

1.  **Calcolo** = "Percentuale" e **Importo** = `0`: l'IVA non è esposta
    in fattura (regime del margine).
2.  Poiché sono imposte italiane allo 0%, nella scheda "Fattura
    elettronica" impostare **Esonero** = `N5` ("Regime del margine / IVA
    non esposta in fattura") e il relativo **Riferimento normativo** (es.
    "Art. 74-ter DPR 633/72"). Senza questi dati l'imposta non può essere
    salvata.
3.  Abilitare la casella **74ter** (`is_tax_74ter`).
4.  In **Importo 74ter** (`tax_74ter_amount`) indicare l'aliquota reale
    da scorporare dal margine (es. `22`). Tutte le imposte 74-ter devono
    avere la **stessa** aliquota, e può esistere **una sola** imposta
    74-ter di tipo vendita.

Sulla sola imposta di **vendita** 74-ter configurare inoltre:

- **Conto ricavi 74ter** (`tax_74_ter_income_account_id`): un conto di
  ricavo (rettifica ricavi), usato in Dare nella scrittura di
  liquidazione;
- nelle righe di ripartizione (scheda "Definizione") l'imposta deve
  puntare a **un solo** conto IVA a debito (es. "IVA C/Vendite"): è il
  conto usato in Avere nella scrittura. Se non è definito, o ne è
  definito più d'uno, la generazione della scrittura di liquidazione
  segnala un errore.

A questo punto usare l'imposta di vendita sulle fatture di vendita dei
viaggi e l'imposta di acquisto sulle fatture dei costi del viaggio: la
liquidazione 74-ter accumulerà la base imponibile di queste imposte per
il calcolo "base su base".

**English**

Before you can settle the 74-ter VAT you have to configure the taxes
used for margin-scheme operations. You need **two** 0% taxes: one for
sales and one for purchases.

In *Accounting → Configuration → Taxes* create (or edit) the two taxes
with:

1.  **Tax Computation** = "Percentage" and **Amount** = `0`: VAT is not
    shown on the invoice (margin scheme).
2.  Because they are 0% Italian taxes, on the "Electronic Invoicing" tab
    set **Exoneration** = `N5` ("Regime del margine / IVA non esposta in
    fattura") and the related **Law Reference** (e.g. "Art. 74-ter DPR
    633/72"). Without these the tax cannot be saved.
3.  Enable the **74ter** checkbox (`is_tax_74ter`).
4.  In **74ter Amount** (`tax_74ter_amount`) enter the real rate to be
    extracted from the margin (e.g. `22`). All 74-ter taxes must share
    the **same** rate, and there can be **only one** sale 74-ter tax.

On the **sale** 74-ter tax only, also configure:

- **74ter Income Account** (`tax_74_ter_income_account_id`): a revenue
  account (revenue adjustment), used on the debit side of the settlement
  entry;
- in the repartition lines ("Definition" tab) the tax must point to
  **exactly one** VAT-on-sales account (e.g. "IVA C/Vendite"): it is the
  account used on the credit side of the entry. If it is missing, or more
  than one is defined, generating the settlement entry raises an error.

Then use the sale tax on travel sale invoices and the purchase tax on the
travel cost bills: the 74-ter settlement will accumulate the taxable base
of these taxes for the "base su base" computation.
