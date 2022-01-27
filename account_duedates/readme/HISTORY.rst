12.0.4.8.31 (2022-01-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Update dependencies

12.0.4.8.30 (2022-01-20)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Standard OCA
* [IMP] sale.order model moved to account_duedate_sale module

12.0.4.8.29 (2021-12-22)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Hotfix0.23 Rimosso ricalcolo scadenze nelle creazione fattura

12.0.4.8.28 (2021-12-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rimosso gestione campi conti bancari

12.0.4.8.27 (2021-12-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestito ricalcolo delle scadenze in create e write

12.0.4.8.26 (2021-12-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Aggiunto filtri "In distinta" e "Effetti incassati"

12.0.4.8.25 (2021-12-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Reimpostato filtro "Non in distinta"

12.0.4.8.24 (2021-11-23)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato e gestito aggiornamento campi banca aziendale e banca partner
* [FIX] Impostato metodo di pagamento per le scadenze NON tecniche

12.0.4.8.23 (2021-11-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostato campo banca aziendale

12.0.4.8.22 (2021-10-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostato in elenco scadenze in stampa fattura il metodo di pagamento

12.0.4.8.21 (2021-10-05)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostato  elenco scadenze in stampa fattura qualora siano più di una

12.0.4.8.20 (2021-09-29)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestito registrazione contabile fattura a zero

12.0.4.8.19 (2021-09-29)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] POW-509 Gestito errore singleton

12.0.4.8.18 (2021-08-25)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Missed dependency: "sale" / Manca dipendenza "ordini clienti"

12.0.4.8.17 (2021-08-19)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] account_duedates: Refactoring metodo di pagamento 'tax' per scadenze tecniche

12.0.4.8.16 (2021-08-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] account_duedates: Impostata dipendenza mancante

12.0.4.8.15 (2021-08-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] account_duedates: POW-465 Gestito errore utente bloccante

12.0.4.8.14 (2021-07-13)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] account_duedates: Aggiornato ordine della generazione dei movimenti contabili
* [FIX] account_duedates: Impostato 15 giorni la ritenuta dopo l'ultima scadenza

12.0.4.8.13 (2021-07-05)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] account_duedates: Impostato manager per la gestione delle scadenze Reverse charge

12.0.4.8.12 (2021-06-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] account_duedates: Impostato manager per la gestione delle scadenze

12.0.4.8.11 (2021-06-25)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] account_duedates: corretto errore che impediva il salvataggio di una registrazione contabile una volta modificata

12.0.4.7.11 (2021-06-22)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] account_duedates: campo non duplicabile 'Data di decorrenza'

12.0.4.7.10 (2021-06-21)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] account_duedates: corretto bug nella creazione fattura

12.0.4.7.9 (2021-06-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostata gestione scadenze con split payment

12.0.4.7.8 (2021-06-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] account_duedates: corretto bug che impediva di salvare correttamente registrazioni contabili di tipo diverso da fattura / nota di credito

12.0.3.3.8 (2021-05-04)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostato cron che aggiorna i periodi dedicati all'esclusione delle scadenze

12.0.3.3.7 (2021-05-04)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretto bug nel metodo che verifica l'intervallo delle esclusioni

12.0.3.3.6 (2021-04-29)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Gestito loop in tutti i multi

12.0.3.3.5 (2021-04-23)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostato e gestito gli intervalli dei giorni di esclusione

12.0.3.3.4 (2021-04-20)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Tolto la possibilità di andare a capo per il campo Conto

12.0.3.3.3 (2021-04-19)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rinominato la colonna 'Saldo' in 'Importo'

12.0.3.3.2 (2021-04-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Integrazione delle modifiche fatte in 12.0.3.2.1_hot

12.0.3.2.2 (2021-04-06)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Aggiornamento campi nell'elenco di Pagamenti e scadenze

12.0.3.2.1_hot (2021-04-15)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Errore in write (mass editing data decorrenza fatture)

12.0.3.2.1 (2021-03-30)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Errore in onchange

12.0.2.1.43 (2021-02-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Riconoscimento riga contabile da funzione di account_move_line_type
* [FIX] Errore in validazione fattura con Reverse Charge misto

12.0.2.1.42 (2021-02-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Tolto onchange su data scadenza
* [FIX] Errore in annulla fattura con Reverse Charge
* [FIX] check_payment gestito con @multi causa error mass editing

12.0.2.1.41 (2021-01-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretto bug sulla gestione del metodo di pagamento

12.0.2.1.40 (2021-01-08)
~~~~~~~~~~~~~~~~~~~~~~~~

* [MOD] Spostati campi "prorogation_ctr" e "unpaid_ctr" di account.move.line da modulo account_banking_invoice_financing a account_duedates

12.0.1.1.39 (2021-01-07)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Added payment done field / Impostato campo incasso effettuato

12.0.1.1.38 (2020-12-30)
~~~~~~~~~~~~~~~~~~~~~~~~

* [MOD] Added convenience field to retrieve the related payment order lines

12.0.0.1.37 (2020-12-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Added filter 'not in order' and state field / Impostato filtro 'Non in scadenza' e campo stato

12.0.0.1.36 (2020-12-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Warning on check duedate payments / Segnalazione al tentativo di annullamento con scadenze in pagamento

12.0.0.1.35 (2020-12-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactoring date effective / Aggiornato gestione data decorrenza

12.0.0.1.34 (2020-12-04)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Set vat on first duedate according to payment term flag / Impostato gestione iva sulla prima scadenza

12.0.0.1.33 (2020-12-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rimossa creazione righe scadenze se almeno una in pagamento

12.0.0.1.32 (2020-11-30)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rimossa creazione righe scadenze se almeno una in pagamento

12.0.0.1.31 (2020-11-23)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Set duedates creation from sale order / Impostato creazione scadenze da ordine di vendita

12.0.0.1.30 (2020-11-23)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Set account invoice 13 more dependency / Inserita dipendenza modulo transizione

12.0.0.1.29 (2020-11-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Set default date effective / Impostato default data decorrenza

12.0.0.1.28 (2020-11-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Added missing dependency / inserita dipendenza mancante

12.0.0.1.27 (2020-11-12)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Added date effective / inserita data di decorrenza

12.0.0.1.26 (2020-11-09)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] impostato ricerca per ordine di pagamento

12.0.0.1.25 (2020-11-06)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] impostato campo ordine di pagamento nella view

12.0.0.1.24 (2020-11-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] gestito validazione fattura da ordine di vendita

12.0.0.1.24 (2020-11-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] corretto calcolo ammontare fattura in account.move

12.0.0.1.23 (2020-11-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] gestione cancellazione ultima scadenza rimasta (mette una nuova riga di scadenza e una nuova riga contabile con scadenza parti alla data fattura e importo pari all'imposto dattura)

12.0.0.1.22 (2020-11-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] corretta gestione scadenze per fatture in stato bozza

12.0.0.1.21 (2020-10-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Update model, removed unused fields

12.0.0.1.18 (2020-10-23)
~~~~~~~~~~~~~~~~~~~~~~~~

* [MOD] Correzioni di forma la codice per adeguamento a segnalazioni Flake8

12.0.0.1.17 (2020-10-22)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Eliminazione righe di scadenza vuote, calcolo proposta per importo scadenze dopo modifica fattura, ricalcolo automaticp scadenze al cambio dei termini di pagamento

12.0.0.1.16 (2020-10-21)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Implementato totalizzazione totale scadenze e differenza tra scadenze e totale fattura

12.0.0.1.15 (2020-10-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Aggiornato duedate manager

12.0.0.1.14 (2020-10-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rimosso campo duplicato (termine di pagamento)

12.0.0.1.13 (2020-10-12)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Aggiornamento bidirezionale di data scadenza e metodo di pagamento tra account.move.line e account.duedate_plus.line

12.0.0.1.12 (2020-10-12)
~~~~~~~~~~~~~~~~~~~~~~~~
* [FIX] Inserita dipendenza modulo OCA Scadenziario account_due_list


12.0.0.1.11 (2020-10-12)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rimossi controlli non validi
