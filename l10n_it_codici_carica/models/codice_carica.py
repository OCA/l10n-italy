# Copyright 2017 Alessandro Camilli - Openforce
# Copyright 2019 Stefano Consolaro (Associazione PNLUG - Gruppo Odoo)

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CodiceCarica(models.Model):
    _name = 'codice.carica'
    _description = 'Role Code'

    @api.constrains('code')
    def _check_code(self):
        for codice in self:
            domain = [('code', '=', codice.code)]
            elements = self.search(domain)
            if len(elements) > 1:
                raise ValidationError(
                    _("The element with code %s already exists") % codice.code)

    code = fields.Char(string='Code', size=2)
    name = fields.Char(string='Name')
