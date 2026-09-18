**Italiano**

Questo modulo implementa il canale PEC (Posta Elettronica Certificata)
per la comunicazione con il Sistema di Interscambio (SdI), in
alternativa al proxy IAP standard di Odoo.

Si basa su `l10n_it_edi_sdi` per la logica condivisa di elaborazione
delle notifiche e ricezione delle fatture, aggiungendo il trasporto
specifico via PEC.

Funzionalità principali:

- Invio fatture elettroniche via PEC al SdI
- Ricezione email PEC dal SdI e instradamento ai gestori appropriati
- Gestione errori PEC con notifica automatica ai contatti configurati
  e disabilitazione del server dopo ripetuti fallimenti
- Configurazione server SMTP e IMAP/POP3 dedicati alla PEC

**English**

This module implements the PEC (Certified Email) transport channel for
communication with the Italian Exchange System (SdI), as an alternative
to Odoo's standard IAP proxy.

It builds on `l10n_it_edi_sdi` for the shared notification processing
and invoice reception logic, adding PEC-specific transport.

Main features:

- Send electronic invoices to SdI via PEC
- Receive PEC emails from SdI and route to appropriate handlers
- PEC error handling with automatic notification to configured contacts
  and server auto-disable after repeated failures
- Dedicated SMTP and IMAP/POP3 server configuration for PEC
