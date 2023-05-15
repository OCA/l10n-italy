# Copyright (c) 2023, Nextev Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model_create_multi
    def create(self, vals):
        """
        Create DN types and their sequences after companies creation
        if they're not already existing
        """
        res = super().create(vals)
        for company in res:
            self.env["stock.delivery.note.type"].sudo().create_dn_types(company)
        return res
