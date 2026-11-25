**English**

From 1 January 2027 the VAT provisions of the D.P.R. 633/1972, the D.L. 331/1993
and the D.L. 41/1995 are replaced by the Testo Unico IVA (D.Lgs. 19 January
2026, n. 10), so the normative reference printed on the invoices changes too.

This module moves the law reference of the Italian taxes to the Testo Unico IVA
(`RiferimentoNormativo` of the electronic invoice): the article is chosen by
exoneration code (`N1`, `N2.1`, `N3.x`, `N4`, `N5`, `N6.x`, `N7`), and the
reference used until 2026 is kept in a field of the tax, so the documents dated
up to 31/12/2026 keep citing the previous decree.

The tax data is updated once, when the module is installed and when the Italian
chart of accounts is loaded: the reference is not computed when the e-invoice is
generated, and from 2027 the law reference of the tax is the one written in the
electronic invoice. Once 2026 is closed the module is no longer needed for the
tax references of the documents from 2027, because the tax data is already the
standard one; keep it installed while documents dated up to 2026 can still be
regenerated or reprinted, as they cite the previous decree, and for the notes of
the fiscal positions, which are translated when the PDF is printed.

The wording follows the document date and not the tax alone, because in the
first days of 2027 invoices dated 31/12/2026 can still be issued and received,
and a credit note issued in 2027 for a 2026 invoice must cite the previous
decree.

The module does not change the aliquots, the `Natura` codes, the VAT reports or
the existing amounts: it rewrites the law reference of the taxes and keeps the
previous wording in the *Law Reference until 2026* field. Nothing has to be
migrated and no tax has to be duplicated.

**Italiano**

Dal 1° gennaio 2027 le disposizioni IVA del D.P.R. 633/1972, del D.L. 331/1993 e
del D.L. 41/1995 sono sostituite dal Testo Unico IVA (D.Lgs. 19 gennaio 2026,
n. 10): cambia quindi anche il riferimento normativo riportato in fattura.

Questo modulo sposta il riferimento normativo delle imposte italiane sul Testo
Unico IVA (elemento `RiferimentoNormativo` della fattura elettronica):
l'articolo viene scelto in base al codice di esenzione (`N1`, `N2.1`, `N3.x`,
`N4`, `N5`, `N6.x`, `N7`) e il riferimento usato fino al 2026 viene conservato
in un campo dell'imposta, così i documenti datati fino al 31/12/2026
continuano a citare il decreto precedente.

I dati delle imposte vengono aggiornati una sola volta, all'installazione del
modulo e al caricamento del piano dei conti italiano: il riferimento non viene
calcolato al momento della generazione della fattura elettronica e dal 2027 il
riferimento normativo dell'imposta è quello scritto nel documento. Chiuso il
2026, il modulo non serve più per i riferimenti delle imposte dei documenti dal
2027, perché i dati delle imposte sono già quelli standard; va mantenuto
installato finché si possono rigenerare o ristampare documenti datati fino al
2026, che citano il decreto precedente, e per le note delle posizioni fiscali,
che vengono tradotte al momento della stampa del PDF.

La dicitura segue la data del documento e non la sola imposta, perché nei primi
giorni del 2027 si possono ancora emettere e ricevere fatture datate 31/12/2026
e una nota di credito emessa nel 2027 per una fattura del 2026 deve citare il
decreto precedente.

Il modulo non modifica le aliquote, i codici `Natura`, le liquidazioni IVA o gli
importi esistenti: riscrive il riferimento normativo delle imposte e conserva
la dicitura precedente nel campo *Law Reference until 2026*. Non serve alcuna
migrazione e non serve duplicare le imposte.
