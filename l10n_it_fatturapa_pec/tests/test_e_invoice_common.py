# -*- coding: utf-8 -*-
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.l10n_it_fatturapa_pec.tests.e_invoice_common \
    import EInvoiceCommon


class TestEInvoiceCommon(EInvoiceCommon):

    def setUp(self):
        super(TestEInvoiceCommon, self).setUp()

    def test_unlink(self):
        """Deleting ready invoice"""
        e_invoice = self._create_e_invoice()
        e_invoice.unlink()
        self.assertFalse(e_invoice.exists())
