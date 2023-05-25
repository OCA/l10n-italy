**Italiano**

Qualora questo modulo venisse installato in un DB dove ``assets_management`` è già installato, è necessario eseguire la seguente procedura.

#. Installare ``openupgradelib``:

   .. code::

       pip3 install git+https://github.com/OCA/openupgradelib.git@master

#. Lanciare Odoo con il paramentro ``shell``
#. Eseguire i seguenti comandi:

   .. code:: python

       >>> from openupgradelib import openupgrade
       >>> openupgrade.rename_xmlids(
             env.cr,
             [
                 (
                     "assets_management.group_asset_user",
                     "l10n_it_asset_management.group_asset_user",
                 ),
             ],
      )
      >>> openupgrade.update_module_names(
             env.cr,
             [
                 ("assets_management", "l10n_it_asset_management"),
             ],
      )
      >>> openupgrade.rename_models(
             env.cr,
             [
                 (
                     "report.assets_management.report_asset_journal_xlsx",
                     "report.l10n_it_asset_management.report_asset_journal_xlsx",
                 ),
                 (
                     "report.assets_management.report_asset_previsional_xlsx",
                     "report.l10n_it_asset_management.report_asset_previsional_xlsx",
                 ),
             ],
      )
      >>> env.cr.commit()

#. Riavviare Odoo
#. Aggiornare ``l10n_it_asset_management``

**English**

When ``assets_management`` is installed in the database you need to follow the following steps.

1. Install ``openupgradelib``:

   .. code::

       pip3 install git+https://github.com/OCA/openupgradelib.git@master

2. Run Odoo with the ``shell`` command
#. Eseguire i seguenti comandi:

   .. code:: python

       >>> from openupgradelib import openupgrade
       >>> openupgrade.rename_xmlids(
             env.cr,
             [
                 (
                     "assets_management.group_asset_user",
                     "l10n_it_asset_management.group_asset_user",
                 ),
             ],
      )
      >>> openupgrade.update_module_names(
             env.cr,
             [
                 ("assets_management", "l10n_it_asset_management"),
             ],
      )
      >>> openupgrade.rename_models(
             env.cr,
             [
                 (
                     "report.assets_management.report_asset_journal_xlsx",
                     "report.l10n_it_asset_management.report_asset_journal_xlsx",
                 ),
                 (
                     "report.assets_management.report_asset_previsional_xlsx",
                     "report.l10n_it_asset_management.report_asset_previsional_xlsx",
                 ),
             ],
      )
      >>> env.cr.commit()

4. Restart Odoo
5. Update ``l10n_it_asset_management`` module
