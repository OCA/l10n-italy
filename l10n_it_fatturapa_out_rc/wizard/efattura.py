# Copyright 2021 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.l10n_it_fatturapa_out.wizard.efattura import (
    EFatturaOut as _EFatturaOut,
)


# extend the EFatturaOut class to add a new helper function
class EFatturaOut(_EFatturaOut):
    def get_template_values(self):
        get_sign = self.env["wizard.export.fatturapa"].getSign
        template_values = super().get_template_values()
        template_values.update({"get_sign": get_sign})
        return template_values
