# Copyright 2014-2019 Dinamiche Aziendali srl
# (http://www.dinamicheaziendali.it/)
# @author: Marco Calcagni <mcalcagni@dinamicheaziendali.it>
# @author: Gianmarco Conte <gconte@dinamicheaziendali.it>
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# Copyright (c) 2020, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models

DELIVERY_NOTE_TYPE_CODES = [
    ('incoming', "Incoming"),
    ('outgoing', "Outgoing"),
    ('internal', "Internal")
]
DOMAIN_DELIVERY_NOTE_TYPE_CODES = [s[0] for s in DELIVERY_NOTE_TYPE_CODES]


class StockDeliveryNoteType(models.Model):
    _name = 'stock.delivery.note.type'
    _description = "Delivery note type"
    _order = 'sequence, name, id'

    active = fields.Boolean(string=_("Active"), default=True)
    sequence = fields.Integer(string=_("Sequence"), index=True, default=10)
    name = fields.Char(string=_("Name"), index=True, required=True,
                       translate=True)
    print_prices = fields.Boolean(string=_("Print prices on report"),
                                  default=False)
    code = fields.Selection(DELIVERY_NOTE_TYPE_CODES,
                            string=_("Type of Operation"),
                            required=True,
                            default=DOMAIN_DELIVERY_NOTE_TYPE_CODES[1])

    default_transport_condition_id = fields.Many2one(
        'stock.picking.transport.condition',
        string=_("Condition of transport"))
    default_goods_appearance_id = fields.Many2one(
        'stock.picking.goods.appearance', string=_("Appearance of goods"))
    default_transport_reason_id = fields.Many2one(
        'stock.picking.transport.reason', string=_("Reason of transport"))
    default_transport_method_id = fields.Many2one(
        'stock.picking.transport.method', string=_("Method of transport"))

    sequence_id = fields.Many2one('ir.sequence', required=True)
    next_sequence_number = fields.Integer(
        related='sequence_id.number_next_actual')
    company_id = fields.Many2one('res.company', string=_("Company"),
                                 default=lambda self: self.env.user.company_id)
    note = fields.Html(string=_("Internal note"))

    _sql_constraints = [(
        'name_uniq',
        'unique(name, company_id)',
        "This delivery note type already exists!"
    )]

    def goto_sequence(self, **kwargs):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ir.sequence',
            'res_id': self.sequence_id.id,
            'views': [(False, 'form')],
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            **kwargs
        }
