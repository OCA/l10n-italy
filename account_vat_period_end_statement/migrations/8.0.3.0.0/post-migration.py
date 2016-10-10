# -*- coding: utf-8 -*-
# Copyright 2016 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, SUPERUSER_ID


def migrate(cr, version):
    """Copy company from that in existing periods."""
    if not version:
        return
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        end_statements = env['account.vat.period.end.statement'].search([])
        for end_statement in end_statements:
            companies = end_statement.mapped('period_ids.company_id')
            company = companies[0] if companies else False
            if company:
                end_statement.write({'company_id': company.id})
