# Copyright 2026 Nextev Srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_it_edi_is_td29 = fields.Boolean(
        string="TD29 - Omitted/Irregular Invoice Communication",
        copy=False,
        help="Check this box to generate a TD29 communication for omitted or "
        "irregular invoicing by the Italian seller/provider "
        "(art. 6, comma 8, D.Lgs. 471/97).",
    )

    def _l10n_it_edi_get_document_type(self):
        if self.l10n_it_edi_is_td29:
            return "TD29"
        return super()._l10n_it_edi_get_document_type()

    def _l10n_it_edi_get_values(self, pdf_values=None):
        res = super()._l10n_it_edi_get_values(pdf_values)
        if self.l10n_it_edi_is_td29:
            # TD29 is not a self-invoice (l10n_it_edi_is_self_invoice must
            # stay False as it is a mere communication to the Tax Agency),
            # but its XML is built the same way: since the field is False,
            # super() returns buyer=supplier and seller=company as for a
            # regular invoice, so they must be swapped back
            # (CedentePrestatore is the supplier, CessionarioCommittente
            # the company). CodiceDestinatario must always be "0000000".
            # "is_self_invoice" here is only the template variable, not the
            # field: it suppresses PECDestinatario (which the template reads
            # from the buyer record, not from buyer_info), IscrizioneREA,
            # RappresentanteFiscale and DatiPagamento, and makes the template
            # use the accounting date instead of the invoice date.
            # RegimeFiscale must be RF18 instead of the company tax system.
            res.update(
                {
                    "is_self_invoice": True,
                    "buyer": res["seller"],
                    "seller": res["buyer"],
                    "buyer_info": dict(res["seller_info"], pa_index="0000000"),
                    "seller_info": res["buyer_info"],
                    "regime_fiscale": "RF18",
                }
            )
        return res
