# -*- coding: utf-8 -*-
# Copyright 2016 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    fyc_id = fields.Many2one(
        comodel_name='account.fiscalyear.closing', delete="cascade",
        string="Fiscal year closing", readonly=True)

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        # Filter out move lines from fiscal year closing unless they
        # were explicitely asked for
        if not self.env.context.get('search_fyc_moves', False):
            if args:
                if not any(item[0] == 'fyc_id' for item in args):
                    args.insert(0, ('fyc_id', '=', False))
            else:
                args = [('fyc_id', '=', False)]

        return super(AccountMoveLine, self).search(
            args, offset=offset, limit=limit, order=order, count=count)
