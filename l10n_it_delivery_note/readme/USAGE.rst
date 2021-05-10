Funzionalità base
~~~~~~~~~~~~~~~~~

Quando un prelievo viene validato compare una scheda DDT.

Nella scheda fare clic su "Crea nuovo", si apre un procedura guidata dove scegliere il tipo di DDT, quindi confermare. Immettere i dati richiesti e poi fare clic su "Valida" per numerare il DDT.

Una volta validato, è possibile emettere fattura direttamente dal DDT se il DDT stesso è di tipo consegna a cliente (In uscita) e si hanno i permessi sull'utente.

È possibile annullare il DDT, reimpostarlo a bozza e poi modificarlo. Se il DDT è fatturato il numero e la data non sono modificabili.

Per i trasferimenti tra magazzini creare un prelievo di tipo interno con le relative ubicazioni. Validare il prelievo visualizza la scheda DDT.

È possibile anche avere DDT in ingresso, ovvero dopo la validazione del prelievo selezionare la scheda per indicare il numero del DDT fornitore e la data.

Funzionalità avanzata
~~~~~~~~~~~~~~~~~~~~~

Vengono attivate varie funzionalità aggiuntive:

- più prelievi per un DDT
- selezione multipla di prelievi e generazione dei DDT
- aggiunta righe nota e righe sezione descrittive.
- lista dei DDT.

Il report DDT stampa in righe aggiuntive i lotti/seriali e le scadenze del prodotto.

Il prezzo può essere indicato anche nel report DDT se nel tipo DDT è indicata la stampa prezzi.
La visibilità dei prezzi si trova nei permessi dell'utente.

Le fatture generate dai DDT contengono i riferimenti al DDT stesso nelle righe nota.


Migrazione dei dati da *l10n_it_ddt*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Il modulo presenta una funzione di migrazione dei dati dal modulo OCA *l10n_it_ddt* da eseguire manualmente.
Al momento, non è ancora presente un menù oppure una voce da interfaccia che permetta di eseguire questa operazione; bensì, è stato definito un comando da CLI da eseguire all’avvio di Odoo.
Di seguito, una piccola lista di passi da seguire per portare a termine la migrazione:

1. Eseguire un back-up del database.

   Questa procedura di migrazione dei dati è stata sì sviluppata e testata, MA solamente per un numero limitato di casi.
   NON è consigliata in alcun modo come funzionalità production-ready.

2. Installare il modulo *l10n_it_delivery_note* SENZA prima disinstallare il modulo OCA *l10n_it_ddt*.

   N.B.: NON iniziare ad usare il modulo *l10n_it_delivery_note* senza aver prima migrato i dati.
   Potrebbero verificarsi, in prima battuta, problemi legati alla numerazione dei documenti creati.
   Inoltre, la procedura di migrazione stessa è progettata affinché verifichi che non siano presenti documenti di *l10n_it_delivery_note*; qualora ne rilevi alcuni, si interromperà non eseguendo alcuna migrazione.

3. Terminata l’installazione del modulo, terminare in sicurezza il processo di Odoo.

4. Lanciare Odoo, nella maniera in cui si è soliti fare, aggiungendo alcuni parametri al comando d’avvio:

   `./odoo-bin migratel10nitddt --database <nome_database> [...]`

5. Una volta terminata l’esecuzione della procedura, verificare che tutti i documenti siano stati migrati con successo e nel modo atteso.

6. Verificata l’esattezza dei dati migrati, disinstallare il modulo *l10n_it_ddt*.

È possibile iniziare ad utilizzare *l10n_it_delivery_note*.
