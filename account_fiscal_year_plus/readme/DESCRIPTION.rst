.. $if version == '12.0
This module just adds the menu

Invoicing > Configuration > Accounting > Fiscal Years

This is totally refactored compared to 11 version, because odoo 12 introduced `account.fiscal.year` object.
See https://github.com/OCA/account-financial-tools/pull/706

WARNING: This module was born to replace account_fiscal_year in account-financial_tools OCA repository.

.. $else
This module extends date.range.type to add fiscal_year flag.

Override official res_company.compute_fiscal_year_dates to get the
fiscal year date start / date end for any given date.
That methods first looks for a date range of type fiscal year that
encloses the give date.
If it does not find it, it falls back on the standard Odoo
technique based on the day/month of end of fiscal year.
.. $fi
