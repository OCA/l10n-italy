# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2013 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2015 Agile Business Group <http://www.agilebg.com>
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2015 Link It Spa <http://www.linkgroup.it/>
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
#

from openerp.osv import orm
from openerp import fields
from openerp.tools.translate import _


class AccountTaxCode(orm.Model):
    _inherit = 'account.tax.code'

    vat_statement_type = fields.Selection(
        (('credit', 'Credit'), ('debit', 'Debit')),
        string='Type',
        help="This establish whether amount will be loaded as debit or credit",
        default='debit')


class account_tax(orm.Model):
    _inherit = 'account.tax'

    nondeductible = fields.Boolean(
        string='Non-deductible',
        help="Partially or totally non-deductible.")

    def copy_data(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        tmp_default = dict(default, base_code_id='', tax_code_id='',
        ref_base_code_id='', ref_tax_code_id='')
        return super(account_tax, self).copy_data(cr, uid, id,
        default=tmp_default, context=context)

    def create(self, cr, uid, vals, context=None):

        if vals['type_tax_use'] == 'purchase':
            if 'base_code_id' in vals:
                if vals['base_code_id']:
                    if self.exist(cr, uid, 'base_code_id',
                         vals['base_code_id']):
                        raise orm.except_orm(_('Error!'),
                                             _('Base code invoice already used '
                                             'in other purchase tax'))
            if 'tax_code_id' in vals:
                if vals['tax_code_id']:
                    if self.exist(cr, uid, 'tax_code_id', vals['tax_code_id']):
                        raise orm.except_orm(_('Error!'),
                                             _('Tax code invoice already '
                                              'used in other purchase tax.'))
            if 'ref_base_code_id' in vals:
                if vals['ref_base_code_id']:
                    if self.exist(cr, uid, 'ref_base_code_id',
                    vals['ref_base_code_id']):
                        raise orm.except_orm(_('Error!'),
                                             _('Base code refunds already used '
                                             'in other purchase tax.'))
            if 'ref_tax_code_id' in vals:
                if vals['ref_tax_code_id']:
                    if self.exist(cr, uid, 'ref_tax_code_id',
                    vals['ref_tax_code_id']):
                        raise orm.except_orm(_('Error!'),
                                             _('Tax code refunds already used '
                                             'in other purchase tax.'))

        return super(account_tax, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        for tax_code in self.browse(cr, uid, ids, context):
            type_tax_use = tax_code.type_tax_use
            base_code_id = tax_code.base_code_id.id
            tax_code_id = tax_code.tax_code_id.id
            ref_base_code_id = tax_code.ref_base_code_id.id
            ref_tax_code_id = tax_code.ref_tax_code_id.id
            if 'type_tax_use' in vals:
                type_tax_use = vals['type_tax_use']
            if 'base_code_id' in vals:
                base_code_id = vals['base_code_id']
            if 'tax_code_id' in vals:
                tax_code_id = vals['tax_code_id']
            if 'ref_base_code_id' in vals:
                ref_base_code_id = vals['ref_base_code_id']
            if 'ref_tax_code_id' in vals:
                ref_tax_code_id = vals['ref_tax_code_id']

            if type_tax_use == 'purchase':
                if base_code_id:
                    if self.exist(cr, uid, 'base_code_id', base_code_id,
                         tax_code.id):
                        raise orm.except_orm(_('Error!'),
                                            _('Base code invoices already used '
                                            'in other purchase tax.'))
                if tax_code_id:
                    if self.exist(cr, uid, 'tax_code_id', tax_code_id,
                    tax_code.id):
                        raise orm.except_orm(_('Error!'),
                                                 _('Tax code invoices already '
                                                 'used in other purchase tax.'))
                if ref_base_code_id:
                    if self.exist(cr, uid, 'ref_base_code_id', ref_base_code_id,
                         tax_code.id):
                        raise orm.except_orm(_('Error!'),
                                            _('Base code refunds already '
                                                 'used in other purchase tax.'))
                if ref_tax_code_id:
                    if self.exist(cr, uid, 'ref_tax_code_id', ref_tax_code_id,
                         tax_code.id):
                        raise orm.except_orm(_('Error!'),
                                            _('Tax code refunds already used '
                                            'in other purchase tax.'))

        return super(account_tax, self).write(cr, uid, ids, vals,
             context=context)

    def exist(self, cr, uid, field, value, id_doc=None):
        if id_doc:
            res = self.pool.get('account.tax').search(cr, uid,
            [(field, '=', value), ('id', '!=', id_doc)])
        else:
            res = self.pool.get('account.tax').search(cr, uid,
            [(field, '=', value)])

        if res:
            return True
        else:
            return False
