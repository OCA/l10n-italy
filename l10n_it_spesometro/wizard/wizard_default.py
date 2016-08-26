# -*- coding: utf-8 -*-
##############################################################################
#    
#    Author: Alessandro Camilli (a.camilli@yahoo.it)
#    Copyright (C) 2014
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
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

from osv import fields,osv
from tools.translate import _
import time

class wizard_spesometro_default(osv.osv_memory):
    
    def default_get(self, cr, uid, fields, context=None):
        
        res = super(wizard_spesometro_default, self).default_get(cr, uid, fields, context=context)
        res = {
               'partner_spesometro_escludi' : False,
               'partner_spesometro_operazione' : 'FA'
               }
        return res

    _name = "wizard.spesometro.default"
    
    _columns = {
        'partner_spesometro_escludi': fields.boolean('Da Escludere'),
        'partner_spesometro_operazione': fields.selection((('FA','Operazioni documentate da fattura'), 
                                  ('SA','Operazioni senza fattura'),
                                  ('BL1','Operazioni con paesi con fiscalit� privilegiata'),
                                  ('BL2','Operazioni con soggetti non residenti'),
                                  ('BL3','Acquisti di servizi da soggetti non residenti')),
                   'Operazione' ),
    }
    
    
    def setting_default(self, cr, uid, ids, context=None):
        
        partners_obj = self.pool.get('res.partner')
        wizard = self.read(cr, uid, ids)[0]
        vals = {
            'spesometro_escludi': wizard.get('partner_spesometro_escludi'),
            'spesometro_operazione': wizard.get('partner_spesometro_operazione'),
            }
        
        partners_ids = partners_obj.search(cr, uid, [('id','!=', 0)], context=context)
        partners_obj.write(cr, uid, partners_ids, vals)
        
        return {
            'type': 'ir.actions.act_window_close',
        }
