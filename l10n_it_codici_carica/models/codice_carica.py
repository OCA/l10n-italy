# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CodiceCarica(models.Model):
    _name = 'codice.carica'
    _description = 'Codice Carica'

    @api.constrains('code')
    def _check_code(self):
        domain = [('code', '=', self.code)]
        elements = self.search(domain)
        if len(elements) > 1:
            raise ValidationError(
                _("The element with this code already exists"))

    code = fields.Char(string='Code', size=2)
    name = fields.Char('Name')
