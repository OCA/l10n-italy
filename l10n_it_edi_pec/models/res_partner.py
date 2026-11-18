from odoo import fields, models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    l10n_it_generic_pec_email = fields.Char(string="Generic PEC e-mail")
