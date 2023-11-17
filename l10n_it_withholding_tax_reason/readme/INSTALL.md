**Italiano**

Qualora questo modulo venisse installato in un DB dove
`l10n_it_withholding_tax_causali` è già installato, è necessario
eseguire la seguente procedura.

1.  Installare `openupgradelib`:

    ``` 
    pip3 install git+https://github.com/OCA/openupgradelib.git@master
    ```

2.  Lanciare Odoo con il paramentro `shell`

3.  Eseguire i seguenti comandi:

    ``` python
    >>> from openupgradelib import openupgrade
    >>> openupgrade.rename_fields(
          env,
          [
              (
                  "withholding.tax",
                  "withholding_tax",
                  "causale_pagamento_id",
                  "payment_reason_id",
              ),
          ],
    )
    >>> env.cr.commit()
    ```

4.  Riavviare Odoo

5.  Installare `l10n_it_withholding_tax_reason`

**English**

When `l10n_it_withholding_tax_causali` is installed in the database you
need to follow the following steps.

1.  Install `openupgradelib`:

    ``` 
    pip3 install git+https://github.com/OCA/openupgradelib.git@master
    ```

2.  Run Odoo with the `shell` command

3.  Execute the following commands:

    ``` python
    >>> from openupgradelib import openupgrade
    >>> openupgrade.rename_fields(
          env,
          [
              (
                  "withholding.tax",
                  "withholding_tax",
                  "causale_pagamento_id",
                  "payment_reason_id",
              ),
          ],
    )
    >>> env.cr.commit()
    ```

4.  Restart Odoo

5.  Install `l10n_it_withholding_tax_reason` module
