from odoo import models


class WizardImportFatturapa(models.TransientModel):
    _inherit = "wizard.import.fatturapa"

    def get_credit_account(self, product=None):
        credit_account = None
        if "partner_id" in self.env.context:
            partner = self.env["res.partner"].browse(self.env.context["partner_id"])
            if partner.property_account_expense:
                credit_account = partner.property_account_expense
        if not credit_account:
            credit_account = super(
                WizardImportFatturapa, self).get_credit_account(product)
        return credit_account

    def invoiceCreate(
        self, fatt, fatturapa_attachment, FatturaBody, partner_id
    ):
        return super(WizardImportFatturapa, self.with_context(
            partner_id=partner_id
        )).invoiceCreate(
            fatt, fatturapa_attachment, FatturaBody, partner_id)
