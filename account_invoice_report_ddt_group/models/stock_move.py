# -*- coding: utf-8 -*-
# © 2015 Nicola Malcontenti - Agile Business Group
# © 2016 Andrea Cometa - Apulia Software
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from openerp.osv import fields, osv


class StockMove(osv.osv):
    _inherit = "stock.move"

    def _create_invoice_line_from_vals(
            self, cr, uid, move, invoice_line_vals, context=None):

        invoice_line_vals['origin'] = move.picking_id.ddt_ids.ddt_number
        return super(StockMove, self)._create_invoice_line_from_vals(
            cr, uid, move, invoice_line_vals, context)
