# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2012 Andrea Cometa.
#    Email: info@andreacometa.it
#    Web site: http://www.andreacometa.it
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2012 Associazione OpenERP Italia
#    (<http://www.odoo-italia.org>).
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

from openerp.osv import fields, orm


class RibaConfiguration(orm.Model):

    _name = "riba.configuration"
    _description = "Configuration parameters for Ricevute Bancarie"

    _columns = {
        'name': fields.char("Description", size=64, required=True),
        'type': fields.selection(
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

    def get_default_value_by_list(self, cr, uid, field_name, context=None):
        if context is None:
            context = {}
        if not context.get('active_id', False):
            return False
        ribalist_pool = self.pool['riba.distinta']
        ribalist = ribalist_pool.browse(cr, uid, context['active_id'],
                                        context=context)
        return (ribalist.config_id[field_name] and
                ribalist.config_id[field_name].id or False)

    def get_default_value_by_list_line(self, cr, uid, field_name,
                                       context=None):
        if context is None:
            context = {}
        if not context.get('active_id', False):
            return False
        ribalist_line = self.pool['riba.distinta.line'].browse(
            cr, uid, context['active_id'], context=context)
        return (ribalist_line.distinta_id.config_id[field_name] and
                ribalist_line.distinta_id.config_id[field_name].id or False)
