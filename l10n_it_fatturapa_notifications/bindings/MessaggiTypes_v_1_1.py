# ./MessaggiTypes_v_1_1.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:169c170641bf52e3c8fbe2875d46a3fd020f92da
# Generated 2015-03-17 10:03:13.924864 by PyXB version 1.2.4
# using Python 2.7.8.final.0
# Namespace http://www.fatturapa.gov.it/sdi/messaggi/v1.0

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import pyxb.utils.six as _six

# Import bindings for namespaces imported into schema
from openerp.addons.l10n_it_fatturapa.bindings import (
    _ds as _ImportedBinding__ds)
import pyxb.binding.datatypes

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier(
    'urn:uuid:6833f7bc-cc84-11e4-b07b-08edb9323673')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI(
    'http://www.fatturapa.gov.it/sdi/messaggi/v1.0',
    create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])
_Namespace_ds = _ImportedBinding__ds.Namespace
_Namespace_ds.configureCategories(['typeBinding', 'elementBinding'])


def CreateFromDocument(xml_text, default_namespace=None, location_base=None):
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
        return CreateFromDOM(
            dom.documentElement,
            default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(
        fallback_namespace=default_namespace,
        location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance


def CreateFromDOM(node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary;
    use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}Codice_Type
class Codice_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Codice_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        131,
        1)
    _Documentation = None
Codice_Type._CF_length = pyxb.binding.facets.CF_length(
    value=pyxb.binding.datatypes.nonNegativeInteger(5))
Codice_Type._InitializeFacetMap(Codice_Type._CF_length)
Namespace.addCategoryObject('typeBinding', 'Codice_Type', Codice_Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}CodiceDestinatario_Type


class CodiceDestinatario_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace,
        'CodiceDestinatario_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        194,
        1)
    _Documentation = None
CodiceDestinatario_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
CodiceDestinatario_Type._CF_pattern.addPattern(pattern='[A-Z0-9]{6}')
CodiceDestinatario_Type._InitializeFacetMap(
    CodiceDestinatario_Type._CF_pattern)
Namespace.addCategoryObject(
    'typeBinding',
    'CodiceDestinatario_Type',
    CodiceDestinatario_Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}Formato_Type


class Formato_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Formato_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        200,
        1)
    _Documentation = None
Formato_Type._CF_maxLength = pyxb.binding.facets.CF_maxLength(
    value=pyxb.binding.datatypes.nonNegativeInteger(5))
Formato_Type._InitializeFacetMap(Formato_Type._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'Formato_Type', Formato_Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}EsitoCommittente_Type


class EsitoCommittente_Type (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace,
        'EsitoCommittente_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        206,
        1)
    _Documentation = None
EsitoCommittente_Type._CF_enumeration = pyxb.binding.facets.CF_enumeration(
    value_datatype=EsitoCommittente_Type,
    enum_prefix=None)
EsitoCommittente_Type.EC01 = (
    EsitoCommittente_Type._CF_enumeration.addEnumeration(
        unicode_value='EC01',
        tag='EC01'))
EsitoCommittente_Type.EC02 = (
    EsitoCommittente_Type._CF_enumeration.addEnumeration(
        unicode_value='EC02',
        tag='EC02'))
EsitoCommittente_Type._InitializeFacetMap(
    EsitoCommittente_Type._CF_enumeration)
Namespace.addCategoryObject(
    'typeBinding',
    'EsitoCommittente_Type',
    EsitoCommittente_Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}Scarto_Type


class Scarto_Type (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Scarto_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        225,
        1)
    _Documentation = None
Scarto_Type._CF_enumeration = pyxb.binding.facets.CF_enumeration(
    value_datatype=Scarto_Type,
    enum_prefix=None)
Scarto_Type.EN00 = Scarto_Type._CF_enumeration.addEnumeration(
    unicode_value='EN00',
    tag='EN00')
Scarto_Type.EN01 = Scarto_Type._CF_enumeration.addEnumeration(
    unicode_value='EN01',
    tag='EN01')
Scarto_Type._InitializeFacetMap(Scarto_Type._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'Scarto_Type', Scarto_Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}IdentificativoSdI_Type


class IdentificativoSdI_Type (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace,
        'IdentificativoSdI_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        247,
        1)
    _Documentation = None
IdentificativoSdI_Type._CF_totalDigits = pyxb.binding.facets.CF_totalDigits(
    value=pyxb.binding.datatypes.positiveInteger(12))
IdentificativoSdI_Type._InitializeFacetMap(
    IdentificativoSdI_Type._CF_totalDigits)
Namespace.addCategoryObject(
    'typeBinding',
    'IdentificativoSdI_Type',
    IdentificativoSdI_Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}NomeFile_Type


class NomeFile_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NomeFile_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        253,
        1)
    _Documentation = None
NomeFile_Type._CF_maxLength = pyxb.binding.facets.CF_maxLength(
    value=pyxb.binding.datatypes.nonNegativeInteger(50))
NomeFile_Type._InitializeFacetMap(NomeFile_Type._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'NomeFile_Type', NomeFile_Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}NumeroFattura_Type


class NumeroFattura_Type (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace,
        'NumeroFattura_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        267,
        1)
    _Documentation = None
NumeroFattura_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
NumeroFattura_Type._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{1,20})')
NumeroFattura_Type._InitializeFacetMap(NumeroFattura_Type._CF_pattern)
Namespace.addCategoryObject(
    'typeBinding',
    'NumeroFattura_Type',
    NumeroFattura_Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}AnnoFattura_Type


class AnnoFattura_Type (pyxb.binding.datatypes.nonNegativeInteger):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AnnoFattura_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        273,
        1)
    _Documentation = None
AnnoFattura_Type._InitializeFacetMap()
Namespace.addCategoryObject(
    'typeBinding',
    'AnnoFattura_Type',
    AnnoFattura_Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}MessageId_Type


class MessageId_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MessageId_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        278,
        1)
    _Documentation = None
MessageId_Type._CF_maxLength = pyxb.binding.facets.CF_maxLength(
    value=pyxb.binding.datatypes.nonNegativeInteger(14))
MessageId_Type._CF_minLength = pyxb.binding.facets.CF_minLength(
    value=pyxb.binding.datatypes.nonNegativeInteger(1))
MessageId_Type._InitializeFacetMap(MessageId_Type._CF_maxLength,
                                   MessageId_Type._CF_minLength)
Namespace.addCategoryObject('typeBinding', 'MessageId_Type', MessageId_Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}PecMessageId_Type


class PecMessageId_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PecMessageId_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        285,
        1)
    _Documentation = None
PecMessageId_Type._InitializeFacetMap()
Namespace.addCategoryObject(
    'typeBinding',
    'PecMessageId_Type',
    PecMessageId_Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}Descrizione_Type


class Descrizione_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Descrizione_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        289,
        1)
    _Documentation = None
Descrizione_Type._CF_maxLength = pyxb.binding.facets.CF_maxLength(
    value=pyxb.binding.datatypes.nonNegativeInteger(255))
Descrizione_Type._InitializeFacetMap(Descrizione_Type._CF_maxLength)
Namespace.addCategoryObject(
    'typeBinding',
    'Descrizione_Type',
    Descrizione_Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}Versione_Type


class Versione_Type (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Versione_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        295,
        1)
    _Documentation = None
Versione_Type._CF_maxLength = pyxb.binding.facets.CF_maxLength(
    value=pyxb.binding.datatypes.nonNegativeInteger(5))
Versione_Type._InitializeFacetMap(Versione_Type._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'Versione_Type', Versione_Type)

# Complex type
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}RiferimentoArchivio_Type
# with content type ELEMENT_ONLY


class RiferimentoArchivio_Type (pyxb.binding.basis.complexTypeDefinition):

    """Complex type
    {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}RiferimentoArchivio_Type
    with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace,
        'RiferimentoArchivio_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        111,
        1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdentificativoSdI uses Python identifier IdentificativoSdI
    __IdentificativoSdI = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        'IdentificativoSdI',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_RiferimentoArchivio_Type_'
        'IdentificativoSdI',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            113,
            3),
    )

    IdentificativoSdI = property(
        __IdentificativoSdI.value,
        __IdentificativoSdI.set,
        None,
        None)

    # Element NomeFile uses Python identifier NomeFile
    __NomeFile = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NomeFile'),
        'NomeFile',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_RiferimentoArchivio_'
        'Type_NomeFile',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            114,
            3),
    )

    NomeFile = property(__NomeFile.value, __NomeFile.set, None, None)

    _ElementMap.update({
        __IdentificativoSdI.name(): __IdentificativoSdI,
        __NomeFile.name(): __NomeFile
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding',
    'RiferimentoArchivio_Type',
    RiferimentoArchivio_Type)


# Complex type
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}ListaErrori_Type with
# content type ELEMENT_ONLY
class ListaErrori_Type (pyxb.binding.basis.complexTypeDefinition):

    """Complex type
    {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}ListaErrori_Type
    with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ListaErrori_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        118,
        1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element Errore uses Python identifier Errore
    __Errore = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Errore'),
        'Errore',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_ListaErrori_Type_Errore',
        True,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            120,
            3),
    )

    Errore = property(__Errore.value, __Errore.set, None, None)

    _ElementMap.update({
        __Errore.name(): __Errore
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding',
    'ListaErrori_Type',
    ListaErrori_Type)


# Complex type {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}Errore_Type
# with content type ELEMENT_ONLY
class Errore_Type (pyxb.binding.basis.complexTypeDefinition):

    """Complex type
    {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}Errore_Type
    with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Errore_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        124,
        1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element Codice uses Python identifier Codice
    __Codice = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Codice'),
        'Codice',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_Errore_Type_Codice',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            126,
            3),
    )

    Codice = property(__Codice.value, __Codice.set, None, None)

    # Element Descrizione uses Python identifier Descrizione
    __Descrizione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Descrizione'),
        'Descrizione',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_Errore_Type_Descrizione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            127,
            3),
    )

    Descrizione = property(__Descrizione.value, __Descrizione.set, None, None)

    _ElementMap.update({
        __Codice.name(): __Codice,
        __Descrizione.name(): __Descrizione
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject('typeBinding', 'Errore_Type', Errore_Type)


# Complex type
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}RiferimentoFattura_Type
# with content type ELEMENT_ONLY
class RiferimentoFattura_Type (pyxb.binding.basis.complexTypeDefinition):

    """Complex type
    {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}RiferimentoFattura_Type
    with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace,
        'RiferimentoFattura_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        259,
        1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element NumeroFattura uses Python identifier NumeroFattura
    __NumeroFattura = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NumeroFattura'),
        'NumeroFattura',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_RiferimentoFattura_'
        'Type_NumeroFattura',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            261,
            3),
    )

    NumeroFattura = property(
        __NumeroFattura.value,
        __NumeroFattura.set,
        None,
        None)

    # Element AnnoFattura uses Python identifier AnnoFattura
    __AnnoFattura = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'AnnoFattura'),
        'AnnoFattura',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_RiferimentoFattura_'
        'Type_AnnoFattura',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            262,
            3),
    )

    AnnoFattura = property(__AnnoFattura.value, __AnnoFattura.set, None, None)

    # Element PosizioneFattura uses Python identifier PosizioneFattura
    __PosizioneFattura = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'PosizioneFattura'),
        'PosizioneFattura',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_RiferimentoFattura_'
        'Type_PosizioneFattura',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            263,
            3),
    )

    PosizioneFattura = property(
        __PosizioneFattura.value,
        __PosizioneFattura.set,
        None,
        None)

    _ElementMap.update({
        __NumeroFattura.name(): __NumeroFattura,
        __AnnoFattura.name(): __AnnoFattura,
        __PosizioneFattura.name(): __PosizioneFattura
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding',
    'RiferimentoFattura_Type',
    RiferimentoFattura_Type)


# Complex type
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}Destinatario_Type with
# content type ELEMENT_ONLY
class Destinatario_Type (pyxb.binding.basis.complexTypeDefinition):

    """Complex type
    {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}Destinatario_Type
    with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Destinatario_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        301,
        1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element Codice uses Python identifier Codice
    __Codice = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Codice'),
        'Codice',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_Destinatario_'
        'Type_Codice',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            303,
            3),
    )

    Codice = property(__Codice.value, __Codice.set, None, None)

    # Element Descrizione uses Python identifier Descrizione
    __Descrizione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Descrizione'),
        'Descrizione',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_Destinatario_'
        'Type_Descrizione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            304,
            3),
    )

    Descrizione = property(__Descrizione.value, __Descrizione.set, None, None)

    _ElementMap.update({
        __Codice.name(): __Codice,
        __Descrizione.name(): __Descrizione
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding',
    'Destinatario_Type',
    Destinatario_Type)


# Complex type
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}RicevutaConsegna_Type
# with content type ELEMENT_ONLY
class RicevutaConsegna_Type (pyxb.binding.basis.complexTypeDefinition):

    """Complex type
    {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}RicevutaConsegna_Type
    with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace,
        'RicevutaConsegna_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        34,
        1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdentificativoSdI uses Python identifier IdentificativoSdI
    __IdentificativoSdI = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        'IdentificativoSdI',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_RicevutaConsegna_'
        'Type_IdentificativoSdI',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            36,
            3),
    )

    IdentificativoSdI = property(
        __IdentificativoSdI.value,
        __IdentificativoSdI.set,
        None,
        None)

    # Element NomeFile uses Python identifier NomeFile
    __NomeFile = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NomeFile'),
        'NomeFile',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_RicevutaConsegna_'
        'Type_NomeFile',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            37,
            3),
    )

    NomeFile = property(__NomeFile.value, __NomeFile.set, None, None)

    # Element DataOraRicezione uses Python identifier DataOraRicezione
    __DataOraRicezione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DataOraRicezione'),
        'DataOraRicezione',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_RicevutaConsegna_'
        'Type_DataOraRicezione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            38,
            3),
    )

    DataOraRicezione = property(
        __DataOraRicezione.value,
        __DataOraRicezione.set,
        None,
        None)

    # Element DataOraConsegna uses Python identifier DataOraConsegna
    __DataOraConsegna = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DataOraConsegna'),
        'DataOraConsegna',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_RicevutaConsegna_'
        'Type_DataOraConsegna',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            39,
            3),
    )

    DataOraConsegna = property(
        __DataOraConsegna.value,
        __DataOraConsegna.set,
        None,
        None)

    # Element Destinatario uses Python identifier Destinatario
    __Destinatario = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Destinatario'),
        'Destinatario',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_RicevutaConsegna_'
        'Type_Destinatario',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            40,
            3),
    )

    Destinatario = property(
        __Destinatario.value,
        __Destinatario.set,
        None,
        None)

    # Element RiferimentoArchivio uses Python identifier RiferimentoArchivio
    __RiferimentoArchivio = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoArchivio'),
        'RiferimentoArchivio',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_RicevutaConsegna_'
        'Type_RiferimentoArchivio',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            41,
            3),
    )

    RiferimentoArchivio = property(
        __RiferimentoArchivio.value,
        __RiferimentoArchivio.set,
        None,
        None)

    # Element MessageId uses Python identifier MessageId
    __MessageId = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'MessageId'),
        'MessageId',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_RicevutaConsegna_'
        'Type_MessageId',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            42,
            3),
    )

    MessageId = property(__MessageId.value, __MessageId.set, None, None)

    # Element PecMessageId uses Python identifier PecMessageId
    __PecMessageId = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'PecMessageId'),
        'PecMessageId',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_RicevutaConsegna_'
        'Type_PecMessageId',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            43,
            3),
    )

    PecMessageId = property(
        __PecMessageId.value,
        __PecMessageId.set,
        None,
        None)

    # Element Note uses Python identifier Note
    __Note = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Note'),
        'Note',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_RicevutaConsegna_'
        'Type_Note',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            44,
            3),
    )

    Note = property(__Note.value, __Note.set, None, None)

    # Element {http://www.w3.org/2000/09/xmldsig#}Signature uses Python
    # identifier Signature
    __Signature = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            _Namespace_ds,
            'Signature'),
        'Signature',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_RicevutaConsegna_'
        'Type_httpwww_w3_org200009xmldsigSignature',
        False,
        pyxb.utils.utility.Location(
            'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/'
            'xmldsig-core-schema.xsd',
            43,
            0),
    )

    Signature = property(__Signature.value, __Signature.set, None, None)

    # Attribute versione uses Python identifier versione
    __versione = pyxb.binding.content.AttributeUse(
        pyxb.namespace.ExpandedName(
            None,
            'versione'),
        'versione',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_RicevutaConsegna_'
        'Type_versione',
        Versione_Type,
        fixed=True,
        unicode_default='1.0',
        required=True)
    __versione._DeclarationLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        47,
        2)
    __versione._UseLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        47,
        2)

    versione = property(__versione.value, __versione.set, None, None)

    # Attribute IntermediarioConDupliceRuolo uses Python identifier
    # IntermediarioConDupliceRuolo
    __IntermediarioConDupliceRuolo = pyxb.binding.content.AttributeUse(
        pyxb.namespace.ExpandedName(
            None,
            'IntermediarioConDupliceRuolo'),
        'IntermediarioConDupliceRuolo',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_RicevutaConsegna_'
        'Type_IntermediarioConDupliceRuolo',
        pyxb.binding.datatypes.string,
        fixed=True,
        unicode_default='Si')
    __IntermediarioConDupliceRuolo._DeclarationLocation = (
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            48,
            2))
    __IntermediarioConDupliceRuolo._UseLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        48,
        2)

    IntermediarioConDupliceRuolo = property(
        __IntermediarioConDupliceRuolo.value,
        __IntermediarioConDupliceRuolo.set,
        None,
        None)

    _ElementMap.update({
        __IdentificativoSdI.name(): __IdentificativoSdI,
        __NomeFile.name(): __NomeFile,
        __DataOraRicezione.name(): __DataOraRicezione,
        __DataOraConsegna.name(): __DataOraConsegna,
        __Destinatario.name(): __Destinatario,
        __RiferimentoArchivio.name(): __RiferimentoArchivio,
        __MessageId.name(): __MessageId,
        __PecMessageId.name(): __PecMessageId,
        __Note.name(): __Note,
        __Signature.name(): __Signature
    })
    _AttributeMap.update({
        __versione.name(): __versione,
        __IntermediarioConDupliceRuolo.name(): __IntermediarioConDupliceRuolo
    })
Namespace.addCategoryObject(
    'typeBinding',
    'RicevutaConsegna_Type',
    RicevutaConsegna_Type)


# Complex type
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}NotificaScarto_Type with
# content type ELEMENT_ONLY
class NotificaScarto_Type (pyxb.binding.basis.complexTypeDefinition):

    """Complex type
    {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}NotificaScarto_Type
    with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace,
        'NotificaScarto_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        51,
        1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdentificativoSdI uses Python identifier IdentificativoSdI
    __IdentificativoSdI = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        'IdentificativoSdI',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaScarto_'
        'Type_IdentificativoSdI',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            53,
            3),
    )

    IdentificativoSdI = property(
        __IdentificativoSdI.value,
        __IdentificativoSdI.set,
        None,
        None)

    # Element NomeFile uses Python identifier NomeFile
    __NomeFile = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NomeFile'),
        'NomeFile',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaScarto_'
        'Type_NomeFile',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            54,
            3),
    )

    NomeFile = property(__NomeFile.value, __NomeFile.set, None, None)

    # Element DataOraRicezione uses Python identifier DataOraRicezione
    __DataOraRicezione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DataOraRicezione'),
        'DataOraRicezione',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaScarto_'
        'Type_DataOraRicezione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            55,
            3),
    )

    DataOraRicezione = property(
        __DataOraRicezione.value,
        __DataOraRicezione.set,
        None,
        None)

    # Element RiferimentoArchivio uses Python identifier RiferimentoArchivio
    __RiferimentoArchivio = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoArchivio'),
        'RiferimentoArchivio',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaScarto_'
        'Type_RiferimentoArchivio',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            56,
            3),
    )

    RiferimentoArchivio = property(
        __RiferimentoArchivio.value,
        __RiferimentoArchivio.set,
        None,
        None)

    # Element ListaErrori uses Python identifier ListaErrori
    __ListaErrori = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'ListaErrori'),
        'ListaErrori',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaScarto_'
        'Type_ListaErrori',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            57,
            3),
    )

    ListaErrori = property(__ListaErrori.value, __ListaErrori.set, None, None)

    # Element MessageId uses Python identifier MessageId
    __MessageId = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'MessageId'),
        'MessageId',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaScarto_'
        'Type_MessageId',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            58,
            3),
    )

    MessageId = property(__MessageId.value, __MessageId.set, None, None)

    # Element PecMessageId uses Python identifier PecMessageId
    __PecMessageId = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'PecMessageId'),
        'PecMessageId',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaScarto_'
        'Type_PecMessageId',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            59,
            3),
    )

    PecMessageId = property(
        __PecMessageId.value,
        __PecMessageId.set,
        None,
        None)

    # Element Note uses Python identifier Note
    __Note = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Note'),
        'Note',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaScarto_'
        'Type_Note',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            60,
            3),
    )

    Note = property(__Note.value, __Note.set, None, None)

    # Element {http://www.w3.org/2000/09/xmldsig#}Signature uses Python
    # identifier Signature
    __Signature = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            _Namespace_ds,
            'Signature'),
        'Signature',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaScarto_'
        'Type_httpwww_w3_org200009xmldsigSignature',
        False,
        pyxb.utils.utility.Location(
            'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/'
            'xmldsig-core-schema.xsd',
            43,
            0),
    )

    Signature = property(__Signature.value, __Signature.set, None, None)

    # Attribute versione uses Python identifier versione
    __versione = pyxb.binding.content.AttributeUse(
        pyxb.namespace.ExpandedName(
            None,
            'versione'),
        'versione',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaScarto_'
        'Type_versione',
        Versione_Type,
        fixed=True,
        unicode_default='1.0',
        required=True)
    __versione._DeclarationLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        63,
        2)
    __versione._UseLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        63,
        2)

    versione = property(__versione.value, __versione.set, None, None)

    _ElementMap.update({
        __IdentificativoSdI.name(): __IdentificativoSdI,
        __NomeFile.name(): __NomeFile,
        __DataOraRicezione.name(): __DataOraRicezione,
        __RiferimentoArchivio.name(): __RiferimentoArchivio,
        __ListaErrori.name(): __ListaErrori,
        __MessageId.name(): __MessageId,
        __PecMessageId.name(): __PecMessageId,
        __Note.name(): __Note,
        __Signature.name(): __Signature
    })
    _AttributeMap.update({
        __versione.name(): __versione
    })
Namespace.addCategoryObject(
    'typeBinding',
    'NotificaScarto_Type',
    NotificaScarto_Type)


# Complex type
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}NotificaMancataConsegna_Type
# with content type ELEMENT_ONLY
class NotificaMancataConsegna_Type (pyxb.binding.basis.complexTypeDefinition):

    """Complex type
    {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}NotificaMancataConsegna_Type
    with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace,
        'NotificaMancataConsegna_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        66,
        1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdentificativoSdI uses Python identifier IdentificativoSdI
    __IdentificativoSdI = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        'IdentificativoSdI',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaMancataConsegna_'
        'Type_IdentificativoSdI',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            68,
            3),
    )

    IdentificativoSdI = property(
        __IdentificativoSdI.value,
        __IdentificativoSdI.set,
        None,
        None)

    # Element NomeFile uses Python identifier NomeFile
    __NomeFile = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NomeFile'),
        'NomeFile',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaMancataConsegna_'
        'Type_NomeFile',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            69,
            3),
    )

    NomeFile = property(__NomeFile.value, __NomeFile.set, None, None)

    # Element DataOraRicezione uses Python identifier DataOraRicezione
    __DataOraRicezione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DataOraRicezione'),
        'DataOraRicezione',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaMancataConsegna_'
        'Type_DataOraRicezione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            70,
            3),
    )

    DataOraRicezione = property(
        __DataOraRicezione.value,
        __DataOraRicezione.set,
        None,
        None)

    # Element RiferimentoArchivio uses Python identifier RiferimentoArchivio
    __RiferimentoArchivio = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoArchivio'),
        'RiferimentoArchivio',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaMancataConsegna_'
        'Type_RiferimentoArchivio',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            71,
            3),
    )

    RiferimentoArchivio = property(
        __RiferimentoArchivio.value,
        __RiferimentoArchivio.set,
        None,
        None)

    # Element Descrizione uses Python identifier Descrizione
    __Descrizione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Descrizione'),
        'Descrizione',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaMancataConsegna_'
        'Type_Descrizione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            72,
            3),
    )

    Descrizione = property(__Descrizione.value, __Descrizione.set, None, None)

    # Element MessageId uses Python identifier MessageId
    __MessageId = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'MessageId'),
        'MessageId',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaMancataConsegna_'
        'Type_MessageId',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            73,
            3),
    )

    MessageId = property(__MessageId.value, __MessageId.set, None, None)

    # Element PecMessageId uses Python identifier PecMessageId
    __PecMessageId = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'PecMessageId'),
        'PecMessageId',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaMancataConsegna_'
        'Type_PecMessageId',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            74,
            3),
    )

    PecMessageId = property(
        __PecMessageId.value,
        __PecMessageId.set,
        None,
        None)

    # Element Note uses Python identifier Note
    __Note = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Note'),
        'Note',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaMancataConsegna_'
        'Type_Note',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            75,
            3),
    )

    Note = property(__Note.value, __Note.set, None, None)

    # Element {http://www.w3.org/2000/09/xmldsig#}Signature uses Python
    # identifier Signature
    __Signature = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            _Namespace_ds,
            'Signature'),
        'Signature',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaMancataConsegna_'
        'Type_httpwww_w3_org200009xmldsigSignature',
        False,
        pyxb.utils.utility.Location(
            'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/'
            'xmldsig-core-schema.xsd',
            43,
            0),
    )

    Signature = property(__Signature.value, __Signature.set, None, None)

    # Attribute versione uses Python identifier versione
    __versione = pyxb.binding.content.AttributeUse(
        pyxb.namespace.ExpandedName(
            None,
            'versione'),
        'versione',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaMancataConsegna_'
        'Type_versione',
        Versione_Type,
        fixed=True,
        unicode_default='1.0',
        required=True)
    __versione._DeclarationLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        78,
        2)
    __versione._UseLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        78,
        2)

    versione = property(__versione.value, __versione.set, None, None)

    _ElementMap.update({
        __IdentificativoSdI.name(): __IdentificativoSdI,
        __NomeFile.name(): __NomeFile,
        __DataOraRicezione.name(): __DataOraRicezione,
        __RiferimentoArchivio.name(): __RiferimentoArchivio,
        __Descrizione.name(): __Descrizione,
        __MessageId.name(): __MessageId,
        __PecMessageId.name(): __PecMessageId,
        __Note.name(): __Note,
        __Signature.name(): __Signature
    })
    _AttributeMap.update({
        __versione.name(): __versione
    })
Namespace.addCategoryObject(
    'typeBinding',
    'NotificaMancataConsegna_Type',
    NotificaMancataConsegna_Type)


# Complex type
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}NotificaEsito_Type with
# content type ELEMENT_ONLY
class NotificaEsito_Type (pyxb.binding.basis.complexTypeDefinition):

    """Complex type
    {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}NotificaEsito_Type
    with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace,
        'NotificaEsito_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        81,
        1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdentificativoSdI uses Python identifier IdentificativoSdI
    __IdentificativoSdI = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        'IdentificativoSdI',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaEsito_'
        'Type_IdentificativoSdI',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            83,
            3),
    )

    IdentificativoSdI = property(
        __IdentificativoSdI.value,
        __IdentificativoSdI.set,
        None,
        None)

    # Element NomeFile uses Python identifier NomeFile
    __NomeFile = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NomeFile'),
        'NomeFile',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaEsito_'
        'Type_NomeFile',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            84,
            3),
    )

    NomeFile = property(__NomeFile.value, __NomeFile.set, None, None)

    # Element EsitoCommittente uses Python identifier EsitoCommittente
    __EsitoCommittente = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'EsitoCommittente'),
        'EsitoCommittente',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaEsito_'
        'Type_EsitoCommittente',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            85,
            3),
    )

    EsitoCommittente = property(
        __EsitoCommittente.value,
        __EsitoCommittente.set,
        None,
        None)

    # Element MessageId uses Python identifier MessageId
    __MessageId = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'MessageId'),
        'MessageId',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaEsito_'
        'Type_MessageId',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            86,
            3),
    )

    MessageId = property(__MessageId.value, __MessageId.set, None, None)

    # Element PecMessageId uses Python identifier PecMessageId
    __PecMessageId = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'PecMessageId'),
        'PecMessageId',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaEsito_'
        'Type_PecMessageId',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            87,
            3),
    )

    PecMessageId = property(
        __PecMessageId.value,
        __PecMessageId.set,
        None,
        None)

    # Element Note uses Python identifier Note
    __Note = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Note'),
        'Note',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaEsito_'
        'Type_Note',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            88,
            3),
    )

    Note = property(__Note.value, __Note.set, None, None)

    # Element {http://www.w3.org/2000/09/xmldsig#}Signature uses Python
    # identifier Signature
    __Signature = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            _Namespace_ds,
            'Signature'),
        'Signature',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaEsito_'
        'Type_httpwww_w3_org200009xmldsigSignature',
        False,
        pyxb.utils.utility.Location(
            'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/'
            'xmldsig-core-schema.xsd',
            43,
            0),
    )

    Signature = property(__Signature.value, __Signature.set, None, None)

    # Attribute versione uses Python identifier versione
    __versione = pyxb.binding.content.AttributeUse(
        pyxb.namespace.ExpandedName(
            None,
            'versione'),
        'versione',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaEsito_'
        'Type_versione',
        Versione_Type,
        fixed=True,
        unicode_default='1.0',
        required=True)
    __versione._DeclarationLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        91,
        2)
    __versione._UseLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        91,
        2)

    versione = property(__versione.value, __versione.set, None, None)

    # Attribute IntermediarioConDupliceRuolo uses Python identifier
    # IntermediarioConDupliceRuolo
    __IntermediarioConDupliceRuolo = pyxb.binding.content.AttributeUse(
        pyxb.namespace.ExpandedName(
            None,
            'IntermediarioConDupliceRuolo'),
        'IntermediarioConDupliceRuolo',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaEsito_'
        'Type_IntermediarioConDupliceRuolo',
        pyxb.binding.datatypes.string,
        fixed=True,
        unicode_default='Si')
    __IntermediarioConDupliceRuolo._DeclarationLocation = (
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            92,
            2))
    __IntermediarioConDupliceRuolo._UseLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        92,
        2)

    IntermediarioConDupliceRuolo = property(
        __IntermediarioConDupliceRuolo.value,
        __IntermediarioConDupliceRuolo.set,
        None,
        None)

    _ElementMap.update({
        __IdentificativoSdI.name(): __IdentificativoSdI,
        __NomeFile.name(): __NomeFile,
        __EsitoCommittente.name(): __EsitoCommittente,
        __MessageId.name(): __MessageId,
        __PecMessageId.name(): __PecMessageId,
        __Note.name(): __Note,
        __Signature.name(): __Signature
    })
    _AttributeMap.update({
        __versione.name(): __versione,
        __IntermediarioConDupliceRuolo.name(): __IntermediarioConDupliceRuolo
    })
Namespace.addCategoryObject(
    'typeBinding',
    'NotificaEsito_Type',
    NotificaEsito_Type)


# Complex type
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}AttestazioneTrasmissioneFattura_Type
# with content type ELEMENT_ONLY
class AttestazioneTrasmissioneFattura_Type (
        pyxb.binding.basis.complexTypeDefinition):

    """Complex type
    {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}
    AttestazioneTrasmissioneFattura_Type
    with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace,
        'AttestazioneTrasmissioneFattura_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        95,
        1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdentificativoSdI uses Python identifier IdentificativoSdI
    __IdentificativoSdI = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        'IdentificativoSdI',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_AttestazioneTrasmissione'
        'Fattura_Type_IdentificativoSdI',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            97,
            3),
    )

    IdentificativoSdI = property(
        __IdentificativoSdI.value,
        __IdentificativoSdI.set,
        None,
        None)

    # Element NomeFile uses Python identifier NomeFile
    __NomeFile = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NomeFile'),
        'NomeFile',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_AttestazioneTrasmissione'
        'Fattura_Type_NomeFile',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            98,
            3),
    )

    NomeFile = property(__NomeFile.value, __NomeFile.set, None, None)

    # Element DataOraRicezione uses Python identifier DataOraRicezione
    __DataOraRicezione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DataOraRicezione'),
        'DataOraRicezione',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_AttestazioneTrasmissione'
        'Fattura_Type_DataOraRicezione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            99,
            3),
    )

    DataOraRicezione = property(
        __DataOraRicezione.value,
        __DataOraRicezione.set,
        None,
        None)

    # Element RiferimentoArchivio uses Python identifier RiferimentoArchivio
    __RiferimentoArchivio = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoArchivio'),
        'RiferimentoArchivio',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_AttestazioneTrasmissione'
        'Fattura_Type_RiferimentoArchivio',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            100,
            3),
    )

    RiferimentoArchivio = property(
        __RiferimentoArchivio.value,
        __RiferimentoArchivio.set,
        None,
        None)

    # Element Destinatario uses Python identifier Destinatario
    __Destinatario = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Destinatario'),
        'Destinatario',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_AttestazioneTrasmissione'
        'Fattura_Type_Destinatario',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            101,
            3),
    )

    Destinatario = property(
        __Destinatario.value,
        __Destinatario.set,
        None,
        None)

    # Element MessageId uses Python identifier MessageId
    __MessageId = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'MessageId'),
        'MessageId',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_AttestazioneTrasmissione'
        'Fattura_Type_MessageId',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            102,
            3),
    )

    MessageId = property(__MessageId.value, __MessageId.set, None, None)

    # Element PecMessageId uses Python identifier PecMessageId
    __PecMessageId = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'PecMessageId'),
        'PecMessageId',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_AttestazioneTrasmissione'
        'Fattura_Type_PecMessageId',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            103,
            3),
    )

    PecMessageId = property(
        __PecMessageId.value,
        __PecMessageId.set,
        None,
        None)

    # Element Note uses Python identifier Note
    __Note = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Note'),
        'Note',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_AttestazioneTrasmissione'
        'Fattura_Type_Note',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            104,
            3),
    )

    Note = property(__Note.value, __Note.set, None, None)

    # Element HashFileOriginale uses Python identifier HashFileOriginale
    __HashFileOriginale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'HashFileOriginale'),
        'HashFileOriginale',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_AttestazioneTrasmissione'
        'Fattura_Type_HashFileOriginale',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            105,
            3),
    )

    HashFileOriginale = property(
        __HashFileOriginale.value,
        __HashFileOriginale.set,
        None,
        None)

    # Element {http://www.w3.org/2000/09/xmldsig#}Signature uses Python
    # identifier Signature
    __Signature = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            _Namespace_ds,
            'Signature'),
        'Signature',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_'
        'AttestazioneTrasmissioneFattura_Type_'
        'httpwww_w3_org200009xmldsigSignature',
        False,
        pyxb.utils.utility.Location(
            'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/'
            'xmldsig-core-schema.xsd',
            43,
            0),
    )

    Signature = property(__Signature.value, __Signature.set, None, None)

    # Attribute versione uses Python identifier versione
    __versione = pyxb.binding.content.AttributeUse(
        pyxb.namespace.ExpandedName(
            None,
            'versione'),
        'versione',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_'
        'AttestazioneTrasmissioneFattura_Type_versione',
        Versione_Type,
        fixed=True,
        unicode_default='1.0',
        required=True)
    __versione._DeclarationLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        108,
        2)
    __versione._UseLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        108,
        2)

    versione = property(__versione.value, __versione.set, None, None)

    _ElementMap.update({
        __IdentificativoSdI.name(): __IdentificativoSdI,
        __NomeFile.name(): __NomeFile,
        __DataOraRicezione.name(): __DataOraRicezione,
        __RiferimentoArchivio.name(): __RiferimentoArchivio,
        __Destinatario.name(): __Destinatario,
        __MessageId.name(): __MessageId,
        __PecMessageId.name(): __PecMessageId,
        __Note.name(): __Note,
        __HashFileOriginale.name(): __HashFileOriginale,
        __Signature.name(): __Signature
    })
    _AttributeMap.update({
        __versione.name(): __versione
    })
Namespace.addCategoryObject(
    'typeBinding',
    'AttestazioneTrasmissioneFattura_Type',
    AttestazioneTrasmissioneFattura_Type)


# Complex type
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}MetadatiInvioFile_Type
# with content type ELEMENT_ONLY
class MetadatiInvioFile_Type (pyxb.binding.basis.complexTypeDefinition):

    """Complex type
    {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}MetadatiInvioFile_Type
    with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace,
        'MetadatiInvioFile_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        140,
        1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdentificativoSdI uses Python identifier IdentificativoSdI
    __IdentificativoSdI = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        'IdentificativoSdI',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_MetadatiInvioFile_'
        'Type_IdentificativoSdI',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            142,
            3),
    )

    IdentificativoSdI = property(
        __IdentificativoSdI.value,
        __IdentificativoSdI.set,
        None,
        None)

    # Element NomeFile uses Python identifier NomeFile
    __NomeFile = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NomeFile'),
        'NomeFile',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_MetadatiInvioFile_'
        'Type_NomeFile',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            143,
            3),
    )

    NomeFile = property(__NomeFile.value, __NomeFile.set, None, None)

    # Element CodiceDestinatario uses Python identifier CodiceDestinatario
    __CodiceDestinatario = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceDestinatario'),
        'CodiceDestinatario',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_MetadatiInvioFile_'
        'Type_CodiceDestinatario',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            144,
            3),
    )

    CodiceDestinatario = property(
        __CodiceDestinatario.value,
        __CodiceDestinatario.set,
        None,
        None)

    # Element Formato uses Python identifier Formato
    __Formato = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Formato'),
        'Formato',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_MetadatiInvioFile_'
        'Type_Formato',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            145,
            3),
    )

    Formato = property(__Formato.value, __Formato.set, None, None)

    # Element TentativiInvio uses Python identifier TentativiInvio
    __TentativiInvio = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'TentativiInvio'),
        'TentativiInvio',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_MetadatiInvioFile_'
        'Type_TentativiInvio',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            146,
            3),
    )

    TentativiInvio = property(
        __TentativiInvio.value,
        __TentativiInvio.set,
        None,
        None)

    # Element MessageId uses Python identifier MessageId
    __MessageId = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'MessageId'),
        'MessageId',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_MetadatiInvioFile_'
        'Type_MessageId',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            147,
            3),
    )

    MessageId = property(__MessageId.value, __MessageId.set, None, None)

    # Element Note uses Python identifier Note
    __Note = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Note'),
        'Note',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_MetadatiInvioFile_'
        'Type_Note',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            148,
            3),
    )

    Note = property(__Note.value, __Note.set, None, None)

    # Attribute versione uses Python identifier versione
    __versione = pyxb.binding.content.AttributeUse(
        pyxb.namespace.ExpandedName(
            None,
            'versione'),
        'versione',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_MetadatiInvioFile_'
        'Type_versione',
        Versione_Type,
        fixed=True,
        unicode_default='1.0',
        required=True)
    __versione._DeclarationLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        150,
        2)
    __versione._UseLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        150,
        2)

    versione = property(__versione.value, __versione.set, None, None)

    _ElementMap.update({
        __IdentificativoSdI.name(): __IdentificativoSdI,
        __NomeFile.name(): __NomeFile,
        __CodiceDestinatario.name(): __CodiceDestinatario,
        __Formato.name(): __Formato,
        __TentativiInvio.name(): __TentativiInvio,
        __MessageId.name(): __MessageId,
        __Note.name(): __Note
    })
    _AttributeMap.update({
        __versione.name(): __versione
    })
Namespace.addCategoryObject(
    'typeBinding',
    'MetadatiInvioFile_Type',
    MetadatiInvioFile_Type)


# Complex type
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}NotificaEsitoCommittente_Type
# with content type ELEMENT_ONLY
class NotificaEsitoCommittente_Type (pyxb.binding.basis.complexTypeDefinition):

    """Complex type
    {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}
    NotificaEsitoCommittente_Type
    with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace,
        'NotificaEsitoCommittente_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        153,
        1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdentificativoSdI uses Python identifier IdentificativoSdI
    __IdentificativoSdI = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        'IdentificativoSdI',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaEsitoCommittente_'
        'Type_IdentificativoSdI',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            155,
            3),
    )

    IdentificativoSdI = property(
        __IdentificativoSdI.value,
        __IdentificativoSdI.set,
        None,
        None)

    # Element RiferimentoFattura uses Python identifier RiferimentoFattura
    __RiferimentoFattura = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoFattura'),
        'RiferimentoFattura',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaEsitoCommittente_'
        'Type_RiferimentoFattura',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            156,
            3),
    )

    RiferimentoFattura = property(
        __RiferimentoFattura.value,
        __RiferimentoFattura.set,
        None,
        None)

    # Element Esito uses Python identifier Esito
    __Esito = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Esito'),
        'Esito',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaEsitoCommittente_'
        'Type_Esito',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            157,
            3),
    )

    Esito = property(__Esito.value, __Esito.set, None, None)

    # Element Descrizione uses Python identifier Descrizione
    __Descrizione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Descrizione'),
        'Descrizione',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaEsitoCommittente_'
        'Type_Descrizione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            158,
            3),
    )

    Descrizione = property(__Descrizione.value, __Descrizione.set, None, None)

    # Element MessageIdCommittente uses Python identifier MessageIdCommittente
    __MessageIdCommittente = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'MessageIdCommittente'),
        'MessageIdCommittente',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaEsitoCommittente_'
        'Type_MessageIdCommittente',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            159,
            3),
    )

    MessageIdCommittente = property(
        __MessageIdCommittente.value,
        __MessageIdCommittente.set,
        None,
        None)

    # Element {http://www.w3.org/2000/09/xmldsig#}Signature uses Python
    # identifier Signature
    __Signature = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            _Namespace_ds,
            'Signature'),
        'Signature',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaEsitoCommittente_'
        'Type_httpwww_w3_org200009xmldsigSignature',
        False,
        pyxb.utils.utility.Location(
            'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/'
            'xmldsig-core-schema.xsd',
            43,
            0),
    )

    Signature = property(__Signature.value, __Signature.set, None, None)

    # Attribute versione uses Python identifier versione
    __versione = pyxb.binding.content.AttributeUse(
        pyxb.namespace.ExpandedName(
            None,
            'versione'),
        'versione',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaEsitoCommittente_'
        'Type_versione',
        Versione_Type,
        fixed=True,
        unicode_default='1.0',
        required=True)
    __versione._DeclarationLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        162,
        2)
    __versione._UseLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        162,
        2)

    versione = property(__versione.value, __versione.set, None, None)

    _ElementMap.update({
        __IdentificativoSdI.name(): __IdentificativoSdI,
        __RiferimentoFattura.name(): __RiferimentoFattura,
        __Esito.name(): __Esito,
        __Descrizione.name(): __Descrizione,
        __MessageIdCommittente.name(): __MessageIdCommittente,
        __Signature.name(): __Signature
    })
    _AttributeMap.update({
        __versione.name(): __versione
    })
Namespace.addCategoryObject(
    'typeBinding',
    'NotificaEsitoCommittente_Type',
    NotificaEsitoCommittente_Type)


# Complex type
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}ScartoEsitoCommittente_Type
# with content type ELEMENT_ONLY
class ScartoEsitoCommittente_Type (pyxb.binding.basis.complexTypeDefinition):

    """Complex type
    {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}ScartoEsitoCommittente_Type
    with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace,
        'ScartoEsitoCommittente_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        165,
        1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdentificativoSdI uses Python identifier IdentificativoSdI
    __IdentificativoSdI = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        'IdentificativoSdI',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_ScartoEsitoCommittente_'
        'Type_IdentificativoSdI',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            167,
            3),
    )

    IdentificativoSdI = property(
        __IdentificativoSdI.value,
        __IdentificativoSdI.set,
        None,
        None)

    # Element RiferimentoFattura uses Python identifier RiferimentoFattura
    __RiferimentoFattura = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoFattura'),
        'RiferimentoFattura',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_ScartoEsitoCommittente_'
        'Type_RiferimentoFattura',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            168,
            3),
    )

    RiferimentoFattura = property(
        __RiferimentoFattura.value,
        __RiferimentoFattura.set,
        None,
        None)

    # Element Scarto uses Python identifier Scarto
    __Scarto = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Scarto'),
        'Scarto',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_ScartoEsitoCommittente_'
        'Type_Scarto',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            169,
            3),
    )

    Scarto = property(__Scarto.value, __Scarto.set, None, None)

    # Element MessageId uses Python identifier MessageId
    __MessageId = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'MessageId'),
        'MessageId',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_ScartoEsitoCommittente_'
        'Type_MessageId',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            170,
            3),
    )

    MessageId = property(__MessageId.value, __MessageId.set, None, None)

    # Element MessageIdCommittente uses Python identifier MessageIdCommittente
    __MessageIdCommittente = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'MessageIdCommittente'),
        'MessageIdCommittente',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_ScartoEsitoCommittente_'
        'Type_MessageIdCommittente',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            171,
            3),
    )

    MessageIdCommittente = property(
        __MessageIdCommittente.value,
        __MessageIdCommittente.set,
        None,
        None)

    # Element PecMessageId uses Python identifier PecMessageId
    __PecMessageId = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'PecMessageId'),
        'PecMessageId',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_ScartoEsitoCommittente_'
        'Type_PecMessageId',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            172,
            3),
    )

    PecMessageId = property(
        __PecMessageId.value,
        __PecMessageId.set,
        None,
        None)

    # Element Note uses Python identifier Note
    __Note = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Note'),
        'Note',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_ScartoEsitoCommittente_'
        'Type_Note',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            173,
            3),
    )

    Note = property(__Note.value, __Note.set, None, None)

    # Element {http://www.w3.org/2000/09/xmldsig#}Signature uses Python
    # identifier Signature
    __Signature = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            _Namespace_ds,
            'Signature'),
        'Signature',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_ScartoEsitoCommittente_'
        'Type_httpwww_w3_org200009xmldsigSignature',
        False,
        pyxb.utils.utility.Location(
            'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/'
            'xmldsig-core-schema.xsd',
            43,
            0),
    )

    Signature = property(__Signature.value, __Signature.set, None, None)

    # Attribute versione uses Python identifier versione
    __versione = pyxb.binding.content.AttributeUse(
        pyxb.namespace.ExpandedName(
            None,
            'versione'),
        'versione',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_ScartoEsitoCommittente_'
        'Type_versione',
        Versione_Type,
        fixed=True,
        unicode_default='1.0',
        required=True)
    __versione._DeclarationLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        176,
        2)
    __versione._UseLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        176,
        2)

    versione = property(__versione.value, __versione.set, None, None)

    _ElementMap.update({
        __IdentificativoSdI.name(): __IdentificativoSdI,
        __RiferimentoFattura.name(): __RiferimentoFattura,
        __Scarto.name(): __Scarto,
        __MessageId.name(): __MessageId,
        __MessageIdCommittente.name(): __MessageIdCommittente,
        __PecMessageId.name(): __PecMessageId,
        __Note.name(): __Note,
        __Signature.name(): __Signature
    })
    _AttributeMap.update({
        __versione.name(): __versione
    })
Namespace.addCategoryObject(
    'typeBinding',
    'ScartoEsitoCommittente_Type',
    ScartoEsitoCommittente_Type)


# Complex type
# {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}NotificaDecorrenzaTermini_Type
# with content type ELEMENT_ONLY
class NotificaDecorrenzaTermini_Type (
        pyxb.binding.basis.complexTypeDefinition):

    """Complex type
    {http://www.fatturapa.gov.it/sdi/messaggi/v1.0}
    NotificaDecorrenzaTermini_Type
    with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace,
        'NotificaDecorrenzaTermini_Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        179,
        1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdentificativoSdI uses Python identifier IdentificativoSdI
    __IdentificativoSdI = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        'IdentificativoSdI',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaDecorrenzaTermini_'
        'Type_IdentificativoSdI',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            181,
            3),
    )

    IdentificativoSdI = property(
        __IdentificativoSdI.value,
        __IdentificativoSdI.set,
        None,
        None)

    # Element RiferimentoFattura uses Python identifier RiferimentoFattura
    __RiferimentoFattura = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoFattura'),
        'RiferimentoFattura',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaDecorrenzaTermini_'
        'Type_RiferimentoFattura',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            182,
            3),
    )

    RiferimentoFattura = property(
        __RiferimentoFattura.value,
        __RiferimentoFattura.set,
        None,
        None)

    # Element NomeFile uses Python identifier NomeFile
    __NomeFile = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NomeFile'),
        'NomeFile',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaDecorrenzaTermini_'
        'Type_NomeFile',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            183,
            3),
    )

    NomeFile = property(__NomeFile.value, __NomeFile.set, None, None)

    # Element Descrizione uses Python identifier Descrizione
    __Descrizione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Descrizione'),
        'Descrizione',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaDecorrenzaTermini_'
        'Type_Descrizione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            184,
            3),
    )

    Descrizione = property(__Descrizione.value, __Descrizione.set, None, None)

    # Element MessageId uses Python identifier MessageId
    __MessageId = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'MessageId'),
        'MessageId',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaDecorrenzaTermini_'
        'Type_MessageId',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            185,
            3),
    )

    MessageId = property(__MessageId.value, __MessageId.set, None, None)

    # Element PecMessageId uses Python identifier PecMessageId
    __PecMessageId = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'PecMessageId'),
        'PecMessageId',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaDecorrenzaTermini_'
        'Type_PecMessageId',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            186,
            3),
    )

    PecMessageId = property(
        __PecMessageId.value,
        __PecMessageId.set,
        None,
        None)

    # Element Note uses Python identifier Note
    __Note = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Note'),
        'Note',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaDecorrenzaTermini_'
        'Type_Note',
        False,
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            187,
            3),
    )

    Note = property(__Note.value, __Note.set, None, None)

    # Element {http://www.w3.org/2000/09/xmldsig#}Signature uses Python
    # identifier Signature
    __Signature = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            _Namespace_ds,
            'Signature'),
        'Signature',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaDecorrenzaTermini_'
        'Type_httpwww_w3_org200009xmldsigSignature',
        False,
        pyxb.utils.utility.Location(
            'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/'
            'xmldsig-core-schema.xsd',
            43,
            0),
    )

    Signature = property(__Signature.value, __Signature.set, None, None)

    # Attribute versione uses Python identifier versione
    __versione = pyxb.binding.content.AttributeUse(
        pyxb.namespace.ExpandedName(
            None,
            'versione'),
        'versione',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaDecorrenzaTermini_'
        'Type_versione',
        Versione_Type,
        fixed=True,
        unicode_default='1.0',
        required=True)
    __versione._DeclarationLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        190,
        2)
    __versione._UseLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        190,
        2)

    versione = property(__versione.value, __versione.set, None, None)

    # Attribute IntermediarioConDupliceRuolo uses Python identifier
    # IntermediarioConDupliceRuolo
    __IntermediarioConDupliceRuolo = pyxb.binding.content.AttributeUse(
        pyxb.namespace.ExpandedName(
            None,
            'IntermediarioConDupliceRuolo'),
        'IntermediarioConDupliceRuolo',
        '__httpwww_fatturapa_gov_itsdimessaggiv1_0_NotificaDecorrenzaTermini_'
        'Type_IntermediarioConDupliceRuolo',
        pyxb.binding.datatypes.string,
        fixed=True,
        unicode_default='Si')
    __IntermediarioConDupliceRuolo._DeclarationLocation = (
        pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            191,
            2))
    __IntermediarioConDupliceRuolo._UseLocation = pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        191,
        2)

    IntermediarioConDupliceRuolo = property(
        __IntermediarioConDupliceRuolo.value,
        __IntermediarioConDupliceRuolo.set,
        None,
        None)

    _ElementMap.update({
        __IdentificativoSdI.name(): __IdentificativoSdI,
        __RiferimentoFattura.name(): __RiferimentoFattura,
        __NomeFile.name(): __NomeFile,
        __Descrizione.name(): __Descrizione,
        __MessageId.name(): __MessageId,
        __PecMessageId.name(): __PecMessageId,
        __Note.name(): __Note,
        __Signature.name(): __Signature
    })
    _AttributeMap.update({
        __versione.name(): __versione,
        __IntermediarioConDupliceRuolo.name(): __IntermediarioConDupliceRuolo
    })
Namespace.addCategoryObject(
    'typeBinding',
    'NotificaDecorrenzaTermini_Type',
    NotificaDecorrenzaTermini_Type)


RicevutaConsegna = pyxb.binding.basis.element(
    pyxb.namespace.ExpandedName(
        Namespace,
        'RicevutaConsegna'),
    RicevutaConsegna_Type,
    location=pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        13,
        1))
Namespace.addCategoryObject(
    'elementBinding',
    RicevutaConsegna.name().localName(),
    RicevutaConsegna)

NotificaMancataConsegna = pyxb.binding.basis.element(
    pyxb.namespace.ExpandedName(
        Namespace,
        'NotificaMancataConsegna'),
    NotificaMancataConsegna_Type,
    location=pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        14,
        1))
Namespace.addCategoryObject(
    'elementBinding',
    NotificaMancataConsegna.name().localName(),
    NotificaMancataConsegna)

NotificaScarto = pyxb.binding.basis.element(
    pyxb.namespace.ExpandedName(
        Namespace,
        'NotificaScarto'),
    NotificaScarto_Type,
    location=pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        15,
        1))
Namespace.addCategoryObject(
    'elementBinding',
    NotificaScarto.name().localName(),
    NotificaScarto)

NotificaEsito = pyxb.binding.basis.element(
    pyxb.namespace.ExpandedName(
        Namespace,
        'NotificaEsito'),
    NotificaEsito_Type,
    location=pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        16,
        1))
Namespace.addCategoryObject(
    'elementBinding',
    NotificaEsito.name().localName(),
    NotificaEsito)

AttestazioneTrasmissioneFattura = pyxb.binding.basis.element(
    pyxb.namespace.ExpandedName(
        Namespace,
        'AttestazioneTrasmissioneFattura'),
    AttestazioneTrasmissioneFattura_Type,
    location=pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        17,
        1))
Namespace.addCategoryObject(
    'elementBinding',
    AttestazioneTrasmissioneFattura.name().localName(),
    AttestazioneTrasmissioneFattura)

MetadatiInvioFile = pyxb.binding.basis.element(
    pyxb.namespace.ExpandedName(
        Namespace,
        'MetadatiInvioFile'),
    MetadatiInvioFile_Type,
    location=pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        22,
        1))
Namespace.addCategoryObject(
    'elementBinding',
    MetadatiInvioFile.name().localName(),
    MetadatiInvioFile)

NotificaEsitoCommittente = pyxb.binding.basis.element(
    pyxb.namespace.ExpandedName(
        Namespace,
        'NotificaEsitoCommittente'),
    NotificaEsitoCommittente_Type,
    location=pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        23,
        1))
Namespace.addCategoryObject(
    'elementBinding',
    NotificaEsitoCommittente.name().localName(),
    NotificaEsitoCommittente)

ScartoEsitoCommittente = pyxb.binding.basis.element(
    pyxb.namespace.ExpandedName(
        Namespace,
        'ScartoEsitoCommittente'),
    ScartoEsitoCommittente_Type,
    location=pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        24,
        1))
Namespace.addCategoryObject(
    'elementBinding',
    ScartoEsitoCommittente.name().localName(),
    ScartoEsitoCommittente)

NotificaDecorrenzaTermini = pyxb.binding.basis.element(
    pyxb.namespace.ExpandedName(
        Namespace,
        'NotificaDecorrenzaTermini'),
    NotificaDecorrenzaTermini_Type,
    location=pyxb.utils.utility.Location(
        '/tmp/MessaggiTypes_v1.1.xsd',
        29,
        1))
Namespace.addCategoryObject(
    'elementBinding',
    NotificaDecorrenzaTermini.name().localName(),
    NotificaDecorrenzaTermini)


RiferimentoArchivio_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        IdentificativoSdI_Type,
        scope=RiferimentoArchivio_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            113,
            3)))

RiferimentoArchivio_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NomeFile'),
        NomeFile_Type,
        scope=RiferimentoArchivio_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            114,
            3)))


def _BuildAutomaton():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        RiferimentoArchivio_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IdentificativoSdI')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 113, 3))
    st_0 = fac.State(
        symbol,
        is_initial=True,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        RiferimentoArchivio_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NomeFile')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 114, 3))
    st_1 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
RiferimentoArchivio_Type._Automaton = _BuildAutomaton()


ListaErrori_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Errore'),
        Errore_Type,
        scope=ListaErrori_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            120,
            3)))


def _BuildAutomaton_():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=1,
        max=200,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            120,
            3))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(
        ListaErrori_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Errore')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 120, 3))
    st_0 = fac.State(
        symbol,
        is_initial=True,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True)]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ListaErrori_Type._Automaton = _BuildAutomaton_()


Errore_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Codice'),
        Codice_Type,
        scope=Errore_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            126,
            3)))

Errore_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Descrizione'),
        Descrizione_Type,
        scope=Errore_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            127,
            3)))


def _BuildAutomaton_2():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        Errore_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Codice')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 126, 3))
    st_0 = fac.State(
        symbol,
        is_initial=True,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        Errore_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Descrizione')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 127, 3))
    st_1 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Errore_Type._Automaton = _BuildAutomaton_2()


RiferimentoFattura_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NumeroFattura'),
        NumeroFattura_Type,
        scope=RiferimentoFattura_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            261,
            3)))

RiferimentoFattura_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'AnnoFattura'),
        AnnoFattura_Type,
        scope=RiferimentoFattura_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            262,
            3)))

RiferimentoFattura_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'PosizioneFattura'),
        pyxb.binding.datatypes.positiveInteger,
        scope=RiferimentoFattura_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            263,
            3)))


def _BuildAutomaton_3():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            263,
            3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        RiferimentoFattura_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NumeroFattura')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 261, 3))
    st_0 = fac.State(
        symbol,
        is_initial=True,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        RiferimentoFattura_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'AnnoFattura')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 262, 3))
    st_1 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(
        RiferimentoFattura_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'PosizioneFattura')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 263, 3))
    st_2 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
    ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True)]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
RiferimentoFattura_Type._Automaton = _BuildAutomaton_3()


Destinatario_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Codice'),
        CodiceDestinatario_Type,
        scope=Destinatario_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            303,
            3)))

Destinatario_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Descrizione'),
        pyxb.binding.datatypes.string,
        scope=Destinatario_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            304,
            3)))


def _BuildAutomaton_4():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        Destinatario_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Codice')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 303, 3))
    st_0 = fac.State(
        symbol,
        is_initial=True,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        Destinatario_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Descrizione')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 304, 3))
    st_1 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Destinatario_Type._Automaton = _BuildAutomaton_4()


RicevutaConsegna_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        IdentificativoSdI_Type,
        scope=RicevutaConsegna_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            36,
            3)))

RicevutaConsegna_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NomeFile'),
        NomeFile_Type,
        scope=RicevutaConsegna_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            37,
            3)))

RicevutaConsegna_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DataOraRicezione'),
        pyxb.binding.datatypes.dateTime,
        scope=RicevutaConsegna_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            38,
            3)))

RicevutaConsegna_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DataOraConsegna'),
        pyxb.binding.datatypes.dateTime,
        scope=RicevutaConsegna_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            39,
            3)))

RicevutaConsegna_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Destinatario'),
        Destinatario_Type,
        scope=RicevutaConsegna_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            40,
            3)))

RicevutaConsegna_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoArchivio'),
        RiferimentoArchivio_Type,
        scope=RicevutaConsegna_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            41,
            3)))

RicevutaConsegna_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'MessageId'),
        MessageId_Type,
        scope=RicevutaConsegna_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            42,
            3)))

RicevutaConsegna_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'PecMessageId'),
        PecMessageId_Type,
        scope=RicevutaConsegna_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            43,
            3)))

RicevutaConsegna_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Note'),
        pyxb.binding.datatypes.string,
        scope=RicevutaConsegna_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            44,
            3)))

RicevutaConsegna_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            _Namespace_ds,
            'Signature'),
        _ImportedBinding__ds.SignatureType,
        scope=RicevutaConsegna_Type,
        location=pyxb.utils.utility.Location(
            'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/'
            'xmldsig-core-schema.xsd',
            43,
            0)))


def _BuildAutomaton_5():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            41,
            3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            43,
            3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            44,
            3))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        RicevutaConsegna_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IdentificativoSdI')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 36, 3))
    st_0 = fac.State(
        symbol,
        is_initial=True,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        RicevutaConsegna_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NomeFile')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 37, 3))
    st_1 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        RicevutaConsegna_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DataOraRicezione')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 38, 3))
    st_2 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        RicevutaConsegna_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DataOraConsegna')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 39, 3))
    st_3 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        RicevutaConsegna_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Destinatario')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 40, 3))
    st_4 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        RicevutaConsegna_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'RiferimentoArchivio')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 41, 3))
    st_5 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        RicevutaConsegna_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'MessageId')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 42, 3))
    st_6 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        RicevutaConsegna_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'PecMessageId')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 43, 3))
    st_7 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        RicevutaConsegna_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Note')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 44, 3))
    st_8 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        RicevutaConsegna_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                _Namespace_ds, 'Signature')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 45, 3))
    st_9 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_9)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
    ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
    ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
    ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
    ]))
    transitions.append(fac.Transition(st_6, [
    ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False)]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
    ]))
    transitions.append(fac.Transition(st_8, [
    ]))
    transitions.append(fac.Transition(st_9, [
    ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False)]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, True)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False)]))
    st_8._set_transitionSet(transitions)
    transitions = []
    st_9._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
RicevutaConsegna_Type._Automaton = _BuildAutomaton_5()


NotificaScarto_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        IdentificativoSdI_Type,
        scope=NotificaScarto_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            53,
            3)))

NotificaScarto_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NomeFile'),
        NomeFile_Type,
        scope=NotificaScarto_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            54,
            3)))

NotificaScarto_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DataOraRicezione'),
        pyxb.binding.datatypes.dateTime,
        scope=NotificaScarto_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            55,
            3)))

NotificaScarto_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoArchivio'),
        RiferimentoArchivio_Type,
        scope=NotificaScarto_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            56,
            3)))

NotificaScarto_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'ListaErrori'),
        ListaErrori_Type,
        scope=NotificaScarto_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            57,
            3)))

NotificaScarto_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'MessageId'),
        MessageId_Type,
        scope=NotificaScarto_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            58,
            3)))

NotificaScarto_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'PecMessageId'),
        PecMessageId_Type,
        scope=NotificaScarto_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            59,
            3)))

NotificaScarto_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Note'),
        pyxb.binding.datatypes.string,
        scope=NotificaScarto_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            60,
            3)))

NotificaScarto_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            _Namespace_ds,
            'Signature'),
        _ImportedBinding__ds.SignatureType,
        scope=NotificaScarto_Type,
        location=pyxb.utils.utility.Location(
            'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/'
            'xmldsig-core-schema.xsd',
            43,
            0)))


def _BuildAutomaton_6():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            56,
            3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            59,
            3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            60,
            3))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaScarto_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IdentificativoSdI')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 53, 3))
    st_0 = fac.State(
        symbol,
        is_initial=True,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaScarto_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NomeFile')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 54, 3))
    st_1 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaScarto_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DataOraRicezione')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 55, 3))
    st_2 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaScarto_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'RiferimentoArchivio')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 56, 3))
    st_3 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaScarto_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'ListaErrori')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 57, 3))
    st_4 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaScarto_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'MessageId')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 58, 3))
    st_5 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaScarto_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'PecMessageId')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 59, 3))
    st_6 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaScarto_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Note')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 60, 3))
    st_7 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        NotificaScarto_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                _Namespace_ds, 'Signature')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 61, 3))
    st_8 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_8)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
    ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
    ]))
    transitions.append(fac.Transition(st_4, [
    ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False)]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
    ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
    ]))
    transitions.append(fac.Transition(st_7, [
    ]))
    transitions.append(fac.Transition(st_8, [
    ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False)]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, True)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False)]))
    st_7._set_transitionSet(transitions)
    transitions = []
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
NotificaScarto_Type._Automaton = _BuildAutomaton_6()


NotificaMancataConsegna_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        IdentificativoSdI_Type,
        scope=NotificaMancataConsegna_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            68,
            3)))

NotificaMancataConsegna_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NomeFile'),
        NomeFile_Type,
        scope=NotificaMancataConsegna_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            69,
            3)))

NotificaMancataConsegna_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DataOraRicezione'),
        pyxb.binding.datatypes.dateTime,
        scope=NotificaMancataConsegna_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            70,
            3)))

NotificaMancataConsegna_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoArchivio'),
        RiferimentoArchivio_Type,
        scope=NotificaMancataConsegna_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            71,
            3)))

NotificaMancataConsegna_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Descrizione'),
        Descrizione_Type,
        scope=NotificaMancataConsegna_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            72,
            3)))

NotificaMancataConsegna_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'MessageId'),
        MessageId_Type,
        scope=NotificaMancataConsegna_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            73,
            3)))

NotificaMancataConsegna_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'PecMessageId'),
        PecMessageId_Type,
        scope=NotificaMancataConsegna_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            74,
            3)))

NotificaMancataConsegna_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Note'),
        pyxb.binding.datatypes.string,
        scope=NotificaMancataConsegna_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            75,
            3)))

NotificaMancataConsegna_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            _Namespace_ds,
            'Signature'),
        _ImportedBinding__ds.SignatureType,
        scope=NotificaMancataConsegna_Type,
        location=pyxb.utils.utility.Location(
            'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/'
            'xmldsig-core-schema.xsd',
            43,
            0)))


def _BuildAutomaton_7():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            71,
            3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            72,
            3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            74,
            3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            75,
            3))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaMancataConsegna_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IdentificativoSdI')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 68, 3))
    st_0 = fac.State(
        symbol,
        is_initial=True,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaMancataConsegna_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NomeFile')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 69, 3))
    st_1 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaMancataConsegna_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DataOraRicezione')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 70, 3))
    st_2 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaMancataConsegna_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'RiferimentoArchivio')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 71, 3))
    st_3 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaMancataConsegna_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Descrizione')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 72, 3))
    st_4 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaMancataConsegna_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'MessageId')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 73, 3))
    st_5 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaMancataConsegna_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'PecMessageId')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 74, 3))
    st_6 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaMancataConsegna_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Note')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 75, 3))
    st_7 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        NotificaMancataConsegna_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                _Namespace_ds, 'Signature')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 76, 3))
    st_8 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_8)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
    ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
    ]))
    transitions.append(fac.Transition(st_4, [
    ]))
    transitions.append(fac.Transition(st_5, [
    ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False)]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False)]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
    ]))
    transitions.append(fac.Transition(st_7, [
    ]))
    transitions.append(fac.Transition(st_8, [
    ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, True)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False)]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False)]))
    st_7._set_transitionSet(transitions)
    transitions = []
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
NotificaMancataConsegna_Type._Automaton = _BuildAutomaton_7()


NotificaEsito_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        IdentificativoSdI_Type,
        scope=NotificaEsito_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            83,
            3)))

NotificaEsito_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NomeFile'),
        NomeFile_Type,
        scope=NotificaEsito_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            84,
            3)))

NotificaEsito_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'EsitoCommittente'),
        NotificaEsitoCommittente_Type,
        scope=NotificaEsito_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            85,
            3)))

NotificaEsito_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'MessageId'),
        MessageId_Type,
        scope=NotificaEsito_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            86,
            3)))

NotificaEsito_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'PecMessageId'),
        PecMessageId_Type,
        scope=NotificaEsito_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            87,
            3)))

NotificaEsito_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Note'),
        pyxb.binding.datatypes.string,
        scope=NotificaEsito_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            88,
            3)))

NotificaEsito_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            _Namespace_ds,
            'Signature'),
        _ImportedBinding__ds.SignatureType,
        scope=NotificaEsito_Type,
        location=pyxb.utils.utility.Location(
            'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/'
            'xmldsig-core-schema.xsd',
            43,
            0)))


def _BuildAutomaton_8():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            87,
            3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            88,
            3))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaEsito_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IdentificativoSdI')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 83, 3))
    st_0 = fac.State(
        symbol,
        is_initial=True,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaEsito_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NomeFile')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 84, 3))
    st_1 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaEsito_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'EsitoCommittente')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 85, 3))
    st_2 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaEsito_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'MessageId')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 86, 3))
    st_3 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaEsito_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'PecMessageId')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 87, 3))
    st_4 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaEsito_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Note')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 88, 3))
    st_5 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        NotificaEsito_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                _Namespace_ds, 'Signature')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 89, 3))
    st_6 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
    ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
    ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
    ]))
    transitions.append(fac.Transition(st_5, [
    ]))
    transitions.append(fac.Transition(st_6, [
    ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False)]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False)]))
    st_5._set_transitionSet(transitions)
    transitions = []
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
NotificaEsito_Type._Automaton = _BuildAutomaton_8()


AttestazioneTrasmissioneFattura_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        IdentificativoSdI_Type,
        scope=AttestazioneTrasmissioneFattura_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            97,
            3)))

AttestazioneTrasmissioneFattura_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NomeFile'),
        NomeFile_Type,
        scope=AttestazioneTrasmissioneFattura_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            98,
            3)))

AttestazioneTrasmissioneFattura_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DataOraRicezione'),
        pyxb.binding.datatypes.dateTime,
        scope=AttestazioneTrasmissioneFattura_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            99,
            3)))

AttestazioneTrasmissioneFattura_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoArchivio'),
        RiferimentoArchivio_Type,
        scope=AttestazioneTrasmissioneFattura_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            100,
            3)))

AttestazioneTrasmissioneFattura_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Destinatario'),
        Destinatario_Type,
        scope=AttestazioneTrasmissioneFattura_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            101,
            3)))

AttestazioneTrasmissioneFattura_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'MessageId'),
        MessageId_Type,
        scope=AttestazioneTrasmissioneFattura_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            102,
            3)))

AttestazioneTrasmissioneFattura_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'PecMessageId'),
        PecMessageId_Type,
        scope=AttestazioneTrasmissioneFattura_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            103,
            3)))

AttestazioneTrasmissioneFattura_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Note'),
        pyxb.binding.datatypes.string,
        scope=AttestazioneTrasmissioneFattura_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            104,
            3)))

AttestazioneTrasmissioneFattura_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'HashFileOriginale'),
        pyxb.binding.datatypes.string,
        scope=AttestazioneTrasmissioneFattura_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            105,
            3)))

AttestazioneTrasmissioneFattura_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            _Namespace_ds,
            'Signature'),
        _ImportedBinding__ds.SignatureType,
        scope=AttestazioneTrasmissioneFattura_Type,
        location=pyxb.utils.utility.Location(
            'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/'
            'xmldsig-core-schema.xsd',
            43,
            0)))


def _BuildAutomaton_9():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            100,
            3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            103,
            3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            104,
            3))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        AttestazioneTrasmissioneFattura_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IdentificativoSdI')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 97, 3))
    st_0 = fac.State(
        symbol,
        is_initial=True,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        AttestazioneTrasmissioneFattura_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NomeFile')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 98, 3))
    st_1 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        AttestazioneTrasmissioneFattura_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DataOraRicezione')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 99, 3))
    st_2 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        AttestazioneTrasmissioneFattura_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'RiferimentoArchivio')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 100, 3))
    st_3 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        AttestazioneTrasmissioneFattura_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Destinatario')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 101, 3))
    st_4 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        AttestazioneTrasmissioneFattura_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'MessageId')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 102, 3))
    st_5 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        AttestazioneTrasmissioneFattura_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'PecMessageId')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 103, 3))
    st_6 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        AttestazioneTrasmissioneFattura_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Note')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 104, 3))
    st_7 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        AttestazioneTrasmissioneFattura_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'HashFileOriginale')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 105, 3))
    st_8 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        AttestazioneTrasmissioneFattura_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                _Namespace_ds, 'Signature')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 106, 3))
    st_9 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_9)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
    ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
    ]))
    transitions.append(fac.Transition(st_4, [
    ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False)]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
    ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
    ]))
    transitions.append(fac.Transition(st_7, [
    ]))
    transitions.append(fac.Transition(st_8, [
    ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False)]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, True)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False)]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
    ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    st_9._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AttestazioneTrasmissioneFattura_Type._Automaton = _BuildAutomaton_9()


MetadatiInvioFile_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        IdentificativoSdI_Type,
        scope=MetadatiInvioFile_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            142,
            3)))

MetadatiInvioFile_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NomeFile'),
        NomeFile_Type,
        scope=MetadatiInvioFile_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            143,
            3)))

MetadatiInvioFile_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceDestinatario'),
        CodiceDestinatario_Type,
        scope=MetadatiInvioFile_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            144,
            3)))

MetadatiInvioFile_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Formato'),
        Formato_Type,
        scope=MetadatiInvioFile_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            145,
            3)))

MetadatiInvioFile_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'TentativiInvio'),
        pyxb.binding.datatypes.integer,
        scope=MetadatiInvioFile_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            146,
            3)))

MetadatiInvioFile_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'MessageId'),
        MessageId_Type,
        scope=MetadatiInvioFile_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            147,
            3)))

MetadatiInvioFile_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Note'),
        pyxb.binding.datatypes.string,
        scope=MetadatiInvioFile_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            148,
            3)))


def _BuildAutomaton_10():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            148,
            3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        MetadatiInvioFile_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IdentificativoSdI')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 142, 3))
    st_0 = fac.State(
        symbol,
        is_initial=True,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        MetadatiInvioFile_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NomeFile')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 143, 3))
    st_1 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        MetadatiInvioFile_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CodiceDestinatario')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 144, 3))
    st_2 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        MetadatiInvioFile_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Formato')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 145, 3))
    st_3 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        MetadatiInvioFile_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'TentativiInvio')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 146, 3))
    st_4 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        MetadatiInvioFile_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'MessageId')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 147, 3))
    st_5 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(
        MetadatiInvioFile_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Note')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 148, 3))
    st_6 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
    ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
    ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
    ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
    ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
    ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True)]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MetadatiInvioFile_Type._Automaton = _BuildAutomaton_10()


NotificaEsitoCommittente_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        IdentificativoSdI_Type,
        scope=NotificaEsitoCommittente_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            155,
            3)))

NotificaEsitoCommittente_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoFattura'),
        RiferimentoFattura_Type,
        scope=NotificaEsitoCommittente_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            156,
            3)))

NotificaEsitoCommittente_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Esito'),
        EsitoCommittente_Type,
        scope=NotificaEsitoCommittente_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            157,
            3)))

NotificaEsitoCommittente_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Descrizione'),
        Descrizione_Type,
        scope=NotificaEsitoCommittente_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            158,
            3)))

NotificaEsitoCommittente_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'MessageIdCommittente'),
        MessageId_Type,
        scope=NotificaEsitoCommittente_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            159,
            3)))

NotificaEsitoCommittente_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            _Namespace_ds,
            'Signature'),
        _ImportedBinding__ds.SignatureType,
        scope=NotificaEsitoCommittente_Type,
        location=pyxb.utils.utility.Location(
            'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/'
            'xmldsig-core-schema.xsd',
            43,
            0)))


def _BuildAutomaton_11():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            156,
            3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            158,
            3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            159,
            3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            160,
            3))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaEsitoCommittente_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IdentificativoSdI')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 155, 3))
    st_0 = fac.State(
        symbol,
        is_initial=True,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaEsitoCommittente_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'RiferimentoFattura')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 156, 3))
    st_1 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        NotificaEsitoCommittente_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Esito')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 157, 3))
    st_2 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(
        NotificaEsitoCommittente_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Descrizione')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 158, 3))
    st_3 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(
        NotificaEsitoCommittente_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'MessageIdCommittente')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 159, 3))
    st_4 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(
        NotificaEsitoCommittente_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                _Namespace_ds, 'Signature')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 160, 3))
    st_5 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    transitions.append(fac.Transition(st_2, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False)]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
    ]))
    transitions.append(fac.Transition(st_4, [
    ]))
    transitions.append(fac.Transition(st_5, [
    ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False)]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False)]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True)]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
NotificaEsitoCommittente_Type._Automaton = _BuildAutomaton_11()


ScartoEsitoCommittente_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        IdentificativoSdI_Type,
        scope=ScartoEsitoCommittente_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            167,
            3)))

ScartoEsitoCommittente_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoFattura'),
        RiferimentoFattura_Type,
        scope=ScartoEsitoCommittente_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            168,
            3)))

ScartoEsitoCommittente_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Scarto'),
        Scarto_Type,
        scope=ScartoEsitoCommittente_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            169,
            3)))

ScartoEsitoCommittente_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'MessageId'),
        MessageId_Type,
        scope=ScartoEsitoCommittente_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            170,
            3)))

ScartoEsitoCommittente_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'MessageIdCommittente'),
        MessageId_Type,
        scope=ScartoEsitoCommittente_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            171,
            3)))

ScartoEsitoCommittente_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'PecMessageId'),
        PecMessageId_Type,
        scope=ScartoEsitoCommittente_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            172,
            3)))

ScartoEsitoCommittente_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Note'),
        pyxb.binding.datatypes.string,
        scope=ScartoEsitoCommittente_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            173,
            3)))

ScartoEsitoCommittente_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            _Namespace_ds,
            'Signature'),
        _ImportedBinding__ds.SignatureType,
        scope=ScartoEsitoCommittente_Type,
        location=pyxb.utils.utility.Location(
            'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/'
            'xmldsig-core-schema.xsd',
            43,
            0)))


def _BuildAutomaton_12():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            168,
            3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            171,
            3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            172,
            3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            173,
            3))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        ScartoEsitoCommittente_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IdentificativoSdI')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 167, 3))
    st_0 = fac.State(
        symbol,
        is_initial=True,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        ScartoEsitoCommittente_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'RiferimentoFattura')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 168, 3))
    st_1 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        ScartoEsitoCommittente_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Scarto')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 169, 3))
    st_2 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        ScartoEsitoCommittente_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'MessageId')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 170, 3))
    st_3 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        ScartoEsitoCommittente_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'MessageIdCommittente')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 171, 3))
    st_4 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        ScartoEsitoCommittente_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'PecMessageId')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 172, 3))
    st_5 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        ScartoEsitoCommittente_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Note')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 173, 3))
    st_6 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        ScartoEsitoCommittente_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                _Namespace_ds, 'Signature')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 174, 3))
    st_7 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_7)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    transitions.append(fac.Transition(st_2, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False)]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
    ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
    ]))
    transitions.append(fac.Transition(st_5, [
    ]))
    transitions.append(fac.Transition(st_6, [
    ]))
    transitions.append(fac.Transition(st_7, [
    ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False)]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False)]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False)]))
    st_6._set_transitionSet(transitions)
    transitions = []
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ScartoEsitoCommittente_Type._Automaton = _BuildAutomaton_12()


NotificaDecorrenzaTermini_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IdentificativoSdI'),
        IdentificativoSdI_Type,
        scope=NotificaDecorrenzaTermini_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            181,
            3)))

NotificaDecorrenzaTermini_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoFattura'),
        RiferimentoFattura_Type,
        scope=NotificaDecorrenzaTermini_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            182,
            3)))

NotificaDecorrenzaTermini_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NomeFile'),
        NomeFile_Type,
        scope=NotificaDecorrenzaTermini_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            183,
            3)))

NotificaDecorrenzaTermini_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Descrizione'),
        Descrizione_Type,
        scope=NotificaDecorrenzaTermini_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            184,
            3)))

NotificaDecorrenzaTermini_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'MessageId'),
        MessageId_Type,
        scope=NotificaDecorrenzaTermini_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            185,
            3)))

NotificaDecorrenzaTermini_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'PecMessageId'),
        PecMessageId_Type,
        scope=NotificaDecorrenzaTermini_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            186,
            3)))

NotificaDecorrenzaTermini_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Note'),
        pyxb.binding.datatypes.string,
        scope=NotificaDecorrenzaTermini_Type,
        location=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            187,
            3)))

NotificaDecorrenzaTermini_Type._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            _Namespace_ds,
            'Signature'),
        _ImportedBinding__ds.SignatureType,
        scope=NotificaDecorrenzaTermini_Type,
        location=pyxb.utils.utility.Location(
            'http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/'
            'xmldsig-core-schema.xsd',
            43,
            0)))


def _BuildAutomaton_13():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            182,
            3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            184,
            3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            186,
            3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd',
            187,
            3))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaDecorrenzaTermini_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IdentificativoSdI')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 181, 3))
    st_0 = fac.State(
        symbol,
        is_initial=True,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaDecorrenzaTermini_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'RiferimentoFattura')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 182, 3))
    st_1 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaDecorrenzaTermini_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NomeFile')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 183, 3))
    st_2 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaDecorrenzaTermini_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Descrizione')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 184, 3))
    st_3 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaDecorrenzaTermini_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'MessageId')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 185, 3))
    st_4 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaDecorrenzaTermini_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'PecMessageId')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 186, 3))
    st_5 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        NotificaDecorrenzaTermini_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Note')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 187, 3))
    st_6 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        NotificaDecorrenzaTermini_Type._UseForTag(
            pyxb.namespace.ExpandedName(
                _Namespace_ds, 'Signature')), pyxb.utils.utility.Location(
            '/tmp/MessaggiTypes_v1.1.xsd', 188, 3))
    st_7 = fac.State(
        symbol,
        is_initial=False,
        final_update=final_update,
        is_unordered_catenation=False)
    states.append(st_7)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    transitions.append(fac.Transition(st_2, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False)]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
    ]))
    transitions.append(fac.Transition(st_4, [
    ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False)]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
    ]))
    transitions.append(fac.Transition(st_6, [
    ]))
    transitions.append(fac.Transition(st_7, [
    ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False)]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False)]))
    st_6._set_transitionSet(transitions)
    transitions = []
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
NotificaDecorrenzaTermini_Type._Automaton = _BuildAutomaton_13()
