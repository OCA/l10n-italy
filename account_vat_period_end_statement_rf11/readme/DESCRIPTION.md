Vedi modulo `l10n_it_fatturapa_out_rf11`

Calcolo dell'IVA secondo il metodo "base su base", sulla base delle registrazioni coinvolte dall'imposta identificata come 74 ter; tale calcolo viene effettuato mensilmente. In caso di calcolo a credito, tale risultato viene memorizzato per il calcolo della liquidazione successiva, se a debito, viene svolta una registrazione come da esempio sotto. Tale iva a debito concorrerà al calcolo della liquidazione IVA ordinaria.

La stampa del resoconto liquidazione IVA verrà modificata in modo tale da riportare una sezione 74 Ter


1) All’atto della liquidazione Iva 74 ter mensile a debito

Ipotizziamo un’iva a debito scorporata di € 5000,00

                      Dare    Avere
0301009 Iva 74 Ter    5000,00
0115001 IVA C/Vendite         5000,00

In caso di 74 ter a credito rimane il credito di costo

Il conto 0301009 Iva 74 Ter è un conto di ricavo in quanto va a rettificare il valore dei ricavi delle vendite dei viaggi UE.

2) Liquidazione Iva mensile a credito

Dopo il calcolo dell’Iva 74 ter ipotizziamo una situazione data da € 50000,00 Iva a debito ordinaria + € 5000,00 di Iva a debito 74 ter; e € 100000,00 Iva a credito ordinaria.

                       Dare       Avere
0115001 Iva C/vendite  55000,00
0115003 Iva C/erario   45000,00
0115002 Iva C/acquisti            100000,00 

