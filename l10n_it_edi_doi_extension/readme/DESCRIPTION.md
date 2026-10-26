**English**

This module extends the functionality of l10n_it_edi_doi, enabling the
use of the Declaration of Intent (Dichiarazione di Intento) for incoming
vendor bills and purchase orders.

Key features:
 - Support for multiple Declarations of Intent per invoice
 - Dedicated tab in invoice form for managing DOI associations
 - Automatic validation of DOI amounts and available thresholds
 - Smart warnings when invoice amounts don't match DOI coverage
 - Backward compatibility with single-declaration workflow
 - Check that the move lines only include the DoI Tax, when present
 - Check that at least one move line contains the DoI Tax when the DoI is set in the Move

**Italiano**

Questo modulo estende la funzionalità di l10n_it_edi_doi, permettendo
l'utilizzo della Dichiarazione di Intento per le fatture di acquisto in
ingresso e gli ordini di acquisto.

Caratteristiche principali:
 - Supporto per dichiarazioni di intento multiple per fattura
 - Tab dedicato nel form fattura per gestire le associazioni DOI
 - Validazione automatica degli importi e soglie disponibili
 - Avvisi intelligenti quando gli importi non corrispondono
 - Retrocompatibilità con il flusso a dichiarazione singola
 - Verifica che i movimenti contabili includano soltanto l'imposta per la DI, quando presente
 - Verifica che almeno un movimento contabile contenga l'imposta per la DI quando la DI è impostata nella registrazione
