Vedi anche il README del modulo l10n_it_fatturapa.

Per ogni fornitore è possibile impostare il 'Livello di dettaglio Fatture elettroniche':

 - Livello minimo: La fattura passiva viene creata senza righe; sarà l'utente a doverle creare in base a quanto indicato dal fornitore nella fattura elettronica
 - Livello Massimo: tutte le righe presenti nella fattura elettronica vengono create come righe della fattura passiva

E' inoltre possibile impostare il campo 'prodotto di default per le fatture elettroniche' nella scheda del fornitore: questo prodotto verrà usato in fase di importazione della fattura passiva quando nessun altro possibile prodotto verrà trovato dal sistema, utilizzando quindi il conto e l'imposta preconfigurati sul prodotto.

Per ogni codice prodotto usato dai fornitori, impostarlo nel campo

Inventario --> Fornitori

nella scheda del prodotto.

Se il fornitore specificherà tale codice nell'XML, il sistema lo userà per recuperare il prodotto ed usarlo nella riga della fattura, impostando il relativo conto acquisti ed eventualmente l'IVA.
