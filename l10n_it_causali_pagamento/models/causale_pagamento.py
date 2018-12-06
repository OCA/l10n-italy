# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class CausalePagamento(models.Model):
    _name = 'causale.pagamento'
    _description = 'Causale Pagamento'

    @api.constrains('code')
    def _check_code(self):
        for causale in self:
            domain = [('code', '=', causale.code)]
            elements = self.search(domain)
            if len(elements) > 1:
                raise ValidationError(
                    _("The element with code %s already exists")
                    % causale.code)

    @api.multi
    def name_get(self):
        res = []
        for cau in self:
            name = "%s - %s" % (cau.code, cau.name)
            if len(name) > 50:
                name = name[:50] + '...'
            res.append((cau.id, name))
        return res

    code = fields.Char(string='Code', size=2, required=True)
    name = fields.Text(string='Description', required=True)
