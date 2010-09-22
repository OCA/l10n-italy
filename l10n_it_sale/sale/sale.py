# -*- encoding: utf-8 -*-
##############################################################################
#
#
##############################################################################

import netsvc
from osv import fields, osv

class sale_order(osv.osv):
    _inherit = "sale.order"
    _columns =  {
        'validity': fields.date('Validity'),
    }
  
sale_order()


