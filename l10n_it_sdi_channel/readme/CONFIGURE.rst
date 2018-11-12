Nel menu: Contabilità > Configurazione > Contabilità > SdI Channels va creato
un nuovo canale di tipo PEC (unico supportato per ora) in cui vanno inseriti:

- La mail PEC dello SdI, inizialmente uguale a sdi01@pec.fatturapa.it.

Dopo il primo invio, lo SdI risponderà segnalando l'indirizzo da utilizzare
per i successivi invii, che va quindi inserito nel server PEC dedicato.

- Il server PEC da utilizzare per gli invii/ricezioni verso lo SdI.

Tale
server è preferibile sia dedicato solo a questo utilizzo, in quanto i messaggi
di altro genere non verrebbero gestiti da Odoo, ma risulterebbero comunque
letti.

In questo server va indicata la mail di invio/ricezione, solitamente
uguale all'utente di connessione (potrebbe essere diversa dall'utente di
connessione in casi particolari).
