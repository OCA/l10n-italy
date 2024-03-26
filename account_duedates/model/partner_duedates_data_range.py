#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
import logging
from dateutil.relativedelta import relativedelta
from odoo import models, api, fields
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class PartnerDuedatesDatarange(models.Model):
    _name = "partner.duedates.datarange"

    def _get_period(self):
        domain = [('active', '=', True)]
        period_list = []
        periods = self.env['date.range'].search([('active', '=', True)])
        for each in periods:
            if each.type_id.name == 'Duedate':
                period_list.append(each.id)
        if period_list:
            domain = [('id', 'in', period_list)]
            return domain
        return domain

    partner_id = fields.Many2one(
        string='Partner',
        comodel_name='res.partner',
        required=False,
    )

    period_id = fields.Many2one(
        string='Periodo',
        comodel_name='date.range',
        required=True,
        domain=_get_period
    )

    split_date = fields.Date(
        string='Data di slittamento',
        required=True,
        default=False
    )

    enable_customer = fields.Boolean(string='Abilita cliente', default=False)
    enable_supplier = fields.Boolean(string='Abilita fornitore', default=False)

    @api.model
    def create(self, values):
        if values['split_date']:
            data_range = self.env['date.range'].browse(values['period_id'])
            df = data_range.date_end.strftime('%d/%m/%Y')
            comparison_date = fields.Date.from_string(values['split_date'])
            if comparison_date <= data_range.date_end:
                raise UserError('La data di slittamento deve essere '
                                'maggiore del periodo che ha data di '
                                'fine {df}!'.format(df=df))
            else:
                return super().create(values)
        # end if
    # end create

    @api.multi
    def write(self, values):
        if 'split_date' in values and values['split_date']:
            if 'period_id' in values and values['period_id']:
                data_range = self.env['date.range'].browse(values['period_id'])
            else:
                data_range = self.period_id
            df = data_range.date_end.strftime('%d/%m/%Y')
            comparison_date = fields.Date.from_string(values['split_date'])
            if comparison_date <= data_range.date_end:
                raise UserError('La data di slittamento deve essere '
                                'maggiore del periodo che ha data di '
                                'fine {df}!'.format(df=df))
        return super().write(values)
        # end if
    # end write

    def _update_year_task(self):
        current_year = fields.Date.context_today(self).year
        # update periods
        records = self.env['partner.duedates.datarange'].read_group(
            [], fields=['period_id'], groupby=['period_id'])
        for item in records:
            drange = self.env['date.range'].browse(item['period_id'][0])
            if drange.type_id.name == 'Duedate':
                # _logger.info('current year = {cy}'.format(cy=current_year))
                start_date_year = drange.date_start.year
                if current_year > start_date_year:
                    _logger.info('update id {id}'.format(id=drange.id))
                    # update period
                    start = drange.date_start + relativedelta(years=1)
                    end = drange.date_end + relativedelta(years=1)
                    drange.write({
                        'date_start': start,
                        'date_end': end,
                    })
                # end if
            # end if
        # end for
        # update split date
        records = self.env['partner.duedates.datarange'].search([])
        for item in records:
            if item.period_id.date_end > item.split_date:
                spl = item.split_date + relativedelta(years=1)
                item.write({
                    'split_date': spl
                })
            # end if
        # end for
    # end _update_year_task


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_duedates_dr_ids = fields.One2many(
        string='Periodi di slittamento',
        comodel_name='partner.duedates.datarange',
        inverse_name='partner_id',
    )
