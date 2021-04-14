**Italiano**

Qualora questo modulo venisse installato in un DB dove ``l10n_it_codici_carica`` è già installato, è necessario eseguire la seguente procedura.

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
                     "l10n_it_codici_carica.view_codice_carica_tree",
                     "l10n_it_appointment_code.view_appointment_code_tree",
                 ),
                 (
                     "l10n_it_codici_carica.view_codice_carica_form",
                     "l10n_it_appointment_code.view_appointment_code_form",
                 ),
                 (
                     "l10n_it_codici_carica.action_codice_carica",
                     "l10n_it_appointment_code.action_appointment_code",
                 ),
                 (
                     "l10n_it_codici_carica.menu_codice_carica",
                     "l10n_it_appointment_code.menu_appointment_code",
                 ),
             ],
      )
      >>> openupgrade.update_module_names(
             env.cr,
             [
                 ("l10n_it_codici_carica", "l10n_it_appointment_code"),
             ],
      )
      >>> openupgrade.rename_models(
             env.cr,
             [
                 ("codice.carica", "appointment.code"),
             ],
      )
      >>> openupgrade.rename_tables(
           env.cr,
           [
               ("codice_carica", "appointment_code"),
           ],
      )
      >>> env.cr.commit()

#. Riavviare Odoo
#. Aggiornare ``l10n_it_appointment_code``

**English**

When ``l10n_it_codici_carica`` is installed in the database you need to follow the following steps.

1. Install ``openupgradelib``:

   .. code::

       pip3 install git+https://github.com/OCA/openupgradelib.git@master

2. Run Odoo with the ``shell`` command
3. Execute the following commands:

   .. code:: python

       >>> from openupgradelib import openupgrade
       >>> openupgrade.rename_xmlids(
             env.cr,
             [
                 (
                     "l10n_it_codici_carica.view_codice_carica_tree",
                     "l10n_it_appointment_code.view_appointment_code_tree",
                 ),
                 (
                     "l10n_it_codici_carica.view_codice_carica_form",
                     "l10n_it_appointment_code.view_appointment_code_form",
                 ),
                 (
                     "l10n_it_codici_carica.action_codice_carica",
                     "l10n_it_appointment_code.action_appointment_code",
                 ),
                 (
                     "l10n_it_codici_carica.menu_codice_carica",
                     "l10n_it_appointment_code.menu_appointment_code",
                 ),
             ],
      )
      >>> openupgrade.update_module_names(
             env.cr,
             [
                 ("l10n_it_codici_carica", "l10n_it_appointment_code"),
             ],
      )
      >>> openupgrade.rename_models(
             env.cr,
             [
                 ("codice.carica", "appointment.code"),
             ],
      )
      >>> openupgrade.rename_tables(
           env.cr,
           [
               ("codice_carica", "appointment_code"),
           ],
      )
      >>> env.cr.commit()

4. Restart Odoo
5. Update ``l10n_it_appointment_code`` module
