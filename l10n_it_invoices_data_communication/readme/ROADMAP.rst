Qualora questo modulo venisse installato in un DB dove ``l10n_it_comunicazione_dati_iva`` è già installato, è necessario eseguire la sequente procedura:

#. Installare ``openupgradelib``
#. Lanciare odoo con il paramentro ``shell``
#. Eseguire i seguenti comandi

    >>> from openupgradelib import openupgrade
    >>> openupgrade.update_module_names(env.cr, [('l10n_it_comunicazione_dati_iva', 'l10n_it_invoices_data_communication'),], merge_modules=False,)
    >>> env.cr.commit()

#. Riavviare odoo
#. Aggiornare ``l10n_it_invoices_data_communication``
