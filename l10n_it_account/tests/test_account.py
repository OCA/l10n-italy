# -*- coding: utf-8 -*-
#
#    Copyright (C) 2015 Agile Business Group <http://www.agilebg.com>
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

from openerp.tests.common import TransactionCase
from openerp.exceptions import except_orm


class TestTax(TransactionCase):

    def setUp(self):
        super(TestTax, self).setUp()
        self.tax_model = self.env['account.tax']
        self.tax_code_model = self.env['account.tax.code']

    def test_create_taxes(self):
        tax_code_22cr = self.tax_code_model.create({
            'name': 'Credit VAT 22%',
            'code': '22CR',
            })
        tax_code_base_22cr = self.tax_code_model.create({
            'name': 'Credit VAT 22% Base',
            'code': '22CRbase',
            })
        tax_code_22cr_sp = self.tax_code_model.create({
            'name': 'Credit VAT 22% SP',
            'code': '22CRSP',
            })
        tax_code_base_22cr_sp = self.tax_code_model.create({
            'name': 'Credit VAT 22% SP Base',
            'code': '22CRSPbase',
            })
        tax_22_cr = self.tax_model.create({
            'name': '22cr',
            'type_tax_use': 'purchase',
            'tax_code_id': tax_code_22cr.id,
            'ref_tax_code_id': tax_code_22cr.id,
            'base_code_id': tax_code_base_22cr.id,
            'ref_base_code_id': tax_code_base_22cr.id,
            })
        tax_22sp_vals = {
            'name': '22crSP',
            'type_tax_use': 'purchase',
            'tax_code_id': tax_code_22cr.id,
            'ref_tax_code_id': tax_code_22cr.id,
            'base_code_id': tax_code_base_22cr.id,
            'ref_base_code_id': tax_code_base_22cr.id,
            }
        # creating 22crSP with the same tax codes as 22cr
        with self.assertRaises(except_orm):
            self.tax_model.create(tax_22sp_vals)
        # deleting because assertRaises does not perform rollback
        self.tax_model.search([('name', '=', '22crSP')]).unlink()
        tax_22sp_vals.update({
            'tax_code_id': tax_code_22cr_sp.id,
            'ref_tax_code_id': tax_code_22cr_sp.id,
            'base_code_id': tax_code_base_22cr_sp.id,
            'ref_base_code_id': tax_code_base_22cr_sp.id,
            })
        # creating 22crSP with other tax codes
        self.tax_model.create(tax_22sp_vals)
        tax_22sp_debit_vals = {
            'name': '22debtSP',
            'type_tax_use': 'sale',
            'tax_code_id': tax_code_22cr.id,
            'ref_tax_code_id': tax_code_22cr.id,
            'base_code_id': tax_code_base_22cr.id,
            'ref_base_code_id': tax_code_base_22cr.id,
            }
        # creating debit VAT with the same tax codes as credit VAT,
        # but with 'sale' type
        self.tax_model.create(tax_22sp_debit_vals)
        # editing 22cr using 22crSP tax code
        with self.assertRaises(except_orm):
            tax_22_cr.write({'tax_code_id': tax_code_22cr_sp.id})
        # if 22cr becomes sale, I can use that tax code
        tax_22_cr.write({
            'tax_code_id': tax_code_22cr_sp.id,
            'type_tax_use': 'sale',
            })
