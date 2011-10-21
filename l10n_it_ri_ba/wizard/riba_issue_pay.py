# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    All Rights Reserved 
#    Thanks to Cecchi s.r.l http://www.cecchi.com/
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv

class riba_issue_make_payment(osv.osv_memory):
    _name = "riba.issue.make.payment"
    _description = "Riba make issue"

    def launch_wizard(self, cr, uid, ids, context=None):
        """
        Search for a wizard to launch according to the type.
        If type is manual. just confirm the order.
        """
        obj_riba_order = self.pool.get('riba.order')
        if context is None:
            context = {}
        obj_riba_order.set_done(cr, uid, [context['active_id']], context)
        return {'type': 'ir.actions.act_window_close'}
riba_issue_make_payment()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
