1. Create a supplier invoice with a reverse charge fiscal position
2. Add invoice lines with fixed discounts (``discount_fixed`` field)
3. Validate the invoice
4. The generated self-invoice will correctly include the fixed discount field

**Example:**

* Original supplier invoice line:

  * Product: Service A
  * Price Unit: 1000.00 EUR
  * Quantity: 1
  * Fixed Discount: 100.00 EUR
  * Net Amount: 900.00 EUR

* Self-invoice line (with this module):

  * Product: Service A
  * Price Unit: 1000.00 EUR
  * Quantity: 1
  * Fixed Discount: 100.00 EUR (correctly copied)
  * Net Amount: 900.00 EUR
