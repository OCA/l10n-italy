**English**

Interim depreciation entries, e.g. for quarterly or half-yearly
financial statements.

The Generate Depreciations wizard has a new Interim Depreciation option,
and the Previsional Report wizard a new Create Interim Depreciation
button: instead of creating depreciation lines, they create and post one
journal entry with the depreciation of the current fiscal year until the
date, and its reversal at the reversal date (by default, the day after).
Assets and depreciations are not changed.

The journal items are those that a depreciation line would have
(accounts, and analytic distribution when
`l10n_it_asset_management_analytic` is installed), grouped by account
and analytic distribution.

The depreciation is the one that the previsional report shows at the
same date, with pro rata temporis forced until the date: with pro rata
temporis, this is the pro rata temporis until the date; in the fiscal
years after the first one, this is the part of the fiscal year passed.

Depreciation lines already created in the fiscal year until the date
are subtracted.

**Italiano**

Registrazioni di ammortamento infrannuali, per esempio per i bilanci
trimestrali o semestrali.

Il wizard Genera ammortamenti ha la nuova opzione Ammortamento
infrannuale, e il wizard del report previsionale il nuovo pulsante Crea
ammortamento infrannuale: invece di creare righe di ammortamento, creano
e confermano una registrazione con l'ammortamento dell'esercizio in
corso fino alla data, e il suo storno alla data di storno (per default,
il giorno dopo). Cespiti e piani di ammortamento non cambiano.

Le righe contabili sono quelle che avrebbe una riga di ammortamento
(conti, e distribuzione analitica se è installato
`l10n_it_asset_management_analytic`), raggruppate per conto e
distribuzione analitica.

L'ammortamento è quello che il report previsionale mostra alla stessa
data, con il pro-rata temporis forzato fino alla data: con il pro-rata
temporis, è il pro-rata temporis fino alla data; negli esercizi
successivi al primo, è la parte di esercizio trascorsa.

Le righe di ammortamento già create nell'esercizio fino alla data
vengono sottratte.
