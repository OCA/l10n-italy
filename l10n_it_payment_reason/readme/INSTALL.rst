**Italiano**

Qualora questo modulo venisse installato in un DB dove ``l10n_it_causali_pagamento`` è già installato, è necessario eseguire la seguente procedura.

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
                     "l10n_it_causali_pagamento.view_causale_pagamento_tree",
                     "l10n_it_payment_reason.view_payment_reason_tree",
                 ),
                 (
                     "l10n_it_causali_pagamento.view_causale_pagamento_form",
                     "l10n_it_payment_reason.view_payment_reason_form",
                 ),
                 (
                     "l10n_it_causali_pagamento.action_causale_pagamento",
                     "l10n_it_payment_reason.action_payment_reason",
                 ),
                 (
                     "l10n_it_causali_pagamento.menu_causale_pagamento",
                     "l10n_it_payment_reason.menu_payment_reason",
                 ),
             ],
      )
      >>> openupgrade.update_module_names(
             env.cr,
             [
                 ("l10n_it_causali_pagamento", "l10n_it_payment_reason"),
             ],
      )
      >>> openupgrade.rename_models(
             env.cr,
             [
                 ("causale.pagamento", "payment.reason"),
             ],
      )
      >>> openupgrade.rename_tables(
           env.cr,
           [
               ("causale_pagamento", "payment_reason"),
           ],
      )
      >>> env.cr.commit()

#. Riavviare Odoo
#. Aggiornare ``l10n_it_payment_reason``

**English**

When ``l10n_it_causali_pagamento`` is installed in the database you need to follow the following steps.

1. Install ``openupgradelib``:

   .. code::

       pip3 install git+https://github.com/OCA/openupgradelib.git@master

2. Run Odoo with the ``shell`` command
3. Execute the following commands:

   .. code:: python

       >>> from openupgradelib import openupgrade
       >>> openupgrade.rename_xmlids(
       >>> openupgrade.rename_xmlids(
             env.cr,
             [
                 (
                     "l10n_it_causali_pagamento.view_causale_pagamento_tree",
                     "l10n_it_payment_reason.view_payment_reason_tree",
                 ),
                 (
                     "l10n_it_causali_pagamento.view_causale_pagamento_form",
                     "l10n_it_payment_reason.view_payment_reason_form",
                 ),
                 (
                     "l10n_it_causali_pagamento.action_causale_pagamento",
                     "l10n_it_payment_reason.action_payment_reason",
                 ),
                 (
                     "l10n_it_causali_pagamento.menu_causale_pagamento",
                     "l10n_it_payment_reason.menu_payment_reason",
                 ),
             ],
      )
      >>> openupgrade.update_module_names(
             env.cr,
             [
                 ("l10n_it_causali_pagamento", "l10n_it_payment_reason"),
             ],
      )
      >>> openupgrade.rename_models(
             env.cr,
             [
                 ("causale.pagamento", "payment.reason"),
             ],
      )
      >>> openupgrade.rename_tables(
           env.cr,
           [
               ("causale_pagamento", "payment_reason"),
           ],
      )
      >>> env.cr.commit()

4. Restart Odoo
5. Update ``l10n_it_payment_reason`` module
