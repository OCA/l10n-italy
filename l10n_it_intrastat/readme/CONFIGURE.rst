**Italiano**

In *Impostazioni → Utenti e aziende → Aziende → Nome azienda*
impostare i parametri delle seguenti sezioni presenti nella scheda "Informazioni generali".

1. Intrastat

   a) *ID utente (codice UA)*: inserire il codice identificativo Intrastat dell’azienda (codice alfanumerico di 4 caratteri, utilizzato come identificativo per l’accesso alle applicazioni delle Dogane).
   b) *Unità di misura per kg*: parametro che indica l’unità di misura che viene verificata sulla riga fattura soggetta a Intrastat. Se sulla riga il peso è espresso nell’unità di misura indicata nel parametro (o in un suo multiplo), il peso che viene riportato nella corrispondente riga Intrastat è quello preso dalla riga fattura.
   c) *Unità supplementare da*:

      i. *peso*: da peso dei prodotti sulla riga Intrastat
      ii. *quantità*: da quantità dei prodotti sulla riga Intrastat
      iii. *nulla*

   d) *Escludere righe omaggio*: esclude dalle righe Intrastat le righe a valore 0.
   e) *Delegato*: il nominativo della persona delegata alla presentazione della dichiarazione Intrastat.
   f) *Partita IVA delegato*: la partita IVA della persona delegata alla presentazione della dichiarazione Intrastat.
   g) *Nome file da esportare*: nome del file che può essere impostato per forzare quello predefinito (SCAMBI.CEE).
   h) *Sezione doganale*: sezione doganale predefinita da proporre in una nuova dichiarazione.
   i) *Ammontare minimo*: in caso di fatture di importo inferiore usa questo valore nella dichiarazione.

2. Valori predefiniti per cessioni (parametri Intrastat per le fatture di vendita)

   a) *Forzare valore statistico in euro*: casella di selezione attualmente non gestita.
   b) *Natura transazione*: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento.
   c) *Condizioni di consegna*: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento.
   d) *Modalità di trasporto*: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento (Modo di trasporto).
   e) *Provincia di origine*: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento (provincia di origine della spedizione dei beni venduti).

3. Valori predefiniti per acquisti (parametri Intrastat per le fatture di acquisto)

   a) *Forzare valore statistico in euro*: casella di selezione attualmente non gestita.
   b) *Natura transazione*: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento.
   c) *Condizioni di consegna*: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento.
   d) *Modalità di trasporto*: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento (Modo di trasporto).
   e) *Provincia di destinazione*: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento (provincia di destinazione della spedizione dei beni acquistati).


**Tabelle di sistema**

In *Fatturazione/Contabilità → Configurazione → Intrastat*
sono presenti le funzionalità per la gestione delle tabelle di sistema.

- Sezioni doganali
- Nomenclature combinate
- Modalità di trasporto
- Natura transazione

Tali tabelle sono pre-popolate in fase di installazione del modulo, in base ai valori ammessi per le dichiarazioni Intrastat.

N.B.: Il sottomenù "Intrastat" è visibile solo se vengono abilitate le funzionalità contabili complete.


**Posizione fiscale**

L'assoggettamento ad Intrastat può essere gestito anche a livello generale di singolo partner, associandogli una posizione fiscale che abbia l'apposita casella "Soggetta a Intrastat" selezionata.

Tutte le fatture create per il partner che ha una posizione fiscale marcata come soggetta ad Intrastat avranno l’apposito campo "Soggetta a Intrastat" selezionato automaticamente.


**Prodotti e categorie**

La classificazione Intrastat dei beni o dei servizi può essere fatta sia a livello di categoria che a livello di prodotto.

La priorità è data al prodotto: se su un prodotto non è configurato un codice Intrastat, il sistema tenta di ricavarlo dalla categoria a cui quel prodotto è associato.

Per il prodotto la sezione Intrastat si trova nella scheda «Fatturazione/Contabilità», ove è necessario inserire:

- la tipologia (Bene, Servizio, Varie, Escludere);
- il codice Intrastat, tra quelli censiti tramite l’apposita tabella di sistema "Nomenclature combinate" (il campo viene abilitato solo per le tipologie "Bene" e "Servizio").

Per le categorie di prodotti, le informazioni sono presenti in un’apposita area Intrastat della maschera di dettaglio.
