# -*- coding: utf-8 -*-
#
#    Copyright (C) 2017 Apulia Software s.r.l. (http://www.apuliasoftware.it)
#    @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields


class AccountTaxKind(models.Model):

    _name = 'account.tax.kind'
    _rec_name = 'display_name'

    code = fields.Char(string='Code', size=3, required=True)
    name = fields.Char(string='Name', required=True)
    display_name = fields.Char(string='Name', compute='_compute_display_name')

    @api.depends('code', 'name')
    @api.multi
    def _compute_display_name(self):
        for record in self:
            record.display_name = u'[%s] %s' % (record.code, record.name)

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            records = self.search([
                '|', ('name', operator, name), ('code', operator, name)
                ] + args, limit=limit)
        else:
            records = self.search(args, limit=limit)
        return records.name_get()
