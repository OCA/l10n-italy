**Italiano**

Non è necessaria alcuna configurazione specifica per l10n_it_edi_extension: una volta installato, le sue funzionalità sono attive.
Tuttavia, è fondamentale capire che questo modulo è un'estensione e si basa su altri moduli preesistenti e sulla configurazione generale di Odoo per la localizzazione italiana e la fatturazione elettronica.
Quindi, affinché le funzionalità di questo modulo siano utilizzabili, è necessario che:

1. Siano installati e configurati i moduli dipendenti:
  - account: Il modulo base della contabilità di Odoo deve essere installato e configurato (piano dei conti, tasse, giornali contabili, ecc.).
  - l10n_it_edi: Il modulo principale per la fatturazione elettronica italiana deve essere installato e correttamente configurato. Questo include:
    - Configurazione dei dati aziendali (partita IVA, codice fiscale, regime fiscale, ecc.).
    - Configurazione dei registri contabili per l'emissione delle fatture elettroniche (indicando il formato FatturaPA/Elettronica).
    - Configurazione delle sequenze dedicate per la numerazione delle fatture elettroniche.
    - Eventuale configurazione delle credenziali SDI se si utilizza l'invio diretto tramite Odoo (se supportato dalla configurazione generale).

Le funzionalità aggiunte da l10n_it_edi_extension si integrano automaticamente nell'interfaccia esistente:

  - Il pulsante "Preview XML" apparirà nel form della fattura.
  - L'opzione per impostare la data a fine mese DDT sarà disponibile nel menu "Azioni" delle fatture selezionate.
  - Il filtro data nel wizard di esportazione userà automaticamente la data fattura.

**English**

No specific configuration is required for l10n_it_edi_extension: once installed, its features are active.
However, it's essential to understand that this module is an extension and relies on other pre-existing modules and Odoo general configuration for Italian localization and electronic invoicing.
Therefore, for this module's features to be usable, it is necessary that:

1. The dependent modules are installed and configured:
  - account: Odoo's basic accounting module must be installed and configured (chart of accounts, taxes, journals, etc.).
  - l10n_it_edi: The main module for Italian electronic invoicing must be installed and properly configured. This includes:
    - Company data configuration (VAT number, fiscal code, tax regime, etc.).
    - Configuration of accounting journals for issuing electronic invoices (indicating FatturaPA/Electronic format).
    - Configuration of dedicated sequences for electronic invoice numbering.
    - Optional SDI credentials configuration if direct sending through Odoo is used (if supported by general configuration).

The features added by l10n_it_edi_extension are automatically integrated into the existing interface:

  - The "Preview XML" button will appear in the invoice form.
  - The option to set the DDT end-of-month date will be available in the "Actions" menu of selected invoices.
  - The date filter in the export wizard will automatically use the invoice date.
