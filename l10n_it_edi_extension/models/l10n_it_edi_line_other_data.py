# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# Copyright 2025 Nextev Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EInvoiceLineOtherData(models.Model):
    """Model for storing AltriDatiGestionali (2.2.1.16) on invoice lines.

    Used both for read-only import data (linked to l10n_it_edi.line) and for
    editable export data (linked to account.move.line).
    """

    _name = "l10n_it_edi.line_other_data"
    _description = "E-invoice line other data"

    l10n_it_edi_line_id = fields.Many2one(
        "l10n_it_edi.line", string="Related E-bill Line", readonly=True
    )
    move_line_id = fields.Many2one(
        "account.move.line",
        string="Invoice Line",
        ondelete="cascade",
        index=True,
    )
    name = fields.Char(
        string="Data Type",
        required=True,
        size=10,
        help="TipoDato: Type of additional data (max 10 characters)",
    )
    text_ref = fields.Char(
        string="Text Reference",
        size=60,
        help="RiferimentoTesto: Text reference (max 60 characters)",
    )
    num_ref = fields.Float(
        string="Number Reference",
        digits=(16, 8),
        help="RiferimentoNumero: Numeric reference (up to 8 decimal places)",
    )
    date_ref = fields.Date(
        string="Date Reference",
        help="RiferimentoData: Date reference",
    )

    @api.depends("name", "text_ref", "num_ref", "date_ref")
    def _compute_display_name(self):
        for record in self:
            parts = [record.name or ""]
            if record.text_ref:
                parts.append(record.text_ref)
            if record.num_ref:
                parts.append(str(record.num_ref))
            if record.date_ref:
                parts.append(str(record.date_ref))
            record.display_name = ": ".join(filter(None, parts))

    def action_delete(self):
        move_line_id = self.move_line_id.id
        self.unlink()
        return {
            "type": "ir.actions.act_window",
            "name": _("Other Management Data"),
            "res_model": self._name,
            "view_mode": "list,form",
            "target": "new",
            "domain": [("move_line_id", "=", move_line_id)],
            "context": {"default_move_line_id": move_line_id},
        }

    @api.constrains("name", "text_ref", "num_ref", "date_ref", "move_line_id")
    def _check_at_least_one_ref(self):
        for record in self:
            # Only validate for export records (linked to account.move.line)
            if not record.move_line_id:
                continue
            has_text = bool(record.text_ref)
            has_num = bool(record.num_ref)
            has_date = bool(record.date_ref)
            if not has_text and not has_num and not has_date:
                raise ValidationError(
                    _(
                        "At least one of Text Reference, Number Reference, "
                        "or Date Reference must be provided."
                    )
                )
