# Copyright 2014 KTec S.r.l.
# (<http://www.ktec.it>).
# Copyright 2014 Associazione Odoo Italia
# (<http://www.odoo-italia.org>).
# Copyright 2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    ipa_code = fields.Char(string="IPA Code")
    is_pa = fields.Boolean(string="Public administration")
