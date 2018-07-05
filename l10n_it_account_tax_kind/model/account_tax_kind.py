# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, models, fields


class AccountTaxKind(models.Model):

    _name = 'account.tax.kind'

    code = fields.Char(string='Code', size=3, required=True)
    name = fields.Char(string='Name', required=True)

    @api.multi
    def name_get(self):
        res = []
        for tax_kind in self:
            res.append(
                (tax_kind.id, '[%s] %s' % (tax_kind.code, tax_kind.name)))
        return res

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
