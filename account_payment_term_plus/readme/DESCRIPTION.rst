This module extends the functionality of payment terms to :

* support rounding, months and weeks on payment term lines
* allow to set more than one day of payment in payment terms
* if a payment term date is a holiday, it is postponed to a selected date
* allow to apply a chronological order on lines
* evaluate tax amount to 1st rate, if required
* set payment method on all lines
* new payment term simulator

  * for example, with a payment term which contains 2 lines

    * on standard, the due date of all lines is calculated from the invoice
      date
    * with this feature, the due date of the second line is calculated from
      the due date of the first line

WARNING: This module was born to replace account_payment_term_extension in account-invoicing OCA repository.