import logging
from odoo.modules.module import get_module_resource
from lxml import etree

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

try:
    import pyxb.binding
except (ImportError) as err:
    _logger.debug(err)

from .binding import *  # noqa: F403

XSD_SCHEMA = 'Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd'

_xsd_schema = get_module_resource('l10n_it_fatturapa', 'bindings', 'xsd',
                                  XSD_SCHEMA)
_root = etree.parse(_xsd_schema)

_CreateFromDocument = CreateFromDocument  # noqa: F405

date_types = {}
datetime_types = {}


def get_parent_element(e):
    for ancestor in e.iterancestors():
        if 'name' in ancestor.attrib:
            return ancestor


def get_type_query(e):
    return "//*[@type='%s']" % e.attrib['name']


def collect_element(target, element, parent=None):
    if parent is None:
        parent = get_parent_element(element)

    path = '//%s/%s' % (parent.attrib['name'], element.attrib['name'])
    mandatory = element.attrib.get('minOccurs') != '0'
    if path not in target:
        target[path] = mandatory
    else:
        assert target[path] == mandatory, \
            'Element %s is already present with different minOccurs value' % \
            path


def collect_elements_by_type_query(target, query):
    for element in _root.xpath(query):
        parent_type = get_parent_element(element)
        for parent in _root.xpath(get_type_query(parent_type)):
            collect_element(target, element, parent)


def collect_elements_by_type(target, element_type):
    collect_elements_by_type_query(target, get_type_query(element_type))


def collect_types():
    # simpleType, we look at the base of restriction
    for element_type in _root.findall('//{*}simpleType'):
        base = element_type.find('{*}restriction').attrib['base']

        if base == 'xs:date':
            collect_elements_by_type(date_types, element_type)
        elif base == 'xs:dateTime':
            collect_elements_by_type(datetime_types, element_type)

    # complexType containing xs:date children
    collect_elements_by_type_query(date_types, "//*[@type='xs:date']")

    # complexType containing xs:dateTime children
    collect_elements_by_type_query(datetime_types, "//*[@type='xs:dateTime']")


def CreateFromDocument(xml_string):
    try:
        root = etree.fromstring(xml_string)
    except Exception as e:
        _logger.warn('lxml was unable to parse xml: %s' % e)
        return _CreateFromDocument(xml_string)

    problems = []
    tree = etree.ElementTree(root)

    # remove timezone from type `xs:date` if any or
    # pyxb will fail to compare with
    for path, mandatory in date_types.items():
        for element in root.xpath(path):
            result = pyxb.binding.datatypes.date(element.text.strip())
            if result.tzinfo is not None:
                result = result.replace(tzinfo=None)
                element.text = result.XsdLiteral(result)
                msg = 'removed timezone information from date only element ' \
                      '%s: %s' % (tree.getpath(element), element.text)
                problems.append(msg)
                _logger.warn(msg)

    # remove bogus dates accepted by ADE but not by python
    for path, mandatory in datetime_types.items():
        for element in root.xpath(path):
            try:
                pyxb.binding.datatypes.dateTime(element.text)
            except OverflowError as e:
                element_path = tree.getpath(element)
                if mandatory:
                    _logger.error('element %s is invalid but is mandatory: '
                                  '%s' % (element_path, element.text))
                else:
                    element.getparent().remove(element)
                    msg = 'removed invalid dateTime element %s: %s (%s)' % (
                        element_path, element.text, e)
                    problems.append(msg)
                    _logger.warn(msg)

    # fix trailing spaces in <PECDestinatario/> and <Email/>
    for pec in root.xpath("//PECDestinatario"):
        pec.text = pec.text.strip()

    for email in root.xpath("//Email"):
        email.text = email.text.strip()

    fatturapa = _CreateFromDocument(etree.tostring(root))
    setattr(fatturapa, '_xmldoctor', problems)
    return fatturapa


collect_types()
