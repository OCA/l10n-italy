.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================
Italian Withholding Tax
=======================

La ritenuta d’acconto odoo provvede a calcolare automaticamente i valori delle diverse tipologie di ritenuta presenti nella contaiblità italiana.

In odoo ritenuta d’acconto è possibile, tramite apposito workflow, gestire i diversi passaggi di stato delle ritenute rilevate: dovuta, applicata, versata

Usage
=====

Per prima cosa dovremo creare una ritenuta d’acconto odoo dove inserire tutti i campi necessari per un corretto calcolo.

Visto che le aliquote possono variare nel corso del tempo, nella codifica sono previsti scaglioni temporali di competenza.

E’ necessario anche inserire i conti contabili che verranno utilizzati quando il modulo si occuperà di generare registrazioni contabili per la rilevazione della ritenuta.

.. figure:: https://raw.githubusercontent.com/OCA/l10n-italy/10.0/l10n_it_withholding_tax/static/img/ritenuta-acconto-odoo-codifica-768x457.png
   :alt: alternative description
   :width: 600 px

Una volta aggiunta, nella tabella ritenute, potrà essere utilizzata all’interno della fattura, in corrispondenza delle righe soggette a ritenute.

Per ogni riga è possibile utilizzare più di una ritenuta. Per alcune casistiche il moduo ritenute viene usato anche per rilevare le trattenute INPS.

Il modulo ritenute per Odoo calcolerà i valori corrispondenti e ne mostrerà il dettaglio nell’apposita area ritenute, dove è possibile verificare per ogni codice ritenuta usato, l’imponibile e l’importo ritenuta applicato.

In calce ai totali, verrà totalizzato l’ammontare della ritenuta e il netto a pagare. Questa sezione sarà visibile solamente in presenza di almeno una ritenuta

.. figure:: https://raw.githubusercontent.com/OCA/l10n-italy/10.0/l10n_it_withholding_tax/static/img/fattura-fornitore-768x517.png
   :alt: alternative description
   :width: 600 px

Successivamente andando nella sezione situazione ritenute d’acconto odoo vi mostrerà una situazione riepilogativa delle varie ritenute divisa per documento di origine.

I campi principalmente da tenere in considerazione in questa tabella sono: ritenuta dovuta, ritenuta applicata e ritenuta versata.

*Ritenuta dovuta* contiene il valore della ritenuta contenuta nella fattura.

*Ritenuta applicata* mostra il valore della ritenuta rilevata al momento del pagamento della fattura.

*Ritenuta versata* contiene l’importo di ritenuta, già applicata, che è stata versata all’erario

.. figure:: https://raw.githubusercontent.com/OCA/l10n-italy/10.0/l10n_it_withholding_tax/static/img/foto-3-1-1024x505.png
   :alt: alternative description
   :width: 600 px

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/122/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/l10n-italy/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback

Credits
=======

Contributors
------------

* Alessandro Camilli <alessandrocamilli@openforce.it>
* Lorenzo Battistini <lorenzo.battistini@agilebg.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.

Sponsor
-------

'Odoo Italia Network <http://www.odoo-italia.net/>'_

