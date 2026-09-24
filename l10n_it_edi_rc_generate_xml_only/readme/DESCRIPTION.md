# English

The base `l10n_it_edi` module creates and sends the FatturaPA XML for
Italian self-invoices in a single step, with no way to only generate the XML
before sending it to SdI.

This module adds a *Generate XML* button on vendor bills that are Italian
self-invoices. Clicking it validates the move, creates the FatturaPA XML
attachment and posts it to the chatter, but does **not** submit the document
to the Exchange System (SdI) and does **not** mark the move as sent.

Users can therefore review the generated XML, make any necessary corrections,
and only click *Send to SDI* when the document is ready. The *Send to SDI*
button reuses the existing attachment if it was already generated, so the XML
is not produced twice.

# Italiano

Il modulo base `l10n_it_edi` crea e invia il file XML FatturaPA per le
autofatture italiane in un'unica operazione, senza offrire la possibilità di
generare solo l'XML prima dell'invio allo SdI.

Questo modulo aggiunge un pulsante *Genera XML* nelle fatture fornitori che
sono autofatture italiane. Premendolo, il sistema valida il movimento, crea
l'allegato XML FatturaPA e lo pubblica nel chatter, ma **non** trasmette il
documento al Sistema di Interscambio (SdI) e **non** contrassegna il
movimento come inviato.

L'utente può quindi esaminare l'XML generato, apportare le correzioni
necessarie e premere *Invia a SDI* solo quando il documento è pronto. Il
pulsante *Invia a SDI* riutilizza l'allegato già creato, evitando così di
produrre l'XML due volte.
