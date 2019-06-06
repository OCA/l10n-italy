**Italiano**

In Impostazioni → Utenti e aziende → Aziende → <nome_azienda>
impostare i parametri delle seguenti sezioni presenti nella scheda "Informazioni generali":

1. Intrastat

   a) ID utente (codice UA): inserire il codice identificativo Intrastat dell’azienda (codice alfanumerico di 4 caratteri, utilizzato come identificativo per l’accesso alle applicazioni delle Dogane)
   b) Unità di misura per Kg: parametro che indica l’unità di misura che viene verificata sulla riga fattura soggetta a Intrastat. Se sulla riga il peso è espresso nell’unità di misura indicata nel parametro (o in un suo multiplo), il peso che viene riportato nella corrispondente riga Intrastat è quello preso dalla riga fattura. In caso contrario, il peso viene rilevato secondo la configurazione del parametro che segue (Peso dal prodotto).
   c) Peso dal Prodotto: indica se, invece che dalla riga fattura, il peso debba essere:

      i. prelevato dalla scheda prodotto (opzioni “Peso netto” o “Peso Lordo)
      ii. impostato manualmente dall’utente (opzione “Nessuno”)

   d) Unità supplementari da:

      i. peso: da peso dei prodotti sulla riga Intrastat
      ii. quantità: da peso dei prodotti sulla riga Intrastat
      iii. nessuno

   e) Escludere righe omaggio: esclude dalle righe Intrastat le righe a valore 0
   f) Persona delegata: il nominativo della persona delegata alla presentazione della dichiarazione Intrastat
   g) P. IVA persona delegata: la partita IVA della persona delegata alla presentazione della dichiarazione Intrastat
   h) Nome file per esportazione: nome del file che può essere impostato per forzare quello predefinito (SCAMBI.CEE)
   i) Sezione doganale: sezione doganale predefinita da proporre in una nuova dichiarazione

2. Valori predefiniti per vendite (parametri Intrastat per le fatture di vendita)

   a) Forzare valore statistico in euro: casella di selezione attualmente non gestita
   b) Natura della transazione: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento
   c) Condizioni di consegna: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento
   d) Modalità di trasporto: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento (Modo di trasporto)
   e) Provincia di origine: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento (Provincia di origine della spedizione di merce venduta)

3. Valori predefiniti per acquisti (parametri Intrastat per le fatture di acquisto)

   a) Forzare valore statistico in euro: flag attualmente non gestito
   b) Natura della transazione: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento
   c) Condizioni di consegna: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento
   d) Modalità di trasporto: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento (Modo di trasporto)
   e) Provincia di destinazione: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento (Provincia di destinazione della spedizione di merce acquistata)

**Tabelle​ di​ ​sistema**


In Fatturazione/Contabilità → Configurazione → Intrastat
sono presenti le funzionalità per la gestione delle tabelle di sistema.

- Sezione doganale
- Nomenclature combinate
- Modalità di trasporto
- Natura della transazione

Tali tabelle sono pre-popolate in fase di installazione del modulo, in base ai valori ammessi per le dichiarazioni Intrastat.

**Posizione​ ​fiscale**

L'assoggettamento ad Intrastat può essere gestito anche a livello generale di singolo partner, associandogli una posizione fiscale che abbia l'apposita casella "Soggetta a Intrastat" selezionata.

Tutte le fatture create per il partner che ha una posizione fiscale marcata come soggetta ad Intrastat avranno l’apposito campo "Soggetta a Intrastat" selezionato automaticamente.


**Prodotti​ e categorie**

La classificazione Intrastat delle merci o dei servizi può essere fatta sia a livello di categoria che a livello​ di prodotto.

La priorità è data al prodotto: se su un prodotto non è configurato un codice Intrastat, il sistema tenta di​ ricavarlo dalla categoria a cui quel prodotto è associato.

Per il prodotto la sezione intrastat​ è nel tab Contabilità, ove è necessario inserire:

- la tipologia (Merce, Servizio, Varie, Escludi)
- il codice Intrastat, tra quelli censiti tramite l’apposita tabella di sistema Nomenclature combinate (il campo viene abilitato solo per le tipologie​ "Merce" e "Servizio")


Per le categorie di prodotti, le informazioni sono presenti in un’apposita area Intrastat della maschera di dettaglio:


**Fatture​ e Note​ di credito​ Intrastat**

E' possibile indicare l’assoggettamento di una fattura ad Intrastat attraverso l'apposito campo presente sulla maschera di modifica della fattura stessa.

Sulla scheda Intrastat è presente un pulsante «Ricalcola righe Intrastat». Il pulsante permette al sistema:

- di verificare se le righe prodotto presenti in fattura (scheda "Righe Fattura") si riferiscono a prodotti che hanno un codice Intrastat assegnato, o appartengono ad una categoria che ha un codice Intrastat​ aggregato
- di generare per questi prodotti le corrispondenti righe Intrastat: le righe accorpano prodotti omogenei per codice Intrastat, indicando nel campo Massa netta (kg) il peso totale dei prodotti presenti nelle corrispondenti righe. La riga Intrastat, ovviamente, raggruppa il valore economico dei prodotti.
- NB: se una riga presente in fattura si riferisce ad un prodotto che ha come tipologia Intrastat “Varie”, l’importo della riga verrà automaticamente suddiviso in maniera uguale sulle altre righe Intrastat che si riferiscono a merci o servizi. Tale automatismo permette di gestire, in maniera conforme a quanto previsto dalla normativa, il ribaltamento proporzionale dei costi sostenuti per spese accessorie (es: spese di trasporto) sui costi sostenuti per l’acquisto vero e proprio di merce o servizi.

Nella scheda Intrastat, un clic su una riga Intrastat permette di accedere alla maschera di dettaglio.

Nella​ ​ maschera:

- il campo Paese partner viene popolato in automatico dal campo "Nazione" dell’indirizzo associato​ al  partner
- i campi configurati in Configurazione → Aziende → Aziende → <company> (vedi Configurazione su company​ ) vengono popolati in automatico con i valori predefiniti impostati, in ragione della tipologia di fattura​ (vendita o acquisto)
- se fattura di vendita:
  1. i campi Origine → "Paese di provenienza" e Origine → "Paese di origine" vengono popolati in automatico con la nazione presente nell’indirizzo associato alla company
  2. il campo Destinazione → Nazione destinazione viene popolato in automatico con la nazione presente nell'indirizzo associato al partner
- se​ fattura di acquisto:
  1. i campi Origine → "Paese di provenienza" e Origine → "Paese di origine" vengono popolati in automatico con la nazione presente nell’indirizzo associato al partner (fornitore)
  2. il​ campo Destinazione → Nazione destinazione viene preso ​dai dati della company

NB: tutti i campi possono ovviamente essere modificati, ma l’utilizzo del pulsante «Ricalcola righe Intrastat» ripristinerà i valori predefiniti, sui campi prelevati dalla configurazione della company o dalla riga fattura.


**Note​ di​ credito**


Nelle note di credito, sulla scheda Intrastat, è presente inoltre un menù a tendina che permette di selezionare il periodo fiscale di riferimento da rettificare per la nota di credito. Tale valore sarà utilizzato automaticamente​ nella dichiarazione (sezioni 2 e 4 - Rettifiche).

Importante:

se si seleziona un periodo che è lo stesso della dichiarazione, la nota di credito, per il suo importo, non confluirà nella sezione di rettifica, ma andrà a stornare direttamente il valore della fattura sulla quale è stata emessa. La verifica sulla fattura da stornare viene fatta confrontando la coppia di valori partner/nomenclatura combinata.
