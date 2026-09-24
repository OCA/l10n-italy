**Italiano**

La maschera "Contabilità / Configurazione / Piano dei conti" è stata
arricchita con due nuovi campi "Associa a Bilancio UE / Dare" e ".../
Avere" che consentono di definire la riclassificazione dei conti,
riclassificazione che viene impostata a valori predefiniti durante
l’installazione del modulo. Dei due campi "Dare" e "Avere" uno solo dei
due è obbligatorio ai fini del report e in caso siano presenti entrambi
vengono usati in base al segno del saldo del valore annuale del conto
contabile.

La nuova voce di menù "Contabilità / Rendicontazione / Bilancio UE"
consente di selezionare il periodo e scegliere la modalità di
esportazione del Bilancio UE. Nel wizard di “Bilancio UE” sono presenti
le seguenti opzioni di generazione:

- Visualizza valori \[2 decimali di Euro / unità di Euro\]: consente di
  stampare i valori del bilancio in Euro (con due decimali) o in unità
  di Euro (senza decimali). In caso si selezioni “unità di Euro” gli
  eventuali delta da arrotondamenti vengono riportati in automatico su
  due apposite voci (una nel Passivo e una nel Conto Economico). I saldi
  dei conti contabili verranno stampati comunque con 2 decimali
- Nascondere conti a 0: consente di non visualizzare i conti contabili
  con saldo a 0 e che quindi non influiscono nel calcolo delle voci del
  bilancio. Il bilancio UE verrà comunque visualizzato completo, con
  anche le voci con importo 0
- Solo registrazioni confermate: per utilizzare solo le registrazioni
  contabili confermate (ignora bozze e annullate)
- Ignora registrazioni di chiusura: consente di stampare un Bilancio UE
  corretto anche in caso sia già stata effettuata la chiusura
  d’esercizio e quindi tutti i conti contabili siano a saldo 0 al 31/12.
  Se per effettuare la chiusura d’esercizio è stato utilizzato il modulo
  “account_fiscal_year_closing”, questa opzione consente di ignorare le
  registrazioni contabili di chiusura

**English**

The "Accounting / Configuration / Chart of Accounts" mask has been
enriched with two new fields "Match to Financial statement EU / Debit"
and "... / Credit" that allow you to define the reclassification of
accounts, a reclassification that is set to default values during
installation of the module. Of the two fields "Debit" and "Credit" only
one of the two is mandatory for the purposes of the report and in the
case are present both are used according to the sign of the financial
statements of the annual value of accounting account.

The new menu item "Accounting / Reporting / Financial statement EU"
allows you to select the period and choose how to export the EU
financial statements. The following generation options are present in
the "Financial statement EU" wizard:

- Values show as \[2 decimals Euro / Euro units\] : allows to print the
  values in Euros (with two decimals) or in Euro units (without
  decimals). If "Euro units" is selected, any delta from rounding is
  automatically reported on two specific Items (one in the Liabilities
  and one in the Income Statement).
- Hide account with amount 0: allows to not display the accounts with a
  balance at 0 and which therefore have no influence on the calculation
  of the financial statements items. The financial statements will be
  anyway displayed complete, even then items with amount 0
- Use only posted registration: to use confirmed postings only (ignore
  drafts and cancelled)
- Ignore closing registration: allows you to print a correct EU
  financial statements even if the year-end has already been closed and
  therefore all accounting accounts have a balance of 0 as at 31/12. If
  the "account_fiscal_year_closing" module was used to carry out the
  year-end closing, this option allows you to ignore the closing moves
