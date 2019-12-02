**Italiano**


**Fatture e note di credito Intrastat**

È possibile indicare l’assoggettamento di una fattura ad Intrastat attraverso l'apposito campo presente sulla maschera di modifica della fattura stessa.

Sulla scheda Intrastat è presente un pulsante «Ricalcola righe Intrastat». Il pulsante permette al sistema:

- di verificare se le righe prodotto presenti in fattura (scheda "Righe fattura") si riferiscono a prodotti che hanno un codice Intrastat assegnato, o appartengono ad una categoria che ha un codice Intrastat aggregato;
- di generare per questi prodotti le corrispondenti righe Intrastat: le righe accorpano prodotti omogenei per codice Intrastat, indicando nel campo "Massa netta (kg)" il peso totale dei prodotti presenti nelle corrispondenti righe. La riga Intrastat, ovviamente, raggruppa il valore economico dei prodotti;
- N.B.: se una riga presente in fattura si riferisce ad un prodotto che ha come tipologia Intrastat “Varie”, l’importo della riga verrà automaticamente suddiviso in maniera uguale sulle altre righe Intrastat che si riferiscono a beni o servizi. Tale automatismo permette di gestire, in maniera conforme a quanto previsto dalla normativa, il ribaltamento proporzionale dei costi sostenuti per spese accessorie (es: spese di trasporto) sui costi sostenuti per l’acquisto vero e proprio di beni o servizi.

Nella scheda Intrastat, un clic su una riga Intrastat permette di accedere alla maschera di dettaglio.

Nella maschera:

- il campo "Stato acquirente/fornitore" viene popolato in automatico dal campo "Nazione" dell’indirizzo associato al partner;
- i campi configurati in *Impostazioni → Utenti e aziende → Aziende → Nome azienda* (vedi "Informazioni generali" su azienda) vengono popolati in automatico con i valori predefiniti impostati, in ragione della tipologia di fattura (vendita o acquisto);
- se fattura di vendita:

  1. i campi *Origine → Paese di provenienza* e *Origine → Paese di origine* vengono popolati in automatico con la nazione presente nell’indirizzo associato all'azienda;
  2. il campo *Destinazione → Paese di destinazione* viene popolato in automatico con la nazione presente nell'indirizzo associato al partner;

- se fattura di acquisto:

  1. i campi *Origine → Paese di provenienza* e *Origine → Paese di origine* vengono popolati in automatico con la nazione presente nell’indirizzo associato al partner (fornitore);
  2. il campo *Destinazione → Paese di destinazione* viene preso dai dati dell'azienda.

N.B.: tutti i campi possono ovviamente essere modificati, ma l’utilizzo del pulsante «Ricalcola righe Intrastat» ripristinerà i valori predefiniti, sui campi prelevati dalla configurazione dell'azienda o dalla riga fattura.


**Note di credito**

Importante:
   Se si seleziona un periodo che è lo stesso della dichiarazione, la nota di credito, per il suo importo, non confluirà nella sezione di rettifica, ma andrà a stornare direttamente il valore della fattura sulla quale è stata emessa. La verifica sulla fattura da stornare viene fatta confrontando la coppia di valori *Partner/Nomenclatura combinata*.
