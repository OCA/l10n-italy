# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountFiscalYear(models.Model):
    _inherit = "account.fiscal.year"

    @api.model
    def get_fiscal_year_by_date(self, date, limit=1, company=None, miss_raise=True):
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
        domain = [("date_from", "<=", date), ("date_to", ">=", date)]
        if company:
            domain.append(("company_id", "in", company.ids))
        return domain

    @api.model
    def _get_passed_years(self, start_date, end_date):
        """Find all fiscal years between `start_date` and `end_date`."""
        if start_date and end_date:
            overlapping_fiscal_year_domain = self.new(
                {
                    "date_from": start_date,
                    "date_to": end_date,
                }
            )._get_overlapping_domain()
            # Exclude current record's NewId
            # because it is not supported in domains
            overlapping_fiscal_year_domain = [
                term if term[0] != "id" else ("id", "!=", 0)
                for term in overlapping_fiscal_year_domain
            ]
            overlapping_fiscal_years = self.search(overlapping_fiscal_year_domain)
            passed_years = len(overlapping_fiscal_years)
        else:
            passed_years = None
        return passed_years
