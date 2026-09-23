# Copyright 2021 Alex Comba - Agile Business Group
# Copyright 2022 Marco Colombo - Phi srl - <marco.colombo@phi.technology>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def group_invoices_by_partner(self):
        res = super().group_invoices_by_partner()
        new_res = {}
        for partner, invoice_groups in res.items():
            for invoice_ids in invoice_groups:
                invoices = self.env["account.move"].browse(invoice_ids)
                rc_invoices = invoices.filtered(lambda x: x.rc_purchase_invoice_id)
                if not rc_invoices:
                    new_res.setdefault(partner, []).append(invoice_ids)
                    continue
                for invoice in rc_invoices:
                    new_res.setdefault(partner, []).append([invoice.id])
        return new_res

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
