**Italiano**

Consultare anche il file README del modulo l10n_it_fatturapa.

Per ciascun fornitore è possibile impostare il "Livello dettaglio
e-fatture":

> - Livello minimo: la fattura fornitore viene creata senza righe, che
>   dovranno essere create dall'utente in base a quanto indicato nella
>   fattura elettronica
> - Livello massimo: le righe della fattura fornitore verranno generate
>   a partire da tutte quelle presenti nella fattura elettronica

Nella scheda fornitore è inoltre possibile impostare il "Prodotto
predefinito per e-fattura": verrà usato, durante la generazione delle
fatture fornitore, quando non sono disponibili altri prodotti adeguati.
Il conto e l'imposta della riga fattura verranno impostati in base a
quelli configurati nel prodotto.

Tutti i codici prodotto usati dai fornitori possono essere impostati
nella relativa scheda, in

Magazzino → Prodotti

Se il fornitore specifica un codice noto nell'XML, questo verrà usato
dal sistema per recuperare il prodotto corretto da usare nella riga
fattura, impostando il conto e l'imposta collegati.

**English**

See also the README file of l10n_it_fatturapa module.

For every supplier, it is possible to set the 'E-bills Detail Level':

> - Minimum level: Bill is created with no lines; User will have to
>   create them, according to what specified in the electronic bill
> - Maximum level: Every line contained in electronic bill will create a
>   line in bill

Moreover, in supplier form you can set the 'E-bill Default Product':
this product will be used, during generation of bills, when no other
possible product is found. Tax and account of bill line will be set
according to what configured in the product.

Every product code used by suppliers can be set, in product form, in

Inventory → Products

If supplier specifies a known code in XML, the system will use it to
retrieve the correct product to be used in bill line, setting the
related tax and account.
