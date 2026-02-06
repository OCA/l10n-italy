**Italiano**

Questo modulo permette di inviare e ricevere fatture elettroniche
tramite PEC (Posta Elettronica Certificata) in alternativa al proxy IAP
standard di Odoo.

Il modulo si integra con il sistema di fatturazione elettronica di
Odoo 18 (`l10n_it_edi`), sovrascrivendo il canale di comunicazione
per utilizzare la PEC come mezzo di trasmissione verso il Sistema
di Interscambio (SdI).

Funzionalità principali:

- Invio fatture elettroniche via PEC al SdI
- Ricezione notifiche SdI (Ricevuta di Consegna, Notifica di Scarto,
  Mancata Consegna, Notifica Esito, Decorrenza Termini,
  Attestazione di Trasmissione)
- Ricezione fatture passive da SdI via PEC
- Gestione errori PEC con notifica automatica e disabilitazione
  del server dopo ripetuti fallimenti

**English**

This module allows sending and receiving electronic invoices
via PEC (Certified Email) as an alternative to Odoo's standard
IAP proxy.

The module integrates with Odoo 18's Italian electronic invoicing
system (`l10n_it_edi`), overriding the communication channel to
use PEC for transmission to the Exchange System (SdI).

Main features:

- Send electronic invoices to SdI via PEC
- Receive SdI notifications (Delivery Receipt, Rejection,
  Failed Delivery, Outcome Notification, Deadline Expiry,
  Transmission Attestation)
- Receive incoming vendor bills from SdI via PEC
- PEC error handling with automatic notification and server
  auto-disable after repeated failures
