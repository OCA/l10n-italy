# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import _, models
from odoo.tools.misc import formatLang

from odoo.addons.report_xlsx_helper.report.report_xlsx_format import (
    FORMATS,
    XLS_HEADERS,
)

_logger = logging.getLogger(__name__)


class ReportRegistroIvaXlsx(models.AbstractModel):
    _name = "report.l10n_it_vat_registries.report_registro_iva_xlsx"
    _inherit = [
        "report.report_xlsx.abstract",
        "report.l10n_it_vat_registries.report_registro_iva",
    ]
    _description = "XLSX report for VAT registries"

    # to override
    def _get_vat_settlement_date_col_spec(self):
        return {}

    def _get_ws_params(self, workbook, data, objects):
        registry_type = data["form"]["registry_type"]
        titles = {
            "customer": "Registro IVA vendite",
            "supplier": "Registro IVA acquisti",
            "corrispettivi": "Registro corrispettivi",
        }
        title = data["form"]["tax_registry_name"] or titles.get(registry_type, _("N/A"))

        col_specs = {
            "date": {
                "header": {"value": _("REG. DATE")},
                "lines": {"value": self._render("format_date(move.date,date_format)")},
                "width": 20,
            },
            "no": {
                "header": {"value": _("REG. NUM.")},
                "lines": {"value": self._render("move.name")},
                "width": 20,
            },
            "reason": {
                "header": {"value": _("REASON")},
                "lines": {"value": self._render("line['invoice_type']")},
                "width": 20,
            },
            "inv_date": {
                "header": {"value": _("INV. DATE")},
                "lines": {
                    "value": self._render(
                        "format_date(line['invoice_date'],date_format)"
                    )
                },
                "width": 20,
            },
            "inv_name": {
                "header": {"value": _("INV. NUM.")},
                "lines": {
                    "value": self._render(
                        "move.ref if move.journal_id.type == 'purchase' "
                        "else move.name"
                    )
                },
                "width": 20,
            },
            "partner": {
                "header": {"value": _("BUSINESS NAME")},
                "lines": {"value": self._render("move.partner_id.name")},
                "width": 20,
            },
            "tin": {
                "header": {"value": _("TIN")},
                "lines": {"value": self._render("move.partner_id.vat")},
                "width": 20,
            },
            "total": {
                "header": {"value": _("TOTAL")},
                "lines": {
                    "value": self._render("formatLang(env, invoice_total(move))")
                },
                "width": 20,
            },
            "tax_name": {
                "header": {"value": _("Tax description")},
                "lines": {"value": self._render("line['tax_code_name']")},
                "width": 20,
            },
            "taxable": {
                "header": {"value": _("Taxable")},
                "lines": {"value": self._render("formatLang(env, line['base'])")},
                "width": 20,
            },
            "tax": {
                "header": {"value": _("Tax")},
                "lines": {"value": self._render("formatLang(env, line['tax'])")},
                "width": 20,
            },
        }

        col_specs.update(self._get_vat_settlement_date_col_spec())
        wanted = col_specs.keys()
        if registry_type == "corrispettivi":
            wanted -= ["reason", "inv_date", "inv_name", "partner", "tin"]

        return [
            {
                "ws_name": "vat_registry",
                "title": title,
                "wanted_list": wanted,
                "col_specs": col_specs,
                "generate_ws_method": "generate_ws",
            }
        ]

    def generate_ws(self, workbook, ws, ws_params, data, objects):
        ws.set_landscape()
        ws.fit_to_pages(1, 0)
        ws.set_header(XLS_HEADERS["xls_headers"]["standard"])
        ws.set_footer(XLS_HEADERS["xls_footers"]["standard"])

        self._set_column_width(ws, ws_params)

        row_pos = 0
        row_pos = self._write_ws_title(ws, row_pos, ws_params)

        row_pos = self._write_line(
            ws,
            row_pos,
            ws_params,
            col_specs_section="header",
            default_format=FORMATS["format_theader_yellow_left"],
        )

        ws.freeze_panes(row_pos, 0)

        for move in objects:
            inv_taxes, used_taxes = self._get_tax_lines(move, data["form"])

            for line in inv_taxes:
                row_pos = self._write_line(
                    ws,
                    row_pos,
                    ws_params,
                    col_specs_section="lines",
                    render_space={
                        "env": self.env,
                        "move": move,
                        "line": line,
                        "format_date": self._format_date,
                        "date_format": data["form"]["date_format"],
                        "formatLang": formatLang,
                        "invoice_total": self._get_move_total,
                    },
                    default_format=FORMATS["format_tcell_left"],
                )
