#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.fields import first
from odoo.tools.float_utils import float_is_zero, float_round


def formatRateType(amount):
    return "%.2f" % float_round(abs(amount), 2)


def formatAmount2DecimalType(amount):
    return "%.2f" % float_round(amount, 2)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def get_dati_cassa_previdenziale(self, invoice_line):
        """
        Return node DatiCassaPrevidenziale,
        its values are based on `invoice_line`.
        """
        DatiCassaPrevidenziale = False
        welfare_amount = invoice_line.welfare_grouping_fund_type_amount_id
        if welfare_amount:
            # Mandatory fields
            tax = first(invoice_line.tax_ids)
            DatiCassaPrevidenziale = {
                "TipoCassa": welfare_amount.welfare_fund_type_id.name,
                "AlCassa": formatRateType(welfare_amount.amount),
                "ImportoContributoCassa": formatAmount2DecimalType(
                    invoice_line.price_subtotal,
                ),
                "AliquotaIVA": formatRateType(tax.amount),
            }

            # Optional fields
            grouped_lines = invoice_line.welfare_grouped_invoice_line_ids
            grouped_lines_subtotal = sum(grouped_lines.mapped("price_subtotal"))
            DatiCassaPrevidenziale["ImponibileCassa"] = False
            if not float_is_zero(grouped_lines_subtotal, 2):
                grouped_lines_subtotal = formatAmount2DecimalType(
                    grouped_lines_subtotal
                )
                DatiCassaPrevidenziale["ImponibileCassa"] = grouped_lines_subtotal

            DatiCassaPrevidenziale["Ritenuta"] = False
            withholding_taxes = invoice_line.invoice_line_tax_wt_ids
            if withholding_taxes:
                DatiCassaPrevidenziale["Ritenuta"] = True

            DatiCassaPrevidenziale["Natura"] = False
            tax_kind = tax.kind_id
            if tax_kind:
                DatiCassaPrevidenziale["Natura"] = tax_kind.code

            DatiCassaPrevidenziale["RiferimentoAmministrazione"] = False
            administration_reference = welfare_amount.administration_reference
            if administration_reference:
                DatiCassaPrevidenziale[
                    "RiferimentoAmministrazione"
                ] = administration_reference

        return DatiCassaPrevidenziale

    @api.model
    def getTemplateValues(self, template_values):
        def set_dati_cassa_previdenziale(invoice):
            """
            Set in `body` and return all the nodes DatiCassaPrevidenziale,
            their values are based on `invoice`.
            """
            DatiCassaPrevidenziale_list = list()
            for invoice_line in invoice.invoice_line_ids:
                DatiCassaPrevidenziale = self.get_dati_cassa_previdenziale(
                    invoice_line,
                )
                if DatiCassaPrevidenziale:
                    DatiCassaPrevidenziale_list.append(DatiCassaPrevidenziale)
            return DatiCassaPrevidenziale_list

        template_values = super().getTemplateValues(template_values)
        template_values["set_dati_cassa_previdenziale"] = set_dati_cassa_previdenziale
        return template_values

    @api.model
    def _get_e_invoice_lines(self, invoice):
        invoice_lines = super()._get_e_invoice_lines(invoice)
        # Exclude Welfare Grouping Lines
        # from the Invoice Lines
        # that will become Electronic Invoice Lines
        welfare_lines = invoice_lines.filtered("welfare_grouping_fund_type_amount_id")
        return invoice_lines - welfare_lines
