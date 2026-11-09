Una scadenza è considerata **scoperta** quando la riga di pagamento nella
fattura ha il flag RiBa attivo (`riba=True`) e la sua data di scadenza è
successiva a oggi (stessa logica del campo `open_amount` in
`l10n_it_riba_oca`).

Lo scoperto è sempre valutato alla data odierna, non alla data del report:
lanciando il report a una data passata, le scadenze già superate oggi
risultano comunque non scoperte.

Modificare la data di scadenza della RiBa riflette immediatamente il
valore scoperto nel report.
