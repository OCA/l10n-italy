# Copyright 2014-2019 Dinamiche Aziendali srl
# (http://www.dinamicheaziendali.it/)
# @author: Marco Calcagni <mcalcagni@dinamicheaziendali.it>
# @author: Gianmarco Conte <gconte@dinamicheaziendali.it>
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models

PRICES_TO_SHOW = [("unit", "Unit price"), ("total", "Total price"), ("none", "None")]
DOMAIN_PRICES_TO_SHOW = [p[0] for p in PRICES_TO_SHOW]


class StockPickingTransportCondition(models.Model):
    _name = "stock.picking.transport.condition"
    _description = "Condition of Transport"
    _order = "sequence, name, id"

    active = fields.Boolean(default=True)
    sequence = fields.Integer(string="Sequence", index=True, default=10)
    name = fields.Char(
        string="Condition name",
        index=True,
        required=True,
        translate=True,
    )
    price_to_show = fields.Selection(
        PRICES_TO_SHOW,
        string="Price to show",
        required=True,
        default=DOMAIN_PRICES_TO_SHOW[0],
    )

    #
    # TODO: Capire come dev'essere utilizzato questo campo.
    #       Deve influenzare il comportamento del campo "prezzo"
    #        solo ed esclusivamente nelle stampe del DdT?
    #

    note = fields.Html(string="Internal note")

    _sql_constraints = [
        ("name_uniq", "unique(name)", "This condition of transport already exists!")
    ]
