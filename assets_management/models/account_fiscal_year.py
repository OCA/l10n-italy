# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountFiscalYear(models.Model):
    _inherit = 'account.fiscal.year'

    @api.model
    def get_fiscal_year_by_date(
        self, date, limit=1, company=None, miss_raise=True
    ):
        """
        Retrieves fiscal year by given ``date`` (a datetime.date object).

        By default, only 1 fiscal year will be returned, unless specified
        differently.
        If ``miss_raise`` is True and no fiscal year is found, an error will be
        raised.
        """
        dom = self.get_fiscal_year_by_date_domain(date, company)
        fiscal_years = self.search(dom, limit=limit)
        if not fiscal_years and miss_raise:
            date_str = fields.Date.to_string(date)
            raise UserError(_("No fiscal year defined for date ") + date_str)
        return fiscal_years

    @api.model
    def get_fiscal_year_by_date_domain(self, date, company=None):
        """
        Prepares a search() domain to retrieve fiscal years by given ``date``.
        """
        domain = [('date_from', '<=', date), ('date_to', '>=', date)]
        if company:
            domain.append(('company_id', 'in', company.ids))
        return domain
