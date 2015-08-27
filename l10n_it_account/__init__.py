# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2010 OpenERP Italian Community
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2014 Associazione Odoo Italia
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2015 Agile Business Group (<http://www.agilebg.com>)
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

from . import models

import logging
from openerp import SUPERUSER_ID


def post_init_hook(cr, registry):
    tax_code_model = registry['account.tax.code']
    tax_model = registry['account.tax']
    logging.getLogger('openerp.addons.l10n_it_account').info(
        'Setting values for account.tax.code new field: VAT statement type')
    # only setting credit tax codes because default value is 'debit'
    credit_tax_code_ids = tax_code_model.search(cr, SUPERUSER_ID, [
        ('name', '=ilike', '%credit%'),
        ])
    tax_code_model.write(cr, SUPERUSER_ID, credit_tax_code_ids, {
        'vat_statement_type': 'credit',
        })

    logging.getLogger('openerp.addons.l10n_it_account').info(
        'Setting values for account.tax new field: Non-deductible')
    unded_tax_ids = tax_model.search(cr, SUPERUSER_ID, [
        ('name', '=ilike', '%detraibile%'),
        ])
    tax_model.write(cr, SUPERUSER_ID, unded_tax_ids, {
        'nondeductible': True,
        })

    logging.getLogger('openerp.addons.l10n_it_account').info(
        'Setting values for account.tax.code new field: Is base')
    base_tax_code_ids = tax_code_model.search(cr, SUPERUSER_ID, [
        ('name', '=ilike', '%imponibile%'),
        ])
    tax_code_model.write(cr, SUPERUSER_ID, base_tax_code_ids, {
        'is_base': True,
        })
