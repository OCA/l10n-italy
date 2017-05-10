# -*- coding: utf-8 -*-
<<<<<<< HEAD
<<<<<<< HEAD
# Copyright 2017 Alessandro Camilli - Openforce
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
=======
>>>>>>> 0590845b855585f5431727c60908bce98ac81350
=======
>>>>>>> 0590845... Tabelle dei codici carica da usale nelle dichiarazioni fiscali

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
<<<<<<< HEAD
<<<<<<< HEAD
    name = fields.Char(string='Name')
=======
    name = fields.Char('Name')
>>>>>>> 0590845b855585f5431727c60908bce98ac81350
=======
    name = fields.Char('Name')
>>>>>>> 0590845... Tabelle dei codici carica da usale nelle dichiarazioni fiscali
