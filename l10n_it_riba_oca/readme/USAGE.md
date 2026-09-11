**Italiano**

Per utilizzare il meccanismo delle RiBa è necessario configurare un
termine di pagamento di tipo 'RiBa'.

Per emettere una distinta è necessario andare su *RiBa → Emetti RiBa* e
selezionare i pagamenti per i quali emettere la distinta. Se per il
cliente è stato abilitato il raggruppamento, i pagamenti dello stesso
cliente e con la stessa data di scadenza andranno a costituire un solo
elemento della distinta.

I possibili stati della distinta sono: *Bozza*, *Accettata*,
*Accreditata*, *Pagata*, *Insoluta* e *Annullata*. Ad ogni passaggio di
stato sarà possibile generare le relative registrazioni contabili, le
quali verranno riepilogate nella scheda «Contabilità». Fa eccezione lo
stato *Pagata*, che non è un'operazione da fare a mano: la distinta ci
arriva quando l'incasso viene riconciliato, come descritto sotto. Questa
scheda è presente sia sulla distinta che sulle sue righe.
Queste ultime hanno una vista dedicata per facilitare le
operazioni sul singolo elemento invece che su tutta la distinta.

Il campo `Data accettazione` è obbligatorio per poter indicare la RiBa come accettata.
All'accettazione, il valore del campo `Data accettazione`
verrà riportato sulle registrazioni contabili di accettazione.

La voce di menù 'Presentazione Riba' permette estrarre le riba fino al
raggiungimento dell'importo massimo inserito dall'utente.

Nella lista delle fatture è presente una colonna per monitorare l'
esposizione, cioè l'importo dovuto dal cliente a fronte dell'emissione 
della RiBa non ancora scaduta.

## Incasso della distinta

Il modulo non genera nessuna registrazione di incasso: la distinta
risulta pagata quando il movimento di conto corrente effettivo, in
riconciliazione bancaria, chiude il credito verso la banca.

Le righe da riconciliare sono elencate nella scheda «Contabilità» della
distinta, sotto «Righe da incassare»:

- 'Salvo buon fine': la riga in DARE del conto RiBa della registrazione
  di accredito. L'accredito rappresenta un credito su un conto a parte,
  di cui si può disporre fino all'incasso effettivo;
- 'Al dopo incasso': le righe in DARE del conto effetti attivi delle
  registrazioni di accettazione.

La riconciliazione avviene sul totale della distinta, e i pagamenti sono
gestiti come in fattura: i campi `Importo pagato` e `Importo residuo`
mostrano quanto la banca ha già accreditato e quanto deve ancora
incassare, e lo `Stato pagamento` passa a *Parzialmente pagata* e poi a
*Pagata*. Quando il residuo è zero la distinta passa in stato *Pagata*, e
il campo `Data pagamento` riporta la data della registrazione che l'ha
incassata. Se la riconciliazione viene annullata, la distinta torna in
stato *Accreditata* (o *Accettata* nel caso 'Al dopo incasso').

Le righe della distinta non hanno un pulsante per l'incasso e restano in
stato *Accreditata*: l'unica operazione che le riguarda singolarmente è
l'insoluto.

## Insoluto

Nei giorni successivi all'incasso la banca può comunicare l'insoluto di
una o più ricevute. L'insoluto è un'operazione manuale, da registrare per
ogni riga interessata: dalla distinta, o da *RiBa → Dettaglio distinte*,
si usa il pulsante "Segna come insoluta" sulla riga.

La registrazione generata riapre il credito verso il cliente sul conto
insoluti e chiude la parte corrispondente del conto RiBa (o del conto
effetti attivi nel caso 'Al dopo incasso'), riducendo quindi il residuo
della distinta come farebbe un incasso. Le eventuali spese di insoluto
addebitate dalla banca sono indicate nel wizard.

Il movimento di conto corrente con cui la banca addebita l'insoluto (e le
relative spese) va poi riconciliato manualmente. Per velocizzare
l'operazione conviene creare un modello di riconciliazione
(*Contabilità → Configurazione → Modelli di riconciliazione*) che
proponga il conto insoluti e il conto spese configurati nella
configurazione RiBa.

Non è possibile emettere Riba per fatture verso Enti che richiedono più di un CIG e un CUP differenti per fattura.
In questo caso particolare, emettere più fatture.
Non è possibile raggruppare Riba in fase di emissione se le fatture contengono CIG e CUP differenti. Verrà creata una riga di distinta per ogni fattura.
