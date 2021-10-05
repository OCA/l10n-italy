This module shows, for each (customer) invoice line, the delivered production
lots that will be also displayed on the invoice report with their corresponding
delivered quantities in case the **Tracking** has been set to **By Lots**.

**Note:** As of v13.0, Odoo provides an option under *Settings* (**Inventory > Configuration > Settings > Traceability**) to **Display Lots & Serial Numbers on Invoices** which provides similar functionality. However, it has some limitations compared to this addon:
* It will only display the associated Lots / Serial Numbers in the generated *Invoice Report*, and not in an extra field in the Invoice view form.
* It will display all the Lots / Serial Numbers grouped together in an extra line in the Invoice Report. This module adds an extra field in each line with that information.
