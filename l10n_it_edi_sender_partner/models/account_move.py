# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models

from odoo.addons.l10n_it_edi.models.account_move import get_text


class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_it_edi_intermediary_id = fields.Many2one("res.partner", string="Intermediary")

    def _l10n_it_edi_import_invoice(self, invoice, data, is_new):
        res = super()._l10n_it_edi_import_invoice(invoice, data, is_new)
        Partner = self.env["res.partner"]
        tree = data["xml_tree"]
        intermediary = tree.xpath("//TerzoIntermediarioOSoggettoEmittente")
        if not intermediary:
            return res
        intermediary = intermediary[0]
        paese = get_text(intermediary, ".//IdPaese")
        codice = get_text(intermediary, ".//IdCodice")
        if not codice:
            return res
        vat = (paese or "") + codice
        intermediary_id = Partner.search([("vat", "=", vat)], limit=1)
        if intermediary_id:
            invoice.l10n_it_edi_intermediary_id = intermediary_id
        return res
