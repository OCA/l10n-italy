# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract (http://www.abstract.it)
#    @author Davide Corio <davide.corio@abstract.it>
#    Copyright (C) 2014 Agile Business Group (http://www.agilebg.com)
#    Copyright (C) 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
#    @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
#    @author Giuseppe Stoduto
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################


from openerp import fields, models, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    gross_weight = fields.Float(string="Gross Weight")
    net_weight = fields.Float(string="Net Weight")
    volume = fields.Float('Volume')

    def _make_invoice(self, cr, uid, order, lines, context=None):
        inv_id = super(SaleOrder, self)._make_invoice(
            cr, uid, order, lines, context)
        weight = order.gross_weight
        net_weight = order.net_weight
        if not weight:
            for picking in order.picking_ids:
                weight += picking.weight
        if not net_weight:
            for picking in order.picking_ids:
                net_weight += picking.weight_net

        self.pool.get('account.invoice').write(cr, uid, [inv_id], {
            'incoterm':order.incoterm.id,
            'gross_weight': weight,
            'net_weight': net_weight,
            'volume': order.volume,
            })
        return inv_id
