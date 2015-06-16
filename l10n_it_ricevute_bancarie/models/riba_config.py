# -*- coding: utf-8 -*-
<<<<<<< HEAD:l10n_it_ricevute_bancarie/configurazione.py
<<<<<<< HEAD
##############################################################################
#    
=======
#
=======
##############################################################################
>>>>>>> 8fe6aa6... added l10n_it_ricevute_bancarie from 8.0-riba:l10n_it_ricevute_bancarie/models/riba_config.py
#
>>>>>>> 20676d5... added l10n_it_ricevute_bancarie from 7.0
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
<<<<<<< HEAD:l10n_it_ricevute_bancarie/configurazione.py
<<<<<<< HEAD
##############################################################################

from openerp.osv import fields, orm

=======
#
=======
##############################################################################
>>>>>>> 8fe6aa6... added l10n_it_ricevute_bancarie from 8.0-riba:l10n_it_ricevute_bancarie/models/riba_config.py

from openerp.osv import fields, orm


<<<<<<< HEAD:l10n_it_ricevute_bancarie/configurazione.py
>>>>>>> 20676d5... added l10n_it_ricevute_bancarie from 7.0
class riba_configurazione(orm.Model):
=======
class riba_configuration(orm.Model):
>>>>>>> 8fe6aa6... added l10n_it_ricevute_bancarie from 8.0-riba:l10n_it_ricevute_bancarie/models/riba_config.py

    _name = "riba.configuration"
    _description = "Configuration parameters for Ricevute Bancarie"

    _columns = {
<<<<<<< HEAD:l10n_it_ricevute_bancarie/configurazione.py
<<<<<<< HEAD
        'name' : fields.char("Descrizione", size=64, required=True),
        'tipo' : fields.selection((('sbf', 'Salvo buon fine'),('incasso', 'Al dopo incasso')), 
            "Modalità Emissione", required=True),
        'bank_id' : fields.many2one('res.partner.bank', "Banca",
            required=True, help="Bank account used for Ri.Ba. issuing"),
            
        'acceptance_journal_id' : fields.many2one('account.journal', "Acceptance journal", 
            domain=[('type', '=', 'bank')],
            help="Journal used when Ri.Ba. is accepted by the bank"),
        'acceptance_account_id' : fields.many2one('account.account', "Acceptance account", 
            domain=[('type', '=', 'receivable')], help='Account used when Ri.Ba. is accepted by the bank'),
            
        'company_id': fields.many2one('res.company', 'Company',required=True),
        
        'accreditation_journal_id' : fields.many2one('account.journal', "Accreditation journal", 
            domain=[('type', '=', 'bank')],
            help="Journal used when Ri.Ba. amount is accredited by the bank"),
        'accreditation_account_id' : fields.many2one('account.account', "Ri.Ba. bank account", help='Account used when Ri.Ba. is accepted by the bank'),
        'bank_account_id' : fields.many2one('account.account', "Bank account", 
            domain=[('type', '=', 'liquidity')]),
        'bank_expense_account_id' : fields.many2one('account.account', "Bank Expenses account"),
        
        'unsolved_journal_id' : fields.many2one('account.journal', "Unsolved journal", 
            domain=[('type', '=', 'bank')],
            help="Journal used when Ri.Ba. is unsolved"),
        'overdue_effects_account_id' : fields.many2one('account.account', "Overdue Effects account", 
            domain=[('type', '=', 'receivable')]),
        'protest_charge_account_id' : fields.many2one('account.account', "Protest charge account"),
    }

    _defaults = {
        'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'riba.configurazione', context=c),
    }
    
=======
        'name': fields.char("Descrizione", size=64, required=True),
        'tipo': fields.selection(
=======
        'name': fields.char("Description", size=64, required=True),
        'type': fields.selection(
>>>>>>> 8fe6aa6... added l10n_it_ricevute_bancarie from 8.0-riba:l10n_it_ricevute_bancarie/models/riba_config.py
            (('sbf', 'Salvo buon fine'), ('incasso', 'Al dopo incasso')),
            "Issuing mode", required=True),
        'bank_id': fields.many2one(
            'res.partner.bank', "Bank", required=True,
            help="Bank account used for Ri.Ba. issuing"),
        'acceptance_journal_id': fields.many2one(
            'account.journal', "Acceptance journal",
            domain=[('type', '=', 'bank')],
            help="Journal used when Ri.Ba. is accepted by the bank"),
        'acceptance_account_id': fields.many2one(
            'account.account', "Acceptance account",
            domain=[('type', '=', 'receivable')],
            help='Account used when Ri.Ba. is accepted by the bank'),
        'company_id': fields.many2one(
            'res.company', 'Company', required=True,
            default=lambda self: self.env['res.company']._company_default_get(
                'riba.configuration')),
        'accreditation_journal_id': fields.many2one(
            'account.journal', "Accreditation journal",
            domain=[('type', '=', 'bank')],
            help="Journal used when Ri.Ba. amount is accredited by the bank"),
        'accreditation_account_id': fields.many2one(
            'account.account', "Ri.Ba. bank account",
            help='Account used when Ri.Ba. is accepted by the bank'),
        'bank_account_id': fields.many2one(
            'account.account', "Bank account",
            domain=[('type', '=', 'liquidity')]),
        'bank_expense_account_id': fields.many2one(
            'account.account', "Bank Expenses account"),
        'unsolved_journal_id': fields.many2one(
            'account.journal', "Unsolved journal",
            domain=[('type', '=', 'bank')],
            help="Journal used when Ri.Ba. is unsolved"),
        'overdue_effects_account_id': fields.many2one(
            'account.account', "Overdue Effects account",
            domain=[('type', '=', 'receivable')]),
        'protest_charge_account_id': fields.many2one(
            'account.account', "Protest charge account"),
    }

<<<<<<< HEAD:l10n_it_ricevute_bancarie/configurazione.py
    _defaults = {
        'company_id': lambda self, cr, uid, c: self.pool.get(
            'res.company'
        )._company_default_get(cr, uid, 'riba.configurazione', context=c),
    }

>>>>>>> 20676d5... added l10n_it_ricevute_bancarie from 7.0
    def get_default_value_by_distinta(self, cr, uid, field_name, context=None):
=======
    def get_default_value_by_list(self, cr, uid, field_name, context=None):
>>>>>>> 8fe6aa6... added l10n_it_ricevute_bancarie from 8.0-riba:l10n_it_ricevute_bancarie/models/riba_config.py
        if context is None:
            context = {}
        if not context.get('active_id', False):
            return False
<<<<<<< HEAD:l10n_it_ricevute_bancarie/configurazione.py
        distinta_pool = self.pool.get('riba.distinta')
<<<<<<< HEAD
        distinta = distinta_pool.browse(cr, uid, context['active_id'], context=context)
        return distinta.config[field_name] and distinta.config[field_name].id or False
    
    def get_default_value_by_distinta_line(self, cr, uid, field_name, context=None):
=======
        distinta = distinta_pool.browse(
            cr, uid, context['active_id'], context=context)
        return distinta.config[field_name] and distinta.config[
            field_name].id or False

    def get_default_value_by_distinta_line(
        self, cr, uid, field_name, context=None
    ):
>>>>>>> 20676d5... added l10n_it_ricevute_bancarie from 7.0
=======
        ribalist_pool = self.pool['riba.list']
        ribalist = ribalist_pool.browse(cr, uid, context['active_id'],
                                        context=context)
        return (ribalist.config_id[field_name] and
                ribalist.config_id[field_name].id or False)

    def get_default_value_by_list_line(self, cr, uid, field_name,
                                       context=None):
>>>>>>> 8fe6aa6... added l10n_it_ricevute_bancarie from 8.0-riba:l10n_it_ricevute_bancarie/models/riba_config.py
        if context is None:
            context = {}
        if not context.get('active_id', False):
            return False
<<<<<<< HEAD:l10n_it_ricevute_bancarie/configurazione.py
<<<<<<< HEAD
        distinta_line = self.pool.get('riba.distinta.line').browse(cr, uid, context['active_id'], context=context)
        return distinta_line.distinta_id.config[field_name] and distinta_line.distinta_id.config[field_name].id or False


=======
        distinta_line = self.pool.get('riba.distinta.line').browse(
            cr, uid, context['active_id'], context=context)
        return distinta_line.distinta_id.config[
            field_name
        ] and distinta_line.distinta_id.config[field_name].id or False
>>>>>>> 20676d5... added l10n_it_ricevute_bancarie from 7.0
=======
        ribalist_line = self.pool['riba.list.line'].browse(
            cr, uid, context['active_id'], context=context)
        return (ribalist_line.list_id.config_id[field_name] and
                ribalist_line.list_id.config_id[field_name].id or False)
<<<<<<< HEAD
>>>>>>> 8fe6aa6... added l10n_it_ricevute_bancarie from 8.0-riba:l10n_it_ricevute_bancarie/models/riba_config.py
=======
>>>>>>> 154323a... fixed errors in tests and added dep needed
