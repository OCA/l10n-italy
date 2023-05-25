# Copyright 2019 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64

from odoo import _, fields, models


class AccountIntrastatExportFile(models.TransientModel):
    _name = "account.intrastat.export.file"
    _description = "Intrastat export file"

    name = fields.Char(string="File Name", readonly=True)
    data = fields.Binary(string="File", readonly=True)
    state = fields.Selection(
        selection=[("choose", "Choose"), ("get", "Get")],
        default="choose",
    )

    def act_getfile(self):
        self.ensure_one()
        statement_id = self.env.context.get("active_id")
        statement = self.env["account.intrastat.statement"].browse(statement_id)

        file = statement.generate_file_export()

        filename = statement._get_file_name()

        out = base64.encodebytes(file.encode())

        view = self.env.ref(
            "l10n_it_intrastat_statement.wizard_account_intrastat_export_file"
        )
        view_id = view.id

        self.write({"state": "get", "data": out, "name": filename})
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.intrastat.export.file",
            "view_mode": "form",
            "name": _("Export Intrastat File"),
            "res_id": self.id,
            "nodestroy": True,
            "view_id": [view_id],
            "target": "new",
        }
