# © 2016 Andrea Cometa
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SlipReportQweb(models.AbstractModel):
    _name = "report.l10n_it_riba.slip_qweb"
    _description = "RiBa Slip Report"

    def _get_report_values(self, docids, data=None):
        return {
            "doc_ids": docids,
            "doc_model": "riba.slip",
            "docs": self.env["riba.slip"].browse(docids),
            "data": data,
        }
