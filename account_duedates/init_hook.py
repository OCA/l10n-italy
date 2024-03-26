#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
import logging
import datetime
from odoo import api, SUPERUSER_ID


logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    """
    The objective of this hook is to update account move line new field
    with the correct value.
    """
    year = datetime.datetime.now().year

    env = api.Environment(cr, SUPERUSER_ID, {})
    date_range_model = env['date.range']
    date_range_type_model = env['date.range.type']

    dtype = date_range_type_model.search([('name', '=', 'Duedate')])
    if dtype and dtype.id:
        records = date_range_model.search([('name', '=', 'Agosto')])
        if not records:
            date_start = datetime.datetime(year, 8, 1).date()
            date_end = datetime.datetime(year, 8, 31).date()
            vals = {
                'name': 'Agosto',
                'date_start': date_start,
                'date_end': date_end,
                'type_id': dtype.id
            }
            date_range_model.create(vals)

        records = date_range_model.search([('name', '=', 'Natale')])
        if not records:
            date_start = datetime.datetime(year, 12, 20).date()
            date_end = datetime.datetime(year, 12, 31).date()
            vals = {
                'name': 'Natale',
                'date_start': date_start,
                'date_end': date_end,
                'type_id': dtype.id
            }
            date_range_model.create(vals)

