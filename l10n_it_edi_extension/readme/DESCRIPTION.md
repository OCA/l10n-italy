**Italiano**

Questo modulo estende le funzionalità standard della fatturazione elettronica italiana di Odoo, introducendo strumenti utili come l'anteprima XML, la gestione facilitata delle date per le fatture differite e una maggiore flessibilità nella numerazione e nell'esportazione.

Le funzionalità principali incluse sono:

1. Anteprima e Download del file XML:

  - Aggiunge un pulsante ("Preview XML") direttamente nel form della fattura.
  - Questo pulsante permette di visualizzare un'anteprima del file XML della fattura elettronica prima dell'invio effettivo.
  - Dalla stessa finestra di anteprima, è possibile scaricare il file XML generato.

2. Rigenerazione Numero Fattura (se non inviata):

  - Se una fattura non è ancora stata inviata allo SDI (Sistema di Interscambio), riportandola in bozza e riconvalidandola, il modulo permette di rigenerare il numero progressivo della fattura se necessario (ad esempio, se nel frattempo sono state emesse altre fatture).

3. Gestione Data Fattura per Fatture Differite:

  - Offre un wizard (accessibile dal menu "Azioni" su una selezione di fatture in stato "Bozza" o "Convalidato") per impostare la data della fattura come l'ultimo giorno del mese del DDT (Documento di Trasporto) associato. Utile per la creazione di fatture differite a fine mese.

4. Filtro Data nell'Export:

  - Modifica il wizard standard di esportazione massiva delle fatture elettroniche (l10n_it_edi.wizard_export_fatturapa).
  - Fa sì che il filtro per data utilizzato nel wizard si basi sulla Data Fattura (invoice_date) invece che sulla Data Contabile (date).

\<<https://www.fatturapa.gov.it>\>


**English**

This module extends Odoo standard Italian electronic invoicing functionality, introducing useful tools such as XML preview, simplified date management for deferred invoices and greater flexibility in numbering and exporting.

The main features included are:

1. XML File Preview and Download:

  - Adds a button ("Preview XML") directly in the invoice form.
  - This button allows you to preview the electronic invoice XML file before actual submission.
  - From the same preview window, you can download the generated XML file.

2. Invoice Number Regeneration (if not sent):

  - If an invoice has not yet been sent to SDI (Exchange System), by setting it back to draft and revalidating it, the module allows regenerating the progressive invoice number if necessary (for example, if other invoices have been issued in the meantime).

3. Invoice Date Management for Deferred Invoices:

  - Provides a wizard (accessible from the "Actions" menu on a selection of invoices in "Draft" or "Validated" status) to set the invoice date as the last day of the month of the associated DDT (Transport Document). Useful for creating end-of-month deferred invoices.

4. Date Filter in Export:

  - Modifies the standard mass export wizard for electronic invoices (l10n_it_edi.wizard_export_fatturapa).
  - Makes the date filter used in the wizard based on Invoice Date (invoice_date) instead of Accounting Date (date).

\<<https://www.fatturapa.gov.it>\>
