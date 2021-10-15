**Italiano**

Andare in Contabilità →  Configurazione →  Contabilità →  Canali SdI

Creare un nuovo canale di tipo PEC (unico supportato per ora) e indicare:

- Il server PEC da utilizzare per inviare/ricevere attraverso lo SdI
- La email PEC dello SdI, inizialmente uguale a sdi01@pec.fatturapa.it

Dopo il primo invio, lo SdI risponderà segnalando l'indirizzo da utilizzare per gli invii successivi, da inserire nella configurazione del server PEC dedicato.

Nella configurazione del server, sezione "PEC e fattura elettronica", selezionare la casella "Server PEC e-fattura".

Indicare quindi la email da usare per l'invio e la ricezione, solitamente è uguale al nome utente di connessione (può essere diversa in casi particolari).

È preferibile avere una email dedicata solo alla fatturazione elettronica, in quanto i messaggi di altro tipo non possono essere gestiti da Odoo (verrebbero marcati comunque come letti).

Se si usano altri server SMTP per l'invio di email non PEC, è necessario aumentare la loro priorità rispetto a quella del server PEC.

**English**

Go to Accounting →  Configuration →  Accounting →  ES Channels

Create a new PEC channel type (the only one supported right now) and indicate:

- PEC server to be used for sending to/receiving from ES
- ES PEC email, initially equal to sdi01@pec.fatturapa.it

After sending the first email, ES will reply indicating the address to use for all the others, to be entered in dedicated PEC server configuration.

In server configuration, select 'E-invoice PEC server' in 'PEC and Electronic Invoice' section.

Then specify the email to use for sending and receiving, it is usually equal to connection username (can be different in special cases).

It would be better to have a dedicated email for electronic invoicing, because other kind of messages can't be managed by Odoo (they would be marked as seen).

If you use other SMTP servers for non-PEC email sending, you need to increase their priority as compared to PEC server one.
