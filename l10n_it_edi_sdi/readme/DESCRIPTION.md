**Italiano**

Questo modulo fornisce la logica condivisa per la comunicazione con il
Sistema di Interscambio (SdI), indipendente dal canale di trasporto
utilizzato (PEC, web service, ecc.).

Funzionalità principali:

- Ricezione e importazione di fatture elettroniche passive da SdI
- Elaborazione delle notifiche SdI (Ricevuta di Consegna, Notifica di
  Scarto, Mancata Consegna, Notifica Esito, Decorrenza Termini)
- Ricerca delle fatture associate alle notifiche tramite il nome file
- Riconoscimento dei file SdI tramite espressioni regolari

Questo modulo non è pensato per essere utilizzato direttamente, ma come
dipendenza per moduli che implementano un canale di trasporto specifico,
come `l10n_it_edi_pec`.

**English**

This module provides shared logic for communication with the Italian
Exchange System (SdI), independent of the transport channel used
(PEC, web service, etc.).

Main features:

- Receive and import incoming vendor bills from SdI
- Process SdI notifications (Delivery Receipt, Rejection, Failed
  Delivery, Outcome Notification, Deadline Expiry)
- Look up invoices related to notifications by attachment filename
- Recognise SdI files through regular expressions

This module is not intended for direct use, but as a dependency for
modules implementing a specific transport channel, such as
`l10n_it_edi_pec`.
