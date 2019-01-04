# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError


class SdICase(TransactionCase):

    def setUp(self):
        super(SdICase, self).setUp()
        self.sdi_model = self.env['sdi.channel']
        self.mail_pec_server = self.env['ir.mail_server'].create({
            'name': 'Pec mail',
            'is_fatturapa_pec': True,
            'email_from_for_fatturaPA': 'test@test.it',
            'smtp_host': 'smtp.host',
        })

    def test_create_sdi_channel(self):
        with self.assertRaises(ValidationError) as e:
            self.sdi_model.create({
                'name': 'Sdi Channel',
                'channel_type': 'pec',
                'pec_server_id': self.mail_pec_server.id,
                'email_exchange_system': 'test%pec.it'
            })
        self.assertEqual(e.exception.message,
                         "Email test%pec.it is not valid")
