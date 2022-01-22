#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#

from odoo import models, fields, api


class AccountTax(models.Model):
    _inherit = 'account.tax'

    def check_rc(self):
        value = ''
        if self.kind_id:
            if self.kind_id.code.startswith('N3'):
                if self.kind_id.code != 'N3.5':
                    value = 'local'
                # end if
            elif self.kind_id.code.startswith('N6'):
                value = 'self'
            # end if
        # end if

        return value
    # end check_rc


