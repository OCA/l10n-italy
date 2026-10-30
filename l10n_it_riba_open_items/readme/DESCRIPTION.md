Estende il report **Partite aperte** (`account_financial_report`) per le
RiBa gestite con `l10n_it_riba_oca`.

Quando una distinta RiBa viene accettata, la scadenza della fattura viene
riconciliata con la scrittura di accettazione e sparisce dalle partite
aperte, anche se il credito è ancora a rischio fino al buon fine.

Con l'opzione **Mostra scoperto RiBa** (attiva di default nel wizard):

- le scadenze chiuse dall'accettazione RiBa e non ancora andate a buon
  fine compaiono nel report con **residuo 0** (non alterano il saldo);
- l'importo a rischio è riportato nella colonna **Scoperto RiBa**; il
  valore viene letto direttamente dal campo `open_amount` già calcolato
  sulla fattura in `l10n_it_riba_oca` — non viene ricalcolato dal
  modulo;
- modificare la data di scadenza di una scadenza RiBa azzera
  immediatamente il valore scoperto (stessa logica di `open_amount`);
- la logica è per singola scadenza, quindi con RiBa a più scadenze si
  vedono separatamente le rate pagate (escluse) e quelle ancora scoperte;
- le righe chiuse da RiBa sono in corsivo (PDF/HTML);
- la colonna è presente anche nell'export XLSX.
