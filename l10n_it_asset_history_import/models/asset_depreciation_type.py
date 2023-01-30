# Copyright 2019-2023 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def pop_import_code(vals):
    if "import_code" in vals:
        vals.pop("import_code")
        _logger.warning("Import Code can never be manually set.")


class DepreciationType(models.Model):
    _inherit = "asset.depreciation.type"

    import_code = fields.Char(
        copy=False,
        help="Used to import data from xls(x) files. Must be unique.",
        readonly=True,
        string="Import Code",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            pop_import_code(vals)
        dep_types = super().create(vals_list)
        for dep_type in dep_types:
            dep_type.assign_import_code()
        return dep_types

    @api.model
    def _create(self, vals):
        pop_import_code(vals)
        return super()._create(vals)

    @api.multi
    def write(self, vals):
        pop_import_code(vals)
        return super().write(vals)

    @api.multi
    def _write(self, vals):
        pop_import_code(vals)
        return super()._write(vals)

    @api.model
    def get_by_import_code(self, code):
        self._cr.execute(
            "SELECT id FROM {} WHERE import_code = %s".format(self._table), (code,)
        )
        res = [x[0] for x in self._cr.fetchall()]
        return self.browse(res)

    def assign_import_code(self):
        self.ensure_one()
        self._cr.execute(
            "UPDATE {} SET import_code = %s WHERE id = %s".format(self._table),
            (f"DEP-TYPE-{self.id}", self.id),
        )
