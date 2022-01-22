This module is a technical module to set line type.
The account.move.line type are:

* receivable / payable: line with header data, partner_id, receivable/payable account type, maturity date (non tax)
* lp: line from invoice line, tax in tax_ids; usually contains cost or revenue account type
* tax: line automatically generated with tax reference in tax_line_id
* other: generic line, not from invoices

Notes:

* If receivable / payable account is set in line with tax, the line is marked as lp line, not receivable / payable
* lp line can contains one or more tax code ids
* tax line contains just one tax code and refers to one or more lp lines
