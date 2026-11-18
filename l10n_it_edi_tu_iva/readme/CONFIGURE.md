**English**

Install the module: the law reference of every Italian tax citing a decree
replaced by the Testo Unico IVA is updated, and the previous wording is copied
in the *Law Reference until 2026* field of the tax.

The references are defined in `models/account_tax.py` (`TU_IVA_REFERENCES`). The
same update runs when the Italian chart of accounts is loaded, so the taxes of a
company whose chart is created after the installation are updated too.

A tax reference is updated only while it still cites a decree replaced by the
Testo Unico IVA (D.P.R. 633/1972, D.L. 331/1993, D.L. 41/1995): a reference
already updated by the user is kept, which also makes the update idempotent.

`N2.2` is not mapped, because the Testo Unico IVA article depends on the
specific operation (art. 5, c. 3, art. 22, art. 139, art. 150, art. 157 ...):
set the article of each operation in the law reference of the tax. The same
`Fuori dall'Unione Europea` wording is shipped by `l10n_it` for the N7 tax,
which is updated, and for the N2.2 tax, which is left to the user: the
exoneration code is part of the key of the known wordings
(`LEGACY_REFERENCES`). The taxes created by the user are configured the same
way: the module never guesses an article for a wording it does not know.
`N6.5`, `N6.6` and `N6.8` are not mapped either, because since art. 64, c. 8,
D.Lgs. 10/2026 they no longer apply to operations carried out from 2027:
archive those taxes.

The law reference of the tax is written in the electronic invoice as latin-1 and
up to 100 characters: `l10n_it_edi` replaces the other characters with `?` and
truncates the text, so keep the references short and use latin-1 characters
only.

To move the date from which the new references apply, override
`_l10n_it_tu_iva_start_date`; to update other wordings, extend
`_l10n_it_tu_iva_get_tu_iva_reference`.

The citations of the notes of the Italian fiscal positions are translated too
(`TU_IVA_NOTE_REFERENCES`), when the PDF is printed: a note edited by the user,
or translated into a language whose wording this module does not ship, is
printed as it is. The notes are translated data shipped by `l10n_it`, so they
are not updated in the database and this part of the module is still needed
after 2026.

**Italiano**

Installare il modulo: il riferimento normativo di ogni imposta italiana che cita
un decreto sostituito dal Testo Unico IVA viene aggiornato e la dicitura
precedente viene copiata nel campo *Law Reference until 2026* dell'imposta.

I riferimenti sono definiti in `models/account_tax.py` (`TU_IVA_REFERENCES`). Lo
stesso aggiornamento viene eseguito al caricamento del piano dei conti italiano,
quindi vengono aggiornate anche le imposte di un'azienda il cui piano dei conti
viene creato dopo l'installazione.

Il riferimento di un'imposta viene aggiornato solo finché cita un decreto
sostituito dal Testo Unico IVA (D.P.R. 633/1972, D.L. 331/1993, D.L. 41/1995):
un riferimento già aggiornato dall'utente viene mantenuto, quindi
l'aggiornamento è idempotente.

`N2.2` non è mappato, perché l'articolo del Testo Unico IVA dipende
dall'operazione specifica (art. 5, c. 3, art. 22, art. 139, art. 150,
art. 157 ...): l'articolo della singola operazione va impostato nel riferimento
normativo dell'imposta. La stessa dicitura `Fuori dall'Unione Europea` è fornita
da `l10n_it` per l'imposta N7, che viene aggiornata, e per quella N2.2, che
viene lasciata all'utente: il codice di esenzione fa parte della chiave delle
diciture note (`LEGACY_REFERENCES`). Le imposte create dall'utente si
configurano allo stesso modo: il modulo non indovina mai un articolo per una
dicitura che non conosce. Anche `N6.5`, `N6.6` e `N6.8` non sono mappati, perché
per l'art. 64, c. 8, D.Lgs. 10/2026 non si applicano più alle operazioni
effettuate dal 2027: quelle imposte vanno archiviate.

Il riferimento normativo dell'imposta viene scritto nella fattura elettronica in
latin-1 e per un massimo di 100 caratteri: `l10n_it_edi` sostituisce gli altri
caratteri con `?` e tronca il testo, quindi conviene usare riferimenti brevi e
solo caratteri latin-1.

Per spostare la data a partire dalla quale si applicano i nuovi riferimenti
sovrascrivere `_l10n_it_tu_iva_start_date`; per aggiornare altre diciture
estendere `_l10n_it_tu_iva_get_tu_iva_reference`.

Vengono tradotti anche i riferimenti delle note delle posizioni fiscali
italiane (`TU_IVA_NOTE_REFERENCES`), al momento della stampa del PDF: una nota
modificata dall'utente, o tradotta in una lingua di cui il modulo non fornisce
la dicitura, viene stampata invariata. Le note sono dati tradotti forniti da
`l10n_it`, quindi non vengono aggiornate nel database e questa parte del modulo
serve ancora dopo il 2026.
