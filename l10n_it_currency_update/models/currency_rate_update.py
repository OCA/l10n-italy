# -*- coding: utf-8 -*-
# Copyright 2017 Giacomo Grasso, Gabriele Baldessari
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from datetime import datetime, time, timedelta

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_compare
from odoo.addons.currency_rate_update.services.currency_getter_interface \
    import CurrencyGetterType

_logger = logging.getLogger(__name__)


class CurrencyRateUpdateService(models.Model):
    """ The 'refresh_currency' method has been override for one main reason.
        The Bank of Italy does not provide exchange rate on a daily basis.
        Usually rates are given with few days delay and are not given during
        the weekend.

        For this reason we decided that every time this methodruns, it exports
        the exchange rates of the last 5 days and creates all missing rates,
        avoiding updating existing rate.

        The Bank of Italy API gets as an input only the date and return an
        Excel file with all available rates for that day.
    """
    _inherit = "currency.rate.update.service"
    _description = "Currency Rate Update"

    @api.multi
    def refresh_currency(self):
        """Refresh the currencies rates for all companies now!!"""
        # override method if Bank of Italy service is selected
        if self.service == "IT_BOI":
            rate_obj = self.env['res.currency.rate']
            for srv in self:
                _logger.info(
                    'Start refreshing currencies with service %s (company: %s)',
                    srv.service, srv.company_id.name)
                company = srv.company_id
                # The multi company currency can be set or no so we handle
                # The two case
                if not company.auto_currency_up:
                    continue
                main_currency = company.currency_id
                # No need to test if main_currency exists, because it is a
                # required field
                if float_compare(
                        main_currency.rate, 1,
                        precision_rounding=main_currency.rounding):
                    raise UserError(_(
                        "In company '%s', the rate of the main currency (%s)"
                        "must be 1.00 (current rate: %s).") % (
                            company.name,
                            main_currency.name,
                            main_currency.rate))
                note = srv.note or ''
                for day in range(5):
                    ref_date = datetime.today() - timedelta(days=day)
                    try:
                        # We initalize the class that will handle the request
                        # and return a dict of rate
                        getter = CurrencyGetterType.get(srv.service)
                        curr_to_fetch = [x.name for x in srv.currency_to_update]
                        res = {}
                        res, log_info, rate_name = getter.get_updated_currency(
                            curr_to_fetch,
                            main_currency.name,
                            srv.max_delta_days,
                            ref_date
                            )
                        # if the above method returns no currencies it is
                        # because they are not available in the Bank archives
                        if not res:
                            continue
                        rate_name = \
                            fields.Datetime.to_string(rate_name.replace(
                                hour=0, minute=0, second=0, microsecond=0))
                        for curr in srv.currency_to_update:
                            if curr == main_currency:
                                continue
                            rates = rate_obj.search([
                                ('currency_id', '=', curr.id),
                                ('company_id', '=', company.id),
                                ('name', '=', rate_name)])
                            if not rates:
                                vals = {
                                    'currency_id': curr.id,
                                    'rate': res[curr.name],
                                    'name': rate_name,
                                    'company_id': company.id,
                                }
                                rate_obj.create(vals)
                                _logger.info(
                                    'Updated currency %s via service %s '
                                    'in company %s',
                                    curr.name, srv.service, company.name)

                        # Show the most recent note at the top
                        msg = '%s \n%s currency updated. %s' % (
                            log_info or '',
                            fields.Datetime.to_string(datetime.today()),
                            note
                        )
                        srv.write({'note': msg})
                    except Exception as exc:
                        error_msg = '\n%s ERROR: %s %s' % (
                            fields.Datetime.to_string(datetime.today()),
                            repr(exc),
                            note
                        )
                        _logger.error(repr(exc))
                        srv.write({'note': error_msg})
                    if self._context.get('cron'):
                        midnight = time(0, 0)
                        next_run = (datetime.combine(
                                    fields.Date.from_string(srv.next_run),
                                    midnight) +
                                    _intervalTypes[str(srv.interval_type)]
                                    (srv.interval_number)).date()
                        srv.next_run = next_run
            return True
        else:
            super(CurrencyRateUpdateService, self).refresh_currency()
