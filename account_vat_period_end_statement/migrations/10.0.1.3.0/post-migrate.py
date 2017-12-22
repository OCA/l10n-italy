# -*- coding: utf-8 -*-
# Copyright 2017 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from openerp import api, SUPERUSER_ID


def migrate(cr, version):
    """Copy account.period to data.range
      only for those periods with vat statement"""
    if not version:
        return
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        # check if account_period table exists
        env.cr.execute(
            """SELECT relname FROM pg_class
            WHERE relname= 'account_period'""")
        if not cr.fetchone():
            return
        env.cr.execute(
            """SELECT vat_statement_id, company_id, name, date_start, date_stop
            from account_period """)
        date_range_model = env['date.range']
        date_range_type_model = env['date.range.type']
        periods = env.cr.fetchall()
        for period in periods:
            # if period has vat statement
            if period[0]:
                date_range_type = date_range_type_model.search(
                    [('name', '=', 'periodo fiscale'),
                     ('company_id', '=', period[1])
                     ])
                if not date_range_type:
                    date_range_type = date_range_type_model.create(
                        {'name': 'periodo fiscale',
                         'company_id': period[1]})
                date_range = date_range_model.search(
                    [('date_start', '=', period[3]),
                     ('date_end', '=', period[4]),
                     ('company_id', '=', period[1])
                     ])
                if date_range:
                    date_range.write(
                        {'vat_statement_id': period[0],
                         'type_id': date_range_type.id})
                else:
                    date_range_vals = {
                        'vat_statement_id': period[0],
                        'company_id': period[1],
                        'name': period[2],
                        'type_id': date_range_type.id,
                        'date_start': period[3],
                        'date_end': period[4]}
                    date_range_model.create(date_range_vals)
