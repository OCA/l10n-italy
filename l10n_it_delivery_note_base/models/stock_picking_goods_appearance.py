# Copyright 2014-2019 Dinamiche Aziendali srl
# (http://www.dinamicheaziendali.it/)
# @author: Marco Calcagni <mcalcagni@dinamicheaziendali.it>
# @author: Gianmarco Conte <gconte@dinamicheaziendali.it>
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPickingGoodsAppearance(models.Model):
    _name = 'stock.picking.goods.appearance'
    _description = "Appearance of Goods"
    _order = 'sequence, name, id'

    active = fields.Boolean(default=True)
    sequence = fields.Integer(string="Sequence", index=True, default=10)
    name = fields.Char(string="Appearance name", index=True,
                       required=True, translate=True)
    note = fields.Html(string="Internal note")

    _sql_constraints = [(
        'name_uniq',
        'unique(name)',
        "This appearance of goods already exists!"
    )]
