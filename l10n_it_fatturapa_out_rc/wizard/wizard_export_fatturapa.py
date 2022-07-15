# Copyright 2021 Alex Comba - Agile Business Group
# Copyright 2022 Marco Colombo - Phi srl - <marco.colombo@phi.technology>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    @api.model
    def getSign(self, invoice):
        sign = 1
        if invoice.move_type in [
            "out_refund",
            "in_refund",
        ] and invoice.fiscal_document_type_id.code not in ["TD04", "TD08"]:
            sign = -1
        return sign

    @api.model
    def getTemplateValues(self, template_values):
        template_values = super().getTemplateValues(template_values)
        template_values.update({"get_sign": self.getSign})
        return template_values

    @api.model
    def getPayments(self, invoice):
        payments = super().getPayments(invoice)
        sign = self.getSign(invoice)
        for payment in payments:
            payment.amount_currency *= sign
            payment.debit *= sign
        return payments

    @api.model
    def getImportoTotale(self, invoice):
        amount_total = super().getImportoTotale(invoice)
        amount_total *= self.getSign(invoice)
        return amount_total
