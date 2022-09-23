import logging
import re
import urllib.parse
from collections.abc import MutableMapping
from datetime import datetime

from lxml import etree

from odoo.addons.l10n_it_account.tools.account_tools import fpa_schema, fpa_schema_etree

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

_root = fpa_schema_etree()

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

    Un altro esempio reale sono spazi lasciati nell'URL del namespace:
    anche in questo caso l'URL non è corretto, per cui procediamo
    a fare l'encoding.
    """

    xml_string = xml_string.decode()
    # HACK#1 - url invalido
    # xmlns:ds="http://www.w3.org/2000/09/xmldsig#&quot;"
    xml_string = re.sub(
        r'xmlns:ds="http://www.w3.org/2000/09/xmldsig([^"]*)"',
        'xmlns:ds="http://www.w3.org/2000/09/xmldsig#"',
        xml_string,
    )
    # xmlns:ds='http://www.w3.org/2000/09/xmldsig#&quot;'
    xml_string = re.sub(
        r"xmlns:ds='http://www.w3.org/2000/09/xmldsig([^']*)'",
        "xmlns:ds='http://www.w3.org/2000/09/xmldsig#'",
        xml_string,
    )
    # xmlns:schemaLocation="http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2 fatturaordinaria_v1.2.xsd" # noqa: B950
    xml_string = re.sub(
        r"xmlns:(\S*?)=(\"|')([^\"']*?)(\"|')",
        lambda m: "xmlns:{}={}{}{}".format(
            m.group(1),
            m.group(2),
            urllib.parse.quote(m.group(3), safe="/:#"),
            m.group(4),
        ),
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

    validat = fpa_schema.to_dict(tree, dict_class=ObjectDict)
    validat._xmldoctor = problems
    return validat


collect_types()
