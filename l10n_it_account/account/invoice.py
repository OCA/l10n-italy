# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2010 OpenERP Italian Community (<http://www.openerp-italia.org>). 
#    All Rights Reserved
#    $Id$
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

import netsvc
import pooler, tools

from osv import fields, osv
from tools.translate import _

class Invoice(osv.osv):
    
    _inherit = 'account.invoice'
    
    def action_number(self, cr, uid, ids, *args):
        super(Invoice, self).action_number(cr, uid, ids, args)
        for obj_inv in self.browse(cr, uid, ids):
            type = obj_inv.type
            number = obj_inv.number
            date_invoice = obj_inv.date_invoice
            cr.execute("SELECT number FROM account_invoice i WHERE i.type = %s AND i.date_invoice > %s AND i.number < %s", (type, date_invoice, number))
            res = cr.dictfetchall()
            if res:
                raise osv.except_osv(_('Date Inconsistency'),
                        _('Cannot create invoice! Post the invoice with a greater date'))
        return True
    
Invoice()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
