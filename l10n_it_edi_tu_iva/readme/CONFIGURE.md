**English**

No configuration is needed: the module applies to every company with the
Italian fiscal localization.

The references are defined in `models/account_move.py` (`TU_IVA_REFERENCES`).
A tax reference is translated only while it still cites a decree replaced by
the Testo Unico IVA (D.P.R. 633/1972, D.L. 331/1993, D.L. 41/1995): a reference
already updated by the user is kept, so the module does not override the work
already done on the taxes.

`N2.2` is not mapped, because the Testo Unico IVA article depends on the
specific operation (art. 5, c. 3, art. 22, art. 139, art. 150, art. 157 ...):
the reference configured on those taxes is left as it is, and the user sets the
article of each operation in the `TU IVA Law Reference` field of the tax.
`N6.5`, `N6.6` and `N6.8` are not mapped either, because since art. 64, c. 8,
D.Lgs. 10/2026 they no longer apply to operations carried out from 2027:
archive those taxes.

The reference of the Testo Unico IVA to cite can be set tax by tax, in the
*TU IVA Law Reference* field of the tax (`l10n_it_tu_iva_law_reference`). It
replaces both the law reference of the tax and the wording the module derives
from the exoneration code, so the taxes created by the user cite the Testo
Unico IVA too. It is used only for the documents dated from 2027: before that
date the law reference of the tax is printed unchanged.

To move the date from which the new references apply, override
`_l10n_it_tu_iva_start_date`; to use different wordings for some exonerations,
override `_l10n_it_tu_iva_get_reference`.

The citations of the notes of the Italian fiscal positions are translated too
(`TU_IVA_NOTE_REFERENCES`): a note edited by the user, or translated into a
language whose wording this module does not ship, is printed as it is.

**Italiano**

Non serve alcuna configurazione: il modulo si applica a tutte le aziende con la
localizzazione fiscale italiana.

I riferimenti sono definiti in `models/account_move.py` (`TU_IVA_REFERENCES`).
Il riferimento di un'imposta viene tradotto solo finché cita un decreto
sostituito dal Testo Unico IVA (D.P.R. 633/1972, D.L. 331/1993, D.L. 41/1995):
un riferimento già aggiornato dall'utente viene mantenuto, quindi il modulo non
sovrascrive il lavoro già fatto sulle imposte.

`N2.2` non è mappato, perché l'articolo del Testo Unico IVA dipende
dall'operazione specifica (art. 5, c. 3, art. 22, art. 139, art. 150,
art. 157 ...): il riferimento configurato su quelle imposte viene lasciato
invariato, e l'utente imposta l'articolo della singola operazione nel campo
`TU IVA Law Reference` dell'imposta. Anche `N6.5`, `N6.6` e `N6.8` non sono
mappati, perché per l'art. 64, c. 8, D.Lgs. 10/2026 non si applicano più
alle operazioni effettuate dal 2027: quelle imposte vanno archiviate.

Il riferimento del Testo Unico IVA da citare può essere impostato imposta per
imposta, nel campo *TU IVA Law Reference* dell'imposta
(`l10n_it_tu_iva_law_reference`). Sostituisce sia il riferimento normativo
dell'imposta sia la dicitura che il modulo ricava dal codice di esenzione,
quindi anche le imposte create dall'utente citano il Testo Unico IVA. Viene
usato solo per i documenti datati dal 2027: prima di tale data il riferimento
normativo dell'imposta viene stampato invariato.

Per spostare la data a partire dalla quale si applicano i nuovi riferimenti
sovrascrivere `_l10n_it_tu_iva_start_date`; per usare diciture diverse per
alcune esenzioni sovrascrivere `_l10n_it_tu_iva_get_reference`.

Vengono tradotti anche i riferimenti delle note delle posizioni fiscali
italiane (`TU_IVA_NOTE_REFERENCES`): una nota modificata dall'utente, o
tradotta in una lingua di cui il modulo non fornisce la dicitura, viene
stampata invariata.
