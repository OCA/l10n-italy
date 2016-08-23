# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2013 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2015 Agile Business Group <http://www.agilebg.com>
#    Copyright (C) 2015 Link It Spa <http://www.linkgroup.it/>
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

from openerp import fields, models
from openerp.tools.translate import _
from openerp.exceptions import except_orm


class AccountTaxCode(models.Model):
    _inherit = 'account.tax.code'

    vat_statement_type = fields.Selection(
        (('credit', 'Credit'), ('debit', 'Debit')),
        string='Type',
        help="This establish whether amount will be loaded as debit or credit",
        default='debit')
    is_base = fields.Boolean(
        string='Is base',
        help="This tax code is used for base amounts \
         (field used by VAT registries)")


class AccountTax(models.Model):
    _inherit = 'account.tax'

    nondeductible = fields.Boolean(
        string='Non-deductible',
        help="Partially or totally non-deductible.")

    def copy_data(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        tmp_default = dict(default, base_code_id='', tax_code_id='',
                           ref_base_code_id='', ref_tax_code_id='')
        return super(AccountTax, self).copy_data(
            cr, uid, id, default=tmp_default, context=context)

    def create(self, cr, uid, vals, context=None):
        res = super(AccountTax, self).create(cr, uid, vals, context=context)
        tax = self.browse(cr, uid, res, context)
        self.check_tax(cr, uid, tax, context=context)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        res = super(AccountTax, self).write(
            cr, uid, ids, vals, context=context)
        for tax in self.browse(cr, uid, ids, context):
            self.check_tax(cr, uid, tax, context=context)
        return res

    def check_tax(self, cr, uid, tax, context=None):
        """
        This is used to check that every (purchase) tax code is linked to
        only one (main) tax.
        This allows to print a VAT register summary where
        tax amount, base amount, deductible amount and non deductible amount
        are all printed on the same line
        """
        if tax.company_id.skip_it_account_check:
            return
        if tax.type_tax_use == 'purchase' and not tax.parent_id:
            if tax.base_code_id:
                if self.exist(
                    cr, uid, 'base_code_id', tax.base_code_id.id, tax.id,
                    context=context
                ):
                    raise except_orm(
                        _('Error!'),
                        _('Tax code %s already used '
                          'in other purchase tax') % tax.base_code_id.name)
            if tax.tax_code_id:
                if self.exist(
                    cr, uid, 'tax_code_id', tax.tax_code_id.id, tax.id,
                    context=context
                ):
                    raise except_orm(
                        _('Error!'),
                        _('Tax code %s already used '
                          'in other purchase tax') % tax.tax_code_id.name)
            if tax.ref_base_code_id:
                if self.exist(
                    cr, uid, 'ref_base_code_id', tax.ref_base_code_id.id,
                    tax.id, context=context
                ):
                    raise except_orm(
                        _('Error!'),
                        _('Tax code %s already used '
                          'in other purchase tax') % tax.ref_base_code_id.name)
            if tax.ref_tax_code_id:
                if self.exist(
                    cr, uid, 'ref_tax_code_id', tax.ref_tax_code_id.id,
                    tax.id, context=context
                ):
                    raise except_orm(
                        _('Error!'),
                        _('Tax code %s already used '
                          'in other purchase tax') % tax.ref_tax_code_id.name)

    def exist(self, cr, uid, field, value, id_doc, context=None):
        res = self.pool.get('account.tax').search(
            cr, uid, [
                (field, '=', value),
                ('id', '!=', id_doc),
                ('parent_id', '=', False),
                ], context=context)
        if res:
            return True
        else:
            return False
