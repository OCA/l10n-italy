**English**

Install the module and issue the invoices as usual: the reference is chosen when
the electronic invoice is generated and when the PDF is printed.

- an invoice dated up to 31/12/2026 cites the D.P.R. 633/1972, even when it is
  issued in 2027, and its PDF is printed as before;
- an invoice dated from 01/01/2027 cites the Testo Unico IVA in the
  `<RiferimentoNormativo>` element and prints the same reference on the PDF,
  below the totals; the note of the fiscal position is printed with the Testo
  Unico IVA citations too (e.g. art. 64, c. 6, lett. a) instead of art. 17,
  c. 6, lett. a) of the D.P.R. 633/1972);
- a credit note cites the reference of the invoice it corrects: a credit note
  dated 2027 for a 2026 invoice still cites the D.P.R. 633/1972. A credit note
  created without the link to the corrected invoice cannot know it, and uses
  its own date;
- a tax with the *TU IVA Law Reference* field filled cites that reference from
  2027, instead of the wording derived from its law reference and from its
  exoneration code; before 2027 the field is ignored and the tax keeps its own
  law reference.

The `Natura` codes, the aliquots and the amounts are not changed, so the SdI
accepts the documents in the same way; only the wording of the
`RiferimentoNormativo` element and of the printed legal notes changes.

**Italiano**

Installare il modulo ed emettere le fatture come sempre: il riferimento viene
scelto al momento della generazione della fattura elettronica e della stampa del
PDF.

- una fattura datata fino al 31/12/2026 cita il D.P.R. 633/1972, anche se
  emessa nel 2027, e il suo PDF viene stampato come prima;
- una fattura datata dal 01/01/2027 cita il Testo Unico IVA nell'elemento
  `<RiferimentoNormativo>` e stampa lo stesso riferimento nel PDF, sotto i
  totali; anche la nota della posizione fiscale viene stampata con i
  riferimenti del Testo Unico IVA (ad es. art. 64, c. 6, lett. a) invece di
  art. 17, c. 6, lett. a) del D.P.R. 633/1972);
- una nota di credito cita il riferimento della fattura che rettifica: una nota
  di credito datata 2027 per una fattura del 2026 cita ancora il D.P.R.
  633/1972. Una nota di credito creata senza il collegamento alla fattura
  rettificata non può saperlo, e usa la propria data;
- un'imposta con il campo *TU IVA Law Reference* compilato cita quel
  riferimento dal 2027, invece della dicitura ricavata dal suo riferimento
  normativo e dal suo codice di esenzione; prima del 2027 il campo viene
  ignorato e l'imposta mantiene il proprio riferimento normativo.

I codici `Natura`, le aliquote e gli importi non cambiano, quindi il SdI accetta
i documenti allo stesso modo: cambia solo la dicitura dell'elemento
`RiferimentoNormativo` e delle note legali stampate.
