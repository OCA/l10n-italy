# Copyright 2019-2023 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class DepreciationLine(models.Model):
    _inherit = "asset.depreciation.line"

    def get_template_file_data(self, file_headers):
        self.ensure_one()

        dtparser = fields.Date.from_string

        model_to_rec = {
            "asset.asset": self.asset_id,
            "asset.category": self.asset_id.category_id,
            "asset.depreciation": self.depreciation_id,
            "asset.depreciation.line": self,
            "asset.depreciation.mode": self.depreciation_id.mode_id,
            "asset.depreciation.type": self.depreciation_id.type_id,
            "res.currency": self.currency_id,
        }
        type_to_method = {
            "bool": lambda v: "X" if v else "",
            "date": lambda v: dtparser(v).strftime("%d/%m/%Y") if v else "",
            "float": lambda v: float(v) if v else 0,
            "selection": lambda v: v,
            "str": lambda v: v,
        }

        template_data = {}
        for header in file_headers:
            rec = model_to_rec[header.model]
            val = rec[header.field]
            if not val:
                val = header.tmpl_default
            val = type_to_method[header.type](val)
            template_data[header.col] = val

        return template_data
