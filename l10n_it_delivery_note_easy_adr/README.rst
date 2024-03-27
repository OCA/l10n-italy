**Delivery Note Easy ADR**
==========================

**Funzionalità:** Questo modulo permette la configurazione dell'ADR semplificata, scegliando se un prodotto è ADR e mostrando in caso positivo un tab relativo
all'adr, nel DDT verrà mostrato un tab relatvo alla mass virtuale.

**Come funziona**
==================

**Diritto di accesso**
-----------------------
- Utente interno: lettura Manager Magazzino: lettura/scrittura/creazioneUtente interno: lettura 
- Manager Magazzino: lettura/scrittura/creazione


**Configurazione**
-----------------------

Nelle impostazioni generali, nel menu magazzino si possono impostare i limiti e i messaggi per l'adr.


Si accede attraverso il menu situato in Magazzino/Configurazione/Prodotti/Cateogrie Adr.

Si configurano le categorie inserendo il nome e il moltiplicatore per il calcolo della massa virtuale.

Si può scegliere se un prodotto è ADR attraverso il flag apposito. Comparirà un tab ADR in cui inserire la categoria e un eventuale testo se necessario. 
Si può scegliere se usare il campo peso o la quantità ordinata nell'ordine per calcolare la massa virtuale.

Nel DDT verrà mostrato un tab Massa Virtuale se presente almeno un prodotto adr.

**Credits**
============

**Contributors**
-----------------------

* Matteo Piciucchi <matteo.piciucchi@bloomup.it>
* Letizia Freda <letizia.freda@bloomup.it>
* Emily Manfredi <emily.manfredi@bloomup.it>


Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/l10n-italy <https://github.com/OCA/l10n-italy/tree/14.0/l10n_it_account>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
