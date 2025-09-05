**Italiano**

Le uniche configurazioni disponibili sono:
  - Livello di dettaglio importazione e-fatture: in Fatturazione (o Contabilità per EE) > Configurazione > Impostazioni > Fatturazione Elettronica Italiana, valorizzare "Livello di dettaglio importazione e-fatture" per importare le fatture elettroniche senza righe, con una riga per ogni aliquota, oppure con tutte le righe (default).
  Questa configurazione può essere sovrascritta dal campo "Livello di dettaglio importazione e-fatture" in ogni fornitore.
  - Crea il partner se non esiste durante l'importazione: in Fatturazione (o Contabilità per EE) > Configurazione > Impostazioni > Fatturazione Elettronica Italiana, spuntare l'opzione se si vuole attivare la funzionalità per i dati dei nodi:
     - `<CessionarioCommittente>`
     - `<CedentePrestatore>`
     - `<RappresentanteFiscale>`

Non sono necessarie altre configurazioni specifiche per l10n_it_edi_extension: una volta installato, le sue funzionalità sono attive e si integrano automaticamente nell'interfaccia esistente.

Tuttavia, è fondamentale capire che questo modulo è un'estensione e si basa su altri moduli preesistenti e sulla configurazione generale di Odoo per la localizzazione italiana e la fatturazione elettronica.
Quindi, affinché le funzionalità di questo modulo siano utilizzabili, è necessario che siano installati e configurati i moduli dipendenti:
  - `account`: Il modulo base della contabilità di Odoo deve essere installato e configurato (piano dei conti, tasse, giornali contabili, ecc.).
  - `l10n_it_edi`: Il modulo principale per la fatturazione elettronica italiana deve essere installato e correttamente configurato. Questo include:
    - Configurazione dei dati aziendali (partita IVA, codice fiscale, regime fiscale, ecc.).
    - Configurazione dei registri contabili per l'emissione delle fatture elettroniche (indicando il formato FatturaPA/Elettronica).
    - Configurazione delle sequenze dedicate per la numerazione delle fatture elettroniche.
    - Eventuale configurazione delle credenziali SDI se si utilizza l'invio diretto tramite Odoo (se supportato dalla configurazione generale).

Nel partner è possibile abilitare il campo "Non aggiornare il contatto dai dettagli della fattura elettronica" così i dati del partner non saranno modificati in base a quanto presente in una delle loro fatture durante l'importazione.

**English**

The only available configurations are:
  - E-invoice import detail level: in Invoicing (or Accounting for EE) > Configuration > Settings > Italian Electronic Invoicing, set "E-invoice import detail level" to import electronic invoices without lines, with one line per tax rate, or with all lines (default).
  This configuration can be overridden by the "E-invoice import detail level" field in each supplier.
  - Create partner if not existing during import: in Invoicing (or Accounting for EE) > Configuration > Settings > Italian Electronic Invoicing, check this option if you want to enable the functionality for the following node data:
     - `<CessionarioCommittente>`
     - `<CedentePrestatore>`
     - `<RappresentanteFiscale>`

No other specific configurations are required for l10n_it_edi_extension: once installed, its features are active and automatically integrate into the existing interface.

However, it's essential to understand that this module is an extension and relies on other pre-existing modules and Odoo's general configuration for Italian localization and electronic invoicing.
Therefore, for this module's features to be usable, the dependent modules must be installed and configured:
  - `account`: Odoo's basic accounting module must be installed and configured (chart of accounts, taxes, journals, etc.).
  - `l10n_it_edi`: The main module for Italian electronic invoicing must be installed and properly configured. This includes:
    - Company data configuration (VAT number, fiscal code, tax regime, etc.).
    - Configuration of accounting journals for issuing electronic invoices (indicating FatturaPA/Electronic format).
    - Configuration of dedicated sequences for electronic invoice numbering.
    - Optional SDI credentials configuration if direct sending through Odoo is used (if supported by general configuration).

In the partner, you can enable "Do not update the contact from Electronic Invoice Details" so that the partner's data are not modified with what is found in one of their imported e-bill.
