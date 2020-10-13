# Copyright 2014 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Copyright 2020 Francesco Apruzzese <francesco.apruzzese@openforce.it>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api


class BetterZipGeonamesImport(models.TransientModel):
    _inherit = 'better.zip.geonames.import'

    @api.model
    def select_or_create_state(
        self, row, country_id, code_row_index=4, name_row_index=3
    ):
        return super(BetterZipGeonamesImport, self).select_or_create_state(
            row, country_id, code_row_index=6, name_row_index=5)
