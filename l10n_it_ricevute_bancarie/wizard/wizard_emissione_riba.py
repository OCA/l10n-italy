# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2012 Andrea Cometa.
#    Email: info@andreacometa.it
#    Web site: http://www.andreacometa.it
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2012 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields,orm

# -------------------------------------------------------
#        EMISSIONE RIBA
# -------------------------------------------------------
class emissione_riba(orm.TransientModel):
    _name = "riba.emissione"
    _description = "Emissione Ricevute Bancarie"
    _columns = {

        'configurazione' : fields.many2one('riba.configurazione', 'Configurazione', required=True),
        }
    
    def crea_distinta(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        def create_rdl(conta, bank_id, rd_id, date_maturity, partner_id, acceptance_account_id):
            rdl = {
                'sequence' : conta,
                'bank_id' : bank_id,
                'distinta_id': rd_id,
                'due_date' : date_maturity,
                'partner_id' : partner_id,
                'state': 'draft',
                'acceptance_account_id': acceptance_account_id,
            }
            return riba_distinta_line.create(cr, uid, rdl, context=context)
            
        """
        Qui creiamo la distinta
        """
        wizard_obj = self.browse(cr,uid,ids)[0]
        active_ids = context and context.get('active_ids', [])
        riba_distinta = self.pool.get('riba.distinta')
        riba_distinta_line = self.pool.get('riba.distinta.line')
        riba_distinta_move_line = self.pool.get('riba.distinta.move.line')
        move_line_obj = self.pool.get('account.move.line')

        # create distinta
        rd = {
            'name': self.pool.get('ir.sequence').get(cr, uid, 'seq.riba.distinta'),
            'config': wizard_obj.configurazione.id,
            'user_id': uid,
            'date_created': fields.date.context_today(self, cr, uid, context),
        }
        rd_id = riba_distinta.create(cr, uid, rd)
        
        # group by partner and due date
        grouped_lines = {}
        move_line_ids = move_line_obj.search(cr, uid, [('id', 'in', active_ids)], context=context)
        for move_line in move_line_obj.browse(cr, uid, move_line_ids, context=context):
            if move_line.partner_id.group_riba:
                if not grouped_lines.get(
                    (move_line.partner_id.id, move_line.date_maturity), False):
                    grouped_lines[(move_line.partner_id.id, move_line.date_maturity)] = []
                grouped_lines[(move_line.partner_id.id, move_line.date_maturity)].append(
                    move_line)
        
        # create lines
        conta = 1
        
        for move_line in move_line_obj.browse(cr, uid, move_line_ids, context=context):
            if move_line.partner_id.bank_ids:
                bank_id = move_line.partner_id.bank_ids[0]
            else:
                raise orm.except_orm('Attenzione!', 'Il cliente %s non ha la banca!!!' % move_line.partner_id.name)
            if move_line.partner_id.group_riba:
                for key in grouped_lines:
                    if key[0] == move_line.partner_id.id and key[1] == move_line.date_maturity:
                        rdl_id = create_rdl(conta, bank_id.id, rd_id, move_line.date_maturity, move_line.partner_id.id, wizard_obj.configurazione.acceptance_account_id.id)
                        total = 0.0
                        invoice_date_group = ''
                        for grouped_line in grouped_lines[key]:
                            riba_distinta_move_line.create(cr, uid, {
                                'riba_line_id': rdl_id,
                                'amount': grouped_line.amount_residual,
                                'move_line_id': grouped_line.id,
                                }, context=context)
                        del grouped_lines[key]
                        break
            else:
                rdl_id = create_rdl(conta, bank_id.id, rd_id, move_line.date_maturity, move_line.partner_id.id, wizard_obj.configurazione.acceptance_account_id.id)
                riba_distinta_move_line.create(cr, uid, {
                    'riba_line_id': rdl_id,
                    'amount': move_line.amount_residual,
                    'move_line_id': move_line.id,
                    }, context=context)
            
            conta+=1
        
        # ----- show distinta form
        mod_obj = self.pool.get('ir.model.data')
        res = mod_obj.get_object_reference(cr, uid, 'l10n_it_ricevute_bancarie', 'view_distinta_riba_form')
        res_id = res and res[1] or False,
        return {
            'name': 'Distinta',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': res_id,
            'res_model': 'riba.distinta',
            'type': 'ir.actions.act_window',
            #'nodestroy': True,
            'target': 'current',
            'res_id': rd_id or False,
        }

emissione_riba()
