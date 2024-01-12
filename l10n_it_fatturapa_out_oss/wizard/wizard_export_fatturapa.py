from odoo import api, models


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    @api.model
    def getAllTaxes(self, invoice):
        out = super().getAllTaxes(invoice)
        for tax_line_id in out:
            tax_line = self.env["account.tax"].browse(tax_line_id)
            out[tax_line_id]["Oss Country"] = tax_line.oss_country_id
        return out
