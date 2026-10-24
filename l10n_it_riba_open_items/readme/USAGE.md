Una scadenza è considerata **scoperta** alla data del report quando la riga
di pagamento nella fattura ha il flag RiBa attivo (`riba=True`) e la sua
data di scadenza è ancora futura (stessa logica del campo `open_amount`
in `l10n_it_riba_oca`).

Modificare la data di scadenza della RiBa riflette immediatamente il
valore scoperto nel report.
