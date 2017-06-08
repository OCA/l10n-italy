# -*- coding: utf-8 -*-
##############################################################################
#    
#    Author: Alessandro Camilli (a.camilli@openforce.it)
#    Copyright (C) 2015
#    Apulia Software srl - info@apuliasoftware.it - www.apuliasoftware.it
#    Openforce di Camilli Alessandro - www.openforce.it
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
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


from openerp import models, fields, api


class stock_picking(models.Model):
    
    _inherit = "stock.picking"
    
    @api.model
    def _get_invoice_vals(self, key, inv_type, journal_id, move, context=None):
        
        res = super(stock_picking, self)._get_invoice_vals(
            key, inv_type, journal_id, move)
        
        partner, currency_id, company_id, user_id = key
        
        res['intrastat'] = partner.property_account_position.intrastat
        
        return res
