**Italiano**

Questo modulo integra il Punto Vendita (POS) di Odoo con stampanti fiscali
Epson compatibili con il protocollo ePOS-Print XML, consentendo la stampa
automatica di scontrini fiscali conformi alla normativa italiana.

Stampanti supportate:

- Epson FP81II
- Epson FP90III

Funzionalita principali:

- **Stampa scontrini fiscali**: alla validazione del pagamento nella sessione
  POS, il sistema genera e invia automaticamente lo scontrino fiscale alla
  stampante, con righe prodotto, sconti, arrotondamenti e metodi di pagamento.
- **Gestione resi e annulli**: supporto per resi parziali (singoli articoli) e
  annulli totali, con riferimento al documento originale (data, numero
  chiusura, numero scontrino, seriale RT). I dati del reso possono essere
  compilati manualmente o auto-popolati dallo storico ordini.
- **Report fiscali (Chiusura Z e Report X)**: esecuzione di chiusure fiscali
  giornaliere (Z-Report) e report finanziari non fiscali (X-Report)
  direttamente dall'interfaccia POS. La chiusura Z viene eseguita
  automaticamente alla chiusura della sessione POS.
- **Lotteria degli scontrini**: inserimento del codice lotteria (fino a 16
  caratteri) sullo scontrino fiscale tramite apposito pulsante nell'interfaccia
  POS.
- **Mappatura imposte e reparti**: associazione tra le imposte di vendita Odoo
  e i reparti (dipartimenti) della stampante fiscale (1-99).
- **Mappatura metodi di pagamento**: configurazione del tipo di pagamento
  fiscale (contanti, assegno, carta di credito, ticket, non riscosso, sconto)
  per ogni metodo di pagamento POS.
- **Apertura cassetto**: apertura automatica del cassetto portadenaro dopo la
  stampa dello scontrino.
- **Operatore fiscale**: associazione di un numero operatore fiscale a
  ciascun utente o dipendente.
- **Gestione errori e debug**: visualizzazione dettagliata degli errori della
  stampante, monitoraggio dello stato (carta, giornale elettronico, stato
  scontrino) e salvataggio delle informazioni di debug nell'ordine POS.

**English**

This module integrates the Odoo Point of Sale (POS) with Epson fiscal printers
compatible with the ePOS-Print XML protocol, enabling automatic printing of
fiscal receipts compliant with Italian tax regulations.

Supported printers:

- Epson FP81II
- Epson FP90III

Main features:

- **Fiscal receipt printing**: upon payment validation in the POS session, the
  system automatically generates and sends the fiscal receipt to the printer,
  including product lines, discounts, rounding adjustments, and payment methods.
- **Refund and void management**: support for partial refunds (individual items)
  and full voids, with reference to the original document (date, closure number,
  receipt number, RT serial). Refund data can be entered manually or
  auto-populated from order history.
- **Fiscal reports (Z-Report and X-Report)**: execution of daily fiscal
  closures (Z-Report) and non-fiscal financial reports (X-Report) directly from
  the POS interface. The Z-Report is automatically executed when closing the POS
  session.
- **Receipt lottery**: entry of the lottery code (up to 16 characters) on the
  fiscal receipt via a dedicated button in the POS interface.
- **Tax and department mapping**: association between Odoo sales taxes and
  fiscal printer departments (1-99).
- **Payment method mapping**: configuration of the fiscal payment type (cash,
  cheque, credit card, ticket, not paid, discount) for each POS payment method.
- **Cash drawer opening**: automatic cash drawer opening after receipt printing.
- **Fiscal operator**: association of a fiscal operator number to each user or
  employee.
- **Error handling and debugging**: detailed printer error display, status
  monitoring (paper, electronic journal, receipt state), and debug information
  storage in the POS order.
