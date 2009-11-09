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
        'company_id': fields.many2one('res.company', 'Company', required=True),
    }
    _defaults = {
        'company_id': lambda self, cr, uid, context: self.pool.get('res.users').browse(cr, uid, uid,context=context).company_id.id,
    }
  
sale_order()


