**Italiano**

Per utilizzare il meccanismo delle Ri.Ba. è necessario configurare un termine
di pagamento di tipo 'Ri.Ba.'.

Per emettere una distinta è necessario andare su *Ri.Ba. → Emetti Ri.Ba.* e
selezionare i pagamenti per i quali emettere la distinta.
Se per il cliente è stato abilitato il raggruppamento, i pagamenti dello stesso
cliente e con la stessa data di scadenza andranno a costituire un solo elemento
della distinta.

I possibili stati della distinta sono: *Bozza*, *Accettata*, *Accreditata*,
*Pagata*, *Insoluta* e *Annullata*.
Ad ogni passaggio di stato sarà possibile generare le relative registrazioni
contabili, le quali verranno riepilogate nella scheda «Contabilità».
Questa scheda è presente sia sulla distinta che sulle sue righe.
Queste ultime hanno una vista dedicata per facilitare le
operazioni sul singolo elemento invece che su tutta la distinta.

La voce di menù 'Presentazione Riba' permette di estrarre le riba fino al
raggiungimento dell'importo massimo inserito dall'utente. La stessa procedura
guidata è possibile utilizzarla selezionando i records dalla vista a lista e poi
cliccare su 'Presentazione Riba' tra le azioni.

Nella lista delle fatture è presente una colonna per monitorare l'
esposizione, cioè l'importo dovuto dal cliente a fronte dell'emissione
della RiBa non ancora scaduta.

In maniera predefinita la data delle registrazioni dei pagamenti viene
impostata con la data di scadenza della RiBa, ma è possibile modificarla in due momenti:

 - durante la creazione del pagamento,
   cliccando su "Segna righe come pagate" o su "Segna coma pagata"
   o usando l'azione "Registrazione Riba a data di scadenza"
   e indicando una data nel campo `Data pagamento`,
 - successivamente a pagamento effettivamente avvenuto selezionando la selezionando la
   registrazione dalla vista ed elenco ed eseguendo l'azione "Imposta data
   di pagamento RiBa".
