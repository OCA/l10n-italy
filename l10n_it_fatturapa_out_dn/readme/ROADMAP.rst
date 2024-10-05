There are a couple of minor issues since `l10n_it_delivery_note` only links a `Note` line of the invoice to the delivery note:

* RiferimentoNumeroLinea refers to a descriptive line, but it should enumerate (at least) the products lines
* RiferimentoNumeroLinea is always populated, but it should only be populated when the linked lines are not all the invoice lines
