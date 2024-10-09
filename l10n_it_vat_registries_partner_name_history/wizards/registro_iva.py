#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json

from odoo import models


class WizardRegistroIva(models.TransientModel):
    _inherit = "wizard.registro.iva"

    def _get_registro_data(self):
        data = super()._get_registro_data()
        context = data.get("context")
        if context:
            context_dict = json.loads(context)
        else:
            context_dict = dict()
        context_dict["use_partner_name_history"] = True
        data["context"] = json.dumps(context_dict)
        return data
