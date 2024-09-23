# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    due_cost_service_id = fields.Many2one(
        string="Default Collection Fees Service",
        related="company_id.due_cost_service_id",
        help="Default Service for RiBa Collection Fees on invoice.",
        domain=[("type", "=", "service")],
        readonly=False,
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if res:
            res["due_cost_service_id"] = self.env.user.company_id.due_cost_service_id.id
        return res


class ResCompany(models.Model):
    _inherit = "res.company"

    due_cost_service_id = fields.Many2one("product.product", "Collection Fees Service")
