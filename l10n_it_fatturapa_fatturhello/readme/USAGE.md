**Italiano**

Per ricevere le fatture elettroniche, attivare il CRON "Importazione e-fatture da Fatturhello".

Per aggiornare lo stato delle fatture elettroniche inviate, attivare il CRON "Aggiornamento stato e-fatture caricate su Fatturhello".

Se una fattura rimane nello stato "Inviata a Fatturhello", vuol dire che Fatturhello non è configurato per inviarla automaticamente allo SdI.
In questo caso:
1. In Odoo: eliminare la fattura elettronica creata,
2. In Fatturhello: abilitare l'invio automatico a SdI,
3. In Odoo: ricreare la fattura elettronica e inviarla.

**English**

In order to receive the electronic bills, activate the "Import E-Bills from Fatturhello" CRON.

In order to update the status of sent electronic invoices, activate the "Update the status of E-Invoices uploaded to Fatturhello" CRON.

If an invoice remains in the "Sent to Fatturhello" status, it means that Fatturhello is not configured to automatically send it to the ES.
In this case:
1. In Odoo: Delete the created electronic invoice,
2. In Fatturhello: Enable automatic sending to ES,
3. In Odoo: Recreate the electronic invoice and send it.
