from lxml import etree

from odoo.tests.common import TransactionCase

from ..wizard.efattura import _fix_xmlstring


class TestFixBadURIs(TransactionCase):
    def test_fix_bad_uris(self):
        bad_strings = [
            b'<FatturaElettronica xmlns:ds="http://www.w3.org/2000/09/xmldsig#&quot;"/>',
            b"<FatturaElettronica xmlns:ds='http://www.w3.org/2000/09/xmldsig#&quot;'/>",
            b'<FatturaElettronica xmlns:schemaLocation="http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2 fatturaordinaria_v1.2.xsd"/>',  # noqa: B950
        ]
        for bad_string in bad_strings:
            with self.assertRaises(etree.XMLSyntaxError):
                # parsing fails
                x = etree.fromstring(bad_string)
            fixed_string = _fix_xmlstring(bad_string)
            x = etree.fromstring(fixed_string)
            # parsing succeeds
            self.assertTrue(x.tag, "FatturaElettronica")
