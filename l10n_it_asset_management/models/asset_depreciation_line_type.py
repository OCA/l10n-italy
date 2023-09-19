# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DepLineType(models.Model):
    _name = "asset.depreciation.line.type"
    _description = "Depreciation Line Type"
    _table = "asset_dep_line_type"
    _order = "name asc, code asc"

    @api.model
    def get_default_company_id(self):
        return self.env.user.company_id

    code = fields.Char()

    company_id = fields.Many2one(
        "res.company", default=get_default_company_id, string="Company"
    )

    name = fields.Char(required=True)

    type = fields.Selection(
        [("in", "In"), ("out", "Out")],
    )

    def unlink(self):
        for line_type in self:
            if self.env["asset.depreciation.line"].search(
                [("depreciation_line_type_id", "=", line_type.id)]
            ):
                raise ValidationError(
                    _(
                        "Cannot remove type {}: there is some depreciation"
                        " line linked to it."
                    ).format(line_type.name)
                )

        return super().unlink()

    def name_get(self):
        return [(line_type.id, line_type.make_name()) for line_type in self]

    def make_name(self):
        self.ensure_one()
        name = ""
        if self.code:
            name += "[{}] ".format(self.code)
        name += self.name
        type_name = dict(self._fields["type"].selection).get(self.type)
        if type_name:
            name += " - " + type_name
        return name.strip()
