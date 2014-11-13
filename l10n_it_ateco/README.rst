l10n_it_ateco
=============

This module registers a model in order to manage Ateco categories.

Each partner can be referenced by one or many Ateco codes
that specify the activities of a partner.

Each partner must have at least one and only one Ateco category set as 'Main category'.

The main Ateco category can be retrieved
by the field _main_ateco_category_id_ on res.partner model.


TODO
----

This module needs a method to import una-tantum ateco codes
from ISTAT web site in order maintain them up to date.

See:

* http://www3.istat.it/strumenti/definizioni/ateco/STRUTTURA.zip
* http://www3.istat.it/strumenti/definizioni/ateco/
