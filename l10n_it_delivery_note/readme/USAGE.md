## Funzionalità base

Quando un prelievo viene validato compare una scheda DDT.

Nella scheda fare clic su "Crea nuovo", si apre un procedura guidata
dove scegliere il tipo di DDT, quindi confermare. Immettere i dati
richiesti e poi fare clic su "Valida" per numerare il DDT.

Una volta validato, è possibile emettere fattura direttamente dal DDT se
il DDT stesso è di tipo consegna a cliente (In uscita) e si hanno i
permessi sull'utente.

È possibile annullare il DDT, reimpostarlo a bozza e poi modificarlo. Se
il DDT è fatturato il numero e la data non sono modificabili.

Per i trasferimenti tra magazzini creare un prelievo di tipo interno con
le relative ubicazioni. Validare il prelievo visualizza la scheda DDT.

È possibile anche avere DDT in ingresso, ovvero dopo la validazione del
prelievo selezionare la scheda per indicare il numero del DDT fornitore
e la data.

## Funzionalità avanzata

Vengono attivate varie funzionalità aggiuntive:

- più prelievi per un DDT
- selezione multipla di prelievi e generazione dei DDT
- aggiunta righe nota e righe sezione descrittive.
- lista dei DDT.

Il report DDT stampa in righe aggiuntive i lotti/seriali e le scadenze
del prodotto.

Il prezzo può essere indicato anche nel report DDT se nel tipo DDT è
indicata la stampa prezzi. La visibilità dei prezzi si trova nei
permessi dell'utente.

Le fatture generate dai DDT contengono i riferimenti al DDT stesso nelle
righe nota.

## Fatturazione da DN

E' possibile creare una fattura selezionando una o più DN dello stesso partner 
dalla tree view tramite il wizard "crea fattura".
Si può scegliere se includere anche i servizi non ancora fatturati dell'ordine 
di vendita correlato o considerare solo le righe nei DN.
In maniera predefinita vengono dedotti gli eventuali anticipi fatturati.

### Utilizzo dei dati dal DDT nelle fatture

Dalle impostazioni (*Inventario → Configurazione → Impostazioni - Documenti di Trasporto*)
è possibile configurare se la fattura deve utilizzare i dati dal DDT anziché
dall'ordine di vendita:

- **Usa Nome Prodotto da DDT nelle Fatture**: Quando attivo, la descrizione del
  prodotto nella fattura viene presa dal DDT invece che dall'ordine di vendita.
  Utile quando si modificano le descrizioni nel DDT per riflettere ciò che è
  stato effettivamente consegnato.

- **Usa Prezzo Unitario da DDT nelle Fatture**: Quando attivo, il prezzo unitario
  nella fattura viene preso dal DDT invece che dall'ordine di vendita.
  Utile per negoziazioni di prezzo al momento della consegna o quando si
  sostituiscono prodotti con prezzi diversi.

**Esempi pratici:**

1. **Prodotto sostituito**: Se ordini "Scrivania Modello A - €500" ma consegni
   "Scrivania Modello B - €450", modificando DDT e attivando entrambe le opzioni,
   la fattura rifletterà automaticamente il prodotto e prezzo reale consegnato.

2. **Negoziazione alla consegna**: Se il cliente nota un difetto e negoziate uno
   sconto, modificando il prezzo nel DDT con l'opzione attiva, la fattura sarà
   corretta senza bisogno di note credito.

3. **Descrizioni dettagliate**: Se nel DDT specifichi "3 sacchi cemento CEM II,
   5 pannelli isolanti" invece di "Materiale edile vario", con l'opzione attiva
   la fattura mostrerà i dettagli completi.

**Nota**: Queste opzioni sono disabilitate per default per mantenere la
retrocompatibilità. Attivarle solo se si desidera questo comportamento.

## Accesso da portale

Gli utenti portal hanno la possibilità di scaricare i report dei DDT di cui loro o la loro azienda padre sono impostati come destinatari o indirizzo di spedizione.
