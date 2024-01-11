# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>


from odoo import fields, models


class StockDeliveryNoteCreateWizard(models.TransientModel):
    _name = "stock.delivery.note.confirm.wizard"
    _description = "Delivery Note Confirm"

    delivery_note_id = fields.Many2one("stock.delivery.note", readonly=True)
    warning_message = fields.Text(readonly=True)

    def confirm(self):
        self.ensure_one()
        self.delivery_note_id._action_confirm()
