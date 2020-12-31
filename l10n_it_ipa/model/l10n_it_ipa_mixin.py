# Copyright 2020 Tecnativa - Víctor Martínez
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import models, fields


class L10nItIpaMixin(models.AbstractModel):
    _name = 'l10n_it_ipa.mixin'
    _description = 'l10n_it_ipa Mixin'

    is_company_it = fields.Boolean(
        compute="_compute_is_company_it"
    )

    def _compute_is_company_it(self):
        for record in self:
            record.is_company_it = False
            country_it = self.env.ref("base.it")
            if (
                (
                    record.company_id and
                    record.company_id.country_id == country_it
                ) or (
                    not record.company_id and
                    self.env.user.company_id.country_id == country_it
                )
            ):
                record.is_company_it = True
