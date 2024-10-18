# Copyright 2020 Marco Colommbo
# Copyright 2022 Simone Rubino - TAKOBI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    @api.model
    def default_get(self, fields):
        res = super(WizardExportFatturapa, self).default_get(fields)
        invoice_ids = self.env.context.get("active_ids", False)
        invoices = self.env["account.move"].browse(invoice_ids)
        # enable option by default if any invoice is connected to a dn
        if any(invoices.invoice_line_ids.mapped("delivery_note_id")):
            res["include_transport_data"] = "dati_dn"
        return res

    include_transport_data = fields.Selection(
        [
            ("dati_dn", "Include DN Data"),
        ],
        string="DN Data",
        help="Include DN data: The field must be entered when a transport "
        "document associated with a deferred invoice is present",
    )

    def getDatiDDT(self, invoice):
        """
        Get the data for rendering DatiDDT.

        :return: a list of dictionaries, with one dictionary per involved DdT.
        Each dictionary has shape:
        {
            '_delivery_note': <stock.delivery.note record of the involved the DdT>,

            'NumeroDDT': <string representing the DdT>,

            'DataDDT': <date of the DdT>,

            '_invoice_lines': (optional)
                <account.move.line records of invoice lines involved in the DdT>,
            'RiferimentoNumeroLinea': (optional)
                <string containing numbers of the invoice lines involved in the DdT>,
        }
        """
        self.ensure_one()
        dati_ddt_list = list()
        for delivery_note in invoice.delivery_note_ids:
            ddt_data = {
                "_delivery_note": delivery_note,
                "NumeroDDT": delivery_note.name,
                "DataDDT": delivery_note.date,
            }
            e_invoice_lines = self.get_e_invoice_lines(invoice)
            e_invoice_delivery_note_lines = e_invoice_lines.filtered(
                lambda l: l.delivery_note_id == delivery_note
            )
            if e_invoice_delivery_note_lines:
                # RiferimentoNumeroLinea should not be populated
                # if all the lines of the invoice
                # are linked to this delivery_note,
                # but we can't verify this condition
                # because only note lines (not product lines)
                # are linked to a delivery note.
                e_invoice_lines_list = list(e_invoice_lines)
                lines_refs_list = [
                    e_invoice_lines_list.index(line) + 1  # NumeroLinea is 1-based
                    for line in e_invoice_delivery_note_lines
                ]
                ddt_data.update(
                    {
                        "_invoice_lines": e_invoice_delivery_note_lines,
                        "RiferimentoNumeroLinea": lines_refs_list,
                    }
                )

            dati_ddt_list.append(ddt_data)
        return dati_ddt_list
