.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

DDT - Italian Delivery note
===========================

This module manage the Italian DDT.
Once the picking is in state done a button will enable the DDT report.
The DDT is for internal transfers between warehouses, outgoing transfers to customers.
The sequence is done by the DDT type sequence so it's possible to have different
sequence depending on the typology of DDT.

This module is similar to DDT :code:`l10n_it_ddt` but i'ts easier (I believe) to use by
warehouse worker.
Unfortunately it's not possible to add on the fly product like the DDT module does.
It's also possible to do a transfer between different warehouses.

For a correct report layout set the address on warehouse.

Next improvement is to add to a picking a DDT sequence of another picking with the
same destination.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/DinamicheAziendali/easy_ddt/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Marco Calcagni <mcalcagni@dinamicheaziendali.it>
* Gianmarco Conte <gconte@dinamicheaziendali.it>
* Matteo Bilotta <mbilotta@linkeurope.it>
