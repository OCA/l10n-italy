**Italiano**

Questo modulo è stato rinominato da `l10n_it_riba` a `l10n_it_riba_oca`
perché a fine 2024 un modulo con lo stesso nome è stato aggiunto ai
moduli di Odoo Enterprise con
<https://github.com/odoo/enterprise/commit/03c2e68ad88e3430e7fe604804d2bcc6332dc962>.

I moduli esistenti che dipendevano da `l10n_it_riba` dovranno quindi:

- adattare il nome della dipendenza da `l10n_it_riba` a `l10n_it_riba_oca`
- adattare eventuali riferimenti esterni (XMLID) da `l10n_it_riba.[...]` a `l10n_it_riba_oca.[...]`
