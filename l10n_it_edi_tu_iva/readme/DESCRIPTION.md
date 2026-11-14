**English**

From 1 January 2027 the VAT provisions of the D.P.R. 633/1972, the D.L. 331/1993
and the D.L. 41/1995 are replaced by the Testo Unico IVA (D.Lgs. 19 January
2026, n. 10), so the normative reference printed on the invoices changes too.

This module updates the `<RiferimentoNormativo>` element of the electronic
invoice for the documents dated from 1 January 2027, translating the
exoneration codes already used by the Italian localization (`N1`, `N2.1`,
`N3.x`, `N4`, `N5`, `N6.x`, `N7`) into the corresponding Testo Unico IVA
articles.

The reference is resolved when the electronic invoice is generated, and not on
the tax: the wording has to follow the document date, because in the first days
of 2027 invoices dated 31/12/2026 can still be issued and received, and a
credit note issued in 2027 for a 2026 invoice must cite the previous decree.
The wording follows the invoice date, or the date of the corrected invoice for
credit notes. The article to cite can be set tax by tax in the *TU IVA Law
Reference* field of the tax, which is used only for the documents dated from
2027: this way the taxes created by the user cite the Testo Unico IVA too.

The module does not change the existing tax values, the aliquots, the
`Natura` codes, the VAT reports or the existing data: nothing has to be
migrated and no tax has to be duplicated.

**Italiano**

Dal 1° gennaio 2027 le disposizioni IVA del D.P.R. 633/1972, del D.L. 331/1993 e
del D.L. 41/1995 sono sostituite dal Testo Unico IVA (D.Lgs. 19 gennaio 2026,
n. 10): cambia quindi anche il riferimento normativo riportato in fattura.

Questo modulo aggiorna l'elemento `<RiferimentoNormativo>` della fattura
elettronica per i documenti datati dal 1° gennaio 2027, traducendo i codici di
esenzione già usati dalla localizzazione italiana (`N1`, `N2.1`, `N3.x`, `N4`,
`N5`, `N6.x`, `N7`) nei corrispondenti articoli del Testo Unico IVA.

Il riferimento viene risolto al momento della generazione della fattura
elettronica e non sull'imposta: la dicitura deve seguire la data del documento,
perché nei primi giorni del 2027 si possono ancora emettere e ricevere fatture
datate 31/12/2026 e una nota di credito emessa nel 2027 per una fattura del 2026
deve citare il decreto precedente. La dicitura segue la data del documento,
oppure la data della fattura rettificata per le note di credito. L'articolo da
citare può essere impostato imposta per imposta nel campo *TU IVA Law Reference*
dell'imposta, usato solo per i documenti datati dal 2027: anche le imposte
create dall'utente citano così il Testo Unico IVA.

Il modulo non modifica i valori delle imposte esistenti, le aliquote, i codici
`Natura`, le liquidazioni IVA o i dati esistenti: non serve alcuna migrazione e
non serve duplicare le imposte.
