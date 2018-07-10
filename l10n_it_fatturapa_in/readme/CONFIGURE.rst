Also see the README file of l10n_it_fatturapa module.

For every supplier, it is possible to set the 'details level of electronic invoices':

 - Minimum level: Supplier invoice is created without lines; user will have to create them, according to what specified in electronic invoice
 - Maximum level: every line contained in electronic invoice will create a line in supplier invoice.

Moreover, it is possible, in supplier form, to set the 'default product for electronic invoices': this product will be used, during generation of supplier invoices, when no other possible product is found. Tax and account of invoice line will be set according to what configured in the product.

Every product code used by suppliers can be set, in product form, in

Inventory --> Suppliers

If supplier specifies a known code in XML, the system will use it to retrieve the correct product to be used in invoice line, setting the related tax and account.
