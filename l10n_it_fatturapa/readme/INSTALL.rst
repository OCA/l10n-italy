**Italiano**

Se non viene usato Openupgrade per effettuare l'aggiornamento del database,
le fatture in stato bozza o annullate non vengono migrate in modo corretto.
La soluzione consigliata è confermare o eliminare tali fatture prima di procedere.

In caso di problemi dovuti all'incompatibilità con il modulo autoinstallante `l10n_it_edi`, per installare questo modulo è necessario:

1. Installare `l10n_it`
2. Disinstallare `l10n_it_edi`
3. Installare `l10n_it_fatturapa`

**English**

If you don't use OpenUpgrade for upgrading your database, you won't be able to correctly migrate
invoices in draft and cancelled states. The recommended solution is to confirm or delete those invoices
before proceeding.

In case of issues due to the incompatibility with the auto-installing module `l10n_it_edi`, in order to install this module you have to:

1. Install `l10n_it`
2. Uninstall `l10n_it_edi`
3. Install `l10n_it_fatturapa`
