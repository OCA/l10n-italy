**Italiano**

Questo modulo sostituisce `l10n_it_intrastat`, rinominato perché Odoo
Enterprise contiene un modulo con lo stesso nome.

Nei database migrati con OpenUpgrade la rinomina è automatica.

Nei database migrati con il servizio di Odoo SA (upgrade.odoo.com),
installare questo modulo: durante l'installazione assorbe i dati del
vecchio modulo `l10n_it_intrastat`.

I moduli che dipendono da `l10n_it_intrastat` devono usare il nuovo nome
nelle dipendenze e negli XMLID.
