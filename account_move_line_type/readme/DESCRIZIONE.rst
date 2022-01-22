Modulo tecnico per impostare i tipi di riga contabile.
I tipi di riga di account.move.line sono:

* receivable / payable: riga da testata, contiene il conto cliente o fornitore, la data di scadenza (no IVA)
* lp: riga fattura con codice IVA; di solito contiene conti economici
* tax: riga creata automaticamente con il codice IVA
* other: riga generica, non IVA

Note:

* Se un conto receivable / payable è impostato in una riga con codice IVA, la riga è considerata tipo lp
* Le righe lp contengono una o più codici IVA
* Le righe tax contengono un solo codice IVA e riferiscono ad 1 o più righe tipo lp
