**Italiano**

- stampare la lista dei reparti della vostra stampante fiscale
- mappare le imposta di vendita di odoo con i gruppi di imposte - dipartimenti della stampante fiscale, per ogni imposta di vendita in odoo, usando il campo "Reparto sulla stampante fiscale 1~99"
- in odoo, utilizzare imposte incluse nel prezzo
- connettere la vostra stampante fiscale alla rete locale e recuperare l'IP
- aprire la configurazione POS e impostare l'indirizzo IP della stampante
- è tutto, alla validazione del pagamento nella sessione POS, il sistema stamperà lo scontrino fiscale.

**English**

- print list departments of your fiscal printer
- map odoo sale taxes with taxes groups - departments of fiscal printer, for each sale tax on odoo, using field "Department on fiscal printer 1~99"
- in odoo, use taxes included in price
- connect your fiscal printer to local network and find IP
- open POS configuration and fill Printer IP Address field
- that's all, at validation of payment on POS session, system prints fiscal receipt.

EFT-POS / pagamento con carta (scambio importo)
-----------------------------------------------

**Italiano**

Questa funzione collega il terminale di pagamento (POS bancario) alla stampante
fiscale RT tramite lo "scambio importo" (protocollo ECR17 / Protocollo 17): al
momento del pagamento la stampante contatta il terminale, l'importo viene
autorizzato sul terminale e solo in caso di esito positivo vengono creati
l'ordine POS e lo scontrino fiscale.

Configurazione della stampante fiscale:

- da tastiera della stampante entrare in impostazione SET 31 (comando nativo
  ``4-031``, sequenza ``3333`` + CHIAVE + ``31``); per le stampanti collegate
  al terminale via seriale usare invece SET 17 (``4-017``)
- OFF-TIPO: tipo di terminale collegato (es. ``2`` = ECR17-INGENICO)
- POS-FP: modalità di gestione POS / stampante fiscale
- N.COPIE: numero di copie della cortesia POS
- ID: identificativo cassa
- RS/USB-LAN: tipo di collegamento verso il terminale (``1`` = LAN)
- LAN ADDR: indirizzo IP del terminale (12 cifre, formato puntato)
- LAN PORT: porta del terminale (default ``9100``)
- TIME-OUT: tempo massimo di attesa risposta (default ``60`` secondi)

Configurazione di odoo:

- aprire il metodo di pagamento (registratore di cassa) usato per la carta e,
  nella scheda del relativo sezionale contabile (account.journal), impostare
  "Payment type" = "Credit or Credit Card"
- valorizzare "Electronic Payment / Ticket Index" con l'indice del pagamento
  elettronico
- spuntare "Activate EFT-POS": con questa opzione, quando il pagamento usa
  questo sezionale, l'importo viene prima autorizzato sul terminale; se il
  terminale rifiuta (Errore 38) viene mostrato un errore e non viene creato
  alcun ordine né scontrino

**English**

This feature connects the payment terminal (bank POS) to the RT fiscal printer
through the "amount exchange" (ECR17 / Protocollo 17 protocol): at payment time
the printer dials the terminal, the amount is authorized on the terminal, and
only on approval are the POS order and the fiscal receipt created.

Fiscal printer configuration:

- from the printer keypad enter SET 31 setup (native command ``4-031``,
  sequence ``3333`` + KEY + ``31``); for printers connected to the terminal
  over serial use SET 17 (``4-017``) instead
- OFF-TIPO: type of connected terminal (e.g. ``2`` = ECR17-INGENICO)
- POS-FP: POS / fiscal-printer handling mode
- N.COPIE: number of POS courtesy copies
- ID: till identifier
- RS/USB-LAN: link type to the terminal (``1`` = LAN)
- LAN ADDR: terminal IP address (12 digits, dotted format)
- LAN PORT: terminal port (default ``9100``)
- TIME-OUT: maximum wait for the answer (default ``60`` seconds)

Odoo configuration:

- open the payment method (cash register) used for the card and, on its
  accounting journal (account.journal), set "Payment type" =
  "Credit or Credit Card"
- fill "Electronic Payment / Ticket Index" with the electronic payment index
- tick "Activate EFT-POS": with this option, when a payment uses this journal
  the amount is first authorized on the terminal; if the terminal declines
  (Error 38) an error is shown and no order and no receipt are created

