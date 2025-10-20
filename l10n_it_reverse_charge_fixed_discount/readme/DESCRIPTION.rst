This module provides integration between the Italian Reverse Charge module
(``l10n_it_reverse_charge``) and the Fixed Discount module
(``account_invoice_fixed_discount``).

**Problem**

When a supplier invoice has:

* A reverse charge fiscal position configured
* One or more invoice lines with fixed discount (``discount_fixed``)

The system creates self-invoices but does not copy the ``discount_fixed`` field
to the self-invoice lines. This results in incorrect amounts in the self-invoice.

**Solution**

This module extends the ``rc_inv_line_vals()`` method to copy the ``discount_fixed``
field from the original supplier invoice line to the self-invoice line (similar to
how the percentage ``discount`` field is already copied). The ``account_invoice_fixed_discount``
module then automatically applies its logic to compute the correct net amounts in the
self-invoice.
