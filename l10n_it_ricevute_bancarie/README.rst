.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================
Ricevute Bancarie
=================

Gestione delle Ricevute Bancarie
--------------------------------

Nella configurazione delle Ri.Ba. è possibile specificare se si tratti di
'salvo buon fine' o 'al dopo incasso'. I due tipi di Ri.Ba. hanno un flusso
completamente diverso. In caso di 'al dopo incasso', nessuna registrazione
verrà effettuata automaticamente e le fatture risulteranno pagate solo al
momento dell'effettivo incasso.

E' possibile specificare diverse configurazioni (dal menù
configurazioni -> varie -> Ri.Ba.). Per ognuna, in caso di 'salvo buon fine',
è necessario specificare almeno il sezionale ed il conto da
utilizzare al momento dell'accettazione della distinta da parte della banca.
La configurazione relativa alla fase di accredito, verrà usata nel momento in
cui la banca accredita l'importo della distinta. Mentre quella relativa
all'insoluto verrà utilizzato in caso di
mancato pagamento da parte del cliente.

Per utilizzare il meccanismo delle Ri.Ba. è necessario configurare un termine
di pagamento di tipo 'Ri.Ba.'.

Per emettere una distinta bisogna andare su Ri.Ba. -> emetti Ri.Ba. e
selezionare i pagamenti per i quali emettere la distinta.
Se per il cliente è stato abilitato il raggruppo, i pagamenti dello stesso
cliente e con la stessa data di scadenza andranno a costituire un solo elemento
della distinta.

I possibili stati della distinta sono: bozza, accettata, accreditata, pagata,
insoluta, annullata.
Ad ogni passaggio di stato sarà possibile generare le relative registrazioni
contabili, le quali verranno riepilogate nel tab 'contabilità'.
Questo tab è presente sia sulla distinta che sulle sue righe.

Qui
http://goo.gl/jpRhJp abbiamo un esempio delle tipiche registrazioni generate
da un flusso 'salvo buon fine'.

Configuration
=============

Nel caso si voglia gestire anche le spese per ogni scadenza con ricevuta bancaria,
si deve configurare un prodotto di tipo servizio e legarlo in Configurazione -> Contabilità


Usage
=====

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/122/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/l10n-italy/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed `feedback
<https://github.com/OCA/
l10n-italy/issues/new?body=module:%20
l10n_it_ricevute_bancarie%0Aversion:%20
8.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Contributors
------------

* Andrea Cometa <a.cometa@apuliasoftware.it>
* Andrea Gallina <a.gallina@apuliasoftware.it>
* Lorenzo Battistini <lorenzo.battistini@agilebg.com>
* Davide Corio <info@davidecorio.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
