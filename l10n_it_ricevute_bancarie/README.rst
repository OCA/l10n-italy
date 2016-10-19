.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================
IT Ricevute Bancarie
====================

Questo modulo serve a gestire il flusso delle ricevute bancarie

Installation
============

Usage
=====

Gestione delle Ricevute Bancarie
--------------------------------

Nella configurazione delle Ri.Ba. è possibile specificare se si tratti di 'salvo buon fine' o 'al dopo incasso'. I due tipi di Ri.Ba. hanno un flusso completamente diverso. In caso di 'al dopo incasso', nessuna registrazione verrà effettuata automaticamente e le fatture risulteranno pagate solo al momento dell'effettivo incasso.

E' possibile specificare diverse configurazioni (dal menù configurazioni -> varie -> Ri.Ba.). Per ognuna, in caso di 'salvo buon fine', è necessario specificare almeno il sezionale ed il conto da utilizzare al momento dell'accettazione della distinta da parte della banca.
La configurazione relativa alla fase di accredito, verrà usata nel momento in cui la banca accredita l'importo della distinta. Mentre quella relativa all'insoluto verrà utilizzato in caso di mancato pagamento da parte del cliente.

Per utilizzare il meccanismo delle Ri.Ba. è necessario configurare un termine di pagamento di tipo 'Ri.Ba.'.

Per emettere una distinta bisogna andare su Ri.Ba. -> emetti Ri.Ba. e selezionare i pagamenti per i quali emettere la distinta.
Se per il cliente è stato abilitato il raggruppo, i pagamenti dello stesso cliente e con la stessa data di scadenza andranno a costituire un solo elemento della distinta.

I possibili stati della distinta sono: bozza, accettata, accreditata, pagata, insoluta, annullata.
Ad ogni passaggio di stato sarà possibile generare le relative registrazioni contabili, le quali verranno riepilogate nel tab 'contabilità'. Questo tab è presente sia sulla distinta che sulle sue righe.

Qui https://docs.google.com/document/d/1xCqeTcY6CF-Dgk_Avthhy7iwg_aG86WzNv3E_HHQkt4/edit# abbiamo un esempio delle tipiche registrazioni generate da un flusso 'salvo buon fine'.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: #


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/l10n-italy/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Odoo Italia Network <http://www.odoo-italia.net/>

Contributors
------------

* Andrea Cometa <a.cometa@apuliasoftware.it>
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

To contribute to this module, please visit https://odoo-community.org.