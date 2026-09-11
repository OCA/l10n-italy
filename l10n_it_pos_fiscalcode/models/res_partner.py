# Copyright 2022 Dinamiche Aziendali srl
# Copyright 2022 Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# Copyright 2026 Simone Rubino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _load_pos_data_fields(self, config_id):
        pos_data_fields = super()._load_pos_data_fields(config_id)
        pos_data_fields.append("l10n_it_codice_fiscale")
        return pos_data_fields
