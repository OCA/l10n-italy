# Copyright 2018-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# Contributions to development, thanks to:
# * Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
#
# from past.builtins import long
# Copyright 2022 powERP enterprise network <https://www.powerp.it>
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/12.0/legal/licenses/licenses.html#odoo-apps).
#

import logging

from z0bug_odoo import test_common

_logger = logging.getLogger(__name__)


class TestPaymentMethod(test_common.SingleTransactionCase):

    PAY_METH_CODE = 'Test-01'
    PAY_METH_NAME = 'Test this module'
    PAY_METH_TYPE = 'inbound'
    PAY_METH_ALTER_NAME = 'Test module itself'

    def setUp(self):
        super(TestPaymentMethod, self).setUp()

    def test_payment_method(self):
        model_name = 'account.payment.method'
        vals = {
            'code': self.PAY_METH_CODE,
            'name': self.PAY_METH_NAME,
            'payment_type': self.PAY_METH_TYPE,
        }
        # Test the <create> function
        self.payment_method_id = self.create_id(
            model_name, vals)
        # Now test the <browse> function
        rec = self.browse_rec(model_name, self.payment_method_id)
        self.assertEqual(rec.name, self.PAY_METH_NAME)
        self.assertEqual(rec.payment_type, self.PAY_METH_TYPE)
        # Now test the <write_rec> functon
        self.write_rec(model_name, self.payment_method_id,
                      {'name': self.PAY_METH_ALTER_NAME})
        rec = self.browse_rec(model_name, self.payment_method_id)
        self.assertEqual(rec.name, self.PAY_METH_ALTER_NAME)
        self.assertEqual(rec.payment_type, self.PAY_METH_TYPE)
        _logger.info(
            'Test %s SUCCESSFULLY ended.' % __file__)
