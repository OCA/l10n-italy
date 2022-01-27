#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#

from odoo import models, fields


class AccountFiscalyear(models.Model):
    _inherit = "account.fiscal.year"

    state = fields.Selection([('draft', 'Open'),
                              ('done', 'Closed')],
                             'Status', copy=False,
                             default='draft')
