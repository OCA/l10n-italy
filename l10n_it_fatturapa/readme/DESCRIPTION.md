**Italiano**

Modulo base per la gestione delle fatture elettroniche.
Durante la creazione di una fattura cliente, viene eseguito un controllo sul modo di pagamento.
Se il modo di pagamento è RiBa e una banca ricevente è impostata, viene mostrato un messaggio di errore:
"Non è consentito impostare una banca ricevente per le fatture cliente con il modo di pagamento RiBa. 
Rimuovere la banca ricevente o scegliere un metodo di pagamento diverso."

La seguente issue su GitHub spiega la motivazione del controllo riportato:
https://github.com/OCA/l10n-italy/issues/4814

Per ulteriori informazioni, consultare il sito ufficiale:
https://www.fatturapa.gov.it

Si consiglia inoltre di consultare i file README dei moduli l10n_it_fatturapa_out e l10n_it_fatturapa_in.

**English**

Base module for managing electronic invoices.
When creating a customer invoice, a validation is performed on the payment method.
If the payment method is RiBa and a recipient bank is set, an error message is displayed:
"It is not allowed to set a recipient bank for customer invoices with the RiBa payment method. 
Please remove the recipient bank or choose a different payment method."

The following GitHub issue explains the reason for this validation:
https://github.com/OCA/l10n-italy/issues/4814

For more information, visit the official website:
https://www.fatturapa.gov.it

It is also recommended to review the README files of the l10n_it_fatturapa_out and l10n_it_fatturapa_in modules.
