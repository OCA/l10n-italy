# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class WizardRegistroIva(models.TransientModel):
    _inherit = "wizard.registro.iva"

    def print_registro_back_compat(self):
        """Print backward-compatible PDF report using v16 logic."""
        move_ids = self._get_move_ids(self)
        datas_form = self._get_datas_form()
        report_name = (
            "l10n_it_vat_registries_back_compat.action_report_registro_iva_back_compat"
        )
        datas = {"ids": move_ids, "model": "account.move", "form": datas_form}
        return self.env.ref(report_name).report_action(self, data=datas)

    def print_registro_back_compat_xlsx(self):
        """Print backward-compatible XLSX report using v16 logic."""
        move_ids = self._get_move_ids(self)
        datas_form = self._get_datas_form()
        report_name = (
            "l10n_it_vat_registries_back_compat."
            "action_report_registro_iva_back_compat_xlsx"
        )
        datas = {"ids": move_ids, "model": "account.move", "form": datas_form}
        moves = self.env["account.move"].browse(move_ids)
        return self.env.ref(report_name).report_action(moves, data=datas)
