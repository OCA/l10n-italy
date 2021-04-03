# Copyright 2020 Marco Colommbo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    @api.model
    def default_get(self, fields):
        res = super(WizardExportFatturapa, self).default_get(fields)
        invoice_ids = self.env.context.get("active_ids", False)
        invoices = self.env["account.move"].browse(invoice_ids)
        for invoice in invoices:
            for line in invoice.invoice_line_ids:
                if line.delivery_note_id:
                    res["include_transport_data"] = "dati_dn"
                    return res
        return res

    include_transport_data = fields.Selection(
        [
            ("dati_dn", "Include DN Data"),
        ],
        string="DN Data",
        help="Include DN data: The field must be entered when a transport "
        "document associated with a deferred invoice is present",
    )
