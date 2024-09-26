# [IMP] l10n_it_delivery_note: Miglioramento generazione fatture da DDT

## Panoramica

Questa PR migliora il modulo dei documenti di trasporto (DDT) potenziando le capacità di generazione fatture e aggiungendo opzioni configurabili su come i dati del DDT vengono utilizzati nella creazione delle fatture.

## Riepilogo Modifiche

### 1. Miglioramento Generazione Fatture (commit 2e85ba11)

**Principali miglioramenti:**
- Semplificata la logica di creazione fatture rimuovendo la "magia" basata sul contesto
- Aggiunto parametro esplicito `sale_orders` in tutto il flusso di fatturazione
- Rimosso il metodo `_get_sale_context()` (eliminate 28 righe di logica complessa)
- Corretta la gestione della distribuzione analitica per copiare correttamente dalle righe ordine
- Aggiunta copertura test completa per la distribuzione analitica

**Modifiche principali:**
- `stock_delivery_note.py`: 
  - Modificato `action_invoice()` per accettare il parametro esplicito `sale_orders`
  - Semplificati `_prepare_invoice()`, `_prepare_invoice_lines()`, `_update_invoice_statuses()`
  - Corretto bug nella gestione dei termini di pagamento vuoti
  - Corretto warning flake8 B023 (binding variabile lambda)
  
- `stock_delivery_note_line.py`:
  - Semplificato `_prepare_invoice_line()` per copiare solo la distribuzione analitica dalla riga ordine
  - Rimossa logica errata che sommava 100 alle percentuali esistenti
  
- `sale_order.py`:
  - Aggiornato `_create_invoices()` per passare il parametro `sale_orders=self`
  - Aggiunto commento TODO che documenta un potenziale miglioramento futuro per la selezione della policy di fatturazione

- **Test**: Aggiunto `test_analytic_distribution_from_sale_order_line()` per verificare la corretta copia delle distribuzioni analitiche

**Miglioramenti tecnici:**
- Codice più esplicito e facile da mantenere
- Nessuna dipendenza nascosta dal contesto
- Segue le best practice OCA per il passaggio di parametri
- Tutti i 17 test passano correttamente

### 2. Origine Dati Fattura Configurabile (commit 26b11daf)

**Opzioni di configurazione aggiunte:**
- `use_dn_product_name_in_invoice`: Usa il nome prodotto del DDT invece del nome dell'ordine di vendita nelle fatture
- `use_dn_price_unit_in_invoice`: Usa il prezzo unitario del DDT invece del prezzo dell'ordine di vendita nelle fatture

**Implementazione:**
- `res_company.py`: Aggiunti due campi booleani per la configurazione
- `res_config_settings.py`: Esposti i parametri nella configurazione aziendale
- `res_config_settings.xml`: Aggiunti controlli UI nella vista impostazioni
- `stock_delivery_note_line.py`: Modificato `_prepare_invoice_line()` per rispettare la configurazione

**Caso d'uso:**
Queste opzioni sono utili quando i dati del DDT (nome/prezzo) differiscono dall'ordine di vendita originale e si vuole che la fattura rifletta le informazioni effettive della merce consegnata.

**Test**: Aggiunto `test_dn_product_name_and_price_in_invoice()` che copre:
- Comportamento predefinito (usa dati ordine di vendita)
- Solo nome prodotto da DDT abilitato
- Sia nome prodotto che prezzo da DDT abilitati

### 3. Correzione Display Type (commit 336c1f60)

**Bug fix:**
- Corretto il campo `display_type` nella generazione righe fattura per usare correttamente "product" invece di dipendere dal display type della riga DDT
- Assicura che le righe fattura siano correttamente categorizzate

## Test

Tutti i test passano:
- 17 test totali (aggiunti 2 nuovi test)
- 0 fallimenti, 0 errori
- Tempo di esecuzione test: ~27s

## Note di Migrazione

- Nessuna migrazione database richiesta
- I nuovi campi di configurazione hanno valore predefinito `False` (mantengono il comportamento attuale)
- Retrocompatibile con installazioni esistenti

## Documentazione

- Aggiornato `README.rst` con informazioni sulla generazione fatture
- Aggiunta documentazione d'uso in `readme/USAGE.md`

## Note per la Review

Questa PR risponde a diversi commenti di code review:
1. ✅ Rimossa la magia del contesto per un codice più pulito ed esplicito
2. ✅ Semplificata la gestione della distribuzione analitica (rimossa logica errata di somma percentuali)
3. ✅ Aggiunta copertura test per le nuove funzionalità
4. 📝 Documentata limitazione nota riguardo la policy di fatturazione (vedi TODO in `sale_order.py`)

Il commento TODO in `sale_order.py` suggerisce un miglioramento futuro per aggiungere un campo selection per la policy di fatturazione negli ordini di vendita, permettendo agli utenti di scegliere tra modalità standard "consegnato" e modalità "documento_trasporto". Questo fornirebbe un migliore controllo su quando appare il pulsante "Crea Fattura" ed eviterebbe di bypassare la logica standard di fatturazione. Questo miglioramento è intenzionalmente lasciato per una PR futura in quanto richiede modifiche significative al calcolo dello stato fatturazione e al comportamento UI.

## Screenshot

N/D - Solo funzionalità backend

## Issue Correlate

Closes: #XXXX (se applicabile)

---

**Co-authored-by:** Giuseppe Borruso <gborruso@dinamicheaziendali.it>
