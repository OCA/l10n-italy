# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DepLineType(models.Model):
    _name = "asset.depreciation.line.type"
    _description = "Depreciation Line Type"
    _table = "asset_dep_line_type"
    _order = "name asc, code asc"

    @api.model
    def get_default_company_id(self):
        return self.env.company

    code = fields.Char()

    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.get_default_company_id(),
        string="Company",
    )

    name = fields.Char(required=True)

    type = fields.Selection(
        [("in", "In"), ("out", "Out")],
    )

    @api.ondelete(
        at_uninstall=False,
    )
    def _unlink_except_in_depreciation_line(self):
        for line_type in self:
            if self.env["asset.depreciation.line"].search(
                [("depreciation_line_type_id", "=", line_type.id)]
            ):
                raise ValidationError(
                    self.env._(
                        "Cannot remove type %(type)s: there is some depreciation"
                        " line linked to it.",
                        type=line_type.name,
                    )
                )

    @api.depends("code", "name", "type")
    def _compute_display_name(self):
        for line_type in self:
            name = ""

            if line_type.code:
                name += f"[{line_type.code}] "

            name += line_type.name

            type_name = dict(line_type._fields["type"].selection).get(line_type.type)
            if type_name:
                name += " - " + type_name

            line_type.display_name = name.strip()
