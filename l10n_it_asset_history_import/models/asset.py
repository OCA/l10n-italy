# Copyright 2019-2023 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import base64
import logging

try:
    import xlsxwriter
except ImportError:
    xlsxwriter = None

from io import BytesIO

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


def pop_import_code(vals):
    if "import_code" in vals:
        vals.pop("import_code")
        _logger.warning("Import Code can never be manually set.")


class Asset(models.Model):
    _inherit = "asset.asset"

    import_code = fields.Char(
        copy=False,
        help="Used to import data from xls(x) files. Must be unique.",
        readonly=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            pop_import_code(vals)
        assets = super().create(vals_list)
        for asset in assets:
            asset.assign_import_code()
        return assets

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
            (f"ASSET-{self.id}", self.id),
        )

    def make_template_file_data(self, file_headers):
        file_data = BytesIO()
        if xlsxwriter is None:
            raise ValidationError(
                _(
                    "Cannot create xlsx file: Python package `xlsxwriter`"
                    " is not available. Please contact your IT assistance."
                )
            )
        wb = xlsxwriter.Workbook(file_data, {})

        sheet = wb.add_worksheet(_("Assets Import"))
        bg_red = wb.add_format({"bg_color": "red"})
        bold = wb.add_format({"bold": True})
        bred = wb.add_format({"bold": True, "color": "red"})
        pos = 0

        mandatory_headers = [h for h in file_headers if h.field == "import_code"]
        for header in file_headers:
            col = header.col
            style = None
            if header in mandatory_headers:
                style = bg_red
            sheet.write(pos, col, header.name, style)
        pos += 1

        if self:
            template_data_list = [
                line.get_template_file_data(file_headers)
                for line in self.mapped("depreciation_ids.line_ids").sorted(
                    key=lambda ln: (ln.asset_id, ln.depreciation_id, ln.date)
                )
            ]
            for template_data in template_data_list:
                for col, val in template_data.items():
                    sheet.write(pos, col, val)
                pos += 1

        pos += 1
        sheet.write(pos, 1, _("WARNING"), bred)
        pos += 1

        warnings = [
            _("Red columns are mandatory."),
            _(
                "Maintain columns order: change in columns positioning may"
                " results in errors while importing!"
            ),
            _("Every cell must be formatted either as text or number."),
            _("`Line Type` column valid values are {}.").format(
                ", ".join(
                    [
                        f"`{s[0]}`"
                        for s in self.env["asset.depreciation.line"]
                        ._fields["move_type"]
                        .selection
                    ]
                )
            ),
            _(
                "After using this file to create your own import file,"
                " please delete these notes."
            ),
        ]
        for msg in warnings:
            sheet.write(pos, 1, msg, bred)
            pos += 1

        pos += 1
        fmt_msgs = {
            _("COLUMN TYPE"): _("HOW TO FORMAT CELLS"),
            _("Dates"): _("dd/mm/yyyy"),
            _("Amounts"): _("Numerical amounts, no currency"),
            _("Currency"): _("`EUR`, `USD`, or equivalent ISO 4217 code"),
            _("True/False"): _("Set an X if True, else leave empty"),
        }
        for title, value in fmt_msgs.items():
            sheet.write(pos, 1, title, bold)
            sheet.write(pos, 2, value, bold)
            pos += 1

        wb.close()
        file_data.seek(0)
        return base64.b64encode(file_data.read())
