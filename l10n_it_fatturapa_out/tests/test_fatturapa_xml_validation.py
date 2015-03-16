# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Davide Corio <davide.corio@lsweb.it>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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

import base64
import tempfile
import netsvc
import openerp.tests.common as test_common
from openerp import addons
from lxml import etree
from io import BytesIO


class TestFatturaPAXMLValidation(test_common.SingleTransactionCase):

    def getFile(self, filename):
        path = addons.get_module_resource('l10n_it_fatturapa_out',
                                          'tests', 'data', filename)
        with open(path) as test_data:
            with tempfile.TemporaryFile() as out:
                base64.encode(test_data, out)
                out.seek(0)
                return path, out.read()

    def setUp(self):
        super(TestFatturaPAXMLValidation, self).setUp()
        self.wizard_model = self.registry('wizard.export.fatturapa')
        self.data_model = self.registry('ir.model.data')
        self.attach_model = self.registry('fatturapa.attachment.out')

    def tearDown(self):
        super(TestFatturaPAXMLValidation, self).tearDown()

    def test_01_xml_export(self):
        cr, uid = self.cr, self.uid

        invoice_id = self.data_model.get_object_reference(
            cr, uid, 'l10n_it_fatturapa', 'fatturapa_invoice_0')
        if invoice_id:
            invoice_id = invoice_id and invoice_id[1] or False

        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(
            uid, 'account.invoice', invoice_id, 'invoice_open', cr)

        wizard_id = self.wizard_model.create(cr, uid, {})
        res = self.wizard_model.exportFatturaPA(
            cr, uid, wizard_id, context={'active_ids': [invoice_id]})

        self.assertTrue(res, 'Export failed.')
        attachment = self.attach_model.browse(cr, uid, res['res_id'])

        # XML doc to be validated
        xml_content = attachment.datas.decode('base64')

        # We need to use a local schema file since lxml fails trying
        # to import remote resource
        dsig_url = "http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/\
xmldsig-core-schema.xsd"
        dsig_path, dsig_data = self.getFile('xmldsig-core-schema.xsd')

        # Replacing remote resource url with local path
        xsd_path, xsd_data = self.getFile('fatturapa_v1.0.xsd')
        xsd_content = xsd_data.decode('base64').decode('utf8')
        xsd_content = xsd_content.replace(dsig_url, dsig_path)

        xsd_tree = etree.parse(BytesIO(xsd_content.encode('utf8')))
        schema = etree.XMLSchema(xsd_tree)
        validation = schema.validate(etree.parse(BytesIO(xml_content)))
        self.assertTrue(validation, 'FatturaPA XML file not valid')
