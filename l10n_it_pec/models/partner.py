# Copyright 2014 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    pec_mail = fields.Char(string='PEC Mail')
