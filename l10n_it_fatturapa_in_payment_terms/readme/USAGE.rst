When importing an electronic invoice (FatturaPA):

1. If the invoice has a payment term with "Retrieve due dates from XML" enabled, the system will use payment information from the XML
2. When you validate the invoice, the system will:
   - Check if the payment term has "Retrieve due dates from XML" enabled
   - Read the DatiPagamento section from the XML
   - Extract DataScadenzaPagamento (due date) and ImportoPagamento (amount) for each payment line
   - Generate account.move.line entries accordingly
   - Validate that the total amount matches the invoice total

The payment data is extracted from:
- DatiPagamento/DettaglioPagamento/DataScadenzaPagamento (due date)
- DatiPagamento/DettaglioPagamento/ImportoPagamento (amount)

Note: The behavior is controlled entirely by the payment term configuration. Invoices will only retrieve payment terms from XML if the assigned payment term has this option enabled.