from odoo import _, fields, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    comunicazione_dati_iva_escludi = fields.Boolean(
        string="Exclude from invoices communication"
    )

    def _compute_taxes_in_company_currency(self, vals):
        try:
            exchange_rate = abs(self.amount_total / self.amount_total_signed)
        except ZeroDivisionError:
            exchange_rate = 1
        vals["ImponibileImporto"] = vals["ImponibileImporto"] / exchange_rate
        vals["Imposta"] = vals["Imposta"] / exchange_rate

    def _get_tax_comunicazione_dati_iva(self):
        self.ensure_one()
        tax_model = self.env["account.tax"]

        tax_lines = []
        tax_grouped = {}
        for tax in self.line_ids.mapped("tax_ids"):
            base_move_lines = self.line_ids.filtered(
                lambda line: tax.id in line.tax_ids.ids
            )
            base = sum(base_move_lines.mapped("price_subtotal"))
            tax_move_lines = self.line_ids.filtered(
                lambda line: tax.id == line.tax_line_id.id
            )
            imposta = sum(tax_move_lines.mapped("price_unit"))
            aliquota = tax.amount
            kind_id = tax.kind_id.id
            payability = tax.payability
            tax_grouped[tax.id] = {
                "ImponibileImporto": base,
                "Imposta": imposta,
                "Aliquota": aliquota,
                "Natura_id": kind_id,
                "EsigibilitaIVA": payability,
                "Detraibile": 0.0,
            }
            if self.move_type in ("in_invoice", "in_refund"):
                tax_grouped[tax.id]["Detraibile"] = 100.0
                partial_tax = tax.invoice_repartition_line_ids.filtered(
                    lambda line: line.repartition_type == "tax" and line.account_id
                )
                if partial_tax:
                    tax_grouped[tax.id]["Detraibile"] = partial_tax.factor_percent

        for tax_id in tax_grouped:
            tax = tax_model.browse(tax_id)
            vals = tax_grouped[tax_id]
            vals = self._check_tax_comunicazione_dati_iva(tax, vals)
            self._compute_taxes_in_company_currency(vals)
            tax_lines.append((0, 0, vals))

        return tax_lines

    def _check_tax_comunicazione_dati_iva(self, tax, val=None):
        if not val:
            val = {}
        if val["Aliquota"] == 0 and not val["Natura_id"]:
            raise ValidationError(
                _("Please specify exemption kind for tax: {} - Invoice {}").format(
                    tax.name, self.name or False
                )
            )
        if not val["EsigibilitaIVA"]:
            raise ValidationError(
                _("Please specify VAT payability for tax: {} - Invoice {}").format(
                    tax.name, self.name or False
                )
            )
        return val
