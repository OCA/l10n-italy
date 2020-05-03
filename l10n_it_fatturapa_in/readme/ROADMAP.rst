Il modulo contiene un cambiamento alla firma di un metodo in ``models/account.py``
il quale cambia da

``compute_xml_amount_untaxed(self, DatiRiepilogo)``

a

``compute_xml_amount_untaxed(self, FatturaBody)``

Il cambiamento è dovuto all'implementazione della gestione degli arrotondamenti
che posso essere presenti in 2 sezioni diverse del file XML della fattura elettronica.

La soluzione ottimale è stata di cambiare la firma del metodo per consentire
la visibilità delle sezioni ``FatturaElettronicaBody.DatiBeniServizi.DatiRiepilogo`` e
``FatturaElettronicaBody.DatiGenerali.DatiGeneraliDocumento`` dove è presente il nodo ``Arrotondamento``

Pertanto, al fine di ottenere il corretto valore del totale imponibile, i moduli che
avessero ridefinito il metodo ``compute_xml_amount_untaxed`` nel modello ``account.invoice``
dovranno adeguare la chiamata al metodo stesso preoccupandosi di utilizzare come primo parametro l'oggetto ``FatturaElettronicaBody``.
