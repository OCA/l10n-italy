**Italiano**

Molto spesso non è possibile stampare un anno intero in un unico PDF per i limiti dello strumento di stampa di Odoo.
Quindi è necessario stampare il Libro giornale suddividendolo in periodi più brevi ad esempio un mese alla volta.
Da normativa quando si suddivide in più periodi bisogna indicare i saldi di riporto tra i vari periodi.
Al momento per poter riportare i saldi tra i vari periodi è necessario fare queste operazioni.

Creare dei periodi appositi per il Libro giornale.
Contabilità/Fatturazione -> Configurazione -> Intervalli data -> Intervalli data.
ad esempio "Libro giornale gennaio 2020", "Libro giornale febbraio 2020", ecc.

Stampare il Libro giornale del mese di gennaio con intervallo data "Libro giornale gennaio 2020" con il pulsante per la stampa definitiva.
In questo modo nell'intervallo data "Libro giornale gennaio 2020" verranno indicati i progressivi dare avere di gennaio.
Copiare questi progressivi nell'intervallo data "Libro giornale febbraio 2020" e poi stampare il Libro giornale in stampa definitiva.
Il report di Febbraio avrà i saldi iniziali indicati in precedenza che con la stampa definitiva vengono aggiornati con i nuovi progressivi di fine febbraio.
Ripetere l'operazione per tutti i periodi.

Il numero di pagina anch'esso è da riportare a mano in fase di stampa. Questo perché il report viene generato in html e poi trasformato in PDF e quindi non è possibile stabilire a priori quante pagine verranno generate.

**English**

Same time is not possible to print the general ledger in one PDF file this due to the report tool of odoo.
To solve print smaller periods eg one month by time.
