**Italiano**

## Invio fatture

Le fatture vengono inviate al SdI tramite PEC quando si utilizza il
normale flusso di invio fattura elettronica di Odoo. Il modulo
intercetta l'invio e usa la PEC al posto del proxy IAP standard.

## Ricezione notifiche

Le notifiche dal SdI vengono ricevute automaticamente tramite il
cron di fetchmail. Lo stato della fattura viene aggiornato
automaticamente in base alla notifica ricevuta:

- RC (Ricevuta di Consegna) → Inoltrata al destinatario
- NS (Notifica di Scarto) → Rifiutata
- MC (Mancata Consegna) → Inoltro al destinatario fallito
- NE (Notifica Esito) → Accettata/Rifiutata dal partner PA
- DT (Decorrenza Termini) → Accettata per decorrenza termini

## Ricezione fatture passive

Le fatture dei fornitori inviate tramite SdI vengono ricevute
automaticamente via PEC e importate come fatture in bozza.

## Verifica manuale stato

Il pulsante "Verifica stato" sulla fattura inviata avvia una
lettura manuale della casella PEC per recuperare eventuali
notifiche in attesa.

**English**

## Sending invoices

Invoices are sent to SdI via PEC when using Odoo's standard
electronic invoice sending flow. The module intercepts the send
and uses PEC instead of the standard IAP proxy.

## Receiving notifications

SdI notifications are received automatically via the fetchmail
cron. The invoice state is updated automatically based on the
notification received:

- RC (Delivery Receipt) → Forwarded to recipient
- NS (Rejection) → Rejected
- MC (Failed Delivery) → Forward to recipient failed
- NE (Outcome Notification) → Accepted/Rejected by PA partner
- DT (Deadline Expiry) → Accepted after term expiry

## Receiving vendor bills

Vendor bills sent through SdI are automatically received via PEC
and imported as draft invoices.

## Manual status check

The "Check status" button on a sent invoice triggers a manual
PEC mailbox read to retrieve any pending notifications.
