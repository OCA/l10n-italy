# Copyright 2022 Marco Colombo <marco.colombo@phi.technology>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.tools import float_is_zero

from odoo.addons.l10n_it_account.tools.account_tools import encode_for_export
from odoo.addons.l10n_it_fatturapa_out.wizard.efattura import (
    format_numbers,
    fpaToEur,
)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    @api.model
    def getAllTaxes(self, invoice):
        """Generate summary data for taxes.
        Odoo does that for us, but only for nonzero taxes.
        SdI expects a summary for every tax mentioned in the invoice,
        even those with price_total == 0.
        """

        def _key(tax_id):
            return tax_id.id

        euro = self.env.ref("base.EUR")
        out_computed = {}
        # existing tax lines
        tax_ids = invoice.line_ids.filtered(
            lambda line: line.tax_line_id and not line.is_split_payment
        )
        for tax_id in tax_ids:
            tax_line_id = tax_id.tax_line_id
            aliquota = format_numbers(tax_line_id.amount)
            key = _key(tax_line_id)
            tax_amount = 0
            dp = self.env["decimal.precision"].precision_get("Account")
            if invoice.move_type == "out_invoice":
                if float_is_zero(tax_id.credit, dp) and tax_id.debit:
                    tax_amount = -tax_id.balance
                if tax_id.credit and float_is_zero(tax_id.debit, dp):
                    tax_amount = abs(tax_id.balance)
            else:
                tax_amount = abs(tax_id.balance)
            if key not in out_computed:
                out_computed[key] = {
                    "AliquotaIVA": aliquota,
                    "Natura": tax_line_id.kind_id.code,
                    # 'Arrotondamento':'',
                    "ImponibileImporto": tax_id.tax_base_amount,
                    "Imposta": tax_amount,
                    "EsigibilitaIVA": tax_line_id.payability,
                }
            else:
                out_computed[key]["ImponibileImporto"] += tax_id.tax_base_amount
                out_computed[key]["Imposta"] += tax_amount

            if tax_line_id.law_reference:
                out_computed[key]["RiferimentoNormativo"] = encode_for_export(
                    tax_line_id.law_reference, 100
                )

        out = {}
        # check for missing tax lines
        for line in invoice.invoice_line_ids:
            if line.display_type in ("line_section", "line_note"):
                # notes and sections
                # we ignore line.tax_ids altogether,
                # (it is popolated with a default tax usually)
                # and use another tax in the template
                continue
            for tax_id in line.tax_ids:
                aliquota = format_numbers(tax_id.amount)
                key = _key(tax_id)
                if key in out_computed:
                    continue
                if key not in out:
                    out[key] = {
                        "AliquotaIVA": aliquota,
                        "Natura": tax_id.kind_id.code,
                        # 'Arrotondamento':'',
                        "ImponibileImporto": fpaToEur(
                            line.price_subtotal, invoice, euro, rate=line.currency_rate
                        ),
                        "Imposta": 0.0,
                        "EsigibilitaIVA": tax_id.payability,
                    }
                    if tax_id.law_reference:
                        out[key]["RiferimentoNormativo"] = encode_for_export(
                            tax_id.law_reference, 100
                        )
                else:
                    out[key]["ImponibileImporto"] += fpaToEur(
                        line.price_subtotal, invoice, euro, rate=line.currency_rate
                    )
                    out[key]["Imposta"] += 0.0
        out.update(out_computed)
        return out

    @api.model
    def getImportoTotale(self, invoice):
        amount_total = super().getImportoTotale(invoice)
        if invoice.split_payment:
            amount_total += sum(
                invoice.line_ids.filtered(
                    lambda ln: ln.tax_line_id and not ln.is_split_payment
                ).mapped(lambda ln: abs(ln.balance))
            )
        return amount_total
