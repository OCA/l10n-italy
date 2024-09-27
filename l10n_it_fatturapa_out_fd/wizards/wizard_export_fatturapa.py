#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    @staticmethod
    def get_importo(line):
        discount_fixed = line.discount_fixed
        if discount_fixed:
            return discount_fixed
        str_number = str(line.discount)
        number = str_number[::-1].find(".")
        if number <= 2:
            return False
        return line.price_unit * line.discount / 100

    @api.model
    def getTemplateValues(self, template_values):
        template_values = super().getTemplateValues(template_values)
        template_values.update({"get_importo": self.get_importo})
        return template_values
