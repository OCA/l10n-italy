**Italiano**

Questo modulo è stato rinominato da `l10n_it_intrastat` a
`l10n_it_intrastat_oca` perché Odoo Enterprise contiene un modulo con
lo stesso nome.

Se nel database è installato `l10n_it_intrastat`, viene sostituito da
`l10n_it_intrastat_oca` mantenendone i dati:

- aggiornando il modulo `l10n_it_account`, se installato;
- altrimenti, installando manualmente `l10n_it_intrastat_oca`.

La sostituzione va fatta prima di migrare il database a una versione
successiva di Odoo.

I moduli esistenti che dipendevano da `l10n_it_intrastat` dovranno
quindi:

- adattare il nome della dipendenza da `l10n_it_intrastat` a
  `l10n_it_intrastat_oca`;
- adattare eventuali riferimenti esterni (XMLID) da
  `l10n_it_intrastat.[...]` a `l10n_it_intrastat_oca.[...]`.

**English**

This module has been renamed from `l10n_it_intrastat` to
`l10n_it_intrastat_oca` because Odoo Enterprise contains a module with
the same name.

If `l10n_it_intrastat` is installed in the database, it is replaced by
`l10n_it_intrastat_oca` keeping its data:

- by updating the module `l10n_it_account`, if installed;
- otherwise, by manually installing `l10n_it_intrastat_oca`.

The replacement must be done before migrating the database to a later
version of Odoo.

Existing modules depending on `l10n_it_intrastat` must then:

- change the dependency name from `l10n_it_intrastat` to
  `l10n_it_intrastat_oca`;
- change any external reference (XMLID) from `l10n_it_intrastat.[...]`
  to `l10n_it_intrastat_oca.[...]`.
