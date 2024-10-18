from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_document_fiscal_type(
        self, move_type=None, partner=None, fiscal_position=None, journal=None
    ):
        self.ensure_one()

        dt = super()._get_document_fiscal_type(
            move_type=move_type,
            partner=partner,
            fiscal_position=fiscal_position,
            journal=journal,
        )
        if self.is_sale_document() and self._is_downpayment():
            td02 = self.env["fiscal.document.type"].search(
                [("code", "=", "TD02")], limit=1
            )
            if td02:
                dt.insert(0, td02.id)
        return dt
