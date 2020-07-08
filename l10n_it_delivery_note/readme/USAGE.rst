Funzionalità base.

Quando un picking è validato si visualizza un tab DdT.
Dal tab "Crea nuovo" si apre un wizard dove scegliere il tipo di DDT e poi conferma. Immettere i dati richiesti poi "Valida" per numerare il DDT.
Una volta Validato il DDT è possibile emettere fattura direttamente dal DDT, se il DDT è di tipo consegna a cliente (outgoing) e si hanno i permessi sull'utente.
E' possibile annullare il DDT reimpostarlo in bozza e poi modificarlo. Se il DDT è fatturato il numero e data non sono modificabili.
per i trasferimenti tra magazzini creare un picking di tipo interno, con le ubicazioni relative, validare il picking e il tab DDT viene visualizzato.
è possibile anche avere i ddt in ingresso ovvero validato il picking si apre il tab DDT per indicare il numero DDT fornitore e data .

Funzionalità Avanzata.

vengono attivate varie funzionalità aggiuntive:
- più picking per un DDT
- selezione multipla di picking e generazione di DDT
- aggiunta righe note e righe sezione descrittive.
- lista dei DDT.

Il report DDT stampa in righe aggiuntive i lotti/ seriali scadenze del prodotto.

Il prezzo può essere indicato anche nel report DDT se il tiipo DDT è indicata la stampa prezzi.
La visibilità dei prezzi è sui permessi dell'utente.

Le fatture generate dai DDT hanno nelle righe note i riferimenti al DDT.


Se è installato :code: “l10n_it_ddt” seguire i seguenti passi.

Migrazione dei dati da “l10n_it_ddt”
Il modulo presenta una funzione di migrazione dei dati dal modulo OCA “l10n_it_ddt” da eseguire manualmente.
Al momento, non è ancora presente un menù oppure una voce in interfaccia che permetta di eseguire questa operazione; bensì, è stato definito un CLI da eseguire all’avvio di Odoo.
Di seguito, una piccola lista di passi da seguire per portare a termine la migrazione:

Eseguire un back-up del database.
Questa procedura di migrazione dei dati è stata, sì, sviluppata e testata MA solamente per un numero limitato di casi.
NON mi sento, assolutamente, confidente nel definirla una feature production-ready.


Installare il modulo “l10n_it_delivery_note” SENZA prima disinstallare il modulo OCA “l10n_it_ddt”.

NON iniziare ad usare il modulo “l10n_it_delivery_note” senza aver prima migrato i dati.
Potrebbero verificarsi, in prima battuta, problemi legati alla numerazione dei documenti creati.
Inoltre, la procedura di migrazione stessa, è progettata affinché verifichi non siano presenti documenti di “l10n_it_delivery_note”; qualora ne rilevi alcuni, si interromperà non eseguendo alcuna migrazione.


Terminata l’installazione del modulo, terminate in sicurezza il processo di Odoo.
Lanciare, nella maniera in cui si è soliti fare, Odoo aggiungendo alcuni parametri al comando d’avvio:

./odoo-bin migrate_ddt_data --database <nome_database> [...]

Una volta terminata l’esecuzione della procedura, verificare che tutti i documenti siano stati migrati con successo e nella maniera in cui ci si aspetterebbe.
Verificata l’esattezza dei dati migrati, disinstallare il modulo “l10n_it_ddt”.
È possibile iniziare ad utilizzare “l10n_it_delivery_note”.
