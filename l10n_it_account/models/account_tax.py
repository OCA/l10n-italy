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

from openerp import fields, models, api
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

    @api.model
    def _compute_tax_amount(self, tax, tax_code, base_code):
        '''
        The Tax is child of another main tax.
        The main tax has more childs:
        - Child with tax_code_id are deductible
        - Child without tax_code_id are undeductible
        '''
        res = {}
        vat_deductible = 0
        vat_undeductible = 0
        if tax.parent_id:
            vat_code = tax.parent_id.description
            vat_name = tax.parent_id.name
            for child in tax.parent_id.child_ids:
                # deductibile
                if (
                    child.tax_code_id and
                    child.tax_code_id.vat_statement_account_id
                ):
                    vat_deductible = child.tax_code_id.sum_period
                # undeductibile
                else:
                    vat_undeductible = child.tax_code_id.sum_period
        else:
            vat_code = tax_code.code
            vat_name = tax_code.name
            vat_deductible = tax_code.sum_period

        res[vat_name] = {
            'code': vat_code,
            'tax_code_name': vat_name,
            'vat': vat_deductible + vat_undeductible,
            'vat_deductible': vat_deductible,
            'vat_undeductible': vat_undeductible,
            'base': base_code.sum_period
        }

        return res

    @api.model
    def _build_codes_dict(self, tax_code, res=None):
        # TODO context
        if res is None:
            res = {}
        tax_model = self.env['account.tax']
        tax_code_model = self.env['account.tax.code']

        # search for taxes linked to that code
        taxes = tax_model.search(
            [('tax_code_id', '=', tax_code.id)])
        if taxes:
            tax = taxes[0]
            # search for the related base code
            base_code = (
                tax.base_code_id or tax.parent_id and
                tax.parent_id.base_code_id or False)
            if not base_code:
                raise except_orm(
                    _('Error'),
                    _('No base code found for tax code %s') % tax_code.name)
            # check if every tax is linked to the same tax code and base code
            for tax in taxes:
                test_base_code = (
                    tax.base_code_id or tax.parent_id and
                    tax.parent_id.base_code_id or False)
                if test_base_code.id != base_code.id:
                    raise except_orm(
                        _('Error'),
                        _('Not every tax linked to tax code %s is linked to '
                          'the same base code')
                        % tax_code.name)
            if tax_code.sum_period or base_code.sum_period:
                tax_vals = tax_code_model._compute_tax_amount(
                    tax, tax_code, base_code)
                res.update(tax_vals)

        for child_code in tax_code.child_ids:
            res = self._build_codes_dict(
                child_code, res=res)

        return res

    @api.model
    def _get_tax_codes_amounts(self, period_id, tax_code_ids=None):
        if tax_code_ids is None:
            tax_code_ids = []
        res = {}
        code_model = self.env['account.tax.code']
        context = self.env.context.copy()
        context['period_id'] = period_id
        for tax_code in code_model.with_context(context).browse(tax_code_ids):
            res = self.with_context(context)._build_codes_dict(
                tax_code, res=res)
        return res

    @api.multi
    def get_tax_by_tax_code(self):
        """
        Get account.tax linked to current tax code.
        If the account.tax has a parent, the parent account.tax is returned.
        """
        self.ensure_one()
        # assumendo l'univocità fra tax code e tax senza genitore, risale
        # all account.tax collegato al tax code passato al metodo
        tax_code_id = self.id
        obj_tax = self.env['account.tax']
        tax_ids = obj_tax.search([
            '&',
            '|',
            ('base_code_id', '=', tax_code_id),
            '|',
            ('tax_code_id', '=', tax_code_id),
            '|',
            ('ref_base_code_id', '=', tax_code_id),
            ('ref_tax_code_id', '=', tax_code_id),
            ('parent_id', '=', False)
        ]).ids
        if not tax_ids:
            # I'm in the case of partially deductible VAT
            child_tax_ids = obj_tax.search([
                '|',
                ('base_code_id', '=', tax_code_id),
                '|',
                ('tax_code_id', '=', tax_code_id),
                '|',
                ('ref_base_code_id', '=', tax_code_id),
                ('ref_tax_code_id', '=', tax_code_id)
            ]).ids
            for tax in obj_tax.browse(child_tax_ids):
                if tax.parent_id:
                    if tax.parent_id.id not in tax_ids:
                        tax_ids.append(tax.parent_id.id)
                else:
                    if tax.id not in tax_ids:
                        tax_ids.append(tax.id)
        # Nel caso in cui due imposte (una con iva inclusa nel prezzo e
        # una con iva esclusa dal prezzo), utilizzino lo stesso account
        # tax code o lo stesso account base code, verrà utilizzata solo
        # quella con iva esclusa dal prezzo.
        if len(tax_ids) > 1:
            tax_ids_temp = []
            for tax in obj_tax.browse(tax_ids):
                if not tax.price_include:
                    tax_ids_temp.append(tax.id)
            tax_ids = tax_ids_temp

        if len(tax_ids) != 1:
            raise Exception(
                _("Tax code %s is not linked to 1 and only 1 tax")
                % tax_code_id)
        return tax_ids[0]


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
