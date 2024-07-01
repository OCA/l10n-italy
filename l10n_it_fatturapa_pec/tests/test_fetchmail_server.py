from odoo.tests import tagged

from .e_invoice_common import EInvoiceCommon


@tagged("post_install", "-at_install")
class TestFetchmailPECServer(EInvoiceCommon):
    def setUp(self):
        super(TestFetchmailPECServer, self).setUp()
        self.PEC_server = self._create_fetchmail_pec_server()

    def test_fetch_mail(self):
        self.assertEqual(self.PEC_server.pec_error_count, 0)
        self.assertEqual(self.PEC_server.lock_on_max_pec_error_count, True)
