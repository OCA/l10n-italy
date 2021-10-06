Per prima cosa dovremo creare una ritenuta d’acconto dove inserire tutti i campi necessari per un corretto calcolo.

Visto che le aliquote possono variare nel corso del tempo, nella codifica sono previsti scaglioni temporali di competenza.

E’ necessario anche inserire i conti contabili che verranno utilizzati quando il modulo si occuperà di generare registrazioni contabili per la rilevazione della ritenuta.

.. figure:: static/img/ritenuta-acconto-odoo-codifica-768x457.png
   :alt: Withholding tax
   :width: 600 px

Una volta aggiunta, nella tabella ritenute, potrà essere utilizzata all’interno della fattura, in corrispondenza delle righe soggette a ritenute.

Per ogni riga è possibile utilizzare più di una ritenuta. Per alcune casistiche il moduo ritenute viene usato anche per rilevare le trattenute INPS.

Il modulo ritenute calcolerà i valori corrispondenti e ne mostrerà il dettaglio nell’apposita area ritenute, dove è possibile verificare per ogni codice ritenuta usato, l’imponibile e l’importo ritenuta applicato.

In calce ai totali, verrà totalizzato l’ammontare della ritenuta e il netto a pagare. Questa sezione sarà visibile solamente in presenza di almeno una ritenuta

.. figure:: static/img/fattura-fornitore-768x517.png
   :alt: Supplier invoice
   :width: 600 px

Per registrare il pagamento di una fattura con ritenuta, indicare come importo il "Netto a pagare" e lasciare aperta la fattura:

.. figure:: static/img/pagamento-fattura-fornitore.png
   :alt: Pagamento fattura fornitore

Il sistema provvederà alla creazione di un ulteriore pagamento che coprirà l'ammontare della ritenuta e la fattura risulterà completamente pagata:

.. figure:: static/img/pagamento-ritenuta.png
   :alt: Pagamento ritenuta

Per il pagamento della ritenuta d'acconto fare riferimento al modulo `l10n_it_withholding_tax_payment`.

Successivamente andando nella sezione situazione ritenute d’acconto il sistema vi mostrerà una situazione riepilogativa delle varie ritenute divisa per documento di origine.

I campi principalmente da tenere in considerazione in questa tabella sono: ritenuta dovuta, ritenuta applicata e ritenuta versata.

*Ritenuta dovuta* contiene il valore della ritenuta contenuta nella fattura.

*Ritenuta applicata* mostra il valore della ritenuta rilevata al momento del pagamento della fattura.

*Ritenuta versata* contiene l’importo di ritenuta, già applicata, che è stata versata all’erario

.. figure:: static/img/foto-3-1-1024x505.png
   :alt: WT statement
   :width: 600 px
