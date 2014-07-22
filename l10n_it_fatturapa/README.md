Premessa
========

Il modulo è stato creato a scopo didattico per comprendere il flusso.
Non è però necessario molto per renderlo completo perlomeno per i casi più semplici.

PS: l'XML generato viene validato correttamente dagli strumenti dell'agenzia delle entrate.
PS2: Al momento funziona solo con fatture cliente

Scelte tecniche
===============

Il file XML finale non viene creato da zero dal wizard.
Bensì viene usato un template di base, il quale viene compilato o integrato con parti aggiuntive.
Gli elementi non necessari possono essere rimossi dal template, programmaticamente.

Il template usato è l'esempio riportato dall'agenzia delle entrate a questa pagina:

<a href="http://www.fatturapa.gov.it/export/fatturazione/it/a-3.htm">Esempi FatturaPA</a>

FatturaPA
=========

Per testare il modulo:

1. Se installate i dati demo, troverete già un metodo di pagamento configurato, un partner (Pubblica Amministrazione) ed una fattura, con i vari campi necessari all'XML già compilati. Altrimenti:

1.1. Create un partner e compilate il campo FatturaPA code nel tab contabilità con il Codice Destinatario
1.2. Create un metodo di pagamento e compilate i campi FatturaPA per termini di pagamento e metodo di pagamento Fattura PA.
1.3. Create una fattura e compilate i campi nel tab FatturaPA

2. Compilate i campi nella sezione Contabilità dal menù Configurazione.

Andando su una fattura o selezionandone più di una, vi troverete l'azione ExportPA nel menù Altro.

TODO
====

1. Importare i dati di default (formati trasmissione, metodi di pagamento, etc)
2. Dati di riepilogo nel wizard di esportazione
3. Migliorare gestione lotti fatture
4. Pagamenti a rate
5. Altri tipi di documento (note di credito, etc)
6. Spedizione merce
7. Molto altro...

Validare il file
================

Per validare il file potere usare questo strumento:

<a href="http://sdi.fatturapa.gov.it/SdI2FatturaPAWeb/AccediAlServizioAction.do?pagina=controlla_fattura">Controllo FatturaPA</a>
