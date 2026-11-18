# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ReportRegistroIvaBackCompatXlsx(models.AbstractModel):
    """XLSX version of the backward-compatible VAT registry report.

    Inherits from the v18 XLSX report (which provides ``_get_ws_params``
    and ``generate_ws``) and overrides tax computation to use v16 logic.
    """

    _name = "report.l10n_it_vat_registries_back_compat.registro_iva_xlsx"
    _inherit = "report.l10n_it_vat_registries.report_registro_iva_xlsx"
    _description = "XLSX report for VAT registries (v16 backward compatible)"

    def _tax_amounts_by_tax_id(self, move, move_lines, registry_type):
        """Delegate to the back-compat PDF report for v16 tax computation."""
        return self.env[
            "report.l10n_it_vat_registries_back_compat.report_registro_iva"
        ]._tax_amounts_by_tax_id(move, move_lines, registry_type)
