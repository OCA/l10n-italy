# Copyright 2022 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.addons.l10n_it_account.tools.account_tools import encode_for_export
from odoo.tools.float_utils import float_round
from odoo.addons.l10n_it_fatturapa.bindings.fatturapa import (
    AltriDatiGestionaliType,
)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def setDettaglioLinea(self, line_no, line, body, price_precision, uom_precision):
        DettaglioLinea = super().setDettaglioLinea(
            line_no, line, body, price_precision, uom_precision)

        invoice_line_tax = line.invoice_line_tax_ids[0]
        if invoice_line_tax.oss_subjected and line.invoice_id.company_id.oss_year_ids.\
            filtered(
                lambda x: x.year == str(line.invoice_id.date.year) and x.oss_subjected
                ) and invoice_line_tax.kind_id:
            dati_gestionali = AltriDatiGestionaliType(
                TipoDato="OSS",
                RiferimentoTesto=encode_for_export(
                    '%.2f' % float_round(invoice_line_tax.amount, 2), 60),
            )
            DettaglioLinea.AltriDatiGestionali.append(dati_gestionali)
            AliquotaIVA = '0.00'
            DettaglioLinea.AliquotaIVA = AliquotaIVA
            DettaglioLinea.Natura = invoice_line_tax.kind_id.code
        return DettaglioLinea

    def setDatiRiepilogo(self, invoice, body):
        super().setDatiRiepilogo(invoice, body)

        if invoice.company_id.oss_year_ids.filtered(
                lambda x: x.year == str(invoice.date.year) and x.oss_subjected):
            for line in invoice.invoice_line_ids:
                if any(
                    y.oss_subjected and y.kind_id for y in line.invoice_line_tax_ids
                ):
                    body.DatiBeniServizi.DatiRiepilogo[0].Imposta = '0.00'
                    body.DatiBeniServizi.DatiRiepilogo[0].AliquotaIVA = '0.00'
                    body.DatiBeniServizi.DatiRiepilogo[0].Natura = \
                        line.invoice_line_tax_ids[0].kind_id.code
                    body.DatiBeniServizi.DatiRiepilogo[0].RiferimentoNormativo = \
                        encode_for_export(
                            line.invoice_line_tax_ids[0].law_reference, 100)
