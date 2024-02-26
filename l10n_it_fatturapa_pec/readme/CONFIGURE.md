**Italiano**

Consultare il modulo l10n_it_sdi_channel.

Creare un nuovo canale di tipo PEC (unico supportato per ora) e
indicare:

- Il server PEC da utilizzare per inviare/ricevere attraverso lo SdI
- La email PEC dello SdI, inizialmente uguale a <sdi01@pec.fatturapa.it>

Dopo il primo invio, lo SdI risponderà segnalando l'indirizzo da
utilizzare per gli invii successivi, da inserire nella configurazione
del server PEC dedicato.

Nella configurazione del server smtp, sezione "PEC e fattura
elettronica", selezionare la casella "Server PEC e-fattura".

Indicare quindi la email da usare per l'invio e la ricezione,
solitamente è uguale al nome utente di connessione (può essere diversa
in casi particolari).

È preferibile avere una email dedicata solo alla fatturazione
elettronica, in quanto i messaggi di altro tipo non possono essere
gestiti da Odoo (verrebbero marcati comunque come letti).

Se si usano altri server SMTP per l'invio di email non PEC, è necessario
aumentare la loro priorità rispetto a quella del server PEC.

Lo stato dell'esportazione XML può essere forzato impostando 'Permettere
di forzare lo stato dell'esportazione e-fattura' nelle impostazioni
tecniche dell'utente.

Per ogni azienda, in

Contabilità → Configurazione → Impostazioni → Fatture elettroniche

specificare l'utente che sarà utilizzato come creatore delle e-fatture
fornitore create dalla PEC.

**English**

See l10n_it_sdi_channel module.

Create a new PEC channel type (the only one supported right now) and
indicate:

- PEC server to be used for sending to/receiving from ES
- ES PEC email, initially equal to <sdi01@pec.fatturapa.it>

After sending the first email, ES will reply indicating the address to
use for all the others, to be entered in dedicated PEC server
configuration.

In smtp server configuration, select 'E-invoice PEC server' in 'PEC and
Electronic Invoice' section.

Then specify the email to use for sending and receiving, it is usually
equal to connection username (can be different in special cases).

It would be better to have a dedicated email for electronic invoicing,
because other kind of messages can't be managed by Odoo (they would be
marked as seen).

If you use other SMTP servers for non-PEC email sending, you need to
increase their priority as compared to PEC server one.

XML export state can ba forced setting 'Allow to force the supplier
e-bill export state' in user's technical settings.

For every company, in

Accounting → Configuration → Settings → Electronic Invoices

set the user who will be used as creator of supplier e-bill
automatically created from PEC.
