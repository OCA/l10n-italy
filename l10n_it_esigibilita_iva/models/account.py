# -*- coding: utf-8 -*-

from openerp.osv import orm, fields


class AccountTax(orm.Model):
    _inherit = 'account.tax'

    _columns = {
        'payability': fields.selection([
            ('I', 'Immediate payability'),
            ('D', 'Deferred payability'),
            ('S', 'Split payment'),
        ], string="VAT payability")
    }
