# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract (http://www.abstract.it)
#    @author Davide Corio <davide.corio@abstract.it>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp.osv import orm
from openerp.osv import fields


class res_partner(orm.Model):

    _inherit = 'res.partner'

    _columns = {
        'carriage_condition_id': fields.many2one(
            'stock.picking.carriage_condition', 'Carriage Condition'),
        'goods_description_id': fields.many2one(
            'stock.picking.goods_description', 'Description of Goods'),
        'transportation_reason_id': fields.many2one(
            'stock.picking.transportation_reason',
            'Reason for Transportation'),
        'transportation_method_id': fields.many2one(
            'stock.picking.transportation_method',
            'Method of Transportation'),
    }
