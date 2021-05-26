import logging
import re
from collections.abc import MutableMapping
from datetime import datetime

import xmlschema
from lxml import etree

from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

# XMLSchema del SdI
# Contiene un riferimento ad un'antica spec di xmldsig-core-schema.xsd, non presente
# nei vari XML Catalog recenti, es. sulla mia Fedora 33
# $ fgrep xmldsig-core-schema.xsd /etc/xml/catalog
#   <system systemId="http://www.w3.org/TR/xmldsig-core/xmldsig-core-schema.xsd" uri="file:///usr/share/xml/xmldsig-core-schema.xsd"/> # noqa: B950
#   <uri name="http://www.w3.org/TR/xmldsig-core/xmldsig-core-schema.xsd" uri="file:///usr/share/xml/xmldsig-core-schema.xsd"/> # noqa: B950
# L'assenza dell'entry nel Catalog fa sì che il documento venga scaricato
# ogni volta, e - a giudicare dalla lentezza nella risposta - qualcuno
# al w3.org ha notato la cosa (la lentezza è relativa a quel solo URL).
#
# Noi interpretiamo lo Schema due volte, per lxml, per le correzioni
# pre-verifica, e successivamente per xmlschema. Entrambe le librerie hanno
# modalità di modificare il comportamento di download delle import esterne.
# Il file xmldsig-core-schema.xsd locale è ottenuto dall'URL indicato dal SdI.
# Per lxml.etree, va creata al classe Resover. Per xmlschema, si indicano
# le locations aggiuntive.

_XSD_SCHEMA = "Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd"
_xml_schema_1_2_1 = get_module_resource("l10n_it_fatturapa", "data", "xsd", _XSD_SCHEMA)
_old_xsd_specs = get_module_resource(
    "l10n_it_fatturapa", "data", "xsd", "xmldsig-core-schema.xsd"
)

_logger = logging.getLogger(__name__)


def _schema_parse():
    # fix <xs:import namespace="http://www.w3.org/2000/09/xmldsig#"
    #      schemaLocation="http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd" /> # noqa: B950
    class VeryOldXSDSpecResolverTYVMSdI(etree.Resolver):
        def resolve(self, system_url, public_id, context):
            if (
                system_url
                == "http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd"  # noqa: B950
            ):
                _logger.info(
                    "mapping URL for %r to local file %r",
                    system_url,
                    _old_xsd_specs,
                )
                return self.resolve_filename(self._old_xsd_specs, context)
            else:
                return super().resolve(system_url, public_id, context)

    parser = etree.XMLParser()
    parser.resolvers.add(VeryOldXSDSpecResolverTYVMSdI())
    return etree.parse(_xml_schema_1_2_1, parser)


_root = _schema_parse()

date_types = {}
datetime_types = {}


def get_parent_element(e):
    for ancestor in e.iterancestors():
        if "name" in ancestor.attrib:
            return ancestor


def get_type_query(e):
    return "//*[@type='%s']" % e.attrib["name"]


def collect_element(target, element, parent=None):
    if parent is None:
        parent = get_parent_element(element)

    path = "//{}/{}".format(parent.attrib["name"], element.attrib["name"])
    mandatory = element.attrib.get("minOccurs") != "0"
    if path not in target:
        target[path] = mandatory
    else:
        assert target[path] == mandatory, (
            "Element %s is already present with different minOccurs value" % path
        )


def collect_elements_by_type_query(target, query):
    for element in _root.xpath(query):
        parent_type = get_parent_element(element)
        for parent in _root.xpath(get_type_query(parent_type)):
            collect_element(target, element, parent)


def collect_elements_by_type(target, element_type):
    collect_elements_by_type_query(target, get_type_query(element_type))


def collect_types():
    # simpleType, we look at the base of restriction
    for element_type in _root.findall("//{*}simpleType"):
        base = element_type.find("{*}restriction").attrib["base"]

        if base == "xs:date":
            collect_elements_by_type(date_types, element_type)
        elif base == "xs:dateTime":
            collect_elements_by_type(datetime_types, element_type)

    # complexType containing xs:date children
    collect_elements_by_type_query(date_types, "//*[@type='xs:date']")

    # complexType containing xs:dateTime children
    collect_elements_by_type_query(datetime_types, "//*[@type='xs:dateTime']")


def parse_datetime(s):
    m = re.match(r"(.*?)(\+|-)(\d+):(\d+)", s)
    if m:
        s = "".join(m.group(1, 2, 3, 4))
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f%z")


def _fix_xmlstring(xml_string):
    """Possono arrivare dallo SdI URL con entity/caratteri aggiuntivi,
    tronchiamo all'URL corretto.

    Sulla sintassi, il W3.org dice:
      In general, however, users should assume that the namespace URI is
      simply a name, not the address of a document on the Web.
    Tuttavia, in questo caso, non è un namespace name deciso arbitrariamente
    dall'utente che ha generato l'XML, ma uno specifico URI,
    http://www.w3.org/2000/09/xmldsig, perché quello è il namespace previsto
    dalle specifiche, anche se il software dell SdI non fa la verifica
    dell'URI.

    Il controllo effettuato è che l'URI che arriva inizi per
    http://www.w3.org/2000/09/xmldsig, e si tronca il resto.

    HACK2: 0.0000000 rappresentato come 0E-7 da decimal.Decimal
    """

    # xmlns:ds="http://www.w3.org/2000/09/xmldsig#&quot;"
    xml_string = xml_string.decode()
    # HACK#1 - url invalido
    xml_string = re.sub(
        r'xmlns:ds="http://www.w3.org/2000/09/xmldsig([^"]*)"',
        'xmlns:ds="http://www.w3.org/2000/09/xmldsig#"',
        xml_string,
    )
    xml_string = re.sub(
        r"xmlns:ds='http://www.w3.org/2000/09/xmldsig([^']*)'",
        "xmlns:ds='http://www.w3.org/2000/09/xmldsig#'",
        xml_string,
    )
    return xml_string.encode()


def CreateFromDocument(xml_string):  # noqa: C901
    # il codice seguente rimpiazza fatturapa.CreateFromDocument(xml_string)
    class ObjectDict(MutableMapping):
        def __getattr__(self, attr):
            try:
                return getattr(self.__dict__, attr)
            except AttributeError:
                return None

        def __getitem__(self, *attr, **kwattr):
            return self.__dict__.__getitem__(*attr, **kwattr)

        def __setitem__(self, *attr, **kwattr):
            return self.__dict__.__setitem__(*attr, **kwattr)

        def __delitem__(self, *attr, **kwattr):
            return self.__dict__.__delitem__(*attr, **kwattr)

        def __iter__(self, *attr, **kwattr):
            return self.__dict__.__iter__(*attr, **kwattr)

        def __len__(self, *attr, **kwattr):
            return self.__dict__.__len__(*attr, **kwattr)

    # TODO: crearlo una tantum?
    validator = xmlschema.XMLSchema(
        _xml_schema_1_2_1,
        locations={"http://www.w3.org/2000/09/xmldsig#": _old_xsd_specs},
    )

    xml_string = _fix_xmlstring(xml_string)
    root = etree.fromstring(xml_string)

    problems = []
    tree = etree.ElementTree(root)

    # remove timezone from type `xs:date` if any or
    # pyxb will fail to compare with
    for path, _mandatory in date_types.items():
        for element in root.xpath(path):
            result = element.text.strip()
            if len(result) > 10:
                msg = (
                    "removed timezone information from date only element "
                    "%s: %s" % (tree.getpath(element), element.text)
                )
                problems.append(msg)
            element.text = result[:10]

    # remove bogus dates accepted by ADE but not by python
    for path, mandatory in datetime_types.items():
        for element in root.xpath(path):
            try:
                d = parse_datetime(element.text)
                if d < parse_datetime("1970-01-01T00:00:00.000+0000"):
                    raise ValueError
            except Exception as e:
                element_path = tree.getpath(element)
                if mandatory:
                    _logger.error(
                        "element %s is invalid but is mandatory: "
                        "%s" % (element_path, element.text)
                    )
                else:
                    element.getparent().remove(element)
                    msg = "removed invalid dateTime element {}: {} ({})".format(
                        element_path,
                        element.text,
                        e,
                    )
                    problems.append(msg)
                    _logger.warning(msg)

    # fix trailing spaces in <PECDestinatario/>
    for pec in root.xpath("//PECDestinatario"):
        pec.text = pec.text.rstrip()

    validat = validator.to_dict(tree, dict_class=ObjectDict)
    validat._xmldoctor = problems
    return validat


collect_types()
