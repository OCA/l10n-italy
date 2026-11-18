# Copyright 2019-2023 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def pop_import_code(vals):
    if "import_code" in vals:
        vals.pop("import_code")
        _logger.warning("Import Code can never be manually set.")


class DepreciationMode(models.Model):
    _inherit = "asset.depreciation.mode"

    import_code = fields.Char(
        copy=False,
        help="Used to import data from xls(x) files. Must be unique.",
        readonly=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            pop_import_code(vals)
        dep_modes = super().create(vals_list)
        for dep_mode in dep_modes:
            dep_mode.assign_import_code()
        return dep_modes

    @api.model
    def _create(self, vals):
        pop_import_code(vals)
        return super()._create(vals)

    def write(self, vals):
        pop_import_code(vals)
        return super().write(vals)

    def _write(self, vals):
        pop_import_code(vals)
        return super()._write(vals)

    @api.model
    def get_by_import_code(self, code):
        self._cr.execute(
            f"SELECT id FROM {self._table} WHERE import_code = %s", (code,)
        )
        res = [x[0] for x in self._cr.fetchall()]
        return self.browse(res)

    def assign_import_code(self):
        self.ensure_one()
        self._cr.execute(
            f"UPDATE {self._table} SET import_code = %s WHERE id = %s",
            (f"DEP-MODE-{self.id}", self.id),
        )
