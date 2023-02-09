**Italiano**

Questo modulo dipende dal modulo account_global_discount.
In fase di creazione fattura con sconto globale impostato, il modulo account_global_discount crea una riga contabile
con lo/gli sconto/i.
Questo modulo sovrascrive questa riga per mostrarla in fattura.
Inoltre, lo sconto globale non viene più calcolato in base alle righe di sconto globale, perchè la riga
visibile in righe fattura è già con importo negativo e al totale viene sottratto l'importo di questa riga.

**English**

This module depend from account_global_discount.
In creation of account move with global discount, module account_global_discount create account move line with discount/s.
This module override this line for show it in invoice line.
Also, global discount is no longer calculated on a per-line basis, because line is visible in invoice line and
is already with negative amount and it is subtracted from amount total.
