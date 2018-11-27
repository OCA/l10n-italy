# ./_cm.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:6d05a298a781c71d177aab761a79c5e637d7f467
# Generated 2018-11-22 12:18:13.668082 by PyXB version 1.2.5 using Python 2.7.15.candidate.1
# Namespace urn:www.agenziaentrate.gov.it:specificheTecniche:common [xmlns:cm]

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:7c714a02-793b-11e7-afb3-b05adae3c683')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.5'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('urn:www.agenziaentrate.gov.it:specificheTecniche:common', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}Identificativo_Type
class Identificativo_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Identificativo_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/fornitura_v3.xsd', 27, 1)
    _Documentation = None
Identificativo_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
Identificativo_Type._CF_pattern.addPattern(pattern='[0-9]{4}[1-9]|[0-9]{3}[1-9][0-9]|[0-9]{2}[1-9][0-9]{2}|[0-9][1-9][0-9]{3}|[1-9][0-9]{4}')
Identificativo_Type._InitializeFacetMap(Identificativo_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'Identificativo_Type', Identificativo_Type)
_module_typeBindings.Identificativo_Type = Identificativo_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoAN_Type
class DatoAN_Type (pyxb.binding.datatypes.string):

    """Tipo semplice costituito da caratteri alfanumerici maiuscoli e dai caratteri: punto, virgola, apice, trattino, spazio, barra semplice, °, ^, ampersand, parentesi aperta e chiusa, doppie virgolette, barra rovesciata, la barra dritta, il più, le maiuscole accentate e la Ü. Tali caratteri non sono ammesi come primo carattere tranne: i numeri da 0 a 9, i caratteri maiuscoli da A a Z, il meno e le dopppie virgolette."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoAN_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 15, 1)
    _Documentation = 'Tipo semplice costituito da caratteri alfanumerici maiuscoli e dai caratteri: punto, virgola, apice, trattino, spazio, barra semplice, \xb0, ^, ampersand, parentesi aperta e chiusa, doppie virgolette, barra rovesciata, la barra dritta, il pi\xf9, le maiuscole accentate e la \xdc. Tali caratteri non sono ammesi come primo carattere tranne: i numeri da 0 a 9, i caratteri maiuscoli da A a Z, il meno e le dopppie virgolette.'
DatoAN_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoAN_Type._CF_pattern.addPattern(pattern='([0-9A-Z\\-]|"){1}([ 0-9A-Z&]|\'|\\-|\\.|,|/|\xb0|\\^|\\(|\\)|\xc0|\xc8|\xc9|\xcc|\xd2|\xd9|\xdc|"|\\\\|\\||\\+)*')
DatoAN_Type._InitializeFacetMap(DatoAN_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoAN_Type', DatoAN_Type)
_module_typeBindings.DatoAN_Type = DatoAN_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoNU_Type
class DatoNU_Type (pyxb.binding.datatypes.string):

    """Tipo semplice che identifica numeri naturali positivi e negativi con al massimo 16 cifre."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoNU_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 23, 1)
    _Documentation = 'Tipo semplice che identifica numeri naturali positivi e negativi con al massimo 16 cifre.'
DatoNU_Type._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(16))
DatoNU_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoNU_Type._CF_pattern.addPattern(pattern='(\\-[1-9]|[1-9])[0-9]*')
DatoNU_Type._InitializeFacetMap(DatoNU_Type._CF_maxLength,
   DatoNU_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoNU_Type', DatoNU_Type)
_module_typeBindings.DatoNU_Type = DatoNU_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoPC_Type
class DatoPC_Type (pyxb.binding.datatypes.string):

    """Tipo semplice che esprime una percentuale e dunque consente valori positivi non superiori a 100, con al massimo 2 cifre decimali. Il separatore decimale previsto è la virgola."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoPC_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 32, 1)
    _Documentation = 'Tipo semplice che esprime una percentuale e dunque consente valori positivi non superiori a 100, con al massimo 2 cifre decimali. Il separatore decimale previsto \xe8 la virgola.'
DatoPC_Type._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(16))
DatoPC_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoPC_Type._CF_pattern.addPattern(pattern='[0-9]?[0-9](,\\d{1,3})?|100(,0{1,3})?')
DatoPC_Type._InitializeFacetMap(DatoPC_Type._CF_maxLength,
   DatoPC_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoPC_Type', DatoPC_Type)
_module_typeBindings.DatoPC_Type = DatoPC_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoQU_Type
class DatoQU_Type (pyxb.binding.datatypes.string):

    """Tipo semplice che identifica numeri positivi con al massimo 5 cifre decimali. La lunghezza massima prevista è di 16 caratteri, il separatore decimale previsto è la virgola."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoQU_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 41, 1)
    _Documentation = 'Tipo semplice che identifica numeri positivi con al massimo 5 cifre decimali. La lunghezza massima prevista \xe8 di 16 caratteri, il separatore decimale previsto \xe8 la virgola.'
DatoQU_Type._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(16))
DatoQU_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoQU_Type._CF_pattern.addPattern(pattern='[0-9]+(,[0-9]{1,5})?')
DatoQU_Type._InitializeFacetMap(DatoQU_Type._CF_maxLength,
   DatoQU_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoQU_Type', DatoQU_Type)
_module_typeBindings.DatoQU_Type = DatoQU_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoVP_Type
class DatoVP_Type (pyxb.binding.datatypes.string):

    """Tipo semplice che identifica numeri positivi con 2 cifre decimali. La lunghezza massima prevista è di 16 caratteri, il separatore decimale previsto è la virgola."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoVP_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 50, 1)
    _Documentation = 'Tipo semplice che identifica numeri positivi con 2 cifre decimali. La lunghezza massima prevista \xe8 di 16 caratteri, il separatore decimale previsto \xe8 la virgola.'
DatoVP_Type._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(16))
DatoVP_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoVP_Type._CF_pattern.addPattern(pattern='[0-9]+,[0-9]{2}')
DatoVP_Type._InitializeFacetMap(DatoVP_Type._CF_maxLength,
   DatoVP_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoVP_Type', DatoVP_Type)
_module_typeBindings.DatoVP_Type = DatoVP_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoN1_Type
class DatoN1_Type (pyxb.binding.datatypes.string):

    """Tipo semplice che identifica i numeri naturali da 1 a 9."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoN1_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 59, 1)
    _Documentation = 'Tipo semplice che identifica i numeri naturali da 1 a 9.'
DatoN1_Type._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
DatoN1_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoN1_Type._CF_pattern.addPattern(pattern='[1-9]')
DatoN1_Type._InitializeFacetMap(DatoN1_Type._CF_maxLength,
   DatoN1_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoN1_Type', DatoN1_Type)
_module_typeBindings.DatoN1_Type = DatoN1_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoNP_Type
class DatoNP_Type (pyxb.binding.datatypes.string):

    """Tipo semplice che identifica numeri naturali positivi con al massimo 16 cifre."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoNP_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 68, 1)
    _Documentation = 'Tipo semplice che identifica numeri naturali positivi con al massimo 16 cifre.'
DatoNP_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoNP_Type._CF_pattern.addPattern(pattern='[1-9]{1}[0-9]*')
DatoNP_Type._InitializeFacetMap(DatoNP_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoNP_Type', DatoNP_Type)
_module_typeBindings.DatoNP_Type = DatoNP_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoPI_Type
class DatoPI_Type (pyxb.binding.datatypes.string):

    """Tipo semplice che identifica la partita IVA rispettandone i vincoli di struttura. """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoPI_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 76, 1)
    _Documentation = 'Tipo semplice che identifica la partita IVA rispettandone i vincoli di struttura. '
DatoPI_Type._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(11))
DatoPI_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoPI_Type._CF_pattern.addPattern(pattern='[0-7][0-9]{10}')
DatoPI_Type._InitializeFacetMap(DatoPI_Type._CF_length,
   DatoPI_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoPI_Type', DatoPI_Type)
_module_typeBindings.DatoPI_Type = DatoPI_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoCN_Type
class DatoCN_Type (pyxb.binding.datatypes.string):

    """Tipo semplice che identifica un codice fiscale numerico rispettandone i vincoli di struttura."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoCN_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 85, 1)
    _Documentation = 'Tipo semplice che identifica un codice fiscale numerico rispettandone i vincoli di struttura.'
DatoCN_Type._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(11))
DatoCN_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoCN_Type._CF_pattern.addPattern(pattern='[0-9]{11}')
DatoCN_Type._InitializeFacetMap(DatoCN_Type._CF_length,
   DatoCN_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoCN_Type', DatoCN_Type)
_module_typeBindings.DatoCN_Type = DatoCN_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoCF_Type
class DatoCF_Type (pyxb.binding.datatypes.string):

    """Tipo semplice che identifica un codice fiscale provvisorio o alfanumerico rispettandone i vincoli di struttura."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoCF_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 94, 1)
    _Documentation = 'Tipo semplice che identifica un codice fiscale provvisorio o alfanumerico rispettandone i vincoli di struttura.'
DatoCF_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoCF_Type._CF_pattern.addPattern(pattern='[0-9]{11}|[A-Z]{6}[0-9LMNPQRSTUV]{2}[A-Z]{1}[0-9LMNPQRSTUV]{2}[A-Z]{1}[0-9LMNPQRSTUV]{3}[A-Z]{1}')
DatoCF_Type._InitializeFacetMap(DatoCF_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoCF_Type', DatoCF_Type)
_module_typeBindings.DatoCF_Type = DatoCF_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoCB_Type
class DatoCB_Type (pyxb.binding.datatypes.byte):

    """Tipo semplice che consente esclusivamente i valori 0 e 1."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoCB_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 102, 1)
    _Documentation = 'Tipo semplice che consente esclusivamente i valori 0 e 1.'
DatoCB_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoCB_Type._CF_pattern.addPattern(pattern='[01]')
DatoCB_Type._InitializeFacetMap(DatoCB_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoCB_Type', DatoCB_Type)
_module_typeBindings.DatoCB_Type = DatoCB_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoCB12_Type
class DatoCB12_Type (pyxb.binding.datatypes.byte):

    """Tipo semplice che consente esclusivamente 12 caratteri con i valori 0 e 1."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoCB12_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 110, 1)
    _Documentation = 'Tipo semplice che consente esclusivamente 12 caratteri con i valori 0 e 1.'
DatoCB12_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoCB12_Type._CF_pattern.addPattern(pattern='[10]{12}')
DatoCB12_Type._InitializeFacetMap(DatoCB12_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoCB12_Type', DatoCB12_Type)
_module_typeBindings.DatoCB12_Type = DatoCB12_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoDT_Type
class DatoDT_Type (pyxb.binding.datatypes.string):

    """Tipo semplice che identifica una data nel formato ggmmaaaa. La data indicata non deve essere successiva alla data corrente."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoDT_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 118, 1)
    _Documentation = 'Tipo semplice che identifica una data nel formato ggmmaaaa. La data indicata non deve essere successiva alla data corrente.'
DatoDT_Type._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(8))
DatoDT_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoDT_Type._CF_pattern.addPattern(pattern='(((0[1-9]|[12][0-9]|3[01])(0[13578]|10|12)(\\d{4}))|(([0][1-9]|[12][0-9]|30)(0[469]|11)(\\d{4}))|((0[1-9]|1[0-9]|2[0-8])(02)(\\d{4}))|((29)(02)([02468][048]00))|((29)(02)([13579][26]00))|((29)(02)([0-9][0-9][0][48]))|((29)(02)([0-9][0-9][2468][048]))|((29)(02)([0-9][0-9][13579][26])))')
DatoDT_Type._InitializeFacetMap(DatoDT_Type._CF_length,
   DatoDT_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoDT_Type', DatoDT_Type)
_module_typeBindings.DatoDT_Type = DatoDT_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoDA_Type
class DatoDA_Type (pyxb.binding.datatypes.string):

    """Tipo semplice che identifica un anno nel formato aaaa. Sono ammessi anni dal 1800 al 2099."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoDA_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 127, 1)
    _Documentation = 'Tipo semplice che identifica un anno nel formato aaaa. Sono ammessi anni dal 1800 al 2099.'
DatoDA_Type._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(4))
DatoDA_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoDA_Type._CF_pattern.addPattern(pattern='(18|19|20)[0-9]{2}')
DatoDA_Type._InitializeFacetMap(DatoDA_Type._CF_length,
   DatoDA_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoDA_Type', DatoDA_Type)
_module_typeBindings.DatoDA_Type = DatoDA_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoDN_Type
class DatoDN_Type (pyxb.binding.datatypes.string):

    """Tipo semplice che identifica una data nel formato ggmmaaaa."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoDN_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 136, 1)
    _Documentation = 'Tipo semplice che identifica una data nel formato ggmmaaaa.'
DatoDN_Type._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(8))
DatoDN_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoDN_Type._CF_pattern.addPattern(pattern='(((0[1-9]|[12][0-9]|3[01])(0[13578]|10|12)(\\d{4}))|(([0][1-9]|[12][0-9]|30)(0[469]|11)(\\d{4}))|((0[1-9]|1[0-9]|2[0-8])(02)(\\d{4}))|((29)(02)([02468][048]00))|((29)(02)([13579][26]00))|((29)(02)([0-9][0-9][0][48]))|((29)(02)([0-9][0-9][2468][048]))|((29)(02)([0-9][0-9][13579][26])))')
DatoDN_Type._InitializeFacetMap(DatoDN_Type._CF_length,
   DatoDN_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoDN_Type', DatoDN_Type)
_module_typeBindings.DatoDN_Type = DatoDN_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoD6_Type
class DatoD6_Type (pyxb.binding.datatypes.string):

    """Tipo semplice che identifica una data nel formato mmaaaa."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoD6_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 145, 1)
    _Documentation = 'Tipo semplice che identifica una data nel formato mmaaaa.'
DatoD6_Type._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(6))
DatoD6_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoD6_Type._CF_pattern.addPattern(pattern='((0[0-9])|(1[0-2]))((19|20)[0-9][0-9])')
DatoD6_Type._InitializeFacetMap(DatoD6_Type._CF_length,
   DatoD6_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoD6_Type', DatoD6_Type)
_module_typeBindings.DatoD6_Type = DatoD6_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoEM_Type
class DatoEM_Type (pyxb.binding.datatypes.string):

    """Tipo semplice che identifica un elemento di tipo email"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoEM_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 154, 1)
    _Documentation = 'Tipo semplice che identifica un elemento di tipo email'
DatoEM_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoEM_Type._CF_pattern.addPattern(pattern='[a-zA-Z0-9._%\\-\'"?^~=]+@[a-zA-Z0-9.\\-]+\\.[a-zA-Z]{2,4}')
DatoEM_Type._InitializeFacetMap(DatoEM_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoEM_Type', DatoEM_Type)
_module_typeBindings.DatoEM_Type = DatoEM_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoGA_Type
class DatoGA_Type (pyxb.binding.datatypes.string):

    """Tipo semplice che identifica il numero di giorni in un anno e va da 1 a 365"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoGA_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 162, 1)
    _Documentation = 'Tipo semplice che identifica il numero di giorni in un anno e va da 1 a 365'
DatoGA_Type._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
DatoGA_Type._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(3))
DatoGA_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoGA_Type._CF_pattern.addPattern(pattern='[1-9]|([1-9][0-9])|([12][0-9][0-9])|(3[0-5][0-9])|(36[0-5])')
DatoGA_Type._InitializeFacetMap(DatoGA_Type._CF_minLength,
   DatoGA_Type._CF_maxLength,
   DatoGA_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoGA_Type', DatoGA_Type)
_module_typeBindings.DatoGA_Type = DatoGA_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoTL_Type
class DatoTL_Type (pyxb.binding.datatypes.string):

    """Tipo semplice che identifica un elemento di tipo telefono"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoTL_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 172, 1)
    _Documentation = 'Tipo semplice che identifica un elemento di tipo telefono'
DatoTL_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoTL_Type._CF_pattern.addPattern(pattern='[0-9]*')
DatoTL_Type._InitializeFacetMap(DatoTL_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoTL_Type', DatoTL_Type)
_module_typeBindings.DatoTL_Type = DatoTL_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}DatoCP_Type
class DatoCP_Type (pyxb.binding.datatypes.string):

    """Tipo semplice che identifica un elemento di tipo cap"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoCP_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesDati_v3.xsd', 180, 1)
    _Documentation = 'Tipo semplice che identifica un elemento di tipo cap'
DatoCP_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoCP_Type._CF_pattern.addPattern(pattern='[0-9]{5}')
DatoCP_Type._InitializeFacetMap(DatoCP_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoCP_Type', DatoCP_Type)
_module_typeBindings.DatoCP_Type = DatoCP_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}ProvincieItaliane
class ProvincieItaliane (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """
			Elenco delle provincie italiane in vigore, valori ammessi:
			
				Agrigento				AG
				Alessandria				AL
				Ancona					AN
				Aosta   				AO
				Ascoli Piceno			AP
				L'Aquila				AQ
				Arezzo					AR
				Asti					AT
				Avellino				AV
				Bari					BA
				Bergamo					BG
				Biella					BI
				Belluno					BL
				Benevento				BN
				Bologna					BO
				Brindisi				BR
				Brescia					BS
				Barletta-Andria-Trani	BT
				Bolzano					BZ
				Cagliari				CA
				Campobasso				CB
				Caserta					CE
				Chieti					CH
				Carbonia-Iglessias		CI
				Caltanissetta			CL
				Cuneo					CN
				Como					CO
				Cremona					CR
				Cosenza					CS
				Catania					CT
				Catanzaro				CZ
				Enna					EN
				Forlì-Cesena			FC
				Ferrara					FE
				Foggia					FG
				Firenze					FI
				Fermo					FM
				Frosinone				FR
				Genova					GE
				Gorizia					GO
				Grosseto				GR
				Imperia					IM
				Isernia					IS
				Crotone					KR
				Lecco					LC
				Lecce					LE
				Livorno					LI
				Lodi					LO
				Latina					LT
				Lucca					LU
				Monza e Brianza			MB
				Macerata				MC
				Messina					ME
				Milano					MI
				Mantova					MN
				Modena					MO
				Massa e Carrara			MS
				Matera					MT
				Napoli					NA
				Novara					NO
				Nuoro					NU
				Ogliastra				OG
				Oristano				OR
				Olbia-Tempio			OT
				Palermo					PA
				Piacenza				PC
				Padova					PD
				Pescara					PE
				Perugia					PG
				Pisa					PI
				Pordenone				PN
				Prato					PO
				Parma					PR
				Pistoia					PT
				Pesaro e Urbino			PU
				Pavia					PV
				Potenza					PZ
				Ravenna					RA
				Reggio Calabria			RC
				Reggio Emilia			RE
				Ragusa					RG
				Rieti					RI
				Roma					RM
				Rimini					RN
				Rovigo					RO
				Salerno					SA
				iena					SI
				Sondrio					SO
				La Spezia				SP
				Siracusa				SR
				Sassari					SS
				Savona					SV
				Taranto					TA
				Teramo					TE
				Trento 					TN
				Torino					TO
				Trapani					TP
				Terni					TR
				Trieste					TS
				Treviso					TV
				Udine					UD
				Varese					VA
				Verbano-Cusio-Ossola	VB
				Vercelli				VC
				Venezia					VE
				Vicenza					VI
				Verona					VR
				Medio Campidano			VS
				Viterbo					VT
				Vibo Valentia			VV
			
			"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ProvincieItaliane')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesProvincie_v3.xsd', 30, 1)
    _Documentation = "\n\t\t\tElenco delle provincie italiane in vigore, valori ammessi:\n\t\t\t\n\t\t\t\tAgrigento\t\t\t\tAG\n\t\t\t\tAlessandria\t\t\t\tAL\n\t\t\t\tAncona\t\t\t\t\tAN\n\t\t\t\tAosta   \t\t\t\tAO\n\t\t\t\tAscoli Piceno\t\t\tAP\n\t\t\t\tL'Aquila\t\t\t\tAQ\n\t\t\t\tArezzo\t\t\t\t\tAR\n\t\t\t\tAsti\t\t\t\t\tAT\n\t\t\t\tAvellino\t\t\t\tAV\n\t\t\t\tBari\t\t\t\t\tBA\n\t\t\t\tBergamo\t\t\t\t\tBG\n\t\t\t\tBiella\t\t\t\t\tBI\n\t\t\t\tBelluno\t\t\t\t\tBL\n\t\t\t\tBenevento\t\t\t\tBN\n\t\t\t\tBologna\t\t\t\t\tBO\n\t\t\t\tBrindisi\t\t\t\tBR\n\t\t\t\tBrescia\t\t\t\t\tBS\n\t\t\t\tBarletta-Andria-Trani\tBT\n\t\t\t\tBolzano\t\t\t\t\tBZ\n\t\t\t\tCagliari\t\t\t\tCA\n\t\t\t\tCampobasso\t\t\t\tCB\n\t\t\t\tCaserta\t\t\t\t\tCE\n\t\t\t\tChieti\t\t\t\t\tCH\n\t\t\t\tCarbonia-Iglessias\t\tCI\n\t\t\t\tCaltanissetta\t\t\tCL\n\t\t\t\tCuneo\t\t\t\t\tCN\n\t\t\t\tComo\t\t\t\t\tCO\n\t\t\t\tCremona\t\t\t\t\tCR\n\t\t\t\tCosenza\t\t\t\t\tCS\n\t\t\t\tCatania\t\t\t\t\tCT\n\t\t\t\tCatanzaro\t\t\t\tCZ\n\t\t\t\tEnna\t\t\t\t\tEN\n\t\t\t\tForl\xec-Cesena\t\t\tFC\n\t\t\t\tFerrara\t\t\t\t\tFE\n\t\t\t\tFoggia\t\t\t\t\tFG\n\t\t\t\tFirenze\t\t\t\t\tFI\n\t\t\t\tFermo\t\t\t\t\tFM\n\t\t\t\tFrosinone\t\t\t\tFR\n\t\t\t\tGenova\t\t\t\t\tGE\n\t\t\t\tGorizia\t\t\t\t\tGO\n\t\t\t\tGrosseto\t\t\t\tGR\n\t\t\t\tImperia\t\t\t\t\tIM\n\t\t\t\tIsernia\t\t\t\t\tIS\n\t\t\t\tCrotone\t\t\t\t\tKR\n\t\t\t\tLecco\t\t\t\t\tLC\n\t\t\t\tLecce\t\t\t\t\tLE\n\t\t\t\tLivorno\t\t\t\t\tLI\n\t\t\t\tLodi\t\t\t\t\tLO\n\t\t\t\tLatina\t\t\t\t\tLT\n\t\t\t\tLucca\t\t\t\t\tLU\n\t\t\t\tMonza e Brianza\t\t\tMB\n\t\t\t\tMacerata\t\t\t\tMC\n\t\t\t\tMessina\t\t\t\t\tME\n\t\t\t\tMilano\t\t\t\t\tMI\n\t\t\t\tMantova\t\t\t\t\tMN\n\t\t\t\tModena\t\t\t\t\tMO\n\t\t\t\tMassa e Carrara\t\t\tMS\n\t\t\t\tMatera\t\t\t\t\tMT\n\t\t\t\tNapoli\t\t\t\t\tNA\n\t\t\t\tNovara\t\t\t\t\tNO\n\t\t\t\tNuoro\t\t\t\t\tNU\n\t\t\t\tOgliastra\t\t\t\tOG\n\t\t\t\tOristano\t\t\t\tOR\n\t\t\t\tOlbia-Tempio\t\t\tOT\n\t\t\t\tPalermo\t\t\t\t\tPA\n\t\t\t\tPiacenza\t\t\t\tPC\n\t\t\t\tPadova\t\t\t\t\tPD\n\t\t\t\tPescara\t\t\t\t\tPE\n\t\t\t\tPerugia\t\t\t\t\tPG\n\t\t\t\tPisa\t\t\t\t\tPI\n\t\t\t\tPordenone\t\t\t\tPN\n\t\t\t\tPrato\t\t\t\t\tPO\n\t\t\t\tParma\t\t\t\t\tPR\n\t\t\t\tPistoia\t\t\t\t\tPT\n\t\t\t\tPesaro e Urbino\t\t\tPU\n\t\t\t\tPavia\t\t\t\t\tPV\n\t\t\t\tPotenza\t\t\t\t\tPZ\n\t\t\t\tRavenna\t\t\t\t\tRA\n\t\t\t\tReggio Calabria\t\t\tRC\n\t\t\t\tReggio Emilia\t\t\tRE\n\t\t\t\tRagusa\t\t\t\t\tRG\n\t\t\t\tRieti\t\t\t\t\tRI\n\t\t\t\tRoma\t\t\t\t\tRM\n\t\t\t\tRimini\t\t\t\t\tRN\n\t\t\t\tRovigo\t\t\t\t\tRO\n\t\t\t\tSalerno\t\t\t\t\tSA\n\t\t\t\tiena\t\t\t\t\tSI\n\t\t\t\tSondrio\t\t\t\t\tSO\n\t\t\t\tLa Spezia\t\t\t\tSP\n\t\t\t\tSiracusa\t\t\t\tSR\n\t\t\t\tSassari\t\t\t\t\tSS\n\t\t\t\tSavona\t\t\t\t\tSV\n\t\t\t\tTaranto\t\t\t\t\tTA\n\t\t\t\tTeramo\t\t\t\t\tTE\n\t\t\t\tTrento \t\t\t\t\tTN\n\t\t\t\tTorino\t\t\t\t\tTO\n\t\t\t\tTrapani\t\t\t\t\tTP\n\t\t\t\tTerni\t\t\t\t\tTR\n\t\t\t\tTrieste\t\t\t\t\tTS\n\t\t\t\tTreviso\t\t\t\t\tTV\n\t\t\t\tUdine\t\t\t\t\tUD\n\t\t\t\tVarese\t\t\t\t\tVA\n\t\t\t\tVerbano-Cusio-Ossola\tVB\n\t\t\t\tVercelli\t\t\t\tVC\n\t\t\t\tVenezia\t\t\t\t\tVE\n\t\t\t\tVicenza\t\t\t\t\tVI\n\t\t\t\tVerona\t\t\t\t\tVR\n\t\t\t\tMedio Campidano\t\t\tVS\n\t\t\t\tViterbo\t\t\t\t\tVT\n\t\t\t\tVibo Valentia\t\t\tVV\n\t\t\t\n\t\t\t"
ProvincieItaliane._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=ProvincieItaliane, enum_prefix=None)
ProvincieItaliane.AG = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='AG', tag='AG')
ProvincieItaliane.AL = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='AL', tag='AL')
ProvincieItaliane.AN = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='AN', tag='AN')
ProvincieItaliane.AO = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='AO', tag='AO')
ProvincieItaliane.AP = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='AP', tag='AP')
ProvincieItaliane.AQ = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='AQ', tag='AQ')
ProvincieItaliane.AR = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='AR', tag='AR')
ProvincieItaliane.AT = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='AT', tag='AT')
ProvincieItaliane.AV = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='AV', tag='AV')
ProvincieItaliane.BA = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='BA', tag='BA')
ProvincieItaliane.BG = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='BG', tag='BG')
ProvincieItaliane.BI = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='BI', tag='BI')
ProvincieItaliane.BL = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='BL', tag='BL')
ProvincieItaliane.BN = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='BN', tag='BN')
ProvincieItaliane.BO = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='BO', tag='BO')
ProvincieItaliane.BR = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='BR', tag='BR')
ProvincieItaliane.BS = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='BS', tag='BS')
ProvincieItaliane.BT = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='BT', tag='BT')
ProvincieItaliane.BZ = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='BZ', tag='BZ')
ProvincieItaliane.CA = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='CA', tag='CA')
ProvincieItaliane.CB = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='CB', tag='CB')
ProvincieItaliane.CE = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='CE', tag='CE')
ProvincieItaliane.CH = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='CH', tag='CH')
ProvincieItaliane.CI = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='CI', tag='CI')
ProvincieItaliane.CL = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='CL', tag='CL')
ProvincieItaliane.CN = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='CN', tag='CN')
ProvincieItaliane.CO = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='CO', tag='CO')
ProvincieItaliane.CR = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='CR', tag='CR')
ProvincieItaliane.CS = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='CS', tag='CS')
ProvincieItaliane.CT = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='CT', tag='CT')
ProvincieItaliane.CZ = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='CZ', tag='CZ')
ProvincieItaliane.EN = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='EN', tag='EN')
ProvincieItaliane.FC = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='FC', tag='FC')
ProvincieItaliane.FE = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='FE', tag='FE')
ProvincieItaliane.FG = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='FG', tag='FG')
ProvincieItaliane.FI = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='FI', tag='FI')
ProvincieItaliane.FM = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='FM', tag='FM')
ProvincieItaliane.FR = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='FR', tag='FR')
ProvincieItaliane.GE = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='GE', tag='GE')
ProvincieItaliane.GO = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='GO', tag='GO')
ProvincieItaliane.GR = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='GR', tag='GR')
ProvincieItaliane.IM = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='IM', tag='IM')
ProvincieItaliane.IS = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='IS', tag='IS')
ProvincieItaliane.KR = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='KR', tag='KR')
ProvincieItaliane.LC = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='LC', tag='LC')
ProvincieItaliane.LE = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='LE', tag='LE')
ProvincieItaliane.LI = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='LI', tag='LI')
ProvincieItaliane.LO = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='LO', tag='LO')
ProvincieItaliane.LT = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='LT', tag='LT')
ProvincieItaliane.LU = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='LU', tag='LU')
ProvincieItaliane.MB = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='MB', tag='MB')
ProvincieItaliane.MC = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='MC', tag='MC')
ProvincieItaliane.ME = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='ME', tag='ME')
ProvincieItaliane.MI = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='MI', tag='MI')
ProvincieItaliane.MN = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='MN', tag='MN')
ProvincieItaliane.MO = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='MO', tag='MO')
ProvincieItaliane.MS = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='MS', tag='MS')
ProvincieItaliane.MT = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='MT', tag='MT')
ProvincieItaliane.NA = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='NA', tag='NA')
ProvincieItaliane.NO = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='NO', tag='NO')
ProvincieItaliane.NU = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='NU', tag='NU')
ProvincieItaliane.OG = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='OG', tag='OG')
ProvincieItaliane.OR = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='OR', tag='OR')
ProvincieItaliane.OT = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='OT', tag='OT')
ProvincieItaliane.PA = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='PA', tag='PA')
ProvincieItaliane.PC = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='PC', tag='PC')
ProvincieItaliane.PD = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='PD', tag='PD')
ProvincieItaliane.PE = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='PE', tag='PE')
ProvincieItaliane.PG = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='PG', tag='PG')
ProvincieItaliane.PI = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='PI', tag='PI')
ProvincieItaliane.PN = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='PN', tag='PN')
ProvincieItaliane.PO = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='PO', tag='PO')
ProvincieItaliane.PR = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='PR', tag='PR')
ProvincieItaliane.PT = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='PT', tag='PT')
ProvincieItaliane.PU = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='PU', tag='PU')
ProvincieItaliane.PV = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='PV', tag='PV')
ProvincieItaliane.PZ = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='PZ', tag='PZ')
ProvincieItaliane.RA = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='RA', tag='RA')
ProvincieItaliane.RC = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='RC', tag='RC')
ProvincieItaliane.RE = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='RE', tag='RE')
ProvincieItaliane.RG = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='RG', tag='RG')
ProvincieItaliane.RI = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='RI', tag='RI')
ProvincieItaliane.RM = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='RM', tag='RM')
ProvincieItaliane.RN = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='RN', tag='RN')
ProvincieItaliane.RO = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='RO', tag='RO')
ProvincieItaliane.SA = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='SA', tag='SA')
ProvincieItaliane.SI = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='SI', tag='SI')
ProvincieItaliane.SO = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='SO', tag='SO')
ProvincieItaliane.SP = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='SP', tag='SP')
ProvincieItaliane.SR = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='SR', tag='SR')
ProvincieItaliane.SS = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='SS', tag='SS')
ProvincieItaliane.SV = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='SV', tag='SV')
ProvincieItaliane.TA = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='TA', tag='TA')
ProvincieItaliane.TE = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='TE', tag='TE')
ProvincieItaliane.TN = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='TN', tag='TN')
ProvincieItaliane.TO = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='TO', tag='TO')
ProvincieItaliane.TP = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='TP', tag='TP')
ProvincieItaliane.TR = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='TR', tag='TR')
ProvincieItaliane.TS = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='TS', tag='TS')
ProvincieItaliane.TV = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='TV', tag='TV')
ProvincieItaliane.UD = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='UD', tag='UD')
ProvincieItaliane.VA = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='VA', tag='VA')
ProvincieItaliane.VB = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='VB', tag='VB')
ProvincieItaliane.VC = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='VC', tag='VC')
ProvincieItaliane.VE = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='VE', tag='VE')
ProvincieItaliane.VI = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='VI', tag='VI')
ProvincieItaliane.VR = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='VR', tag='VR')
ProvincieItaliane.VS = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='VS', tag='VS')
ProvincieItaliane.VT = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='VT', tag='VT')
ProvincieItaliane.VV = ProvincieItaliane._CF_enumeration.addEnumeration(unicode_value='VV', tag='VV')
ProvincieItaliane._InitializeFacetMap(ProvincieItaliane._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'ProvincieItaliane', ProvincieItaliane)
_module_typeBindings.ProvincieItaliane = ProvincieItaliane

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}ProvincieCroate
class ProvincieCroate (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ProvincieCroate')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesProvincie_v3.xsd', 261, 1)
    _Documentation = None
ProvincieCroate._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=ProvincieCroate, enum_prefix=None)
ProvincieCroate.FU = ProvincieCroate._CF_enumeration.addEnumeration(unicode_value='FU', tag='FU')
ProvincieCroate.PL = ProvincieCroate._CF_enumeration.addEnumeration(unicode_value='PL', tag='PL')
ProvincieCroate.ZA = ProvincieCroate._CF_enumeration.addEnumeration(unicode_value='ZA', tag='ZA')
ProvincieCroate._InitializeFacetMap(ProvincieCroate._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'ProvincieCroate', ProvincieCroate)
_module_typeBindings.ProvincieCroate = ProvincieCroate

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}Estero
class Estero (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Estero')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesProvincie_v3.xsd', 280, 1)
    _Documentation = None
Estero._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=Estero, enum_prefix=None)
Estero.EE = Estero._CF_enumeration.addEnumeration(unicode_value='EE', tag='EE')
Estero._InitializeFacetMap(Estero._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'Estero', Estero)
_module_typeBindings.Estero = Estero

# Union simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}PR_Type
# superclasses pyxb.binding.datatypes.anySimpleType
class PR_Type (pyxb.binding.basis.STD_union):

    """Tipo semplice costituito dalle sigle delle provincie italiane in vigore."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PR_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesProvincie_v3.xsd', 12, 1)
    _Documentation = 'Tipo semplice costituito dalle sigle delle provincie italiane in vigore.'

    _MemberTypes = ( ProvincieItaliane, )
PR_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
PR_Type._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=PR_Type)
PR_Type.AG = 'AG'                                 # originally ProvincieItaliane.AG
PR_Type.AL = 'AL'                                 # originally ProvincieItaliane.AL
PR_Type.AN = 'AN'                                 # originally ProvincieItaliane.AN
PR_Type.AO = 'AO'                                 # originally ProvincieItaliane.AO
PR_Type.AP = 'AP'                                 # originally ProvincieItaliane.AP
PR_Type.AQ = 'AQ'                                 # originally ProvincieItaliane.AQ
PR_Type.AR = 'AR'                                 # originally ProvincieItaliane.AR
PR_Type.AT = 'AT'                                 # originally ProvincieItaliane.AT
PR_Type.AV = 'AV'                                 # originally ProvincieItaliane.AV
PR_Type.BA = 'BA'                                 # originally ProvincieItaliane.BA
PR_Type.BG = 'BG'                                 # originally ProvincieItaliane.BG
PR_Type.BI = 'BI'                                 # originally ProvincieItaliane.BI
PR_Type.BL = 'BL'                                 # originally ProvincieItaliane.BL
PR_Type.BN = 'BN'                                 # originally ProvincieItaliane.BN
PR_Type.BO = 'BO'                                 # originally ProvincieItaliane.BO
PR_Type.BR = 'BR'                                 # originally ProvincieItaliane.BR
PR_Type.BS = 'BS'                                 # originally ProvincieItaliane.BS
PR_Type.BT = 'BT'                                 # originally ProvincieItaliane.BT
PR_Type.BZ = 'BZ'                                 # originally ProvincieItaliane.BZ
PR_Type.CA = 'CA'                                 # originally ProvincieItaliane.CA
PR_Type.CB = 'CB'                                 # originally ProvincieItaliane.CB
PR_Type.CE = 'CE'                                 # originally ProvincieItaliane.CE
PR_Type.CH = 'CH'                                 # originally ProvincieItaliane.CH
PR_Type.CI = 'CI'                                 # originally ProvincieItaliane.CI
PR_Type.CL = 'CL'                                 # originally ProvincieItaliane.CL
PR_Type.CN = 'CN'                                 # originally ProvincieItaliane.CN
PR_Type.CO = 'CO'                                 # originally ProvincieItaliane.CO
PR_Type.CR = 'CR'                                 # originally ProvincieItaliane.CR
PR_Type.CS = 'CS'                                 # originally ProvincieItaliane.CS
PR_Type.CT = 'CT'                                 # originally ProvincieItaliane.CT
PR_Type.CZ = 'CZ'                                 # originally ProvincieItaliane.CZ
PR_Type.EN = 'EN'                                 # originally ProvincieItaliane.EN
PR_Type.FC = 'FC'                                 # originally ProvincieItaliane.FC
PR_Type.FE = 'FE'                                 # originally ProvincieItaliane.FE
PR_Type.FG = 'FG'                                 # originally ProvincieItaliane.FG
PR_Type.FI = 'FI'                                 # originally ProvincieItaliane.FI
PR_Type.FM = 'FM'                                 # originally ProvincieItaliane.FM
PR_Type.FR = 'FR'                                 # originally ProvincieItaliane.FR
PR_Type.GE = 'GE'                                 # originally ProvincieItaliane.GE
PR_Type.GO = 'GO'                                 # originally ProvincieItaliane.GO
PR_Type.GR = 'GR'                                 # originally ProvincieItaliane.GR
PR_Type.IM = 'IM'                                 # originally ProvincieItaliane.IM
PR_Type.IS = 'IS'                                 # originally ProvincieItaliane.IS
PR_Type.KR = 'KR'                                 # originally ProvincieItaliane.KR
PR_Type.LC = 'LC'                                 # originally ProvincieItaliane.LC
PR_Type.LE = 'LE'                                 # originally ProvincieItaliane.LE
PR_Type.LI = 'LI'                                 # originally ProvincieItaliane.LI
PR_Type.LO = 'LO'                                 # originally ProvincieItaliane.LO
PR_Type.LT = 'LT'                                 # originally ProvincieItaliane.LT
PR_Type.LU = 'LU'                                 # originally ProvincieItaliane.LU
PR_Type.MB = 'MB'                                 # originally ProvincieItaliane.MB
PR_Type.MC = 'MC'                                 # originally ProvincieItaliane.MC
PR_Type.ME = 'ME'                                 # originally ProvincieItaliane.ME
PR_Type.MI = 'MI'                                 # originally ProvincieItaliane.MI
PR_Type.MN = 'MN'                                 # originally ProvincieItaliane.MN
PR_Type.MO = 'MO'                                 # originally ProvincieItaliane.MO
PR_Type.MS = 'MS'                                 # originally ProvincieItaliane.MS
PR_Type.MT = 'MT'                                 # originally ProvincieItaliane.MT
PR_Type.NA = 'NA'                                 # originally ProvincieItaliane.NA
PR_Type.NO = 'NO'                                 # originally ProvincieItaliane.NO
PR_Type.NU = 'NU'                                 # originally ProvincieItaliane.NU
PR_Type.OG = 'OG'                                 # originally ProvincieItaliane.OG
PR_Type.OR = 'OR'                                 # originally ProvincieItaliane.OR
PR_Type.OT = 'OT'                                 # originally ProvincieItaliane.OT
PR_Type.PA = 'PA'                                 # originally ProvincieItaliane.PA
PR_Type.PC = 'PC'                                 # originally ProvincieItaliane.PC
PR_Type.PD = 'PD'                                 # originally ProvincieItaliane.PD
PR_Type.PE = 'PE'                                 # originally ProvincieItaliane.PE
PR_Type.PG = 'PG'                                 # originally ProvincieItaliane.PG
PR_Type.PI = 'PI'                                 # originally ProvincieItaliane.PI
PR_Type.PN = 'PN'                                 # originally ProvincieItaliane.PN
PR_Type.PO = 'PO'                                 # originally ProvincieItaliane.PO
PR_Type.PR = 'PR'                                 # originally ProvincieItaliane.PR
PR_Type.PT = 'PT'                                 # originally ProvincieItaliane.PT
PR_Type.PU = 'PU'                                 # originally ProvincieItaliane.PU
PR_Type.PV = 'PV'                                 # originally ProvincieItaliane.PV
PR_Type.PZ = 'PZ'                                 # originally ProvincieItaliane.PZ
PR_Type.RA = 'RA'                                 # originally ProvincieItaliane.RA
PR_Type.RC = 'RC'                                 # originally ProvincieItaliane.RC
PR_Type.RE = 'RE'                                 # originally ProvincieItaliane.RE
PR_Type.RG = 'RG'                                 # originally ProvincieItaliane.RG
PR_Type.RI = 'RI'                                 # originally ProvincieItaliane.RI
PR_Type.RM = 'RM'                                 # originally ProvincieItaliane.RM
PR_Type.RN = 'RN'                                 # originally ProvincieItaliane.RN
PR_Type.RO = 'RO'                                 # originally ProvincieItaliane.RO
PR_Type.SA = 'SA'                                 # originally ProvincieItaliane.SA
PR_Type.SI = 'SI'                                 # originally ProvincieItaliane.SI
PR_Type.SO = 'SO'                                 # originally ProvincieItaliane.SO
PR_Type.SP = 'SP'                                 # originally ProvincieItaliane.SP
PR_Type.SR = 'SR'                                 # originally ProvincieItaliane.SR
PR_Type.SS = 'SS'                                 # originally ProvincieItaliane.SS
PR_Type.SV = 'SV'                                 # originally ProvincieItaliane.SV
PR_Type.TA = 'TA'                                 # originally ProvincieItaliane.TA
PR_Type.TE = 'TE'                                 # originally ProvincieItaliane.TE
PR_Type.TN = 'TN'                                 # originally ProvincieItaliane.TN
PR_Type.TO = 'TO'                                 # originally ProvincieItaliane.TO
PR_Type.TP = 'TP'                                 # originally ProvincieItaliane.TP
PR_Type.TR = 'TR'                                 # originally ProvincieItaliane.TR
PR_Type.TS = 'TS'                                 # originally ProvincieItaliane.TS
PR_Type.TV = 'TV'                                 # originally ProvincieItaliane.TV
PR_Type.UD = 'UD'                                 # originally ProvincieItaliane.UD
PR_Type.VA = 'VA'                                 # originally ProvincieItaliane.VA
PR_Type.VB = 'VB'                                 # originally ProvincieItaliane.VB
PR_Type.VC = 'VC'                                 # originally ProvincieItaliane.VC
PR_Type.VE = 'VE'                                 # originally ProvincieItaliane.VE
PR_Type.VI = 'VI'                                 # originally ProvincieItaliane.VI
PR_Type.VR = 'VR'                                 # originally ProvincieItaliane.VR
PR_Type.VS = 'VS'                                 # originally ProvincieItaliane.VS
PR_Type.VT = 'VT'                                 # originally ProvincieItaliane.VT
PR_Type.VV = 'VV'                                 # originally ProvincieItaliane.VV
PR_Type._InitializeFacetMap(PR_Type._CF_pattern,
   PR_Type._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'PR_Type', PR_Type)
_module_typeBindings.PR_Type = PR_Type

# Union simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}PN_Type
# superclasses pyxb.binding.datatypes.anySimpleType
class PN_Type (pyxb.binding.basis.STD_union):

    """Tipo semplice costituito dalle sigle delle provincie italiane in vigore,  dalle sigle delle provincie croate di Fiume, Pola e Zara e dalla sigla “EE” che indica un paese estero."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PN_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesProvincie_v3.xsd', 18, 1)
    _Documentation = 'Tipo semplice costituito dalle sigle delle provincie italiane in vigore,  dalle sigle delle provincie croate di Fiume, Pola e Zara e dalla sigla \u201cEE\u201d che indica un paese estero.'

    _MemberTypes = ( ProvincieItaliane, ProvincieCroate, Estero, )
PN_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
PN_Type._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=PN_Type)
PN_Type.AG = 'AG'                                 # originally ProvincieItaliane.AG
PN_Type.AL = 'AL'                                 # originally ProvincieItaliane.AL
PN_Type.AN = 'AN'                                 # originally ProvincieItaliane.AN
PN_Type.AO = 'AO'                                 # originally ProvincieItaliane.AO
PN_Type.AP = 'AP'                                 # originally ProvincieItaliane.AP
PN_Type.AQ = 'AQ'                                 # originally ProvincieItaliane.AQ
PN_Type.AR = 'AR'                                 # originally ProvincieItaliane.AR
PN_Type.AT = 'AT'                                 # originally ProvincieItaliane.AT
PN_Type.AV = 'AV'                                 # originally ProvincieItaliane.AV
PN_Type.BA = 'BA'                                 # originally ProvincieItaliane.BA
PN_Type.BG = 'BG'                                 # originally ProvincieItaliane.BG
PN_Type.BI = 'BI'                                 # originally ProvincieItaliane.BI
PN_Type.BL = 'BL'                                 # originally ProvincieItaliane.BL
PN_Type.BN = 'BN'                                 # originally ProvincieItaliane.BN
PN_Type.BO = 'BO'                                 # originally ProvincieItaliane.BO
PN_Type.BR = 'BR'                                 # originally ProvincieItaliane.BR
PN_Type.BS = 'BS'                                 # originally ProvincieItaliane.BS
PN_Type.BT = 'BT'                                 # originally ProvincieItaliane.BT
PN_Type.BZ = 'BZ'                                 # originally ProvincieItaliane.BZ
PN_Type.CA = 'CA'                                 # originally ProvincieItaliane.CA
PN_Type.CB = 'CB'                                 # originally ProvincieItaliane.CB
PN_Type.CE = 'CE'                                 # originally ProvincieItaliane.CE
PN_Type.CH = 'CH'                                 # originally ProvincieItaliane.CH
PN_Type.CI = 'CI'                                 # originally ProvincieItaliane.CI
PN_Type.CL = 'CL'                                 # originally ProvincieItaliane.CL
PN_Type.CN = 'CN'                                 # originally ProvincieItaliane.CN
PN_Type.CO = 'CO'                                 # originally ProvincieItaliane.CO
PN_Type.CR = 'CR'                                 # originally ProvincieItaliane.CR
PN_Type.CS = 'CS'                                 # originally ProvincieItaliane.CS
PN_Type.CT = 'CT'                                 # originally ProvincieItaliane.CT
PN_Type.CZ = 'CZ'                                 # originally ProvincieItaliane.CZ
PN_Type.EN = 'EN'                                 # originally ProvincieItaliane.EN
PN_Type.FC = 'FC'                                 # originally ProvincieItaliane.FC
PN_Type.FE = 'FE'                                 # originally ProvincieItaliane.FE
PN_Type.FG = 'FG'                                 # originally ProvincieItaliane.FG
PN_Type.FI = 'FI'                                 # originally ProvincieItaliane.FI
PN_Type.FM = 'FM'                                 # originally ProvincieItaliane.FM
PN_Type.FR = 'FR'                                 # originally ProvincieItaliane.FR
PN_Type.GE = 'GE'                                 # originally ProvincieItaliane.GE
PN_Type.GO = 'GO'                                 # originally ProvincieItaliane.GO
PN_Type.GR = 'GR'                                 # originally ProvincieItaliane.GR
PN_Type.IM = 'IM'                                 # originally ProvincieItaliane.IM
PN_Type.IS = 'IS'                                 # originally ProvincieItaliane.IS
PN_Type.KR = 'KR'                                 # originally ProvincieItaliane.KR
PN_Type.LC = 'LC'                                 # originally ProvincieItaliane.LC
PN_Type.LE = 'LE'                                 # originally ProvincieItaliane.LE
PN_Type.LI = 'LI'                                 # originally ProvincieItaliane.LI
PN_Type.LO = 'LO'                                 # originally ProvincieItaliane.LO
PN_Type.LT = 'LT'                                 # originally ProvincieItaliane.LT
PN_Type.LU = 'LU'                                 # originally ProvincieItaliane.LU
PN_Type.MB = 'MB'                                 # originally ProvincieItaliane.MB
PN_Type.MC = 'MC'                                 # originally ProvincieItaliane.MC
PN_Type.ME = 'ME'                                 # originally ProvincieItaliane.ME
PN_Type.MI = 'MI'                                 # originally ProvincieItaliane.MI
PN_Type.MN = 'MN'                                 # originally ProvincieItaliane.MN
PN_Type.MO = 'MO'                                 # originally ProvincieItaliane.MO
PN_Type.MS = 'MS'                                 # originally ProvincieItaliane.MS
PN_Type.MT = 'MT'                                 # originally ProvincieItaliane.MT
PN_Type.NA = 'NA'                                 # originally ProvincieItaliane.NA
PN_Type.NO = 'NO'                                 # originally ProvincieItaliane.NO
PN_Type.NU = 'NU'                                 # originally ProvincieItaliane.NU
PN_Type.OG = 'OG'                                 # originally ProvincieItaliane.OG
PN_Type.OR = 'OR'                                 # originally ProvincieItaliane.OR
PN_Type.OT = 'OT'                                 # originally ProvincieItaliane.OT
PN_Type.PA = 'PA'                                 # originally ProvincieItaliane.PA
PN_Type.PC = 'PC'                                 # originally ProvincieItaliane.PC
PN_Type.PD = 'PD'                                 # originally ProvincieItaliane.PD
PN_Type.PE = 'PE'                                 # originally ProvincieItaliane.PE
PN_Type.PG = 'PG'                                 # originally ProvincieItaliane.PG
PN_Type.PI = 'PI'                                 # originally ProvincieItaliane.PI
PN_Type.PN = 'PN'                                 # originally ProvincieItaliane.PN
PN_Type.PO = 'PO'                                 # originally ProvincieItaliane.PO
PN_Type.PR = 'PR'                                 # originally ProvincieItaliane.PR
PN_Type.PT = 'PT'                                 # originally ProvincieItaliane.PT
PN_Type.PU = 'PU'                                 # originally ProvincieItaliane.PU
PN_Type.PV = 'PV'                                 # originally ProvincieItaliane.PV
PN_Type.PZ = 'PZ'                                 # originally ProvincieItaliane.PZ
PN_Type.RA = 'RA'                                 # originally ProvincieItaliane.RA
PN_Type.RC = 'RC'                                 # originally ProvincieItaliane.RC
PN_Type.RE = 'RE'                                 # originally ProvincieItaliane.RE
PN_Type.RG = 'RG'                                 # originally ProvincieItaliane.RG
PN_Type.RI = 'RI'                                 # originally ProvincieItaliane.RI
PN_Type.RM = 'RM'                                 # originally ProvincieItaliane.RM
PN_Type.RN = 'RN'                                 # originally ProvincieItaliane.RN
PN_Type.RO = 'RO'                                 # originally ProvincieItaliane.RO
PN_Type.SA = 'SA'                                 # originally ProvincieItaliane.SA
PN_Type.SI = 'SI'                                 # originally ProvincieItaliane.SI
PN_Type.SO = 'SO'                                 # originally ProvincieItaliane.SO
PN_Type.SP = 'SP'                                 # originally ProvincieItaliane.SP
PN_Type.SR = 'SR'                                 # originally ProvincieItaliane.SR
PN_Type.SS = 'SS'                                 # originally ProvincieItaliane.SS
PN_Type.SV = 'SV'                                 # originally ProvincieItaliane.SV
PN_Type.TA = 'TA'                                 # originally ProvincieItaliane.TA
PN_Type.TE = 'TE'                                 # originally ProvincieItaliane.TE
PN_Type.TN = 'TN'                                 # originally ProvincieItaliane.TN
PN_Type.TO = 'TO'                                 # originally ProvincieItaliane.TO
PN_Type.TP = 'TP'                                 # originally ProvincieItaliane.TP
PN_Type.TR = 'TR'                                 # originally ProvincieItaliane.TR
PN_Type.TS = 'TS'                                 # originally ProvincieItaliane.TS
PN_Type.TV = 'TV'                                 # originally ProvincieItaliane.TV
PN_Type.UD = 'UD'                                 # originally ProvincieItaliane.UD
PN_Type.VA = 'VA'                                 # originally ProvincieItaliane.VA
PN_Type.VB = 'VB'                                 # originally ProvincieItaliane.VB
PN_Type.VC = 'VC'                                 # originally ProvincieItaliane.VC
PN_Type.VE = 'VE'                                 # originally ProvincieItaliane.VE
PN_Type.VI = 'VI'                                 # originally ProvincieItaliane.VI
PN_Type.VR = 'VR'                                 # originally ProvincieItaliane.VR
PN_Type.VS = 'VS'                                 # originally ProvincieItaliane.VS
PN_Type.VT = 'VT'                                 # originally ProvincieItaliane.VT
PN_Type.VV = 'VV'                                 # originally ProvincieItaliane.VV
PN_Type.FU = 'FU'                                 # originally ProvincieCroate.FU
PN_Type.PL = 'PL'                                 # originally ProvincieCroate.PL
PN_Type.ZA = 'ZA'                                 # originally ProvincieCroate.ZA
PN_Type.EE = 'EE'                                 # originally Estero.EE
PN_Type._InitializeFacetMap(PN_Type._CF_pattern,
   PN_Type._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'PN_Type', PN_Type)
_module_typeBindings.PN_Type = PN_Type

# Union simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:common}PE_Type
# superclasses pyxb.binding.datatypes.anySimpleType
class PE_Type (pyxb.binding.basis.STD_union):

    """Tipo semplice costituito dalle sigle delle provincie italiane in vigore e dalla sigla “EE” che indica un paese estero."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PE_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/typesProvincie_v3.xsd', 24, 1)
    _Documentation = 'Tipo semplice costituito dalle sigle delle provincie italiane in vigore e dalla sigla \u201cEE\u201d che indica un paese estero.'

    _MemberTypes = ( ProvincieItaliane, Estero, )
PE_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
PE_Type._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=PE_Type)
PE_Type.AG = 'AG'                                 # originally ProvincieItaliane.AG
PE_Type.AL = 'AL'                                 # originally ProvincieItaliane.AL
PE_Type.AN = 'AN'                                 # originally ProvincieItaliane.AN
PE_Type.AO = 'AO'                                 # originally ProvincieItaliane.AO
PE_Type.AP = 'AP'                                 # originally ProvincieItaliane.AP
PE_Type.AQ = 'AQ'                                 # originally ProvincieItaliane.AQ
PE_Type.AR = 'AR'                                 # originally ProvincieItaliane.AR
PE_Type.AT = 'AT'                                 # originally ProvincieItaliane.AT
PE_Type.AV = 'AV'                                 # originally ProvincieItaliane.AV
PE_Type.BA = 'BA'                                 # originally ProvincieItaliane.BA
PE_Type.BG = 'BG'                                 # originally ProvincieItaliane.BG
PE_Type.BI = 'BI'                                 # originally ProvincieItaliane.BI
PE_Type.BL = 'BL'                                 # originally ProvincieItaliane.BL
PE_Type.BN = 'BN'                                 # originally ProvincieItaliane.BN
PE_Type.BO = 'BO'                                 # originally ProvincieItaliane.BO
PE_Type.BR = 'BR'                                 # originally ProvincieItaliane.BR
PE_Type.BS = 'BS'                                 # originally ProvincieItaliane.BS
PE_Type.BT = 'BT'                                 # originally ProvincieItaliane.BT
PE_Type.BZ = 'BZ'                                 # originally ProvincieItaliane.BZ
PE_Type.CA = 'CA'                                 # originally ProvincieItaliane.CA
PE_Type.CB = 'CB'                                 # originally ProvincieItaliane.CB
PE_Type.CE = 'CE'                                 # originally ProvincieItaliane.CE
PE_Type.CH = 'CH'                                 # originally ProvincieItaliane.CH
PE_Type.CI = 'CI'                                 # originally ProvincieItaliane.CI
PE_Type.CL = 'CL'                                 # originally ProvincieItaliane.CL
PE_Type.CN = 'CN'                                 # originally ProvincieItaliane.CN
PE_Type.CO = 'CO'                                 # originally ProvincieItaliane.CO
PE_Type.CR = 'CR'                                 # originally ProvincieItaliane.CR
PE_Type.CS = 'CS'                                 # originally ProvincieItaliane.CS
PE_Type.CT = 'CT'                                 # originally ProvincieItaliane.CT
PE_Type.CZ = 'CZ'                                 # originally ProvincieItaliane.CZ
PE_Type.EN = 'EN'                                 # originally ProvincieItaliane.EN
PE_Type.FC = 'FC'                                 # originally ProvincieItaliane.FC
PE_Type.FE = 'FE'                                 # originally ProvincieItaliane.FE
PE_Type.FG = 'FG'                                 # originally ProvincieItaliane.FG
PE_Type.FI = 'FI'                                 # originally ProvincieItaliane.FI
PE_Type.FM = 'FM'                                 # originally ProvincieItaliane.FM
PE_Type.FR = 'FR'                                 # originally ProvincieItaliane.FR
PE_Type.GE = 'GE'                                 # originally ProvincieItaliane.GE
PE_Type.GO = 'GO'                                 # originally ProvincieItaliane.GO
PE_Type.GR = 'GR'                                 # originally ProvincieItaliane.GR
PE_Type.IM = 'IM'                                 # originally ProvincieItaliane.IM
PE_Type.IS = 'IS'                                 # originally ProvincieItaliane.IS
PE_Type.KR = 'KR'                                 # originally ProvincieItaliane.KR
PE_Type.LC = 'LC'                                 # originally ProvincieItaliane.LC
PE_Type.LE = 'LE'                                 # originally ProvincieItaliane.LE
PE_Type.LI = 'LI'                                 # originally ProvincieItaliane.LI
PE_Type.LO = 'LO'                                 # originally ProvincieItaliane.LO
PE_Type.LT = 'LT'                                 # originally ProvincieItaliane.LT
PE_Type.LU = 'LU'                                 # originally ProvincieItaliane.LU
PE_Type.MB = 'MB'                                 # originally ProvincieItaliane.MB
PE_Type.MC = 'MC'                                 # originally ProvincieItaliane.MC
PE_Type.ME = 'ME'                                 # originally ProvincieItaliane.ME
PE_Type.MI = 'MI'                                 # originally ProvincieItaliane.MI
PE_Type.MN = 'MN'                                 # originally ProvincieItaliane.MN
PE_Type.MO = 'MO'                                 # originally ProvincieItaliane.MO
PE_Type.MS = 'MS'                                 # originally ProvincieItaliane.MS
PE_Type.MT = 'MT'                                 # originally ProvincieItaliane.MT
PE_Type.NA = 'NA'                                 # originally ProvincieItaliane.NA
PE_Type.NO = 'NO'                                 # originally ProvincieItaliane.NO
PE_Type.NU = 'NU'                                 # originally ProvincieItaliane.NU
PE_Type.OG = 'OG'                                 # originally ProvincieItaliane.OG
PE_Type.OR = 'OR'                                 # originally ProvincieItaliane.OR
PE_Type.OT = 'OT'                                 # originally ProvincieItaliane.OT
PE_Type.PA = 'PA'                                 # originally ProvincieItaliane.PA
PE_Type.PC = 'PC'                                 # originally ProvincieItaliane.PC
PE_Type.PD = 'PD'                                 # originally ProvincieItaliane.PD
PE_Type.PE = 'PE'                                 # originally ProvincieItaliane.PE
PE_Type.PG = 'PG'                                 # originally ProvincieItaliane.PG
PE_Type.PI = 'PI'                                 # originally ProvincieItaliane.PI
PE_Type.PN = 'PN'                                 # originally ProvincieItaliane.PN
PE_Type.PO = 'PO'                                 # originally ProvincieItaliane.PO
PE_Type.PR = 'PR'                                 # originally ProvincieItaliane.PR
PE_Type.PT = 'PT'                                 # originally ProvincieItaliane.PT
PE_Type.PU = 'PU'                                 # originally ProvincieItaliane.PU
PE_Type.PV = 'PV'                                 # originally ProvincieItaliane.PV
PE_Type.PZ = 'PZ'                                 # originally ProvincieItaliane.PZ
PE_Type.RA = 'RA'                                 # originally ProvincieItaliane.RA
PE_Type.RC = 'RC'                                 # originally ProvincieItaliane.RC
PE_Type.RE = 'RE'                                 # originally ProvincieItaliane.RE
PE_Type.RG = 'RG'                                 # originally ProvincieItaliane.RG
PE_Type.RI = 'RI'                                 # originally ProvincieItaliane.RI
PE_Type.RM = 'RM'                                 # originally ProvincieItaliane.RM
PE_Type.RN = 'RN'                                 # originally ProvincieItaliane.RN
PE_Type.RO = 'RO'                                 # originally ProvincieItaliane.RO
PE_Type.SA = 'SA'                                 # originally ProvincieItaliane.SA
PE_Type.SI = 'SI'                                 # originally ProvincieItaliane.SI
PE_Type.SO = 'SO'                                 # originally ProvincieItaliane.SO
PE_Type.SP = 'SP'                                 # originally ProvincieItaliane.SP
PE_Type.SR = 'SR'                                 # originally ProvincieItaliane.SR
PE_Type.SS = 'SS'                                 # originally ProvincieItaliane.SS
PE_Type.SV = 'SV'                                 # originally ProvincieItaliane.SV
PE_Type.TA = 'TA'                                 # originally ProvincieItaliane.TA
PE_Type.TE = 'TE'                                 # originally ProvincieItaliane.TE
PE_Type.TN = 'TN'                                 # originally ProvincieItaliane.TN
PE_Type.TO = 'TO'                                 # originally ProvincieItaliane.TO
PE_Type.TP = 'TP'                                 # originally ProvincieItaliane.TP
PE_Type.TR = 'TR'                                 # originally ProvincieItaliane.TR
PE_Type.TS = 'TS'                                 # originally ProvincieItaliane.TS
PE_Type.TV = 'TV'                                 # originally ProvincieItaliane.TV
PE_Type.UD = 'UD'                                 # originally ProvincieItaliane.UD
PE_Type.VA = 'VA'                                 # originally ProvincieItaliane.VA
PE_Type.VB = 'VB'                                 # originally ProvincieItaliane.VB
PE_Type.VC = 'VC'                                 # originally ProvincieItaliane.VC
PE_Type.VE = 'VE'                                 # originally ProvincieItaliane.VE
PE_Type.VI = 'VI'                                 # originally ProvincieItaliane.VI
PE_Type.VR = 'VR'                                 # originally ProvincieItaliane.VR
PE_Type.VS = 'VS'                                 # originally ProvincieItaliane.VS
PE_Type.VT = 'VT'                                 # originally ProvincieItaliane.VT
PE_Type.VV = 'VV'                                 # originally ProvincieItaliane.VV
PE_Type.EE = 'EE'                                 # originally Estero.EE
PE_Type._InitializeFacetMap(PE_Type._CF_pattern,
   PE_Type._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'PE_Type', PE_Type)
_module_typeBindings.PE_Type = PE_Type

# Complex type {urn:www.agenziaentrate.gov.it:specificheTecniche:common}Documento_Type with content type EMPTY
class Documento_Type (pyxb.binding.basis.complexTypeDefinition):
    """Documento trasmesso"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Documento_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/fornitura_v3.xsd', 21, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute identificativo uses Python identifier identificativo
    __identificativo = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'identificativo'), 'identificativo', '__urnwww_agenziaentrate_gov_itspecificheTecnichecommon_Documento_Type_identificativo', _module_typeBindings.Identificativo_Type, required=True)
    __identificativo._DeclarationLocation = pyxb.utils.utility.Location('../common/fornitura_v3.xsd', 25, 2)
    __identificativo._UseLocation = pyxb.utils.utility.Location('../common/fornitura_v3.xsd', 25, 2)
    
    identificativo = property(__identificativo.value, __identificativo.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __identificativo.name() : __identificativo
    })
_module_typeBindings.Documento_Type = Documento_Type
Namespace.addCategoryObject('typeBinding', 'Documento_Type', Documento_Type)


Documento = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Documento'), Documento_Type, abstract=pyxb.binding.datatypes.boolean(1), location=pyxb.utils.utility.Location('../common/fornitura_v3.xsd', 20, 1))
Namespace.addCategoryObject('elementBinding', Documento.name().localName(), Documento)
