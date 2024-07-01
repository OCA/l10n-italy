# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    delivery_note_line_id = fields.Many2one(
        "stock.delivery.note.line",
        string="Delivery Note Line",
        ondelete="set null",
        index=True,
    )
    delivery_note_id = fields.Many2one(
        "stock.delivery.note",
        "Delivery Note",
        related="delivery_note_line_id.delivery_note_id",
    )

    def _copy_data_extend_business_fields(self, values):
        super(AccountMoveLine, self)._copy_data_extend_business_fields(values)
        values["delivery_note_line_id"] = self.delivery_note_line_id.id
