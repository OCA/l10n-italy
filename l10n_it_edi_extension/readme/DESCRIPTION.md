**Italiano**

Questo modulo estende le funzionalità standard della fatturazione elettronica italiana di Odoo, introducendo strumenti utili come l'anteprima XML ed il calcolo dei codici fiscali e miglioramenti nell'importazione e nell'esportazione delle fatture XML.

Le funzionalità principali incluse sono:

1. Anteprima e Download del file XML:

   - Aggiunge un pulsante ("Preview") direttamente nel form della fattura, sia per fatture inviate che ricevute.
   - Dalla stessa finestra della fattura, è possibile scaricare il file XML generato.

2. Valorizza i seguenti campi/nodi della fattura elettronica esportata:

   - `<RiferimentoAmministrazione>` (sia sulla riga o nell'azienda): identificativo utilizzato per uso amministrativo/gestionale interno. È un campo libero che può essere utilizzato per inserire riferimenti specifici richiesti dalla Pubblica Amministrazione o altri riferimenti utili per la gestione amministrativa.
   - `<StabileOrganizzazione>`: rappresenta i dati della sede operativa stabile del cedente/prestatore in Italia se diversa dalla sede legale. Da impostare in odoo nell'azienda, tab "Informazioni Generali"
   - `<Causale>`: in questo caso non c'è un campo apposito, ma trascrive i "Termini e condizioni" della fattura
   - `<Art73>`: indica se il documento è stato emesso secondo modalità e termini stabiliti con decreto ministeriale ai sensi dell'articolo 73 del DPR 633/72. Da impostare in odoo nell'azienda o direttamente in fattura.
   - `<AltriDatiGestionali>` (2.2.1.16): dati gestionali aggiuntivi che possono essere inseriti manualmente su ogni riga fattura ed esportati nel file XML FatturaPA. Ogni voce include:
     - `<TipoDato>`: tipo di dato (max 10 caratteri, obbligatorio)
     - `<RiferimentoTesto>`: riferimento testuale (max 60 caratteri)
     - `<RiferimentoNumero>`: riferimento numerico (fino a 8 decimali)
     - `<RiferimentoData>`: riferimento data
     - Per aggiungere questi dati, aprire la riga fattura e compilare la sezione "Altri Dati Gestionali".
   - `<IndirizzoResa>`: rappresenta l'indirizzo di consegna della merce.

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

5. Allegati nell'XML della fattura elettronica, che nella 18.0 erano gestiti dal modello `l10n_it_edi.attachment` (i dati vengono migrati, vedi sotto):

   - Nella scheda «Fatturazione elettronica» della fattura si caricano i file da allegare: ognuno diventa un nodo `<Allegati>` dell'XML, dopo l'eventuale PDF della fattura inserito da `l10n_it_edi`. Vale sia per il tracciato ordinario sia per quello semplificato:
     - `<NomeAttachment>`: il nome del file, ridotto a 60 caratteri senza perdere l'estensione;
     - `<FormatoAttachment>`: l'estensione del file;
     - `<DescrizioneAttachment>`: la descrizione scritta sotto il file nell'elenco (al massimo 100 caratteri) o, se vuota, il nome del file senza estensione;
     - `<Attachment>`: il contenuto del file.
   - I file caricati da questa scheda non vengono importati come documenti della fattura, diversamente dagli allegati caricati dal chatter.
   - Il chatter e l'anteprima laterale mostrano gli allegati dell'elenco, e di ogni fattura solo i suoi: un documento condiviso da più fatture compare solo in quelle che lo elencano.
   - Per togliere un file dall'elenco serve una conferma. Al salvataggio il file viene eliminato, se appartiene a quella fattura e nessun'altra fattura lo elenca; i documenti di altri record restano.
   - Un file presente in un elenco non si può eliminare (per esempio dal chatter): va prima tolto dall'elenco.
   - Se l'XML è già stato generato, la stessa scheda mostra gli allegati effettivamente presenti nel file e avvisa quando non corrispondono all'elenco: allegati dell'elenco che mancano nell'XML, allegati dell'XML tolti dall'elenco (escluso il PDF della fattura), o entrambi. In questi casi può convenire rigenerare l'XML.
   - Anche le fatture e le note di credito fornitore mostrano, nella stessa scheda, gli allegati presenti nell'XML ricevuto, anche se caricato a mano o firmato (`.p7m`).
   - Prima dell'esportazione viene controllato che l'XML non superi il limite SdI di 5 MB per file. La dimensione è stimata: allegati dell'elenco e PDF della fattura, se già generato, codificati in base64, più una stima del resto dell'XML in base alle righe; si tiene un margine di 100 KB.
   - Nella migrazione dalla 18.0, gli allegati del modello `l10n_it_edi.attachment` delle fatture e note di credito cliente vengono riportati nell'elenco (escluso il PDF della fattura proveniente dalla 16.0, che `l10n_it_edi` inserisce già da solo). Quelli delle fatture fornitore restano allegati normali: i loro allegati si leggono dall'XML ricevuto. La descrizione resta e viene esportata; formato e algoritmo di compressione salvati nella 18.0 non si usano più: il formato si ricava dall'estensione.
   - Altri moduli possono aggiungere allegati scrivendo nel campo `l10n_it_edi_ext_doc_attachment_ids` o estendendo `_l10n_it_edi_ext_get_doc_attachments`, e cambiare la descrizione estendendo `_l10n_it_edi_ext_attachment_xml_description`.

   *Scelte di progetto*

   Gli allegati sono un Many2many verso `ir.attachment` e non un modello intermedio con una riga per allegato, come il `fatturapa.attachments` della 16.0 o il `l10n_it_edi.attachment` della 18.0. Si è scelto così per semplicità: niente modello in più con permessi e regole multiazienda, e altri moduli possono allegare file già esistenti senza duplicarli. Le conseguenze sono due:

   - la descrizione è quella del file (`ir.attachment.description`), e si scrive e si esporta solo per i file della fattura (caricati dall'elenco o migrati). Per i file di altri record si usa il nome del file: la loro descrizione è condivisa da tutti i record a cui sono allegati e spesso contiene testi interni;
   - serve una variante del widget `many2many_binary` (`l10n_it_edi_ext_doc_attachments`). Il widget standard caricherebbe il file come allegato della fattura, e `account` prova a importare come documento ogni allegato di una fattura (`_extend_with_attachments`): un XML potrebbe aggiungere righe alla fattura. La variante carica il file senza record collegato, e il modulo lo collega alla fattura al salvataggio.

   I file caricati sono collegati alla fattura con `res_field` uguale al campo dell'elenco, come fa `l10n_it_edi` per l'XML: non sono documenti della fattura, quindi non finiscono nel chatter da soli, e il chatter mostra esattamente l'elenco (`_get_mail_thread_data_attachments`). Il campo ha nel contesto `skip_res_field_check`, altrimenti `ir.attachment._search` li nasconderebbe anche dall'elenco.

\<<https://www.fatturapa.gov.it>\>


**English**

This module extends Odoo's standard Italian electronic invoicing functionality, introducing useful tools such as XML preview and fiscal code calculation and improvements in importing and exporting XML invoices.

The main features included are:

1. XML File Preview and Download:

   - Adds a button ("Preview") directly in the invoice form, both for exported and imported invoices.
   - From the same invoice form, you can download the generated XML file.

2. Adds fields in XML invoice export:

   - `<RiferimentoAmministrazione>` (both on line or on company): identifier used for internal administrative/management purposes. It's a free field that can be used to insert specific references required by Public Administration or other useful references for administrative management.
   - `<StabileOrganizzazione>`: represents the data of the seller/provider's permanent establishment in Italy if different from the registered office
   - `<Causale>`: in this case there is no specific field, but it transcribes the "Terms and conditions" of the invoice.
   - `<Art73>`: indicates if the document was issued according to methods and terms established by ministerial decree pursuant to article 73 of DPR 633/72
   - `<AltriDatiGestionali>` (2.2.1.16): additional management data that can be manually entered on each invoice line and exported to the FatturaPA XML file. Each entry includes:
     - `<TipoDato>`: data type (max 10 characters, required)
     - `<RiferimentoTesto>`: text reference (max 60 characters)
     - `<RiferimentoNumero>`: numeric reference (up to 8 decimal places)
     - `<RiferimentoData>`: date reference
     - To add this data, open the invoice line and fill in the "Other Management Data" section.
   - `<IndirizzoResa>`: represents the shipping address of the goods.

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

5. Attachments in the e-invoice XML, handled in 18.0 by the `l10n_it_edi.attachment` model (the data is migrated, see below):

   - In the "Electronic Invoicing" tab of the invoice, upload the files to be attached: each one becomes an `<Allegati>` node of the XML, after the invoice PDF possibly added by `l10n_it_edi`. Both the ordinary and the simplified formats are supported:
     - `<NomeAttachment>`: the file name, reduced to 60 characters keeping the extension;
     - `<FormatoAttachment>`: the file extension;
     - `<DescrizioneAttachment>`: the description written below the file in the list (100 characters at most) or, when empty, the file name without extension;
     - `<Attachment>`: the file content.
   - The files uploaded from this tab are not imported as invoice documents, unlike the attachments uploaded from the chatter.
   - The chatter and the side preview show the attachments of the list, and for each invoice only its own: a document shared by several invoices appears only in those listing it.
   - Removing a file from the list asks for a confirmation. On save, the file is deleted if it belongs to that invoice and no other invoice lists it; documents of other records are kept.
   - A file present in a list cannot be deleted (e.g. from the chatter): it must be removed from the list first.
   - If the XML has already been generated, the same tab shows the attachments actually present in the file and warns when they do not match the list: attachments of the list missing from the XML, attachments of the XML removed from the list (except the invoice PDF), or both. In these cases the XML might need to be generated again.
   - Vendor bills and refunds also show, in the same tab, the attachments present in the received XML, even when uploaded by hand or signed (`.p7m`).
   - Before the export, the XML is checked against the SdI limit of 5 MB per file. The size is estimated: attachments of the list and invoice PDF, if already generated, base64 encoded, plus an estimate of the rest of the XML based on the lines; a 100 KB margin is kept.
   - When migrating from 18.0, the attachments of the `l10n_it_edi.attachment` model of customer invoices and credit notes are moved to the list (except the invoice PDF coming from 16.0, that `l10n_it_edi` already includes). Those of vendor bills stay plain attachments: their attachments are read from the received XML. The description is kept and exported; the format and compression algorithm stored in 18.0 are no longer used: the format is taken from the extension.
   - Other modules can add attachments by writing in the `l10n_it_edi_ext_doc_attachment_ids` field or by extending `_l10n_it_edi_ext_get_doc_attachments`, and change the description by extending `_l10n_it_edi_ext_attachment_xml_description`.

   *Design choices*

   The attachments are a Many2many to `ir.attachment`, not an intermediate model with one line per attachment like the `fatturapa.attachments` of 16.0 or the `l10n_it_edi.attachment` of 18.0. This was chosen for simplicity: no additional model with access rights and multi-company rules, and other modules can attach existing files without duplicating them. This has two consequences:

   - the description is the one of the file (`ir.attachment.description`), and it is written and exported only for the files of the invoice (uploaded from the list or migrated). For files of other records the file name is used: their description is shared by all the records they are attached to and often holds internal texts;
   - a variant of the `many2many_binary` widget is needed (`l10n_it_edi_ext_doc_attachments`). The standard widget would upload the file as an attachment of the invoice, and `account` tries to import every attachment of an invoice as a document (`_extend_with_attachments`): an XML could add lines to the invoice. The variant uploads the file without a linked record, and the module links it to the invoice on save.

   The uploaded files are linked to the invoice with `res_field` set to the list field, as `l10n_it_edi` does for the XML: they are not documents of the invoice, so they do not end up in the chatter by themselves, and the chatter shows exactly the list (`_get_mail_thread_data_attachments`). The field has `skip_res_field_check` in its context, otherwise `ir.attachment._search` would hide them from the list too.

\<<https://www.fatturapa.gov.it>\>
