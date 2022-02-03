# Copyright 2021 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.l10n_it_fatturapa_out.wizard.efattura import (
    EFatturaOut as _EFatturaOut,
)


class EFatturaOut(_EFatturaOut):
    def get_template_values(self):
        def get_sign(invoice):
            sign = 1
            if (
                invoice.move_type
                in [
                    "out_refund",
                    "in_refund",
                ]
                and invoice.fiscal_document_type_id.code not in ["TD04", "TD08"]
            ):
                sign = -1
            return sign

        template_values = super().get_template_values()
        template_values.update({"get_sign": get_sign})
        return template_values
