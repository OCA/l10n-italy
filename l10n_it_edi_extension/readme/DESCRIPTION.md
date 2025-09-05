**Italiano**

Questo modulo estende le funzionalità standard della fatturazione elettronica italiana di Odoo, introducendo strumenti utili come l'anteprima XML ed il calcolo dei codici fiscali e miglioramenti nell'importazione e nell'esportazione delle fatture XML.

Le funzionalità principali incluse sono:

1. Anteprima e Download del file XML:

   - Aggiunge un pulsante ("Preview XML") direttamente nel form della fattura.
   - Dalla stessa finestra della fattura, è possibile scaricare il file XML generato.

2. Valorizza i seguenti campi/nodi della fattura elettronica esportata:

   - `<RiferimentoAmministrazione>` (sia sulla riga o nell'azienda): identificativo utilizzato per uso amministrativo/gestionale interno. È un campo libero che può essere utilizzato per inserire riferimenti specifici richiesti dalla Pubblica Amministrazione o altri riferimenti utili per la gestione amministrativa.
   - `<StabileOrganizzazione>`: rappresenta i dati della sede operativa stabile del cedente/prestatore in Italia se diversa dalla sede legale. Da impostare in odoo nell'azienda, tab "Informazioni Generali"
   - `<Causale>`: in questo caso non c'è un campo apposito, ma trascrive i "Termini e condizioni" della fattura
   - `<Art73>`: indica se il documento è stato emesso secondo modalità e termini stabiliti con decreto ministeriale ai sensi dell'articolo 73 del DPR 633/72. Da impostare in odoo nell'azienda o direttamente in fattura.

3. Miglioramenti nell'import delle fatture XML:

   - Aggiunge un'opzione per creare i contatti presenti in una fattura elettronica se non esistono in anagrafica tra cui:
     - `<CessionarioCommittente>` e `<CedentePrestatore>` invece di scrivere solamente i dettagli nel chatter.
   - Creazione di altri contatti presenti in una fattura elettronica se non esistono in anagrafica tra cui:
     - `<RappresentanteFiscale>`
   - Nome e cognome vengono assegnati ai nuovi contatti in base ai nodi `<Nome>` e `<Cognome>` della fattura elettronica.
   - Gestione delle Fatture Elettroniche Multiple:
     - Supporto per la suddivisione automatica di file XML contenenti più fatture
     - Ogni `<FatturaElettronicaBody>` viene convertito in una fattura separata mantenendo l'header originale
   - Aggiunge la possibilità di scegliere tra 3 modalità di importazione:
     - senza righe
     - una riga per ogni aliquota
     - tutte le righe (default)
   - Importazione dei `<DatiRiepilogo>`:
     - `<AliquotaIVA>`
     - `<Natura>`: Indica il motivo per cui un'operazione non prevede l'IVA
     - `<SpeseAccessorie>`: es. trasporto, imballaggio
     - `<Arrotondamento>`
     - `<ImponibileImporto>`
     - `<Imposta>`
     - `<EsigibilitaIVA>`: Indica quando l'IVA diventa esigibile (immediata, differita o scissione dei pagamenti)
     - `<RiferimentoNormativo>`: Obbligatorio quando si usa il campo `<Natura>`
   - Importazione dei `<DatiGeneraliDocumento>`:
     - `<Arrotondamento>`
     - `<Art73>`: indica se il documento è stato emesso secondo modalità e termini stabiliti con decreto ministeriale ai sensi dell'articolo 73 del DPR 633/72
     - `<DatiSAL>` e `<RiferimentoFase>`: utilizzati per indicare lo stato di avanzamento dei lavori in caso di fatturazione dilazionata/progressiva (contratti di appalto, servizi continuativi o lavori in corso d'opera)
   - Importazione dei dati della fattura principale (`<NumeroFatturaPrincipale>` e `<DataFatturaPrincipale>`)
   - Scrittura nel chatter dei nodi di `<DatiGenerali><DatiTrasporto>` e `<DatiVeicoli>`
   - Gestione avanzata dei Dati delle Righe Fattura:
     - Creazione dei codici articolo in fase di importazione.
       Questi codici servono per identificare univocamente i prodotti/servizi secondo diversi standard di codifica.
       Nel file XML, questi codici sono nel nodo `<CodiceArticolo>` che può contenere:
       - `<CodiceTipo>`: identifica il tipo di codifica utilizzata
       - `<CodiceValore>`: il valore effettivo del codice
     - Registrazione dello sconto o maggiorazione, nodo `<ScontoMaggiorazione>`, nelle righe di dettaglio della fattura.
     - Importazione dei dati del nodo `<AltriDatiGestionali>` (informazioni supplementari che non trovano posto negli altri campi standard della fattura elettronica) che può contenere:
       - `<TipoDato>`: identifica il tipo di informazione aggiuntiva che si sta inserendo
       - `<RiferimentoTesto>`: contiene un valore testuale dell'informazione aggiuntiva
       - `<RiferimentoNumero>`: contiene un valore numerico dell'informazione aggiuntiva
       - `<RiferimentoData>`: contiene un valore data dell'informazione aggiuntiva
     - Importazione dei nodi:
       - `<NumeroLinea>`: numero progressivo della riga all'interno della fattura
       - `<TipoCessionePrestazione>`: indica la tipologia della cessione o prestazione e può contenere valori come:
         - "SC" (Sconto)
         - "PR" (Premio)
         - "AB" (Abbuono)
         - "AC" (Spesa accessoria)
       - `<DataInizioPeriodo>` e `<DataFinePeriodo>`: indicano il periodo di riferimento di una prestazione e sono utili per servizi continuativi o prestazioni che si estendono su un periodo di tempo
       - `<RiferimentoAmministrazione>`: identificativo utilizzato per uso amministrativo/gestionale interno. È un campo libero che può essere utilizzato per inserire riferimenti specifici richiesti dalla Pubblica Amministrazione o altri riferimenti utili per la gestione amministrativa.

    - Convalida della fattura importata: se i seguenti importi sono diversi da quelli presenti nel file XML, nella fattura viene visualizzato un messaggio:
      - importo totale imponibile
      - IVA totale
      - IVA inclusa

    - I dati del partner possono essere aggiornati per corrispondere a quelli nella fattura elettronica.

4. Aggiunge di un wizard per calcolare i codici fiscali

\<<https://www.fatturapa.gov.it>\>


**English**

This module extends Odoo's standard Italian electronic invoicing functionality, introducing useful tools such as XML preview and fiscal code calculation and improvements in importing and exporting XML invoices.

The main features included are:

1. XML File Preview and Download:

   - Adds a button ("Preview XML") directly in the invoice form.
   - From the same invoice form, you can download the generated XML file.

2. Adds fields in XML invoice export:

   - `<RiferimentoAmministrazione>` (both on line or on company): identifier used for internal administrative/management purposes. It's a free field that can be used to insert specific references required by Public Administration or other useful references for administrative management.
   - `<StabileOrganizzazione>`: represents the data of the seller/provider's permanent establishment in Italy if different from the registered office
   - `<Causale>`: in this case there is no specific field, but it transcribes the "Terms and conditions" of the invoice.
   - `<Art73>`: indicates if the document was issued according to methods and terms established by ministerial decree pursuant to article 73 of DPR 633/72

3. Improvements in XML invoice import:

   - Adds an option to create contacts present in an electronic invoice if they don't exist in the address book, including:
     - `<CessionarioCommittente>` and `<CedentePrestatore>` instead of just writing the details in the chatter.
   - Creation of other contacts present in an electronic invoice if they don't exist in the address book, including:
     - `<RappresentanteFiscale>`
   - Name and surname are set in the new contacts based on the `<Nome>` and `<Cognome>` nodes of the E-Bill.
   - Multiple Electronic Invoice Management:
     - Support for automatic splitting of XML files containing multiple invoices
     - Each `<FatturaElettronicaBody>` is converted into a separate invoice maintaining the original header
   - Adds the ability to choose between 3 import modes:
     - without lines
     - one line for each VAT rate
     - all lines (default)
   - Import of `<DatiRiepilogo>`:
     - `<AliquotaIVA>`
     - `<Natura>`: Indicates the reason why an operation does not include VAT
     - `<SpeseAccessorie>`: e.g., transport, packaging
     - `<Arrotondamento>`
     - `<ImponibileImporto>`
     - `<Imposta>`
     - `<EsigibilitaIVA>`: Indicates when VAT becomes payable (immediate, deferred, or split payment)
     - `<RiferimentoNormativo>`: Required when using the `<Natura>` field
   - Import of `<DatiGeneraliDocumento>`:
     - `<Arrotondamento>`
     - `<Art73>`: indicates if the document was issued according to methods and terms established by ministerial decree pursuant to article 73 of DPR 633/72
     - `<DatiSAL>` and `<RiferimentoFase>`: used to indicate the progress status of work in case of deferred/progressive invoicing (procurement contracts, continuous services, or work in progress)
   - Import of main invoice data (`<NumeroFatturaPrincipale>` and `<DataFatturaPrincipale>`)
   - Writing in chatter of `<DatiGenerali><DatiTrasporto>` and `<DatiVeicoli>` nodes
   - Advanced management of Invoice Line Data:
     - Creation of article codes during import.
       These codes are used to uniquely identify products/services according to different coding standards.
       In the XML file, these codes are in the `<CodiceArticolo>` node which can contain:
       - `<CodiceTipo>`: identifies the type of coding used
       - `<CodiceValore>`: the actual code value
     - Recording of discounts or surcharges, `<ScontoMaggiorazione>`, in the invoice detail lines.
     - Import of `<AltriDatiGestionali>` node data (supplementary information that doesn't fit in other standard electronic invoice fields) which can contain:
       - `<TipoDato>`: identifies the type of additional information being entered
       - `<RiferimentoTesto>`: contains a textual value of the additional information
       - `<RiferimentoNumero>`: contains a numerical value of the additional information
       - `<RiferimentoData>`: contains a date value of the additional information
     - Import of nodes:
       - `<NumeroLinea>`: progressive line number within the invoice
       - `<TipoCessionePrestazione>`: indicates the type of transfer or service and can contain values such as:
         - "SC" (Discount)
         - "PR" (Prize)
         - "AB" (Allowance)
         - "AC" (Ancillary expense)
       - `<DataInizioPeriodo>` and `<DataFinePeriodo>`: indicate the reference period of a service and are useful for continuous services or services that extend over a period of time
       - `<RiferimentoAmministrazione>`: identifier used for internal administrative/management purposes. It's a free field that can be used to insert specific references required by Public Administration or other useful references for administrative management.

    - Validation of imported bill: if the following amounts are different than the amount in the XML a message is shown in the bill:
      - total taxable amount
      - total VAT
      - total including VAT

    - Partner's data can be updated to match the data in the e-bill

4. Adds a wizard to calculate fiscal codes

\<<https://www.fatturapa.gov.it>\>
