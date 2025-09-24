# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models


class ReportRegistroIvaXlsx(models.AbstractModel):
    _inherit = "report.l10n_it_vat_registries.report_registro_iva_xlsx"

    def _get_vat_settlement_date_col_spec(self):
        ret = {
            "vat_settlement_date": {
                "header": {"value": _("VAT settlement date")},
                "lines": {
                    "value": self._render(
                        "format_date(move.l10n_it_vat_settlement_date, date_format)"
                    )
                },
                "width": 20,
            }
        }
        return ret
