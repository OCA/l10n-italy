**English**

*74-ter electronic invoice (autofattura)*

1. Register the vendor bill received from the travel agency (the agency must be
   flagged as *74ter agency*), using the extra-EU 0% N3.6 tax or the intra-EU
   22% N6.9 tax on the commission line.
2. On posting, the bill is treated as a self-invoice: in the FatturaPA XML the
   agency becomes the *CedentePrestatore* and the company the
   *CessionarioCommittente*, with `RegimeFiscale` RF11, `TipoDocumento` TD01,
   `SoggettoEmittente` CC, the *Terzo Intermediario o Soggetto Emittente* block
   filled with the company, `CodiceDestinatario` = the agency's code, and the
   total (`ImportoTotaleDocumento`) omitted. For intra-EU lines the 22% VAT is
   stripped and reported as Natura N6.9.
3. Use the **Send to Tax Agency** button on the bill to send the XML to the SdI.
   A courtesy copy can then be forwarded to the agency.

*Invoice paid by the agency*

1. On a customer invoice, set **Agency** and tick **To be paid by agency**.
2. On posting, an entry is booked in the agencies-payments journal that moves
   the customer receivable to the agency, and the invoice is reconciled.

**Italiano**

*Fattura elettronica 74-ter (autofattura)*

1. Registrare la fattura fornitore ricevuta dall'agenzia viaggi (l'agenzia deve
   essere marcata come *Agenzia 74ter*), usando sulla riga della provvigione
   l'imposta extra-UE 0% N3.6 oppure l'imposta intra-UE 22% N6.9.
2. Alla conferma, la fattura viene trattata come autofattura: nell'XML
   FatturaPA l'agenzia diventa il *CedentePrestatore* e l'azienda il
   *CessionarioCommittente*, con `RegimeFiscale` RF11, `TipoDocumento` TD01,
   `SoggettoEmittente` CC, il blocco *Terzo Intermediario o Soggetto Emittente*
   valorizzato con l'azienda, `CodiceDestinatario` = codice dell'agenzia e
   l'importo totale (`ImportoTotaleDocumento`) omesso. Per le righe intra-UE
   l'IVA al 22% viene azzerata e riportata come Natura N6.9.
3. Usare il pulsante **Invia all'Agenzia delle Entrate** sulla fattura per
   inviare l'XML allo SdI. Una copia di cortesia può poi essere inviata
   all'agenzia.

*Fattura pagata dall'agenzia*

1. Su una fattura cliente, impostare l'**Agenzia** e spuntare **Da pagare a
   cura dell'agenzia**.
2. Alla conferma, viene registrata nel registro pagamenti agenzie una scrittura
   che trasferisce il credito dal cliente all'agenzia, e la fattura viene
   riconciliata.
