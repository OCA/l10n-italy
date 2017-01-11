.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============
IT Fiscal Code
==============

This module extends the functionality of partner to fit italian laws and mores
and to allow you to computation Fiscal code computation for partner

Installation
============

To install this module, you need the following external Python Packages:

* Python module to handle/check standardized numbers and codes  `python-stdnum`_.
* Python library for Italian fiscal code creation - `codicefiscale`_.

.. _python-stdnum: https://pypi.python.org/pypi/python-stdnum/
.. _codicefiscale: https://pypi.python.org/pypi/codicefiscale


Usage
=====

Il modulo: 

* verifica l'esattezza del codice fiscale (anche con possibili omocodie),in fase di inserimento 
* permette la ricerca del partner con il numero di codice fiscale, dalla barra di ricerca della scheda partner
* avvisa se eventualmente il codice fiscale è già presente nel sistema durante l'inserimento o modifica
* aggiunge il campo "impresa individuale" per le pesone fisiche, nella maschera del partner
* stampa il codice fiscale (se presente) nella fattura.

L'inserimento del CF, nonchè la sua uguaglianza o meno tra CF e partita IVA è considerata corretta nei casi sotto indicati:

* Persona:

a) Sotto-caso privato cittadino (solo CF),
b) Sotto-caso libero professionista (CF + PIVA, diversi)

* Azienda:

c) Sotto-caso impresa individuale (CF + PIVA, diversi)
d) Sotto-caso impresa societaria/associazioni (CF + PIVA, uguali)

Il modulo può generare anche un nuovo codice fiscale, richiedendo i dati
anagrafici della persona a cui riferisce:

#. Go to Partner and Run Wizard "Compute F.C."

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/122/10.0


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/l10n-italy/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======


Contributors
------------

* Davide Corio <davide.corio@abstract.it>
* Luca Subiaco <subluca@gmail.com>
* Simone Orsi <simone.orsi@domsense.com>
* Mario Riva <mario.riva@agilebg.com>
* Mauro Soligo <mauro.soligo@katodo.com>
* Giovanni Barzan <giovanni.barzan@gmail.com>
* Lorenzo Battistini <lorenzo.battistini@agilebg.com>
* Roberto Onnis <onnis.roberto@gmail.com>
* Franco Tampieri <franco.tampieri@agilebg.com>
* Andrea Cometa <info@andreacometa.it>
* Andrea Gallina <a.gallina@apuliasoftware.it>
* Giuliano Lotta <giuliano.lotta@gmail.com>


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
