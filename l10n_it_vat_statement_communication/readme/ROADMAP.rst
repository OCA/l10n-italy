Qualora questo modulo venisse installato in un DB dove ``l10n_it_comunicazione_liquidazione_iva`` è già installato, è necessario eseguire la sequente procedura:

1 - Installare ``openupgradelib``

2 - Lanciare odoo con il paramentro ``shell``

3 - Eseguire i seguenti comandi

>>> from openupgradelib import openupgrade
>>> openupgrade.update_module_names(env.cr, [('l10n_it_comunicazione_liquidazione_iva', 'l10n_it_vat_statement_communication'),], merge_modules=False,)
>>> env.cr.commit()

4 - Riavviare odoo

5 - Aggiornare ``l10n_it_vat_statement_communication``
