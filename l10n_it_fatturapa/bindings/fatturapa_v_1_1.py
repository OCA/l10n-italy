# ./fatturapa_v_1_1.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:fac8120e3d9662db350b331106843ea79dd690ee
# Generated 2015-03-14 09:02:52.700921
# by PyXB version 1.2.4 using Python 2.7.8.final.0
# By Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Namespace http://www.fatturapa.gov.it/sdi/fatturapa/v1.1

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
# ~ import sys
import pyxb.utils.six as _six
# Import bindings for namespaces imported into schema
from . import _ds as _ImportedBinding__ds

import pyxb.binding.datatypes
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier(
    'urn:uuid:7a7eaf68-ca20-11e4-ba6a-08edb9323673')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.4'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)


# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI(
    'http://www.fatturapa.gov.it/sdi/fatturapa/v1.1', create_if_missing=True)
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
        fallback_namespace=default_namespace, location_base=location_base)
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

    @deprecated: Forcing use of DOM interface
    is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}VersioneSchemaType
class VersioneSchemaType (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'VersioneSchemaType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 38, 2)
    _Documentation = None
VersioneSchemaType._CF_maxLength = pyxb.binding.facets.CF_maxLength(
    value=pyxb.binding.datatypes.nonNegativeInteger(5))
VersioneSchemaType._CF_enumeration = pyxb.binding.facets.CF_enumeration(
    value_datatype=VersioneSchemaType, enum_prefix=None)
VersioneSchemaType.n1_1 = VersioneSchemaType._CF_enumeration.addEnumeration(
    unicode_value='1.1', tag='n1_1')
VersioneSchemaType._InitializeFacetMap(VersioneSchemaType._CF_maxLength,
                                       VersioneSchemaType._CF_enumeration)
Namespace.addCategoryObject(
    'typeBinding', 'VersioneSchemaType', VersioneSchemaType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}CodiceDestinatarioType


class CodiceDestinatarioType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'CodiceDestinatarioType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 58, 2)
    _Documentation = None
CodiceDestinatarioType._CF_pattern = pyxb.binding.facets.CF_pattern()
CodiceDestinatarioType._CF_pattern.addPattern(pattern='[A-Z0-9]{6}')
CodiceDestinatarioType._InitializeFacetMap(CodiceDestinatarioType._CF_pattern)
Namespace.addCategoryObject(
    'typeBinding', 'CodiceDestinatarioType', CodiceDestinatarioType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}CodiceType


class CodiceType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CodiceType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 69, 2)
    _Documentation = None
CodiceType._CF_maxLength = pyxb.binding.facets.CF_maxLength(
    value=pyxb.binding.datatypes.nonNegativeInteger(28))
CodiceType._CF_minLength = pyxb.binding.facets.CF_minLength(
    value=pyxb.binding.datatypes.nonNegativeInteger(1))
CodiceType._InitializeFacetMap(CodiceType._CF_maxLength,
                               CodiceType._CF_minLength)
Namespace.addCategoryObject('typeBinding', 'CodiceType', CodiceType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}FormatoTrasmissioneType


class FormatoTrasmissioneType (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'FormatoTrasmissioneType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 75, 2)
    _Documentation = None
FormatoTrasmissioneType._CF_length = pyxb.binding.facets.CF_length(
    value=pyxb.binding.datatypes.nonNegativeInteger(5))
FormatoTrasmissioneType._CF_enumeration = pyxb.binding.facets.CF_enumeration(
    value_datatype=FormatoTrasmissioneType, enum_prefix=None)
FormatoTrasmissioneType.SDI11 = (
    FormatoTrasmissioneType._CF_enumeration.addEnumeration(
        unicode_value='SDI11',
        tag='SDI11'))
FormatoTrasmissioneType._InitializeFacetMap(
    FormatoTrasmissioneType._CF_length,
    FormatoTrasmissioneType._CF_enumeration)
Namespace.addCategoryObject(
    'typeBinding', 'FormatoTrasmissioneType', FormatoTrasmissioneType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}IdDestinatarioCodUfficioType


class IdDestinatarioCodUfficioType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'IdDestinatarioCodUfficioType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 87, 2)
    _Documentation = None
IdDestinatarioCodUfficioType._CF_maxLength = pyxb.binding.facets.CF_maxLength(
    value=pyxb.binding.datatypes.nonNegativeInteger(16))
IdDestinatarioCodUfficioType._CF_minLength = pyxb.binding.facets.CF_minLength(
    value=pyxb.binding.datatypes.nonNegativeInteger(1))
IdDestinatarioCodUfficioType._InitializeFacetMap(
    IdDestinatarioCodUfficioType._CF_maxLength,
    IdDestinatarioCodUfficioType._CF_minLength)
Namespace.addCategoryObject(
    'typeBinding',
    'IdDestinatarioCodUfficioType',
    IdDestinatarioCodUfficioType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}CausalePagamentoType


class CausalePagamentoType (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'CausalePagamentoType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 167, 2)
    _Documentation = None
CausalePagamentoType._CF_enumeration = pyxb.binding.facets.CF_enumeration(
    value_datatype=CausalePagamentoType, enum_prefix=None)
CausalePagamentoType.A = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='A', tag='A')
CausalePagamentoType.B = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='B', tag='B')
CausalePagamentoType.C = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='C', tag='C')
CausalePagamentoType.D = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='D', tag='D')
CausalePagamentoType.E = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='E', tag='E')
CausalePagamentoType.G = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='G', tag='G')
CausalePagamentoType.H = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='H', tag='H')
CausalePagamentoType.I = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='I', tag='I')
CausalePagamentoType.L = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='L', tag='L')
CausalePagamentoType.M = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='M', tag='M')
CausalePagamentoType.N = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='N', tag='N')
CausalePagamentoType.O = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='O', tag='O')
CausalePagamentoType.P = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='P', tag='P')
CausalePagamentoType.Q = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='Q', tag='Q')
CausalePagamentoType.R = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='R', tag='R')
CausalePagamentoType.S = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='S', tag='S')
CausalePagamentoType.T = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='T', tag='T')
CausalePagamentoType.U = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='U', tag='U')
CausalePagamentoType.V = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='V', tag='V')
CausalePagamentoType.W = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='W', tag='W')
CausalePagamentoType.X = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='X', tag='X')
CausalePagamentoType.Y = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='Y', tag='Y')
CausalePagamentoType.Z = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='Z', tag='Z')
CausalePagamentoType.L1 = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='L1', tag='L1')
CausalePagamentoType.M1 = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='M1', tag='M1')
CausalePagamentoType.O1 = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='O1', tag='O1')
CausalePagamentoType.V1 = CausalePagamentoType._CF_enumeration.addEnumeration(
    unicode_value='V1', tag='V1')
CausalePagamentoType._InitializeFacetMap(CausalePagamentoType._CF_enumeration)
Namespace.addCategoryObject(
    'typeBinding', 'CausalePagamentoType', CausalePagamentoType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}TipoScontoMaggiorazioneType


class TipoScontoMaggiorazioneType (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'TipoScontoMaggiorazioneType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 199, 2)
    _Documentation = None
TipoScontoMaggiorazioneType._CF_length = pyxb.binding.facets.CF_length(
    value=pyxb.binding.datatypes.nonNegativeInteger(2))
TipoScontoMaggiorazioneType._CF_enumeration = (
    pyxb.binding.facets.CF_enumeration(
        value_datatype=TipoScontoMaggiorazioneType,
        enum_prefix=None))
TipoScontoMaggiorazioneType.SC = (
    TipoScontoMaggiorazioneType._CF_enumeration.addEnumeration(
        unicode_value='SC', tag='SC'))
TipoScontoMaggiorazioneType.MG = (
    TipoScontoMaggiorazioneType._CF_enumeration.addEnumeration(
        unicode_value='MG', tag='MG'))
TipoScontoMaggiorazioneType._InitializeFacetMap(
    TipoScontoMaggiorazioneType._CF_length,
    TipoScontoMaggiorazioneType._CF_enumeration)
Namespace.addCategoryObject(
    'typeBinding', 'TipoScontoMaggiorazioneType', TipoScontoMaggiorazioneType)

# Atomic simple type: {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}Art73Type


class Art73Type (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Art73Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 218, 2)
    _Documentation = None
Art73Type._CF_length = pyxb.binding.facets.CF_length(
    value=pyxb.binding.datatypes.nonNegativeInteger(2))
Art73Type._CF_enumeration = pyxb.binding.facets.CF_enumeration(
    value_datatype=Art73Type, enum_prefix=None)
Art73Type.SI = Art73Type._CF_enumeration.addEnumeration(
    unicode_value='SI', tag='SI')
Art73Type._InitializeFacetMap(Art73Type._CF_length,
                              Art73Type._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'Art73Type', Art73Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}TipoCassaType


class TipoCassaType (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TipoCassaType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 230, 2)
    _Documentation = None
TipoCassaType._CF_length = pyxb.binding.facets.CF_length(
    value=pyxb.binding.datatypes.nonNegativeInteger(4))
TipoCassaType._CF_enumeration = pyxb.binding.facets.CF_enumeration(
    value_datatype=TipoCassaType, enum_prefix=None)
TipoCassaType.TC01 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC01', tag='TC01')
TipoCassaType.TC02 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC02', tag='TC02')
TipoCassaType.TC03 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC03', tag='TC03')
TipoCassaType.TC04 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC04', tag='TC04')
TipoCassaType.TC05 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC05', tag='TC05')
TipoCassaType.TC06 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC06', tag='TC06')
TipoCassaType.TC07 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC07', tag='TC07')
TipoCassaType.TC08 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC08', tag='TC08')
TipoCassaType.TC09 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC09', tag='TC09')
TipoCassaType.TC10 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC10', tag='TC10')
TipoCassaType.TC11 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC11', tag='TC11')
TipoCassaType.TC12 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC12', tag='TC12')
TipoCassaType.TC13 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC13', tag='TC13')
TipoCassaType.TC14 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC14', tag='TC14')
TipoCassaType.TC15 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC15', tag='TC15')
TipoCassaType.TC16 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC16', tag='TC16')
TipoCassaType.TC17 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC17', tag='TC17')
TipoCassaType.TC18 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC18', tag='TC18')
TipoCassaType.TC19 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC19', tag='TC19')
TipoCassaType.TC20 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC20', tag='TC20')
TipoCassaType.TC21 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC21', tag='TC21')
TipoCassaType.TC22 = TipoCassaType._CF_enumeration.addEnumeration(
    unicode_value='TC22', tag='TC22')
TipoCassaType._InitializeFacetMap(TipoCassaType._CF_length,
                                  TipoCassaType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'TipoCassaType', TipoCassaType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}TipoDocumentoType


class TipoDocumentoType (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TipoDocumentoType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 389, 2)
    _Documentation = None
TipoDocumentoType._CF_length = pyxb.binding.facets.CF_length(
    value=pyxb.binding.datatypes.nonNegativeInteger(4))
TipoDocumentoType._CF_enumeration = pyxb.binding.facets.CF_enumeration(
    value_datatype=TipoDocumentoType, enum_prefix=None)
TipoDocumentoType.TD01 = TipoDocumentoType._CF_enumeration.addEnumeration(
    unicode_value='TD01', tag='TD01')
TipoDocumentoType.TD02 = TipoDocumentoType._CF_enumeration.addEnumeration(
    unicode_value='TD02', tag='TD02')
TipoDocumentoType.TD03 = TipoDocumentoType._CF_enumeration.addEnumeration(
    unicode_value='TD03', tag='TD03')
TipoDocumentoType.TD04 = TipoDocumentoType._CF_enumeration.addEnumeration(
    unicode_value='TD04', tag='TD04')
TipoDocumentoType.TD05 = TipoDocumentoType._CF_enumeration.addEnumeration(
    unicode_value='TD05', tag='TD05')
TipoDocumentoType.TD06 = TipoDocumentoType._CF_enumeration.addEnumeration(
    unicode_value='TD06', tag='TD06')
TipoDocumentoType._InitializeFacetMap(TipoDocumentoType._CF_length,
                                      TipoDocumentoType._CF_enumeration)
Namespace.addCategoryObject(
    'typeBinding', 'TipoDocumentoType', TipoDocumentoType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}TipoRitenutaType


class TipoRitenutaType (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TipoRitenutaType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 424, 2)
    _Documentation = None
TipoRitenutaType._CF_length = pyxb.binding.facets.CF_length(
    value=pyxb.binding.datatypes.nonNegativeInteger(4))
TipoRitenutaType._CF_enumeration = pyxb.binding.facets.CF_enumeration(
    value_datatype=TipoRitenutaType, enum_prefix=None)
TipoRitenutaType.RT01 = TipoRitenutaType._CF_enumeration.addEnumeration(
    unicode_value='RT01', tag='RT01')
TipoRitenutaType.RT02 = TipoRitenutaType._CF_enumeration.addEnumeration(
    unicode_value='RT02', tag='RT02')
TipoRitenutaType._InitializeFacetMap(TipoRitenutaType._CF_length,
                                     TipoRitenutaType._CF_enumeration)
Namespace.addCategoryObject(
    'typeBinding', 'TipoRitenutaType', TipoRitenutaType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}RiferimentoNumeroLineaType


class RiferimentoNumeroLineaType (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'RiferimentoNumeroLineaType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 455, 2)
    _Documentation = None

RiferimentoNumeroLineaType._CF_maxInclusive = (
    pyxb.binding.facets.CF_maxInclusive(
        value_datatype=RiferimentoNumeroLineaType,
        value=pyxb.binding.datatypes.integer(9999)))
RiferimentoNumeroLineaType._CF_minInclusive = (
    pyxb.binding.facets.CF_minInclusive(
        value_datatype=RiferimentoNumeroLineaType,
        value=pyxb.binding.datatypes.integer(1)))
RiferimentoNumeroLineaType._InitializeFacetMap(
    RiferimentoNumeroLineaType._CF_maxInclusive,
    RiferimentoNumeroLineaType._CF_minInclusive)
Namespace.addCategoryObject(
    'typeBinding', 'RiferimentoNumeroLineaType', RiferimentoNumeroLineaType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}SoggettoEmittenteType


class SoggettoEmittenteType (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'SoggettoEmittenteType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 501, 2)
    _Documentation = None
SoggettoEmittenteType._CF_length = pyxb.binding.facets.CF_length(
    value=pyxb.binding.datatypes.nonNegativeInteger(2))
SoggettoEmittenteType._CF_enumeration = pyxb.binding.facets.CF_enumeration(
    value_datatype=SoggettoEmittenteType, enum_prefix=None)
SoggettoEmittenteType.CC = (
    SoggettoEmittenteType._CF_enumeration.addEnumeration(
        unicode_value='CC', tag='CC'))
SoggettoEmittenteType.TZ = (
    SoggettoEmittenteType._CF_enumeration.addEnumeration(
        unicode_value='TZ', tag='TZ'))
SoggettoEmittenteType._InitializeFacetMap(
    SoggettoEmittenteType._CF_length,
    SoggettoEmittenteType._CF_enumeration)
Namespace.addCategoryObject(
    'typeBinding', 'SoggettoEmittenteType', SoggettoEmittenteType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}RegimeFiscaleType


class RegimeFiscaleType (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'RegimeFiscaleType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 543, 2)
    _Documentation = None
RegimeFiscaleType._CF_length = pyxb.binding.facets.CF_length(
    value=pyxb.binding.datatypes.nonNegativeInteger(4))
RegimeFiscaleType._CF_enumeration = pyxb.binding.facets.CF_enumeration(
    value_datatype=RegimeFiscaleType, enum_prefix=None)
RegimeFiscaleType.RF01 = RegimeFiscaleType._CF_enumeration.addEnumeration(
    unicode_value='RF01', tag='RF01')
RegimeFiscaleType.RF02 = RegimeFiscaleType._CF_enumeration.addEnumeration(
    unicode_value='RF02', tag='RF02')
RegimeFiscaleType.RF03 = RegimeFiscaleType._CF_enumeration.addEnumeration(
    unicode_value='RF03', tag='RF03')
RegimeFiscaleType.RF04 = RegimeFiscaleType._CF_enumeration.addEnumeration(
    unicode_value='RF04', tag='RF04')
RegimeFiscaleType.RF05 = RegimeFiscaleType._CF_enumeration.addEnumeration(
    unicode_value='RF05', tag='RF05')
RegimeFiscaleType.RF06 = RegimeFiscaleType._CF_enumeration.addEnumeration(
    unicode_value='RF06', tag='RF06')
RegimeFiscaleType.RF07 = RegimeFiscaleType._CF_enumeration.addEnumeration(
    unicode_value='RF07', tag='RF07')
RegimeFiscaleType.RF08 = RegimeFiscaleType._CF_enumeration.addEnumeration(
    unicode_value='RF08', tag='RF08')
RegimeFiscaleType.RF09 = RegimeFiscaleType._CF_enumeration.addEnumeration(
    unicode_value='RF09', tag='RF09')
RegimeFiscaleType.RF10 = RegimeFiscaleType._CF_enumeration.addEnumeration(
    unicode_value='RF10', tag='RF10')
RegimeFiscaleType.RF11 = RegimeFiscaleType._CF_enumeration.addEnumeration(
    unicode_value='RF11', tag='RF11')
RegimeFiscaleType.RF12 = RegimeFiscaleType._CF_enumeration.addEnumeration(
    unicode_value='RF12', tag='RF12')
RegimeFiscaleType.RF13 = RegimeFiscaleType._CF_enumeration.addEnumeration(
    unicode_value='RF13', tag='RF13')
RegimeFiscaleType.RF14 = RegimeFiscaleType._CF_enumeration.addEnumeration(
    unicode_value='RF14', tag='RF14')
RegimeFiscaleType.RF15 = RegimeFiscaleType._CF_enumeration.addEnumeration(
    unicode_value='RF15', tag='RF15')
RegimeFiscaleType.RF16 = RegimeFiscaleType._CF_enumeration.addEnumeration(
    unicode_value='RF16', tag='RF16')
RegimeFiscaleType.RF17 = RegimeFiscaleType._CF_enumeration.addEnumeration(
    unicode_value='RF17', tag='RF17')
RegimeFiscaleType.RF19 = RegimeFiscaleType._CF_enumeration.addEnumeration(
    unicode_value='RF19', tag='RF19')
RegimeFiscaleType.RF18 = RegimeFiscaleType._CF_enumeration.addEnumeration(
    unicode_value='RF18', tag='RF18')
RegimeFiscaleType._InitializeFacetMap(RegimeFiscaleType._CF_length,
                                      RegimeFiscaleType._CF_enumeration)
Namespace.addCategoryObject(
    'typeBinding', 'RegimeFiscaleType', RegimeFiscaleType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}CondizioniPagamentoType


class CondizioniPagamentoType (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'CondizioniPagamentoType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 759, 2)
    _Documentation = None
CondizioniPagamentoType._CF_maxLength = pyxb.binding.facets.CF_maxLength(
    value=pyxb.binding.datatypes.nonNegativeInteger(4))
CondizioniPagamentoType._CF_minLength = pyxb.binding.facets.CF_minLength(
    value=pyxb.binding.datatypes.nonNegativeInteger(4))
CondizioniPagamentoType._CF_enumeration = pyxb.binding.facets.CF_enumeration(
    value_datatype=CondizioniPagamentoType, enum_prefix=None)
CondizioniPagamentoType.TP01 = (
    CondizioniPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='TP01', tag='TP01'))
CondizioniPagamentoType.TP02 = (
    CondizioniPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='TP02', tag='TP02'))
CondizioniPagamentoType.TP03 = (
    CondizioniPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='TP03', tag='TP03'))
CondizioniPagamentoType._InitializeFacetMap(
    CondizioniPagamentoType._CF_maxLength,
    CondizioniPagamentoType._CF_minLength,
    CondizioniPagamentoType._CF_enumeration)
Namespace.addCategoryObject(
    'typeBinding', 'CondizioniPagamentoType', CondizioniPagamentoType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}ModalitaPagamentoType


class ModalitaPagamentoType (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'ModalitaPagamentoType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 805, 2)
    _Documentation = None
ModalitaPagamentoType._CF_length = pyxb.binding.facets.CF_length(
    value=pyxb.binding.datatypes.nonNegativeInteger(4))
ModalitaPagamentoType._CF_enumeration = pyxb.binding.facets.CF_enumeration(
    value_datatype=ModalitaPagamentoType, enum_prefix=None)
ModalitaPagamentoType.MP01 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP01',
        tag='MP01'))
ModalitaPagamentoType.MP02 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP02',
        tag='MP02'))
ModalitaPagamentoType.MP03 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP03',
        tag='MP03'))
ModalitaPagamentoType.MP04 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP04',
        tag='MP04'))
ModalitaPagamentoType.MP05 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP05',
        tag='MP05'))
ModalitaPagamentoType.MP06 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP06',
        tag='MP06'))
ModalitaPagamentoType.MP07 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP07',
        tag='MP07'))
ModalitaPagamentoType.MP08 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP08',
        tag='MP08'))
ModalitaPagamentoType.MP09 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP09',
        tag='MP09'))
ModalitaPagamentoType.MP10 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP10',
        tag='MP10'))
ModalitaPagamentoType.MP11 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP11',
        tag='MP11'))
ModalitaPagamentoType.MP12 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP12',
        tag='MP12'))
ModalitaPagamentoType.MP13 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP13',
        tag='MP13'))
ModalitaPagamentoType.MP14 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP14',
        tag='MP14'))
ModalitaPagamentoType.MP15 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP15',
        tag='MP15'))
ModalitaPagamentoType.MP16 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP16',
        tag='MP16'))
ModalitaPagamentoType.MP17 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP17',
        tag='MP17'))
ModalitaPagamentoType.MP18 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP18',
        tag='MP18'))
ModalitaPagamentoType.MP19 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP19',
        tag='MP19'))
ModalitaPagamentoType.MP20 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP20',
        tag='MP20'))
ModalitaPagamentoType.MP21 = (
    ModalitaPagamentoType._CF_enumeration.addEnumeration(
        unicode_value='MP21',
        tag='MP21'))
ModalitaPagamentoType._InitializeFacetMap(
    ModalitaPagamentoType._CF_length,
    ModalitaPagamentoType._CF_enumeration)
Namespace.addCategoryObject(
    'typeBinding', 'ModalitaPagamentoType', ModalitaPagamentoType)

# Atomic simple type: {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}IBANType


class IBANType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IBANType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 915, 2)
    _Documentation = None
IBANType._CF_pattern = pyxb.binding.facets.CF_pattern()
IBANType._CF_pattern.addPattern(
    pattern='[a-zA-Z]{2}[0-9]{2}[a-zA-Z0-9]{23,30}')
IBANType._InitializeFacetMap(IBANType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'IBANType', IBANType)

# Atomic simple type: {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}BICType


class BICType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'BICType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 920, 2)
    _Documentation = None
BICType._CF_pattern = pyxb.binding.facets.CF_pattern()
BICType._CF_pattern.addPattern(
    pattern='[A-Z]{6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3}){0,1}')
BICType._InitializeFacetMap(BICType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'BICType', BICType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}RitenutaType


class RitenutaType (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'RitenutaType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 992, 2)
    _Documentation = None
RitenutaType._CF_length = pyxb.binding.facets.CF_length(
    value=pyxb.binding.datatypes.nonNegativeInteger(2))
RitenutaType._CF_enumeration = pyxb.binding.facets.CF_enumeration(
    value_datatype=RitenutaType, enum_prefix=None)
RitenutaType.SI = RitenutaType._CF_enumeration.addEnumeration(
    unicode_value='SI', tag='SI')
RitenutaType._InitializeFacetMap(RitenutaType._CF_length,
                                 RitenutaType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'RitenutaType', RitenutaType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}EsigibilitaIVAType


class EsigibilitaIVAType (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'EsigibilitaIVAType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1016, 2)
    _Documentation = None
EsigibilitaIVAType._CF_maxLength = pyxb.binding.facets.CF_maxLength(
    value=pyxb.binding.datatypes.nonNegativeInteger(1))
EsigibilitaIVAType._CF_minLength = pyxb.binding.facets.CF_minLength(
    value=pyxb.binding.datatypes.nonNegativeInteger(1))
EsigibilitaIVAType._CF_enumeration = pyxb.binding.facets.CF_enumeration(
    value_datatype=EsigibilitaIVAType, enum_prefix=None)
EsigibilitaIVAType.D = EsigibilitaIVAType._CF_enumeration.addEnumeration(
    unicode_value='D', tag='D')
EsigibilitaIVAType.I = EsigibilitaIVAType._CF_enumeration.addEnumeration(
    unicode_value='I', tag='I')
EsigibilitaIVAType.S = EsigibilitaIVAType._CF_enumeration.addEnumeration(
    unicode_value='S', tag='S')
EsigibilitaIVAType._InitializeFacetMap(EsigibilitaIVAType._CF_maxLength,
                                       EsigibilitaIVAType._CF_minLength,
                                       EsigibilitaIVAType._CF_enumeration)
Namespace.addCategoryObject(
    'typeBinding', 'EsigibilitaIVAType', EsigibilitaIVAType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}NaturaType


class NaturaType (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NaturaType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1037, 2)
    _Documentation = None
NaturaType._CF_enumeration = pyxb.binding.facets.CF_enumeration(
    value_datatype=NaturaType, enum_prefix=None)
NaturaType.N1 = NaturaType._CF_enumeration.addEnumeration(
    unicode_value='N1', tag='N1')
NaturaType.N2 = NaturaType._CF_enumeration.addEnumeration(
    unicode_value='N2', tag='N2')
NaturaType.N3 = NaturaType._CF_enumeration.addEnumeration(
    unicode_value='N3', tag='N3')
NaturaType.N4 = NaturaType._CF_enumeration.addEnumeration(
    unicode_value='N4', tag='N4')
NaturaType.N5 = NaturaType._CF_enumeration.addEnumeration(
    unicode_value='N5', tag='N5')
NaturaType.N6 = NaturaType._CF_enumeration.addEnumeration(
    unicode_value='N6', tag='N6')
NaturaType._InitializeFacetMap(NaturaType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'NaturaType', NaturaType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}CodiceFiscaleType


class CodiceFiscaleType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CodiceFiscaleType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1071, 2)
    _Documentation = None
CodiceFiscaleType._CF_pattern = pyxb.binding.facets.CF_pattern()
CodiceFiscaleType._CF_pattern.addPattern(pattern='[A-Z0-9]{11,16}')
CodiceFiscaleType._InitializeFacetMap(CodiceFiscaleType._CF_pattern)
Namespace.addCategoryObject(
    'typeBinding', 'CodiceFiscaleType', CodiceFiscaleType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}CodiceFiscalePFType


class CodiceFiscalePFType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'CodiceFiscalePFType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1076, 2)
    _Documentation = None
CodiceFiscalePFType._CF_pattern = pyxb.binding.facets.CF_pattern()
CodiceFiscalePFType._CF_pattern.addPattern(pattern='[A-Z0-9]{16}')
CodiceFiscalePFType._InitializeFacetMap(CodiceFiscalePFType._CF_pattern)
Namespace.addCategoryObject(
    'typeBinding', 'CodiceFiscalePFType', CodiceFiscalePFType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}CodEORIType


class CodEORIType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CodEORIType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1081, 2)
    _Documentation = None
CodEORIType._CF_maxLength = pyxb.binding.facets.CF_maxLength(
    value=pyxb.binding.datatypes.nonNegativeInteger(17))
CodEORIType._CF_minLength = pyxb.binding.facets.CF_minLength(
    value=pyxb.binding.datatypes.nonNegativeInteger(13))
CodEORIType._InitializeFacetMap(CodEORIType._CF_maxLength,
                                CodEORIType._CF_minLength)
Namespace.addCategoryObject('typeBinding', 'CodEORIType', CodEORIType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}SocioUnicoType


class SocioUnicoType (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SocioUnicoType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1087, 2)
    _Documentation = None
SocioUnicoType._CF_enumeration = pyxb.binding.facets.CF_enumeration(
    value_datatype=SocioUnicoType, enum_prefix=None)
SocioUnicoType.SU = SocioUnicoType._CF_enumeration.addEnumeration(
    unicode_value='SU', tag='SU')
SocioUnicoType.SM = SocioUnicoType._CF_enumeration.addEnumeration(
    unicode_value='SM', tag='SM')
SocioUnicoType._InitializeFacetMap(SocioUnicoType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'SocioUnicoType', SocioUnicoType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}StatoLiquidazioneType


class StatoLiquidazioneType (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'StatoLiquidazioneType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1101, 2)
    _Documentation = None
StatoLiquidazioneType._CF_enumeration = pyxb.binding.facets.CF_enumeration(
    value_datatype=StatoLiquidazioneType, enum_prefix=None)
StatoLiquidazioneType.LS = (
    StatoLiquidazioneType._CF_enumeration.addEnumeration(
        unicode_value='LS',
        tag='LS'))
StatoLiquidazioneType.LN = (
    StatoLiquidazioneType._CF_enumeration.addEnumeration(
        unicode_value='LN',
        tag='LN'))
StatoLiquidazioneType._InitializeFacetMap(
    StatoLiquidazioneType._CF_enumeration)
Namespace.addCategoryObject(
    'typeBinding', 'StatoLiquidazioneType', StatoLiquidazioneType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}TipoCessionePrestazioneType


class TipoCessionePrestazioneType (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'TipoCessionePrestazioneType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1115, 2)
    _Documentation = None
TipoCessionePrestazioneType._CF_length = pyxb.binding.facets.CF_length(
    value=pyxb.binding.datatypes.nonNegativeInteger(2))
TipoCessionePrestazioneType._CF_enumeration = (
    pyxb.binding.facets.CF_enumeration(
        value_datatype=TipoCessionePrestazioneType,
        enum_prefix=None))
TipoCessionePrestazioneType.SC = (
    TipoCessionePrestazioneType._CF_enumeration.addEnumeration(
        unicode_value='SC',
        tag='SC'))
TipoCessionePrestazioneType.PR = (
    TipoCessionePrestazioneType._CF_enumeration.addEnumeration(
        unicode_value='PR',
        tag='PR'))
TipoCessionePrestazioneType.AB = (
    TipoCessionePrestazioneType._CF_enumeration.addEnumeration(
        unicode_value='AB',
        tag='AB'))
TipoCessionePrestazioneType.AC = (
    TipoCessionePrestazioneType._CF_enumeration.addEnumeration(
        unicode_value='AC',
        tag='AC'))
TipoCessionePrestazioneType._InitializeFacetMap(
    TipoCessionePrestazioneType._CF_length,
    TipoCessionePrestazioneType._CF_enumeration)
Namespace.addCategoryObject(
    'typeBinding', 'TipoCessionePrestazioneType', TipoCessionePrestazioneType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}TitoloType


class TitoloType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TitoloType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1140, 2)
    _Documentation = None
TitoloType._CF_pattern = pyxb.binding.facets.CF_pattern()
TitoloType._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{2,10})')
TitoloType._CF_whiteSpace = pyxb.binding.facets.CF_whiteSpace(
    value=pyxb.binding.facets._WhiteSpace_enum.collapse)
TitoloType._InitializeFacetMap(TitoloType._CF_pattern,
                               TitoloType._CF_whiteSpace)
Namespace.addCategoryObject('typeBinding', 'TitoloType', TitoloType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}String10Type


class String10Type (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String10Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1146, 2)
    _Documentation = None
String10Type._CF_pattern = pyxb.binding.facets.CF_pattern()
String10Type._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{0,10})')
String10Type._InitializeFacetMap(String10Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'String10Type', String10Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}String15Type


class String15Type (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String15Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1151, 2)
    _Documentation = None
String15Type._CF_pattern = pyxb.binding.facets.CF_pattern()
String15Type._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{0,15})')
String15Type._InitializeFacetMap(String15Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'String15Type', String15Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}String20Type


class String20Type (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String20Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1156, 2)
    _Documentation = None
String20Type._CF_pattern = pyxb.binding.facets.CF_pattern()
String20Type._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{0,20})')
String20Type._InitializeFacetMap(String20Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'String20Type', String20Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}String35Type


class String35Type (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String35Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1161, 2)
    _Documentation = None
String35Type._CF_pattern = pyxb.binding.facets.CF_pattern()
String35Type._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{0,35})')
String35Type._InitializeFacetMap(String35Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'String35Type', String35Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}String60Type


class String60Type (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String60Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1166, 2)
    _Documentation = None
String60Type._CF_pattern = pyxb.binding.facets.CF_pattern()
String60Type._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{0,60})')
String60Type._InitializeFacetMap(String60Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'String60Type', String60Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}String80Type


class String80Type (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String80Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1171, 2)
    _Documentation = None
String80Type._CF_pattern = pyxb.binding.facets.CF_pattern()
String80Type._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{0,80})')
String80Type._InitializeFacetMap(String80Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'String80Type', String80Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}String100Type


class String100Type (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String100Type')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1176, 2)
    _Documentation = None
String100Type._CF_pattern = pyxb.binding.facets.CF_pattern()
String100Type._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{0,100})')
String100Type._InitializeFacetMap(String100Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'String100Type', String100Type)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}String60LatinType


class String60LatinType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String60LatinType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1181, 2)
    _Documentation = None
String60LatinType._CF_pattern = pyxb.binding.facets.CF_pattern()
String60LatinType._CF_pattern.addPattern(
    pattern='[\\p{IsBasicLatin}\\p{IsLatin-1Supplement}]{0,60}')
String60LatinType._InitializeFacetMap(String60LatinType._CF_pattern)
Namespace.addCategoryObject(
    'typeBinding', 'String60LatinType', String60LatinType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}String80LatinType


class String80LatinType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String80LatinType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1186, 2)
    _Documentation = None
String80LatinType._CF_pattern = pyxb.binding.facets.CF_pattern()
String80LatinType._CF_pattern.addPattern(
    pattern='[\\p{IsBasicLatin}\\p{IsLatin-1Supplement}]{0,80}')
String80LatinType._InitializeFacetMap(String80LatinType._CF_pattern)
Namespace.addCategoryObject(
    'typeBinding', 'String80LatinType', String80LatinType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}String100LatinType


class String100LatinType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'String100LatinType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1191, 2)
    _Documentation = None
String100LatinType._CF_pattern = pyxb.binding.facets.CF_pattern()
String100LatinType._CF_pattern.addPattern(
    pattern='[\\p{IsBasicLatin}\\p{IsLatin-1Supplement}]{0,100}')
String100LatinType._InitializeFacetMap(String100LatinType._CF_pattern)
Namespace.addCategoryObject(
    'typeBinding', 'String100LatinType', String100LatinType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}String200LatinType


class String200LatinType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'String200LatinType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1196, 2)
    _Documentation = None
String200LatinType._CF_pattern = pyxb.binding.facets.CF_pattern()
String200LatinType._CF_pattern.addPattern(
    pattern='[\\p{IsBasicLatin}\\p{IsLatin-1Supplement}]{0,200}')
String200LatinType._InitializeFacetMap(String200LatinType._CF_pattern)
Namespace.addCategoryObject(
    'typeBinding', 'String200LatinType', String200LatinType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}String1000LatinType


class String1000LatinType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'String1000LatinType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1201, 2)
    _Documentation = None
String1000LatinType._CF_pattern = pyxb.binding.facets.CF_pattern()
String1000LatinType._CF_pattern.addPattern(
    pattern='[\\p{IsBasicLatin}\\p{IsLatin-1Supplement}]{0,1000}')
String1000LatinType._InitializeFacetMap(String1000LatinType._CF_pattern)
Namespace.addCategoryObject(
    'typeBinding', 'String1000LatinType', String1000LatinType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}ProvinciaType


class ProvinciaType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ProvinciaType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1206, 2)
    _Documentation = None
ProvinciaType._CF_pattern = pyxb.binding.facets.CF_pattern()
ProvinciaType._CF_pattern.addPattern(pattern='[A-Z]{2}')
ProvinciaType._InitializeFacetMap(ProvinciaType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'ProvinciaType', ProvinciaType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}NazioneType


class NazioneType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NazioneType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1211, 2)
    _Documentation = None
NazioneType._CF_pattern = pyxb.binding.facets.CF_pattern()
NazioneType._CF_pattern.addPattern(pattern='[A-Z]{2}')
NazioneType._InitializeFacetMap(NazioneType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'NazioneType', NazioneType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DivisaType


class DivisaType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DivisaType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1216, 2)
    _Documentation = None
DivisaType._CF_pattern = pyxb.binding.facets.CF_pattern()
DivisaType._CF_pattern.addPattern(pattern='[A-Z]{3}')
DivisaType._InitializeFacetMap(DivisaType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DivisaType', DivisaType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}TipoResaType


class TipoResaType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TipoResaType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1221, 2)
    _Documentation = None
TipoResaType._CF_pattern = pyxb.binding.facets.CF_pattern()
TipoResaType._CF_pattern.addPattern(pattern='[A-Z]{3}')
TipoResaType._InitializeFacetMap(TipoResaType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'TipoResaType', TipoResaType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}NumeroCivicoType


class NumeroCivicoType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NumeroCivicoType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1226, 2)
    _Documentation = None
NumeroCivicoType._CF_pattern = pyxb.binding.facets.CF_pattern()
NumeroCivicoType._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{1,8})')
NumeroCivicoType._InitializeFacetMap(NumeroCivicoType._CF_pattern)
Namespace.addCategoryObject(
    'typeBinding', 'NumeroCivicoType', NumeroCivicoType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}BolloVirtualeType


class BolloVirtualeType (
        pyxb.binding.datatypes.string,
        pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'BolloVirtualeType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1231, 2)
    _Documentation = None
BolloVirtualeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(
    value_datatype=BolloVirtualeType, enum_prefix=None)
BolloVirtualeType.SI = BolloVirtualeType._CF_enumeration.addEnumeration(
    unicode_value='SI', tag='SI')
BolloVirtualeType._InitializeFacetMap(BolloVirtualeType._CF_enumeration)
Namespace.addCategoryObject(
    'typeBinding', 'BolloVirtualeType', BolloVirtualeType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}TelFaxType


class TelFaxType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TelFaxType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1236, 2)
    _Documentation = None
TelFaxType._CF_pattern = pyxb.binding.facets.CF_pattern()
TelFaxType._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{5,12})')
TelFaxType._InitializeFacetMap(TelFaxType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'TelFaxType', TelFaxType)

# Atomic simple type: {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}EmailType


class EmailType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'EmailType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1241, 2)
    _Documentation = None
EmailType._CF_pattern = pyxb.binding.facets.CF_pattern()
EmailType._CF_pattern.addPattern(pattern='.+@.+[.]+.+')
EmailType._CF_maxLength = pyxb.binding.facets.CF_maxLength(
    value=pyxb.binding.datatypes.nonNegativeInteger(256))
EmailType._CF_minLength = pyxb.binding.facets.CF_minLength(
    value=pyxb.binding.datatypes.nonNegativeInteger(7))
EmailType._InitializeFacetMap(EmailType._CF_pattern,
                              EmailType._CF_maxLength,
                              EmailType._CF_minLength)
Namespace.addCategoryObject('typeBinding', 'EmailType', EmailType)

# Atomic simple type: {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}PesoType


class PesoType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PesoType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1249, 2)
    _Documentation = None
PesoType._CF_pattern = pyxb.binding.facets.CF_pattern()
PesoType._CF_pattern.addPattern(pattern='[0-9]{1,4}\\.[0-9]{1,2}')
PesoType._InitializeFacetMap(PesoType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'PesoType', PesoType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}Amount8DecimalType


class Amount8DecimalType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'Amount8DecimalType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1254, 2)
    _Documentation = None
Amount8DecimalType._CF_pattern = pyxb.binding.facets.CF_pattern()
Amount8DecimalType._CF_pattern.addPattern(
    pattern='[\\-]?[0-9]{1,11}\\.[0-9]{2,8}')
Amount8DecimalType._InitializeFacetMap(Amount8DecimalType._CF_pattern)
Namespace.addCategoryObject(
    'typeBinding', 'Amount8DecimalType', Amount8DecimalType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}Amount2DecimalType


class Amount2DecimalType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'Amount2DecimalType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1259, 2)
    _Documentation = None
Amount2DecimalType._CF_pattern = pyxb.binding.facets.CF_pattern()
Amount2DecimalType._CF_pattern.addPattern(
    pattern='[\\-]?[0-9]{1,11}\\.[0-9]{2}')
Amount2DecimalType._InitializeFacetMap(Amount2DecimalType._CF_pattern)
Namespace.addCategoryObject(
    'typeBinding', 'Amount2DecimalType', Amount2DecimalType)

# Atomic simple type: {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}RateType


class RateType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'RateType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1264, 2)
    _Documentation = None
RateType._CF_pattern = pyxb.binding.facets.CF_pattern()
RateType._CF_pattern.addPattern(pattern='[0-9]{1,3}\\.[0-9]{2}')
# RateType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(
#     value_datatype=RateType, value=pyxb.binding.datatypes.decimal('100.0'))
RateType._InitializeFacetMap(RateType._CF_pattern)
#                             RateType._CF_maxInclusive)
Namespace.addCategoryObject('typeBinding', 'RateType', RateType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}RiferimentoFaseType


class RiferimentoFaseType (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'RiferimentoFaseType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1270, 2)
    _Documentation = None
RiferimentoFaseType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(
    value_datatype=RiferimentoFaseType,
    value=pyxb.binding.datatypes.integer(999))
RiferimentoFaseType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(
    value_datatype=RiferimentoFaseType,
    value=pyxb.binding.datatypes.integer(1))
RiferimentoFaseType._InitializeFacetMap(RiferimentoFaseType._CF_maxInclusive,
                                        RiferimentoFaseType._CF_minInclusive)
Namespace.addCategoryObject(
    'typeBinding', 'RiferimentoFaseType', RiferimentoFaseType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}NumeroColliType


class NumeroColliType (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NumeroColliType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1276, 2)
    _Documentation = None
NumeroColliType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(
    value_datatype=NumeroColliType, value=pyxb.binding.datatypes.integer(9999))
NumeroColliType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(
    value_datatype=NumeroColliType, value=pyxb.binding.datatypes.integer(1))
NumeroColliType._InitializeFacetMap(NumeroColliType._CF_maxInclusive,
                                    NumeroColliType._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'NumeroColliType', NumeroColliType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}NumeroLineaType


class NumeroLineaType (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NumeroLineaType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1282, 2)
    _Documentation = None
NumeroLineaType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(
    value_datatype=NumeroLineaType, value=pyxb.binding.datatypes.integer(9999))
NumeroLineaType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(
    value_datatype=NumeroLineaType, value=pyxb.binding.datatypes.integer(1))
NumeroLineaType._InitializeFacetMap(NumeroLineaType._CF_maxInclusive,
                                    NumeroLineaType._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'NumeroLineaType', NumeroLineaType)

# Atomic simple type: {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}CAPType


class CAPType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CAPType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1288, 2)
    _Documentation = None
CAPType._CF_pattern = pyxb.binding.facets.CF_pattern()
CAPType._CF_pattern.addPattern(pattern='[0-9][0-9][0-9][0-9][0-9]')
CAPType._InitializeFacetMap(CAPType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'CAPType', CAPType)

# Atomic simple type: {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}ABIType


class ABIType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ABIType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1293, 2)
    _Documentation = None
ABIType._CF_pattern = pyxb.binding.facets.CF_pattern()
ABIType._CF_pattern.addPattern(pattern='[0-9][0-9][0-9][0-9][0-9]')
ABIType._InitializeFacetMap(ABIType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'ABIType', ABIType)

# Atomic simple type: {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}CABType


class CABType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CABType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1298, 2)
    _Documentation = None
CABType._CF_pattern = pyxb.binding.facets.CF_pattern()
CABType._CF_pattern.addPattern(pattern='[0-9][0-9][0-9][0-9][0-9]')
CABType._InitializeFacetMap(CABType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'CABType', CABType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}GiorniTerminePagamentoType


class GiorniTerminePagamentoType (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'GiorniTerminePagamentoType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1303, 2)
    _Documentation = None
GiorniTerminePagamentoType._CF_maxInclusive = (
    pyxb.binding.facets.CF_maxInclusive(
        value_datatype=GiorniTerminePagamentoType,
        value=pyxb.binding.datatypes.integer(999)))
GiorniTerminePagamentoType._CF_minInclusive = (
    pyxb.binding.facets.CF_minInclusive(
        value_datatype=GiorniTerminePagamentoType,
        value=pyxb.binding.datatypes.integer(0)))
GiorniTerminePagamentoType._InitializeFacetMap(
    GiorniTerminePagamentoType._CF_maxInclusive,
    GiorniTerminePagamentoType._CF_minInclusive)
Namespace.addCategoryObject(
    'typeBinding', 'GiorniTerminePagamentoType', GiorniTerminePagamentoType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}QuantitaType


class QuantitaType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'QuantitaType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1309, 2)
    _Documentation = None
QuantitaType._CF_pattern = pyxb.binding.facets.CF_pattern()
QuantitaType._CF_pattern.addPattern(pattern='[0-9]{1,12}\\.[0-9]{2,8}')
QuantitaType._InitializeFacetMap(QuantitaType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'QuantitaType', QuantitaType)

# Atomic simple type:
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DataFatturaType


class DataFatturaType (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DataFatturaType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1314, 2)
    _Documentation = None
DataFatturaType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'DataFatturaType', DataFatturaType)

# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}FatturaElettronicaHeaderType
# with content type ELEMENT_ONLY


class FatturaElettronicaHeaderType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
FatturaElettronicaHeaderType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'FatturaElettronicaHeaderType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 19, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element DatiTrasmissione uses Python identifier DatiTrasmissione
    __DatiTrasmissione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiTrasmissione'),
        'DatiTrasmissione',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'FatturaElettronicaHeaderType_DatiTrasmissione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            21,
            6),
    )

    DatiTrasmissione = property(
        __DatiTrasmissione.value, __DatiTrasmissione.set, None, None)

    # Element CedentePrestatore uses Python identifier CedentePrestatore
    __CedentePrestatore = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CedentePrestatore'),
        'CedentePrestatore',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'FatturaElettronicaHeaderType_CedentePrestatore',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            22,
            6),
    )

    CedentePrestatore = property(
        __CedentePrestatore.value, __CedentePrestatore.set, None, None)

    # Element RappresentanteFiscale uses Python identifier
    # RappresentanteFiscale
    __RappresentanteFiscale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'RappresentanteFiscale'),
        'RappresentanteFiscale',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'FatturaElettronicaHeaderType_RappresentanteFiscale',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            23,
            6),
    )

    RappresentanteFiscale = property(
        __RappresentanteFiscale.value, __RappresentanteFiscale.set, None, None)

    # Element CessionarioCommittente uses Python identifier
    # CessionarioCommittente
    __CessionarioCommittente = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CessionarioCommittente'),
        'CessionarioCommittente',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'FatturaElettronicaHeaderType_CessionarioCommittente',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            24,
            6),
    )

    CessionarioCommittente = property(
        __CessionarioCommittente.value,
        __CessionarioCommittente.set,
        None,
        None)

    # Element TerzoIntermediarioOSoggettoEmittente uses Python identifier
    # TerzoIntermediarioOSoggettoEmittente
    __TerzoIntermediarioOSoggettoEmittente = (
        pyxb.binding.content.ElementDeclaration(
            pyxb.namespace.ExpandedName(
                None,
                'TerzoIntermediarioOSoggettoEmittente'),
            'TerzoIntermediarioOSoggettoEmittente',
            '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
            'FatturaElettronicaHeaderType_'
            'TerzoIntermediarioOSoggettoEmittente',
            False,
            pyxb.utils.utility.Location(
                '/tmp/fatturapa_v1.1.xsd',
                25,
                6),
        )
    )
    TerzoIntermediarioOSoggettoEmittente = property(
        __TerzoIntermediarioOSoggettoEmittente.value,
        __TerzoIntermediarioOSoggettoEmittente.set,
        None,
        None)

    # Element SoggettoEmittente uses Python identifier SoggettoEmittente
    __SoggettoEmittente = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'SoggettoEmittente'),
        'SoggettoEmittente',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'FatturaElettronicaHeaderType_SoggettoEmittente',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            26,
            6),
    )

    SoggettoEmittente = property(
        __SoggettoEmittente.value, __SoggettoEmittente.set, None, None)

    _ElementMap.update({
        __DatiTrasmissione.name(): __DatiTrasmissione,
        __CedentePrestatore.name(): __CedentePrestatore,
        __RappresentanteFiscale.name(): __RappresentanteFiscale,
        __CessionarioCommittente.name(): __CessionarioCommittente,
        __TerzoIntermediarioOSoggettoEmittente.name():
        __TerzoIntermediarioOSoggettoEmittente,
        __SoggettoEmittente.name(): __SoggettoEmittente
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding',
    'FatturaElettronicaHeaderType',
    FatturaElettronicaHeaderType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}FatturaElettronicaBodyType
# with content type ELEMENT_ONLY
class FatturaElettronicaBodyType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
FatturaElettronicaBodyType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'FatturaElettronicaBodyType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 29, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element DatiGenerali uses Python identifier DatiGenerali
    __DatiGenerali = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiGenerali'),
        'DatiGenerali',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'FatturaElettronicaBodyType_DatiGenerali',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            31,
            6),
    )

    DatiGenerali = property(
        __DatiGenerali.value, __DatiGenerali.set, None, None)

    # Element DatiBeniServizi uses Python identifier DatiBeniServizi
    __DatiBeniServizi = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiBeniServizi'),
        'DatiBeniServizi',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'FatturaElettronicaBodyType_DatiBeniServizi',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            32,
            6),
    )

    DatiBeniServizi = property(
        __DatiBeniServizi.value, __DatiBeniServizi.set, None, None)

    # Element DatiVeicoli uses Python identifier DatiVeicoli
    __DatiVeicoli = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiVeicoli'),
        'DatiVeicoli',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'FatturaElettronicaBodyType_DatiVeicoli',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            33,
            6),
    )

    DatiVeicoli = property(__DatiVeicoli.value, __DatiVeicoli.set, None, None)

    # Element DatiPagamento uses Python identifier DatiPagamento
    __DatiPagamento = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiPagamento'),
        'DatiPagamento',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'FatturaElettronicaBodyType_DatiPagamento',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            34,
            6),
    )

    DatiPagamento = property(
        __DatiPagamento.value, __DatiPagamento.set, None, None)

    # Element Allegati uses Python identifier Allegati
    __Allegati = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Allegati'),
        'Allegati',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'FatturaElettronicaBodyType_Allegati',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            35,
            6),
    )

    Allegati = property(__Allegati.value, __Allegati.set, None, None)

    _ElementMap.update({
        __DatiGenerali.name(): __DatiGenerali,
        __DatiBeniServizi.name(): __DatiBeniServizi,
        __DatiVeicoli.name(): __DatiVeicoli,
        __DatiPagamento.name(): __DatiPagamento,
        __Allegati.name(): __Allegati
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'FatturaElettronicaBodyType', FatturaElettronicaBodyType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DatiTrasmissioneType
# with content type ELEMENT_ONLY
class DatiTrasmissioneType (pyxb.binding.basis.complexTypeDefinition):

    """
           Blocco relativo ai dati di trasmissione della Fattura Elettronica
                        """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'DatiTrasmissioneType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 44, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdTrasmittente uses Python identifier IdTrasmittente
    __IdTrasmittente = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IdTrasmittente'),
        'IdTrasmittente',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiTrasmissioneType_IdTrasmittente',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            51,
            6),
    )

    IdTrasmittente = property(
        __IdTrasmittente.value, __IdTrasmittente.set, None, None)

    # Element ProgressivoInvio uses Python identifier ProgressivoInvio
    __ProgressivoInvio = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'ProgressivoInvio'),
        'ProgressivoInvio',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiTrasmissioneType_ProgressivoInvio',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            52,
            6),
    )

    ProgressivoInvio = property(
        __ProgressivoInvio.value, __ProgressivoInvio.set, None, None)

    # Element FormatoTrasmissione uses Python identifier FormatoTrasmissione
    __FormatoTrasmissione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'FormatoTrasmissione'),
        'FormatoTrasmissione',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiTrasmissioneType_FormatoTrasmissione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            53,
            6),
    )

    FormatoTrasmissione = property(
        __FormatoTrasmissione.value, __FormatoTrasmissione.set, None, None)

    # Element CodiceDestinatario uses Python identifier CodiceDestinatario
    __CodiceDestinatario = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceDestinatario'),
        'CodiceDestinatario',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiTrasmissioneType_CodiceDestinatario',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            54,
            6),
    )

    CodiceDestinatario = property(
        __CodiceDestinatario.value, __CodiceDestinatario.set, None, None)

    # Element ContattiTrasmittente uses Python identifier ContattiTrasmittente
    __ContattiTrasmittente = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'ContattiTrasmittente'),
        'ContattiTrasmittente',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiTrasmissioneType_ContattiTrasmittente',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            55,
            6),
    )

    ContattiTrasmittente = property(
        __ContattiTrasmittente.value, __ContattiTrasmittente.set, None, None)

    _ElementMap.update({
        __IdTrasmittente.name(): __IdTrasmittente,
        __ProgressivoInvio.name(): __ProgressivoInvio,
        __FormatoTrasmissione.name(): __FormatoTrasmissione,
        __CodiceDestinatario.name(): __CodiceDestinatario,
        __ContattiTrasmittente.name(): __ContattiTrasmittente
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'DatiTrasmissioneType', DatiTrasmissioneType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}IdFiscaleType with
# content type ELEMENT_ONLY
class IdFiscaleType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
IdFiscaleType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IdFiscaleType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 63, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdPaese uses Python identifier IdPaese
    __IdPaese = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IdPaese'),
        'IdPaese',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'IdFiscaleType_IdPaese',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            65,
            6),
    )

    IdPaese = property(__IdPaese.value, __IdPaese.set, None, None)

    # Element IdCodice uses Python identifier IdCodice
    __IdCodice = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IdCodice'),
        'IdCodice',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'IdFiscaleType_IdCodice',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            66,
            6),
    )

    IdCodice = property(__IdCodice.value, __IdCodice.set, None, None)

    _ElementMap.update({
        __IdPaese.name(): __IdPaese,
        __IdCodice.name(): __IdCodice
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject('typeBinding', 'IdFiscaleType', IdFiscaleType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}ContattiTrasmittenteType
# with content type ELEMENT_ONLY
class ContattiTrasmittenteType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
ContattiTrasmittenteType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'ContattiTrasmittenteType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 93, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element Telefono uses Python identifier Telefono
    __Telefono = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Telefono'),
        'Telefono',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'ContattiTrasmittenteType_Telefono',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            95,
            6),
    )

    Telefono = property(__Telefono.value, __Telefono.set, None, None)

    # Element Email uses Python identifier Email
    __Email = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Email'),
        'Email',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'ContattiTrasmittenteType_Email',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            96,
            6),
    )

    Email = property(__Email.value, __Email.set, None, None)

    _ElementMap.update({
        __Telefono.name(): __Telefono,
        __Email.name(): __Email
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'ContattiTrasmittenteType', ContattiTrasmittenteType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DatiGeneraliType with
# content type ELEMENT_ONLY
class DatiGeneraliType (pyxb.binding.basis.complexTypeDefinition):

    """
                    Blocco relativo ai Dati Generali della Fattura Elettronica
                        """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiGeneraliType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 99, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element DatiGeneraliDocumento uses Python identifier
    # DatiGeneraliDocumento
    __DatiGeneraliDocumento = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiGeneraliDocumento'),
        'DatiGeneraliDocumento',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliType_DatiGeneraliDocumento',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            106,
            6),
    )

    DatiGeneraliDocumento = property(
        __DatiGeneraliDocumento.value, __DatiGeneraliDocumento.set, None, None)

    # Element DatiOrdineAcquisto uses Python identifier DatiOrdineAcquisto
    __DatiOrdineAcquisto = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiOrdineAcquisto'),
        'DatiOrdineAcquisto',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliType_DatiOrdineAcquisto',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            107,
            6),
    )

    DatiOrdineAcquisto = property(
        __DatiOrdineAcquisto.value, __DatiOrdineAcquisto.set, None, None)

    # Element DatiContratto uses Python identifier DatiContratto
    __DatiContratto = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiContratto'),
        'DatiContratto',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliType_DatiContratto',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            108,
            6),
    )

    DatiContratto = property(
        __DatiContratto.value, __DatiContratto.set, None, None)

    # Element DatiConvenzione uses Python identifier DatiConvenzione
    __DatiConvenzione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiConvenzione'),
        'DatiConvenzione',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliType_DatiConvenzione',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            109,
            6),
    )

    DatiConvenzione = property(
        __DatiConvenzione.value, __DatiConvenzione.set, None, None)

    # Element DatiRicezione uses Python identifier DatiRicezione
    __DatiRicezione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiRicezione'),
        'DatiRicezione',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliType_DatiRicezione',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            110,
            6),
    )

    DatiRicezione = property(
        __DatiRicezione.value, __DatiRicezione.set, None, None)

    # Element DatiFattureCollegate uses Python identifier DatiFattureCollegate
    __DatiFattureCollegate = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiFattureCollegate'),
        'DatiFattureCollegate',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliType_DatiFattureCollegate',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            111,
            6),
    )

    DatiFattureCollegate = property(
        __DatiFattureCollegate.value, __DatiFattureCollegate.set, None, None)

    # Element DatiSAL uses Python identifier DatiSAL
    __DatiSAL = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiSAL'),
        'DatiSAL',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliType_DatiSAL',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            112,
            6),
    )

    DatiSAL = property(__DatiSAL.value, __DatiSAL.set, None, None)

    # Element DatiDDT uses Python identifier DatiDDT
    __DatiDDT = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiDDT'),
        'DatiDDT',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliType_DatiDDT',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            113,
            6),
    )

    DatiDDT = property(__DatiDDT.value, __DatiDDT.set, None, None)

    # Element DatiTrasporto uses Python identifier DatiTrasporto
    __DatiTrasporto = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiTrasporto'),
        'DatiTrasporto',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliType_DatiTrasporto',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            114,
            6),
    )

    DatiTrasporto = property(
        __DatiTrasporto.value, __DatiTrasporto.set, None, None)

    # Element FatturaPrincipale uses Python identifier FatturaPrincipale
    __FatturaPrincipale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'FatturaPrincipale'),
        'FatturaPrincipale',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliType_FatturaPrincipale',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            115,
            6),
    )

    FatturaPrincipale = property(
        __FatturaPrincipale.value, __FatturaPrincipale.set, None, None)

    _ElementMap.update({
        __DatiGeneraliDocumento.name(): __DatiGeneraliDocumento,
        __DatiOrdineAcquisto.name(): __DatiOrdineAcquisto,
        __DatiContratto.name(): __DatiContratto,
        __DatiConvenzione.name(): __DatiConvenzione,
        __DatiRicezione.name(): __DatiRicezione,
        __DatiFattureCollegate.name(): __DatiFattureCollegate,
        __DatiSAL.name(): __DatiSAL,
        __DatiDDT.name(): __DatiDDT,
        __DatiTrasporto.name(): __DatiTrasporto,
        __FatturaPrincipale.name(): __FatturaPrincipale
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'DatiGeneraliType', DatiGeneraliType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DatiGeneraliDocumentoType
# with content type ELEMENT_ONLY
class DatiGeneraliDocumentoType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
DatiGeneraliDocumentoType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'DatiGeneraliDocumentoType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 118, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element TipoDocumento uses Python identifier TipoDocumento
    __TipoDocumento = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'TipoDocumento'),
        'TipoDocumento',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliDocumentoType_TipoDocumento',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            120,
            6),
    )

    TipoDocumento = property(
        __TipoDocumento.value, __TipoDocumento.set, None, None)

    # Element Divisa uses Python identifier Divisa
    __Divisa = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Divisa'),
        'Divisa',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliDocumentoType_Divisa',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            121,
            6),
    )

    Divisa = property(__Divisa.value, __Divisa.set, None, None)

    # Element Data uses Python identifier Data
    __Data = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Data'),
        'Data',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliDocumentoType_Data',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            122,
            6),
    )

    Data = property(__Data.value, __Data.set, None, None)

    # Element Numero uses Python identifier Numero
    __Numero = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Numero'),
        'Numero',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliDocumentoType_Numero',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            123,
            6),
    )

    Numero = property(__Numero.value, __Numero.set, None, None)

    # Element DatiRitenuta uses Python identifier DatiRitenuta
    __DatiRitenuta = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiRitenuta'),
        'DatiRitenuta',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliDocumentoType_DatiRitenuta',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            124,
            6),
    )

    DatiRitenuta = property(
        __DatiRitenuta.value, __DatiRitenuta.set, None, None)

    # Element DatiBollo uses Python identifier DatiBollo
    __DatiBollo = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiBollo'),
        'DatiBollo',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliDocumentoType_DatiBollo',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            125,
            6),
    )

    DatiBollo = property(__DatiBollo.value, __DatiBollo.set, None, None)

    # Element DatiCassaPrevidenziale uses Python identifier
    # DatiCassaPrevidenziale
    __DatiCassaPrevidenziale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiCassaPrevidenziale'),
        'DatiCassaPrevidenziale',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliDocumentoType_DatiCassaPrevidenziale',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            126,
            6),
    )

    DatiCassaPrevidenziale = property(
        __DatiCassaPrevidenziale.value,
        __DatiCassaPrevidenziale.set,
        None,
        None)

    # Element ScontoMaggiorazione uses Python identifier ScontoMaggiorazione
    __ScontoMaggiorazione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'ScontoMaggiorazione'),
        'ScontoMaggiorazione',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliDocumentoType_ScontoMaggiorazione',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            127,
            6),
    )

    ScontoMaggiorazione = property(
        __ScontoMaggiorazione.value, __ScontoMaggiorazione.set, None, None)

    # Element ImportoTotaleDocumento uses Python identifier
    # ImportoTotaleDocumento
    __ImportoTotaleDocumento = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'ImportoTotaleDocumento'),
        'ImportoTotaleDocumento',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliDocumentoType_ImportoTotaleDocumento',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            128,
            6),
    )

    ImportoTotaleDocumento = property(
        __ImportoTotaleDocumento.value,
        __ImportoTotaleDocumento.set,
        None,
        None)

    # Element Arrotondamento uses Python identifier Arrotondamento
    __Arrotondamento = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Arrotondamento'),
        'Arrotondamento',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliDocumentoType_Arrotondamento',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            129,
            6),
    )

    Arrotondamento = property(
        __Arrotondamento.value, __Arrotondamento.set, None, None)

    # Element Causale uses Python identifier Causale
    __Causale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Causale'),
        'Causale',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliDocumentoType_Causale',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            130,
            6),
    )

    Causale = property(__Causale.value, __Causale.set, None, None)

    # Element Art73 uses Python identifier Art73
    __Art73 = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Art73'),
        'Art73',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiGeneraliDocumentoType_Art73',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            131,
            6),
    )

    Art73 = property(__Art73.value, __Art73.set, None, None)

    _ElementMap.update({
        __TipoDocumento.name(): __TipoDocumento,
        __Divisa.name(): __Divisa,
        __Data.name(): __Data,
        __Numero.name(): __Numero,
        __DatiRitenuta.name(): __DatiRitenuta,
        __DatiBollo.name(): __DatiBollo,
        __DatiCassaPrevidenziale.name(): __DatiCassaPrevidenziale,
        __ScontoMaggiorazione.name(): __ScontoMaggiorazione,
        __ImportoTotaleDocumento.name(): __ImportoTotaleDocumento,
        __Arrotondamento.name(): __Arrotondamento,
        __Causale.name(): __Causale,
        __Art73.name(): __Art73
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'DatiGeneraliDocumentoType', DatiGeneraliDocumentoType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DatiRitenutaType with
# content type ELEMENT_ONLY
class DatiRitenutaType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
DatiRitenutaType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiRitenutaType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 134, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element TipoRitenuta uses Python identifier TipoRitenuta
    __TipoRitenuta = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'TipoRitenuta'),
        'TipoRitenuta',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiRitenutaType_TipoRitenuta',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            136,
            6),
    )

    TipoRitenuta = property(
        __TipoRitenuta.value, __TipoRitenuta.set, None, None)

    # Element ImportoRitenuta uses Python identifier ImportoRitenuta
    __ImportoRitenuta = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'ImportoRitenuta'),
        'ImportoRitenuta',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiRitenutaType_ImportoRitenuta',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            137,
            6),
    )

    ImportoRitenuta = property(
        __ImportoRitenuta.value, __ImportoRitenuta.set, None, None)

    # Element AliquotaRitenuta uses Python identifier AliquotaRitenuta
    __AliquotaRitenuta = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'AliquotaRitenuta'),
        'AliquotaRitenuta',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiRitenutaType_AliquotaRitenuta',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            138,
            6),
    )

    AliquotaRitenuta = property(
        __AliquotaRitenuta.value, __AliquotaRitenuta.set, None, None)

    # Element CausalePagamento uses Python identifier CausalePagamento
    __CausalePagamento = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CausalePagamento'),
        'CausalePagamento',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiRitenutaType_CausalePagamento',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            139,
            6),
    )

    CausalePagamento = property(
        __CausalePagamento.value, __CausalePagamento.set, None, None)

    _ElementMap.update({
        __TipoRitenuta.name(): __TipoRitenuta,
        __ImportoRitenuta.name(): __ImportoRitenuta,
        __AliquotaRitenuta.name(): __AliquotaRitenuta,
        __CausalePagamento.name(): __CausalePagamento
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'DatiRitenutaType', DatiRitenutaType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DatiBolloType with
# content type ELEMENT_ONLY
class DatiBolloType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
DatiBolloType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiBolloType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 142, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element BolloVirtuale uses Python identifier BolloVirtuale
    __BolloVirtuale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'BolloVirtuale'),
        'BolloVirtuale',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiBolloType_BolloVirtuale',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            144,
            6),
    )

    BolloVirtuale = property(
        __BolloVirtuale.value, __BolloVirtuale.set, None, None)

    # Element ImportoBollo uses Python identifier ImportoBollo
    __ImportoBollo = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'ImportoBollo'),
        'ImportoBollo',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiBolloType_ImportoBollo',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            145,
            6),
    )

    ImportoBollo = property(
        __ImportoBollo.value, __ImportoBollo.set, None, None)

    _ElementMap.update({
        __BolloVirtuale.name(): __BolloVirtuale,
        __ImportoBollo.name(): __ImportoBollo
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject('typeBinding', 'DatiBolloType', DatiBolloType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DatiCassaPrevidenzialeType
# with content type ELEMENT_ONLY
class DatiCassaPrevidenzialeType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
DatiCassaPrevidenzialeType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'DatiCassaPrevidenzialeType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 148, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element TipoCassa uses Python identifier TipoCassa
    __TipoCassa = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'TipoCassa'),
        'TipoCassa',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiCassaPrevidenzialeType_TipoCassa',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            150,
            6),
    )

    TipoCassa = property(__TipoCassa.value, __TipoCassa.set, None, None)

    # Element AlCassa uses Python identifier AlCassa
    __AlCassa = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'AlCassa'),
        'AlCassa',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiCassaPrevidenzialeType_AlCassa',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            151,
            6),
    )

    AlCassa = property(__AlCassa.value, __AlCassa.set, None, None)

    # Element ImportoContributoCassa uses Python identifier
    # ImportoContributoCassa
    __ImportoContributoCassa = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'ImportoContributoCassa'),
        'ImportoContributoCassa',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiCassaPrevidenzialeType_ImportoContributoCassa',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            152,
            6),
    )

    ImportoContributoCassa = property(
        __ImportoContributoCassa.value,
        __ImportoContributoCassa.set,
        None,
        None)

    # Element ImponibileCassa uses Python identifier ImponibileCassa
    __ImponibileCassa = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'ImponibileCassa'),
        'ImponibileCassa',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiCassaPrevidenzialeType_ImponibileCassa',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            153,
            6),
    )

    ImponibileCassa = property(
        __ImponibileCassa.value, __ImponibileCassa.set, None, None)

    # Element AliquotaIVA uses Python identifier AliquotaIVA
    __AliquotaIVA = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'AliquotaIVA'),
        'AliquotaIVA',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiCassaPrevidenzialeType_AliquotaIVA',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            154,
            6),
    )

    AliquotaIVA = property(__AliquotaIVA.value, __AliquotaIVA.set, None, None)

    # Element Ritenuta uses Python identifier Ritenuta
    __Ritenuta = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Ritenuta'),
        'Ritenuta',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiCassaPrevidenzialeType_Ritenuta',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            155,
            6),
    )

    Ritenuta = property(__Ritenuta.value, __Ritenuta.set, None, None)

    # Element Natura uses Python identifier Natura
    __Natura = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Natura'),
        'Natura',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiCassaPrevidenzialeType_Natura',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            156,
            6),
    )

    Natura = property(__Natura.value, __Natura.set, None, None)

    # Element RiferimentoAmministrazione uses Python identifier
    # RiferimentoAmministrazione
    __RiferimentoAmministrazione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoAmministrazione'),
        'RiferimentoAmministrazione',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiCassaPrevidenzialeType_RiferimentoAmministrazione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            157,
            6),
    )

    RiferimentoAmministrazione = property(
        __RiferimentoAmministrazione.value,
        __RiferimentoAmministrazione.set,
        None,
        None)

    _ElementMap.update({
        __TipoCassa.name(): __TipoCassa,
        __AlCassa.name(): __AlCassa,
        __ImportoContributoCassa.name(): __ImportoContributoCassa,
        __ImponibileCassa.name(): __ImponibileCassa,
        __AliquotaIVA.name(): __AliquotaIVA,
        __Ritenuta.name(): __Ritenuta,
        __Natura.name(): __Natura,
        __RiferimentoAmministrazione.name(): __RiferimentoAmministrazione
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'DatiCassaPrevidenzialeType', DatiCassaPrevidenzialeType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}ScontoMaggiorazioneType
# with content type ELEMENT_ONLY
class ScontoMaggiorazioneType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
ScontoMaggiorazioneType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'ScontoMaggiorazioneType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 160, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element Tipo uses Python identifier Tipo
    __Tipo = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Tipo'),
        'Tipo',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'ScontoMaggiorazioneType_Tipo',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            162,
            6),
    )

    Tipo = property(__Tipo.value, __Tipo.set, None, None)

    # Element Percentuale uses Python identifier Percentuale
    __Percentuale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Percentuale'),
        'Percentuale',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'ScontoMaggiorazioneType_Percentuale',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            163,
            6),
    )

    Percentuale = property(__Percentuale.value, __Percentuale.set, None, None)

    # Element Importo uses Python identifier Importo
    __Importo = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Importo'),
        'Importo',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'ScontoMaggiorazioneType_Importo',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            164,
            6),
    )

    Importo = property(__Importo.value, __Importo.set, None, None)

    _ElementMap.update({
        __Tipo.name(): __Tipo,
        __Percentuale.name(): __Percentuale,
        __Importo.name(): __Importo
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'ScontoMaggiorazioneType', ScontoMaggiorazioneType)


# Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DatiSALType
# with content type ELEMENT_ONLY
class DatiSALType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
DatiSALType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiSALType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 439, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element RiferimentoFase uses Python identifier RiferimentoFase
    __RiferimentoFase = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoFase'),
        'RiferimentoFase',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiSALType_RiferimentoFase',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            441,
            6),
    )

    RiferimentoFase = property(
        __RiferimentoFase.value, __RiferimentoFase.set, None, None)

    _ElementMap.update({
        __RiferimentoFase.name(): __RiferimentoFase
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject('typeBinding', 'DatiSALType', DatiSALType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DatiDocumentiCorrelatiType
# with content type ELEMENT_ONLY
class DatiDocumentiCorrelatiType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
DatiDocumentiCorrelatiType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'DatiDocumentiCorrelatiType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 444, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element RiferimentoNumeroLinea uses Python identifier
    # RiferimentoNumeroLinea
    __RiferimentoNumeroLinea = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoNumeroLinea'),
        'RiferimentoNumeroLinea',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiDocumentiCorrelatiType_RiferimentoNumeroLinea',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            446,
            6),
    )

    RiferimentoNumeroLinea = property(
        __RiferimentoNumeroLinea.value,
        __RiferimentoNumeroLinea.set,
        None,
        None)

    # Element IdDocumento uses Python identifier IdDocumento
    __IdDocumento = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IdDocumento'),
        'IdDocumento',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiDocumentiCorrelatiType_IdDocumento',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            447,
            6),
    )

    IdDocumento = property(__IdDocumento.value, __IdDocumento.set, None, None)

    # Element Data uses Python identifier Data
    __Data = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Data'),
        'Data',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiDocumentiCorrelatiType_Data',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            448,
            6),
    )

    Data = property(__Data.value, __Data.set, None, None)

    # Element NumItem uses Python identifier NumItem
    __NumItem = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NumItem'),
        'NumItem',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiDocumentiCorrelatiType_NumItem',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            449,
            6),
    )

    NumItem = property(__NumItem.value, __NumItem.set, None, None)

    # Element CodiceCommessaConvenzione uses Python identifier
    # CodiceCommessaConvenzione
    __CodiceCommessaConvenzione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceCommessaConvenzione'),
        'CodiceCommessaConvenzione',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiDocumentiCorrelatiType_CodiceCommessaConvenzione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            450,
            6),
    )

    CodiceCommessaConvenzione = property(
        __CodiceCommessaConvenzione.value,
        __CodiceCommessaConvenzione.set,
        None,
        None)

    # Element CodiceCUP uses Python identifier CodiceCUP
    __CodiceCUP = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceCUP'),
        'CodiceCUP',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiDocumentiCorrelatiType_CodiceCUP',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            451,
            6),
    )

    CodiceCUP = property(__CodiceCUP.value, __CodiceCUP.set, None, None)

    # Element CodiceCIG uses Python identifier CodiceCIG
    __CodiceCIG = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceCIG'),
        'CodiceCIG',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiDocumentiCorrelatiType_CodiceCIG',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            452,
            6),
    )

    CodiceCIG = property(__CodiceCIG.value, __CodiceCIG.set, None, None)

    _ElementMap.update({
        __RiferimentoNumeroLinea.name(): __RiferimentoNumeroLinea,
        __IdDocumento.name(): __IdDocumento,
        __Data.name(): __Data,
        __NumItem.name(): __NumItem,
        __CodiceCommessaConvenzione.name(): __CodiceCommessaConvenzione,
        __CodiceCUP.name(): __CodiceCUP,
        __CodiceCIG.name(): __CodiceCIG
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'DatiDocumentiCorrelatiType', DatiDocumentiCorrelatiType)


# Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DatiDDTType
# with content type ELEMENT_ONLY
class DatiDDTType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
DatiDDTType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiDDTType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 461, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element NumeroDDT uses Python identifier NumeroDDT
    __NumeroDDT = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NumeroDDT'),
        'NumeroDDT',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiDDTType_NumeroDDT',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            463,
            6),
    )

    NumeroDDT = property(__NumeroDDT.value, __NumeroDDT.set, None, None)

    # Element DataDDT uses Python identifier DataDDT
    __DataDDT = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DataDDT'),
        'DataDDT',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiDDTType_DataDDT',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            464,
            6),
    )

    DataDDT = property(__DataDDT.value, __DataDDT.set, None, None)

    # Element RiferimentoNumeroLinea uses Python identifier
    # RiferimentoNumeroLinea
    __RiferimentoNumeroLinea = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoNumeroLinea'),
        'RiferimentoNumeroLinea',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiDDTType_RiferimentoNumeroLinea',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            465,
            6),
    )

    RiferimentoNumeroLinea = property(
        __RiferimentoNumeroLinea.value,
        __RiferimentoNumeroLinea.set,
        None,
        None)

    _ElementMap.update({
        __NumeroDDT.name(): __NumeroDDT,
        __DataDDT.name(): __DataDDT,
        __RiferimentoNumeroLinea.name(): __RiferimentoNumeroLinea
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject('typeBinding', 'DatiDDTType', DatiDDTType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DatiTrasportoType with
# content type ELEMENT_ONLY
class DatiTrasportoType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
DatiTrasportoType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiTrasportoType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 468, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element DatiAnagraficiVettore uses Python identifier
    # DatiAnagraficiVettore
    __DatiAnagraficiVettore = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiAnagraficiVettore'),
        'DatiAnagraficiVettore',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiTrasportoType_DatiAnagraficiVettore',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            470,
            6),
    )

    DatiAnagraficiVettore = property(
        __DatiAnagraficiVettore.value, __DatiAnagraficiVettore.set, None, None)

    # Element MezzoTrasporto uses Python identifier MezzoTrasporto
    __MezzoTrasporto = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'MezzoTrasporto'),
        'MezzoTrasporto',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiTrasportoType_MezzoTrasporto',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            471,
            6),
    )

    MezzoTrasporto = property(
        __MezzoTrasporto.value, __MezzoTrasporto.set, None, None)

    # Element CausaleTrasporto uses Python identifier CausaleTrasporto
    __CausaleTrasporto = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CausaleTrasporto'),
        'CausaleTrasporto',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiTrasportoType_CausaleTrasporto',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            472,
            6),
    )

    CausaleTrasporto = property(
        __CausaleTrasporto.value, __CausaleTrasporto.set, None, None)

    # Element NumeroColli uses Python identifier NumeroColli
    __NumeroColli = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NumeroColli'),
        'NumeroColli',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiTrasportoType_NumeroColli',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            473,
            6),
    )

    NumeroColli = property(__NumeroColli.value, __NumeroColli.set, None, None)

    # Element Descrizione uses Python identifier Descrizione
    __Descrizione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Descrizione'),
        'Descrizione',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiTrasportoType_Descrizione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            474,
            6),
    )

    Descrizione = property(__Descrizione.value, __Descrizione.set, None, None)

    # Element UnitaMisuraPeso uses Python identifier UnitaMisuraPeso
    __UnitaMisuraPeso = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'UnitaMisuraPeso'),
        'UnitaMisuraPeso',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiTrasportoType_UnitaMisuraPeso',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            475,
            6),
    )

    UnitaMisuraPeso = property(
        __UnitaMisuraPeso.value, __UnitaMisuraPeso.set, None, None)

    # Element PesoLordo uses Python identifier PesoLordo
    __PesoLordo = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'PesoLordo'),
        'PesoLordo',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiTrasportoType_PesoLordo',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            476,
            6),
    )

    PesoLordo = property(__PesoLordo.value, __PesoLordo.set, None, None)

    # Element PesoNetto uses Python identifier PesoNetto
    __PesoNetto = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'PesoNetto'),
        'PesoNetto',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiTrasportoType_PesoNetto',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            477,
            6),
    )

    PesoNetto = property(__PesoNetto.value, __PesoNetto.set, None, None)

    # Element DataOraRitiro uses Python identifier DataOraRitiro
    __DataOraRitiro = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DataOraRitiro'),
        'DataOraRitiro',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiTrasportoType_DataOraRitiro',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            478,
            6),
    )

    DataOraRitiro = property(
        __DataOraRitiro.value, __DataOraRitiro.set, None, None)

    # Element DataInizioTrasporto uses Python identifier DataInizioTrasporto
    __DataInizioTrasporto = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DataInizioTrasporto'),
        'DataInizioTrasporto',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiTrasportoType_DataInizioTrasporto',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            479,
            6),
    )

    DataInizioTrasporto = property(
        __DataInizioTrasporto.value, __DataInizioTrasporto.set, None, None)

    # Element TipoResa uses Python identifier TipoResa
    __TipoResa = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'TipoResa'),
        'TipoResa',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiTrasportoType_TipoResa',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            480,
            6),
    )

    TipoResa = property(__TipoResa.value, __TipoResa.set, None, None)

    # Element IndirizzoResa uses Python identifier IndirizzoResa
    __IndirizzoResa = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IndirizzoResa'),
        'IndirizzoResa',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiTrasportoType_IndirizzoResa',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            481,
            6),
    )

    IndirizzoResa = property(
        __IndirizzoResa.value, __IndirizzoResa.set, None, None)

    # Element DataOraConsegna uses Python identifier DataOraConsegna
    __DataOraConsegna = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DataOraConsegna'),
        'DataOraConsegna',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiTrasportoType_DataOraConsegna',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            482,
            6),
    )

    DataOraConsegna = property(
        __DataOraConsegna.value, __DataOraConsegna.set, None, None)

    _ElementMap.update({
        __DatiAnagraficiVettore.name(): __DatiAnagraficiVettore,
        __MezzoTrasporto.name(): __MezzoTrasporto,
        __CausaleTrasporto.name(): __CausaleTrasporto,
        __NumeroColli.name(): __NumeroColli,
        __Descrizione.name(): __Descrizione,
        __UnitaMisuraPeso.name(): __UnitaMisuraPeso,
        __PesoLordo.name(): __PesoLordo,
        __PesoNetto.name(): __PesoNetto,
        __DataOraRitiro.name(): __DataOraRitiro,
        __DataInizioTrasporto.name(): __DataInizioTrasporto,
        __TipoResa.name(): __TipoResa,
        __IndirizzoResa.name(): __IndirizzoResa,
        __DataOraConsegna.name(): __DataOraConsegna
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'DatiTrasportoType', DatiTrasportoType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}IndirizzoType with
# content type ELEMENT_ONLY
class IndirizzoType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
IndirizzoType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IndirizzoType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 485, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element Indirizzo uses Python identifier Indirizzo
    __Indirizzo = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Indirizzo'),
        'Indirizzo',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'IndirizzoType_Indirizzo',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            487,
            6),
    )

    Indirizzo = property(__Indirizzo.value, __Indirizzo.set, None, None)

    # Element NumeroCivico uses Python identifier NumeroCivico
    __NumeroCivico = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NumeroCivico'),
        'NumeroCivico',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'IndirizzoType_NumeroCivico',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            488,
            6),
    )

    NumeroCivico = property(
        __NumeroCivico.value, __NumeroCivico.set, None, None)

    # Element CAP uses Python identifier CAP
    __CAP = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CAP'),
        'CAP',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'IndirizzoType_CAP',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            489,
            6),
    )

    CAP = property(__CAP.value, __CAP.set, None, None)

    # Element Comune uses Python identifier Comune
    __Comune = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Comune'),
        'Comune',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'IndirizzoType_Comune',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            490,
            6),
    )

    Comune = property(__Comune.value, __Comune.set, None, None)

    # Element Provincia uses Python identifier Provincia
    __Provincia = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Provincia'),
        'Provincia',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'IndirizzoType_Provincia',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            491,
            6),
    )

    Provincia = property(__Provincia.value, __Provincia.set, None, None)

    # Element Nazione uses Python identifier Nazione
    __Nazione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Nazione'),
        'Nazione',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'IndirizzoType_Nazione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            492,
            6),
    )

    Nazione = property(__Nazione.value, __Nazione.set, None, None)

    _ElementMap.update({
        __Indirizzo.name(): __Indirizzo,
        __NumeroCivico.name(): __NumeroCivico,
        __CAP.name(): __CAP,
        __Comune.name(): __Comune,
        __Provincia.name(): __Provincia,
        __Nazione.name(): __Nazione
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject('typeBinding', 'IndirizzoType', IndirizzoType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}FatturaPrincipaleType
# with content type ELEMENT_ONLY
class FatturaPrincipaleType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
FatturaPrincipaleType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'FatturaPrincipaleType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 495, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element NumeroFatturaPrincipale uses Python identifier
    # NumeroFatturaPrincipale
    __NumeroFatturaPrincipale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NumeroFatturaPrincipale'),
        'NumeroFatturaPrincipale',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'FatturaPrincipaleType_NumeroFatturaPrincipale',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            497,
            6),
    )

    NumeroFatturaPrincipale = property(
        __NumeroFatturaPrincipale.value,
        __NumeroFatturaPrincipale.set,
        None,
        None)

    # Element DataFatturaPrincipale uses Python identifier
    # DataFatturaPrincipale
    __DataFatturaPrincipale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DataFatturaPrincipale'),
        'DataFatturaPrincipale',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'FatturaPrincipaleType_DataFatturaPrincipale',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            498,
            6),
    )

    DataFatturaPrincipale = property(
        __DataFatturaPrincipale.value, __DataFatturaPrincipale.set, None, None)

    _ElementMap.update({
        __NumeroFatturaPrincipale.name(): __NumeroFatturaPrincipale,
        __DataFatturaPrincipale.name(): __DataFatturaPrincipale
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'FatturaPrincipaleType', FatturaPrincipaleType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}CedentePrestatoreType
# with content type ELEMENT_ONLY
class CedentePrestatoreType (pyxb.binding.basis.complexTypeDefinition):

    """
                              Blocco relativo ai dati del Cedente / Prestatore
                        """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'CedentePrestatoreType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 516, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element DatiAnagrafici uses Python identifier DatiAnagrafici
    __DatiAnagrafici = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiAnagrafici'),
        'DatiAnagrafici',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'CedentePrestatoreType_DatiAnagrafici',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            523,
            6),
    )

    DatiAnagrafici = property(
        __DatiAnagrafici.value, __DatiAnagrafici.set, None, None)

    # Element Sede uses Python identifier Sede
    __Sede = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Sede'),
        'Sede',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'CedentePrestatoreType_Sede',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            524,
            6),
    )

    Sede = property(__Sede.value, __Sede.set, None, None)

    # Element StabileOrganizzazione uses Python identifier
    # StabileOrganizzazione
    __StabileOrganizzazione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'StabileOrganizzazione'),
        'StabileOrganizzazione',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'CedentePrestatoreType_StabileOrganizzazione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            525,
            6),
    )

    StabileOrganizzazione = property(
        __StabileOrganizzazione.value, __StabileOrganizzazione.set, None, None)

    # Element IscrizioneREA uses Python identifier IscrizioneREA
    __IscrizioneREA = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IscrizioneREA'),
        'IscrizioneREA',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'CedentePrestatoreType_IscrizioneREA',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            526,
            6),
    )

    IscrizioneREA = property(
        __IscrizioneREA.value, __IscrizioneREA.set, None, None)

    # Element Contatti uses Python identifier Contatti
    __Contatti = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Contatti'),
        'Contatti',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'CedentePrestatoreType_Contatti',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            527,
            6),
    )

    Contatti = property(__Contatti.value, __Contatti.set, None, None)

    # Element RiferimentoAmministrazione uses Python identifier
    # RiferimentoAmministrazione
    __RiferimentoAmministrazione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoAmministrazione'),
        'RiferimentoAmministrazione',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'CedentePrestatoreType_RiferimentoAmministrazione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            528,
            6),
    )

    RiferimentoAmministrazione = property(
        __RiferimentoAmministrazione.value,
        __RiferimentoAmministrazione.set,
        None,
        None)

    _ElementMap.update({
        __DatiAnagrafici.name(): __DatiAnagrafici,
        __Sede.name(): __Sede,
        __StabileOrganizzazione.name(): __StabileOrganizzazione,
        __IscrizioneREA.name(): __IscrizioneREA,
        __Contatti.name(): __Contatti,
        __RiferimentoAmministrazione.name(): __RiferimentoAmministrazione
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'CedentePrestatoreType', CedentePrestatoreType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DatiAnagraficiCedenteType
# with content type ELEMENT_ONLY
class DatiAnagraficiCedenteType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
DatiAnagraficiCedenteType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'DatiAnagraficiCedenteType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 531, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdFiscaleIVA uses Python identifier IdFiscaleIVA
    __IdFiscaleIVA = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IdFiscaleIVA'),
        'IdFiscaleIVA',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiCedenteType_IdFiscaleIVA',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            533,
            6),
    )

    IdFiscaleIVA = property(
        __IdFiscaleIVA.value, __IdFiscaleIVA.set, None, None)

    # Element CodiceFiscale uses Python identifier CodiceFiscale
    __CodiceFiscale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceFiscale'),
        'CodiceFiscale',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiCedenteType_CodiceFiscale',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            534,
            6),
    )

    CodiceFiscale = property(
        __CodiceFiscale.value, __CodiceFiscale.set, None, None)

    # Element Anagrafica uses Python identifier Anagrafica
    __Anagrafica = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Anagrafica'),
        'Anagrafica',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiCedenteType_Anagrafica',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            535,
            6),
    )

    Anagrafica = property(__Anagrafica.value, __Anagrafica.set, None, None)

    # Element AlboProfessionale uses Python identifier AlboProfessionale
    __AlboProfessionale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'AlboProfessionale'),
        'AlboProfessionale',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiCedenteType_AlboProfessionale',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            536,
            6),
    )

    AlboProfessionale = property(
        __AlboProfessionale.value, __AlboProfessionale.set, None, None)

    # Element ProvinciaAlbo uses Python identifier ProvinciaAlbo
    __ProvinciaAlbo = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'ProvinciaAlbo'),
        'ProvinciaAlbo',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiCedenteType_ProvinciaAlbo',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            537,
            6),
    )

    ProvinciaAlbo = property(
        __ProvinciaAlbo.value, __ProvinciaAlbo.set, None, None)

    # Element NumeroIscrizioneAlbo uses Python identifier NumeroIscrizioneAlbo
    __NumeroIscrizioneAlbo = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NumeroIscrizioneAlbo'),
        'NumeroIscrizioneAlbo',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiCedenteType_NumeroIscrizioneAlbo',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            538,
            6),
    )

    NumeroIscrizioneAlbo = property(
        __NumeroIscrizioneAlbo.value, __NumeroIscrizioneAlbo.set, None, None)

    # Element DataIscrizioneAlbo uses Python identifier DataIscrizioneAlbo
    __DataIscrizioneAlbo = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DataIscrizioneAlbo'),
        'DataIscrizioneAlbo',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiCedenteType_DataIscrizioneAlbo',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            539,
            6),
    )

    DataIscrizioneAlbo = property(
        __DataIscrizioneAlbo.value, __DataIscrizioneAlbo.set, None, None)

    # Element RegimeFiscale uses Python identifier RegimeFiscale
    __RegimeFiscale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'RegimeFiscale'),
        'RegimeFiscale',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiCedenteType_RegimeFiscale',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            540,
            6),
    )

    RegimeFiscale = property(
        __RegimeFiscale.value, __RegimeFiscale.set, None, None)

    _ElementMap.update({
        __IdFiscaleIVA.name(): __IdFiscaleIVA,
        __CodiceFiscale.name(): __CodiceFiscale,
        __Anagrafica.name(): __Anagrafica,
        __AlboProfessionale.name(): __AlboProfessionale,
        __ProvinciaAlbo.name(): __ProvinciaAlbo,
        __NumeroIscrizioneAlbo.name(): __NumeroIscrizioneAlbo,
        __DataIscrizioneAlbo.name(): __DataIscrizioneAlbo,
        __RegimeFiscale.name(): __RegimeFiscale
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'DatiAnagraficiCedenteType', DatiAnagraficiCedenteType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}AnagraficaType with
# content type ELEMENT_ONLY
class AnagraficaType (pyxb.binding.basis.complexTypeDefinition):

    """
        Il campo Denominazione è in alternativa ai campi Nome e Cognome
                        """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AnagraficaType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 644, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element Denominazione uses Python identifier Denominazione
    __Denominazione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Denominazione'),
        'Denominazione',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'AnagraficaType_Denominazione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            653,
            10),
    )

    Denominazione = property(
        __Denominazione.value, __Denominazione.set, None, None)

    # Element Nome uses Python identifier Nome
    __Nome = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Nome'),
        'Nome',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'AnagraficaType_Nome',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            656,
            10),
    )

    Nome = property(__Nome.value, __Nome.set, None, None)

    # Element Cognome uses Python identifier Cognome
    __Cognome = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Cognome'),
        'Cognome',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'AnagraficaType_Cognome',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            657,
            10),
    )

    Cognome = property(__Cognome.value, __Cognome.set, None, None)

    # Element Titolo uses Python identifier Titolo
    __Titolo = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Titolo'),
        'Titolo',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'AnagraficaType_Titolo',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            660,
            6),
    )

    Titolo = property(__Titolo.value, __Titolo.set, None, None)

    # Element CodEORI uses Python identifier CodEORI
    __CodEORI = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CodEORI'),
        'CodEORI',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'AnagraficaType_CodEORI',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            661,
            6),
    )

    CodEORI = property(__CodEORI.value, __CodEORI.set, None, None)

    _ElementMap.update({
        __Denominazione.name(): __Denominazione,
        __Nome.name(): __Nome,
        __Cognome.name(): __Cognome,
        __Titolo.name(): __Titolo,
        __CodEORI.name(): __CodEORI
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject('typeBinding', 'AnagraficaType', AnagraficaType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DatiAnagraficiVettoreType
# with content type ELEMENT_ONLY
class DatiAnagraficiVettoreType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
DatiAnagraficiVettoreType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'DatiAnagraficiVettoreType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 664, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdFiscaleIVA uses Python identifier IdFiscaleIVA
    __IdFiscaleIVA = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IdFiscaleIVA'),
        'IdFiscaleIVA',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiVettoreType_IdFiscaleIVA',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            666,
            6),
    )

    IdFiscaleIVA = property(
        __IdFiscaleIVA.value, __IdFiscaleIVA.set, None, None)

    # Element CodiceFiscale uses Python identifier CodiceFiscale
    __CodiceFiscale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceFiscale'),
        'CodiceFiscale',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiVettoreType_CodiceFiscale',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            667,
            6),
    )

    CodiceFiscale = property(
        __CodiceFiscale.value, __CodiceFiscale.set, None, None)

    # Element Anagrafica uses Python identifier Anagrafica
    __Anagrafica = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Anagrafica'),
        'Anagrafica',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiVettoreType_Anagrafica',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            668,
            6),
    )

    Anagrafica = property(__Anagrafica.value, __Anagrafica.set, None, None)

    # Element NumeroLicenzaGuida uses Python identifier NumeroLicenzaGuida
    __NumeroLicenzaGuida = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NumeroLicenzaGuida'),
        'NumeroLicenzaGuida',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiVettoreType_NumeroLicenzaGuida',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            669,
            6),
    )

    NumeroLicenzaGuida = property(
        __NumeroLicenzaGuida.value, __NumeroLicenzaGuida.set, None, None)

    _ElementMap.update({
        __IdFiscaleIVA.name(): __IdFiscaleIVA,
        __CodiceFiscale.name(): __CodiceFiscale,
        __Anagrafica.name(): __Anagrafica,
        __NumeroLicenzaGuida.name(): __NumeroLicenzaGuida
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'DatiAnagraficiVettoreType', DatiAnagraficiVettoreType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}IscrizioneREAType with
# content type ELEMENT_ONLY
class IscrizioneREAType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
IscrizioneREAType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IscrizioneREAType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 672, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element Ufficio uses Python identifier Ufficio
    __Ufficio = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Ufficio'),
        'Ufficio',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'IscrizioneREAType_Ufficio',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            674,
            6),
    )

    Ufficio = property(__Ufficio.value, __Ufficio.set, None, None)

    # Element NumeroREA uses Python identifier NumeroREA
    __NumeroREA = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NumeroREA'),
        'NumeroREA',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'IscrizioneREAType_NumeroREA',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            675,
            6),
    )

    NumeroREA = property(__NumeroREA.value, __NumeroREA.set, None, None)

    # Element CapitaleSociale uses Python identifier CapitaleSociale
    __CapitaleSociale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CapitaleSociale'),
        'CapitaleSociale',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'IscrizioneREAType_CapitaleSociale',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            676,
            6),
    )

    CapitaleSociale = property(
        __CapitaleSociale.value, __CapitaleSociale.set, None, None)

    # Element SocioUnico uses Python identifier SocioUnico
    __SocioUnico = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'SocioUnico'),
        'SocioUnico',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'IscrizioneREAType_SocioUnico',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            677,
            6),
    )

    SocioUnico = property(__SocioUnico.value, __SocioUnico.set, None, None)

    # Element StatoLiquidazione uses Python identifier StatoLiquidazione
    __StatoLiquidazione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'StatoLiquidazione'),
        'StatoLiquidazione',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'IscrizioneREAType_StatoLiquidazione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            678,
            6),
    )

    StatoLiquidazione = property(
        __StatoLiquidazione.value, __StatoLiquidazione.set, None, None)

    _ElementMap.update({
        __Ufficio.name(): __Ufficio,
        __NumeroREA.name(): __NumeroREA,
        __CapitaleSociale.name(): __CapitaleSociale,
        __SocioUnico.name(): __SocioUnico,
        __StatoLiquidazione.name(): __StatoLiquidazione
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'IscrizioneREAType', IscrizioneREAType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}ContattiType with
# content type ELEMENT_ONLY
class ContattiType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
ContattiType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ContattiType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 681, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element Telefono uses Python identifier Telefono
    __Telefono = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Telefono'),
        'Telefono',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'ContattiType_Telefono',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            683,
            6),
    )

    Telefono = property(__Telefono.value, __Telefono.set, None, None)

    # Element Fax uses Python identifier Fax
    __Fax = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Fax'),
        'Fax',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'ContattiType_Fax',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            684,
            6),
    )

    Fax = property(__Fax.value, __Fax.set, None, None)

    # Element Email uses Python identifier Email
    __Email = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Email'),
        'Email',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'ContattiType_Email',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            685,
            6),
    )

    Email = property(__Email.value, __Email.set, None, None)

    _ElementMap.update({
        __Telefono.name(): __Telefono,
        __Fax.name(): __Fax,
        __Email.name(): __Email
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject('typeBinding', 'ContattiType', ContattiType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}RappresentanteFiscaleType
# with content type ELEMENT_ONLY
class RappresentanteFiscaleType (pyxb.binding.basis.complexTypeDefinition):

    """
            Blocco relativo ai dati del Rappresentante Fiscale
                        """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'RappresentanteFiscaleType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 688, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element DatiAnagrafici uses Python identifier DatiAnagrafici
    __DatiAnagrafici = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiAnagrafici'),
        'DatiAnagrafici',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'RappresentanteFiscaleType_DatiAnagrafici',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            695,
            6),
    )

    DatiAnagrafici = property(
        __DatiAnagrafici.value, __DatiAnagrafici.set, None, None)

    _ElementMap.update({
        __DatiAnagrafici.name(): __DatiAnagrafici
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'RappresentanteFiscaleType', RappresentanteFiscaleType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
# DatiAnagraficiRappresentanteType
# with content type ELEMENT_ONLY
class DatiAnagraficiRappresentanteType(
        pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
DatiAnagraficiRappresentanteType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'DatiAnagraficiRappresentanteType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 698, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdFiscaleIVA uses Python identifier IdFiscaleIVA
    __IdFiscaleIVA = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IdFiscaleIVA'),
        'IdFiscaleIVA',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiRappresentanteType_IdFiscaleIVA',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            700,
            6),
    )

    IdFiscaleIVA = property(
        __IdFiscaleIVA.value, __IdFiscaleIVA.set, None, None)

    # Element CodiceFiscale uses Python identifier CodiceFiscale
    __CodiceFiscale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceFiscale'),
        'CodiceFiscale',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiRappresentanteType_CodiceFiscale',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            701,
            6),
    )

    CodiceFiscale = property(
        __CodiceFiscale.value, __CodiceFiscale.set, None, None)

    # Element Anagrafica uses Python identifier Anagrafica
    __Anagrafica = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Anagrafica'),
        'Anagrafica',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiRappresentanteType_Anagrafica',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            702,
            6),
    )

    Anagrafica = property(__Anagrafica.value, __Anagrafica.set, None, None)

    _ElementMap.update({
        __IdFiscaleIVA.name(): __IdFiscaleIVA,
        __CodiceFiscale.name(): __CodiceFiscale,
        __Anagrafica.name(): __Anagrafica
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding',
    'DatiAnagraficiRappresentanteType',
    DatiAnagraficiRappresentanteType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}CessionarioCommittenteType
# with content type ELEMENT_ONLY
class CessionarioCommittenteType (pyxb.binding.basis.complexTypeDefinition):

    """
            Blocco relativo ai dati del Cessionario / Committente
                        """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'CessionarioCommittenteType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 705, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element DatiAnagrafici uses Python identifier DatiAnagrafici
    __DatiAnagrafici = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiAnagrafici'),
        'DatiAnagrafici',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'CessionarioCommittenteType_DatiAnagrafici',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            712,
            6),
    )

    DatiAnagrafici = property(
        __DatiAnagrafici.value, __DatiAnagrafici.set, None, None)

    # Element Sede uses Python identifier Sede
    __Sede = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Sede'),
        'Sede',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'CessionarioCommittenteType_Sede',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            713,
            6),
    )

    Sede = property(__Sede.value, __Sede.set, None, None)

    _ElementMap.update({
        __DatiAnagrafici.name(): __DatiAnagrafici,
        __Sede.name(): __Sede
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'CessionarioCommittenteType', CessionarioCommittenteType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DatiAnagraficiCessionarioType
# with content type ELEMENT_ONLY
class DatiAnagraficiCessionarioType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
DatiAnagraficiCessionarioType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'DatiAnagraficiCessionarioType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 716, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdFiscaleIVA uses Python identifier IdFiscaleIVA
    __IdFiscaleIVA = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IdFiscaleIVA'),
        'IdFiscaleIVA',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiCessionarioType_IdFiscaleIVA',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            718,
            6),
    )

    IdFiscaleIVA = property(
        __IdFiscaleIVA.value, __IdFiscaleIVA.set, None, None)

    # Element CodiceFiscale uses Python identifier CodiceFiscale
    __CodiceFiscale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceFiscale'),
        'CodiceFiscale',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiCessionarioType_CodiceFiscale',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            719,
            6),
    )

    CodiceFiscale = property(
        __CodiceFiscale.value, __CodiceFiscale.set, None, None)

    # Element Anagrafica uses Python identifier Anagrafica
    __Anagrafica = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Anagrafica'),
        'Anagrafica',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiCessionarioType_Anagrafica',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            720,
            6),
    )

    Anagrafica = property(__Anagrafica.value, __Anagrafica.set, None, None)

    _ElementMap.update({
        __IdFiscaleIVA.name(): __IdFiscaleIVA,
        __CodiceFiscale.name(): __CodiceFiscale,
        __Anagrafica.name(): __Anagrafica
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding',
    'DatiAnagraficiCessionarioType',
    DatiAnagraficiCessionarioType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DatiBeniServiziType with
# content type ELEMENT_ONLY
class DatiBeniServiziType (pyxb.binding.basis.complexTypeDefinition):

    """
        Blocco relativo ai dati di Beni Servizi della Fattura   Elettronica
                        """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'DatiBeniServiziType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 723, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element DettaglioLinee uses Python identifier DettaglioLinee
    __DettaglioLinee = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DettaglioLinee'),
        'DettaglioLinee',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiBeniServiziType_DettaglioLinee',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            730,
            6),
    )

    DettaglioLinee = property(
        __DettaglioLinee.value, __DettaglioLinee.set, None, None)

    # Element DatiRiepilogo uses Python identifier DatiRiepilogo
    __DatiRiepilogo = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiRiepilogo'),
        'DatiRiepilogo',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiBeniServiziType_DatiRiepilogo',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            731,
            6),
    )

    DatiRiepilogo = property(
        __DatiRiepilogo.value, __DatiRiepilogo.set, None, None)

    _ElementMap.update({
        __DettaglioLinee.name(): __DettaglioLinee,
        __DatiRiepilogo.name(): __DatiRiepilogo
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'DatiBeniServiziType', DatiBeniServiziType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DatiVeicoliType with
# content type ELEMENT_ONLY
class DatiVeicoliType (pyxb.binding.basis.complexTypeDefinition):

    """
                    Blocco relativo ai dati dei Veicoli della Fattura
                    Elettronica (da indicare nei casi di cessioni tra Paesi
                    membri di mezzi di trasporto nuovi, in base all'art. 38,
                    comma 4 del dl 331 del 1993)
                        """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiVeicoliType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 734, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element Data uses Python identifier Data
    __Data = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Data'),
        'Data',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiVeicoliType_Data',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            744,
            6),
    )

    Data = property(__Data.value, __Data.set, None, None)

    # Element TotalePercorso uses Python identifier TotalePercorso
    __TotalePercorso = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'TotalePercorso'),
        'TotalePercorso',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiVeicoliType_TotalePercorso',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            745,
            6),
    )

    TotalePercorso = property(
        __TotalePercorso.value, __TotalePercorso.set, None, None)

    _ElementMap.update({
        __Data.name(): __Data,
        __TotalePercorso.name(): __TotalePercorso
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject('typeBinding', 'DatiVeicoliType', DatiVeicoliType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DatiPagamentoType with
# content type ELEMENT_ONLY
class DatiPagamentoType (pyxb.binding.basis.complexTypeDefinition):

    """
            Blocco relativo ai dati di Pagamento della Fattura  Elettronica
                        """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiPagamentoType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 748, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element CondizioniPagamento uses Python identifier CondizioniPagamento
    __CondizioniPagamento = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CondizioniPagamento'),
        'CondizioniPagamento',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiPagamentoType_CondizioniPagamento',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            755,
            6),
    )

    CondizioniPagamento = property(
        __CondizioniPagamento.value, __CondizioniPagamento.set, None, None)

    # Element DettaglioPagamento uses Python identifier DettaglioPagamento
    __DettaglioPagamento = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DettaglioPagamento'),
        'DettaglioPagamento',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiPagamentoType_DettaglioPagamento',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            756,
            6),
    )

    DettaglioPagamento = property(
        __DettaglioPagamento.value, __DettaglioPagamento.set, None, None)

    _ElementMap.update({
        __CondizioniPagamento.name(): __CondizioniPagamento,
        __DettaglioPagamento.name(): __DettaglioPagamento
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'DatiPagamentoType', DatiPagamentoType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DettaglioPagamentoType
# with content type ELEMENT_ONLY
class DettaglioPagamentoType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
DettaglioPagamentoType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'DettaglioPagamentoType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 780, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element Beneficiario uses Python identifier Beneficiario
    __Beneficiario = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Beneficiario'),
        'Beneficiario',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_Beneficiario',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            782,
            6),
    )

    Beneficiario = property(
        __Beneficiario.value, __Beneficiario.set, None, None)

    # Element ModalitaPagamento uses Python identifier ModalitaPagamento
    __ModalitaPagamento = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'ModalitaPagamento'),
        'ModalitaPagamento',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_ModalitaPagamento',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            783,
            6),
    )

    ModalitaPagamento = property(
        __ModalitaPagamento.value, __ModalitaPagamento.set, None, None)

    # Element DataRiferimentoTerminiPagamento uses Python identifier
    # DataRiferimentoTerminiPagamento
    __DataRiferimentoTerminiPagamento = (
        pyxb.binding.content.ElementDeclaration(
            pyxb.namespace.ExpandedName(
                None,
                'DataRiferimentoTerminiPagamento'),
            'DataRiferimentoTerminiPagamento',
            '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
            'DettaglioPagamentoType_DataRiferimentoTerminiPagamento',
            False,
            pyxb.utils.utility.Location(
                '/tmp/fatturapa_v1.1.xsd',
                784,
                6),
        )
    )

    DataRiferimentoTerminiPagamento = property(
        __DataRiferimentoTerminiPagamento.value,
        __DataRiferimentoTerminiPagamento.set,
        None,
        None)

    # Element GiorniTerminiPagamento uses Python identifier
    # GiorniTerminiPagamento
    __GiorniTerminiPagamento = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'GiorniTerminiPagamento'),
        'GiorniTerminiPagamento',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_GiorniTerminiPagamento',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            785,
            6),
    )

    GiorniTerminiPagamento = property(
        __GiorniTerminiPagamento.value,
        __GiorniTerminiPagamento.set,
        None,
        None)

    # Element DataScadenzaPagamento uses Python identifier
    # DataScadenzaPagamento
    __DataScadenzaPagamento = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DataScadenzaPagamento'),
        'DataScadenzaPagamento',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_DataScadenzaPagamento',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            786,
            6),
    )

    DataScadenzaPagamento = property(
        __DataScadenzaPagamento.value, __DataScadenzaPagamento.set, None, None)

    # Element ImportoPagamento uses Python identifier ImportoPagamento
    __ImportoPagamento = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'ImportoPagamento'),
        'ImportoPagamento',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_ImportoPagamento',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            787,
            6),
    )

    ImportoPagamento = property(
        __ImportoPagamento.value, __ImportoPagamento.set, None, None)

    # Element CodUfficioPostale uses Python identifier CodUfficioPostale
    __CodUfficioPostale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CodUfficioPostale'),
        'CodUfficioPostale',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_CodUfficioPostale',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            788,
            6),
    )

    CodUfficioPostale = property(
        __CodUfficioPostale.value, __CodUfficioPostale.set, None, None)

    # Element CognomeQuietanzante uses Python identifier CognomeQuietanzante
    __CognomeQuietanzante = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CognomeQuietanzante'),
        'CognomeQuietanzante',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_CognomeQuietanzante',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            789,
            6),
    )

    CognomeQuietanzante = property(
        __CognomeQuietanzante.value, __CognomeQuietanzante.set, None, None)

    # Element NomeQuietanzante uses Python identifier NomeQuietanzante
    __NomeQuietanzante = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NomeQuietanzante'),
        'NomeQuietanzante',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_NomeQuietanzante',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            790,
            6),
    )

    NomeQuietanzante = property(
        __NomeQuietanzante.value, __NomeQuietanzante.set, None, None)

    # Element CFQuietanzante uses Python identifier CFQuietanzante
    __CFQuietanzante = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CFQuietanzante'),
        'CFQuietanzante',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_CFQuietanzante',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            791,
            6),
    )

    CFQuietanzante = property(
        __CFQuietanzante.value, __CFQuietanzante.set, None, None)

    # Element TitoloQuietanzante uses Python identifier TitoloQuietanzante
    __TitoloQuietanzante = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'TitoloQuietanzante'),
        'TitoloQuietanzante',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_TitoloQuietanzante',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            792,
            6),
    )

    TitoloQuietanzante = property(
        __TitoloQuietanzante.value, __TitoloQuietanzante.set, None, None)

    # Element IstitutoFinanziario uses Python identifier IstitutoFinanziario
    __IstitutoFinanziario = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IstitutoFinanziario'),
        'IstitutoFinanziario',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_IstitutoFinanziario',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            793,
            6),
    )

    IstitutoFinanziario = property(
        __IstitutoFinanziario.value, __IstitutoFinanziario.set, None, None)

    # Element IBAN uses Python identifier IBAN
    __IBAN = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IBAN'),
        'IBAN',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_IBAN',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            794,
            6),
    )

    IBAN = property(__IBAN.value, __IBAN.set, None, None)

    # Element ABI uses Python identifier ABI
    __ABI = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'ABI'),
        'ABI',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_ABI',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            795,
            6),
    )

    ABI = property(__ABI.value, __ABI.set, None, None)

    # Element CAB uses Python identifier CAB
    __CAB = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CAB'),
        'CAB',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_CAB',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            796,
            6),
    )

    CAB = property(__CAB.value, __CAB.set, None, None)

    # Element BIC uses Python identifier BIC
    __BIC = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'BIC'),
        'BIC',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_BIC',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            797,
            6),
    )

    BIC = property(__BIC.value, __BIC.set, None, None)

    # Element ScontoPagamentoAnticipato uses Python identifier
    # ScontoPagamentoAnticipato
    __ScontoPagamentoAnticipato = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'ScontoPagamentoAnticipato'),
        'ScontoPagamentoAnticipato',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_ScontoPagamentoAnticipato',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            798,
            6),
    )

    ScontoPagamentoAnticipato = property(
        __ScontoPagamentoAnticipato.value,
        __ScontoPagamentoAnticipato.set,
        None,
        None)

    # Element DataLimitePagamentoAnticipato uses Python identifier
    # DataLimitePagamentoAnticipato
    __DataLimitePagamentoAnticipato = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DataLimitePagamentoAnticipato'),
        'DataLimitePagamentoAnticipato',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_DataLimitePagamentoAnticipato',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            799,
            6),
    )

    DataLimitePagamentoAnticipato = property(
        __DataLimitePagamentoAnticipato.value,
        __DataLimitePagamentoAnticipato.set,
        None,
        None)

    # Element PenalitaPagamentiRitardati uses Python identifier
    # PenalitaPagamentiRitardati
    __PenalitaPagamentiRitardati = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'PenalitaPagamentiRitardati'),
        'PenalitaPagamentiRitardati',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_PenalitaPagamentiRitardati',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            800,
            6),
    )

    PenalitaPagamentiRitardati = property(
        __PenalitaPagamentiRitardati.value,
        __PenalitaPagamentiRitardati.set,
        None,
        None)

    # Element DataDecorrenzaPenale uses Python identifier DataDecorrenzaPenale
    __DataDecorrenzaPenale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DataDecorrenzaPenale'),
        'DataDecorrenzaPenale',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_DataDecorrenzaPenale',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            801,
            6),
    )

    DataDecorrenzaPenale = property(
        __DataDecorrenzaPenale.value, __DataDecorrenzaPenale.set, None, None)

    # Element CodicePagamento uses Python identifier CodicePagamento
    __CodicePagamento = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CodicePagamento'),
        'CodicePagamento',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioPagamentoType_CodicePagamento',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            802,
            6),
    )

    CodicePagamento = property(
        __CodicePagamento.value, __CodicePagamento.set, None, None)

    _ElementMap.update({
        __Beneficiario.name(): __Beneficiario,
        __ModalitaPagamento.name(): __ModalitaPagamento,
        __DataRiferimentoTerminiPagamento.name():
        __DataRiferimentoTerminiPagamento,
        __GiorniTerminiPagamento.name():
        __GiorniTerminiPagamento,
        __DataScadenzaPagamento.name():
        __DataScadenzaPagamento,
        __ImportoPagamento.name(): __ImportoPagamento,
        __CodUfficioPostale.name():
        __CodUfficioPostale,
        __CognomeQuietanzante.name():
        __CognomeQuietanzante,
        __NomeQuietanzante.name():
        __NomeQuietanzante,
        __CFQuietanzante.name():
        __CFQuietanzante,
        __TitoloQuietanzante.name():
        __TitoloQuietanzante,
        __IstitutoFinanziario.name():
        __IstitutoFinanziario,
        __IBAN.name(): __IBAN,
        __ABI.name(): __ABI,
        __CAB.name(): __CAB,
        __BIC.name(): __BIC,
        __ScontoPagamentoAnticipato.name():
        __ScontoPagamentoAnticipato,
        __DataLimitePagamentoAnticipato.name():
        __DataLimitePagamentoAnticipato,
        __PenalitaPagamentiRitardati.name():
        __PenalitaPagamentiRitardati,
        __DataDecorrenzaPenale.name():
        __DataDecorrenzaPenale,
        __CodicePagamento.name(): __CodicePagamento
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'DettaglioPagamentoType', DettaglioPagamentoType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
# TerzoIntermediarioSoggettoEmittenteType
# with content type ELEMENT_ONLY
class TerzoIntermediarioSoggettoEmittenteType(
        pyxb.binding.basis.complexTypeDefinition):

    """
    Blocco relativo ai dati del Terzo Intermediario che
    emette fattura elettronica per conto del
    Cedente/Prestatore
                        """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'TerzoIntermediarioSoggettoEmittenteType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 925, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element DatiAnagrafici uses Python identifier DatiAnagrafici
    __DatiAnagrafici = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DatiAnagrafici'),
        'DatiAnagrafici',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'TerzoIntermediarioSoggettoEmittenteType_DatiAnagrafici',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            934,
            6),
    )

    DatiAnagrafici = property(
        __DatiAnagrafici.value, __DatiAnagrafici.set, None, None)

    _ElementMap.update({
        __DatiAnagrafici.name(): __DatiAnagrafici
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding',
    'TerzoIntermediarioSoggettoEmittenteType',
    TerzoIntermediarioSoggettoEmittenteType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DatiAnagraficiTerzoIntermediarioType
# with content type ELEMENT_ONLY
class DatiAnagraficiTerzoIntermediarioType(
        pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
DatiAnagraficiTerzoIntermediarioType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'DatiAnagraficiTerzoIntermediarioType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 937, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdFiscaleIVA uses Python identifier IdFiscaleIVA
    __IdFiscaleIVA = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'IdFiscaleIVA'),
        'IdFiscaleIVA',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiTerzoIntermediarioType_IdFiscaleIVA',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            939,
            6),
    )

    IdFiscaleIVA = property(
        __IdFiscaleIVA.value, __IdFiscaleIVA.set, None, None)

    # Element CodiceFiscale uses Python identifier CodiceFiscale
    __CodiceFiscale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceFiscale'),
        'CodiceFiscale',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiTerzoIntermediarioType_CodiceFiscale',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            940,
            6),
    )

    CodiceFiscale = property(
        __CodiceFiscale.value, __CodiceFiscale.set, None, None)

    # Element Anagrafica uses Python identifier Anagrafica
    __Anagrafica = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Anagrafica'),
        'Anagrafica',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiAnagraficiTerzoIntermediarioType_Anagrafica',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            941,
            6),
    )

    Anagrafica = property(__Anagrafica.value, __Anagrafica.set, None, None)

    _ElementMap.update({
        __IdFiscaleIVA.name(): __IdFiscaleIVA,
        __CodiceFiscale.name(): __CodiceFiscale,
        __Anagrafica.name(): __Anagrafica
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding',
    'DatiAnagraficiTerzoIntermediarioType',
    DatiAnagraficiTerzoIntermediarioType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}AllegatiType with
# content type ELEMENT_ONLY
class AllegatiType (pyxb.binding.basis.complexTypeDefinition):

    """
                                Blocco relativo ai dati di eventuali allegati
                        """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AllegatiType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 944, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element NomeAttachment uses Python identifier NomeAttachment
    __NomeAttachment = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NomeAttachment'),
        'NomeAttachment',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'AllegatiType_NomeAttachment',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            951,
            6),
    )

    NomeAttachment = property(
        __NomeAttachment.value, __NomeAttachment.set, None, None)

    # Element AlgoritmoCompressione uses Python identifier
    # AlgoritmoCompressione
    __AlgoritmoCompressione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'AlgoritmoCompressione'),
        'AlgoritmoCompressione',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'AllegatiType_AlgoritmoCompressione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            952,
            6),
    )

    AlgoritmoCompressione = property(
        __AlgoritmoCompressione.value, __AlgoritmoCompressione.set, None, None)

    # Element FormatoAttachment uses Python identifier FormatoAttachment
    __FormatoAttachment = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'FormatoAttachment'),
        'FormatoAttachment',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'AllegatiType_FormatoAttachment',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            953,
            6),
    )

    FormatoAttachment = property(
        __FormatoAttachment.value, __FormatoAttachment.set, None, None)

    # Element DescrizioneAttachment uses Python identifier
    # DescrizioneAttachment
    __DescrizioneAttachment = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DescrizioneAttachment'),
        'DescrizioneAttachment',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'AllegatiType_DescrizioneAttachment',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            954,
            6),
    )

    DescrizioneAttachment = property(
        __DescrizioneAttachment.value, __DescrizioneAttachment.set, None, None)

    # Element Attachment uses Python identifier Attachment
    __Attachment = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Attachment'),
        'Attachment',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'AllegatiType_Attachment',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            955,
            6),
    )

    Attachment = property(__Attachment.value, __Attachment.set, None, None)

    _ElementMap.update({
        __NomeAttachment.name(): __NomeAttachment,
        __AlgoritmoCompressione.name(): __AlgoritmoCompressione,
        __FormatoAttachment.name(): __FormatoAttachment,
        __DescrizioneAttachment.name(): __DescrizioneAttachment,
        __Attachment.name(): __Attachment
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject('typeBinding', 'AllegatiType', AllegatiType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DettaglioLineeType with
# content type ELEMENT_ONLY
class DettaglioLineeType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
DettaglioLineeType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'DettaglioLineeType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 958, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element NumeroLinea uses Python identifier NumeroLinea
    __NumeroLinea = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'NumeroLinea'),
        'NumeroLinea',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioLineeType_NumeroLinea',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            960,
            6),
    )

    NumeroLinea = property(__NumeroLinea.value, __NumeroLinea.set, None, None)

    # Element TipoCessionePrestazione uses Python identifier
    # TipoCessionePrestazione
    __TipoCessionePrestazione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'TipoCessionePrestazione'),
        'TipoCessionePrestazione',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioLineeType_TipoCessionePrestazione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            961,
            6),
    )

    TipoCessionePrestazione = property(
        __TipoCessionePrestazione.value,
        __TipoCessionePrestazione.set,
        None,
        None)

    # Element CodiceArticolo uses Python identifier CodiceArticolo
    __CodiceArticolo = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceArticolo'),
        'CodiceArticolo',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioLineeType_CodiceArticolo',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            962,
            6),
    )

    CodiceArticolo = property(
        __CodiceArticolo.value, __CodiceArticolo.set, None, None)

    # Element Descrizione uses Python identifier Descrizione
    __Descrizione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Descrizione'),
        'Descrizione',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioLineeType_Descrizione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            963,
            6),
    )

    Descrizione = property(__Descrizione.value, __Descrizione.set, None, None)

    # Element Quantita uses Python identifier Quantita
    __Quantita = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Quantita'),
        'Quantita',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioLineeType_Quantita',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            964,
            6),
    )

    Quantita = property(__Quantita.value, __Quantita.set, None, None)

    # Element UnitaMisura uses Python identifier UnitaMisura
    __UnitaMisura = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'UnitaMisura'),
        'UnitaMisura',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioLineeType_UnitaMisura',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            965,
            6),
    )

    UnitaMisura = property(__UnitaMisura.value, __UnitaMisura.set, None, None)

    # Element DataInizioPeriodo uses Python identifier DataInizioPeriodo
    __DataInizioPeriodo = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DataInizioPeriodo'),
        'DataInizioPeriodo',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioLineeType_DataInizioPeriodo',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            966,
            6),
    )

    DataInizioPeriodo = property(
        __DataInizioPeriodo.value, __DataInizioPeriodo.set, None, None)

    # Element DataFinePeriodo uses Python identifier DataFinePeriodo
    __DataFinePeriodo = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'DataFinePeriodo'),
        'DataFinePeriodo',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioLineeType_DataFinePeriodo',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            967,
            6),
    )

    DataFinePeriodo = property(
        __DataFinePeriodo.value, __DataFinePeriodo.set, None, None)

    # Element PrezzoUnitario uses Python identifier PrezzoUnitario
    __PrezzoUnitario = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'PrezzoUnitario'),
        'PrezzoUnitario',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioLineeType_PrezzoUnitario',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            968,
            6),
    )

    PrezzoUnitario = property(
        __PrezzoUnitario.value, __PrezzoUnitario.set, None, None)

    # Element ScontoMaggiorazione uses Python identifier ScontoMaggiorazione
    __ScontoMaggiorazione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'ScontoMaggiorazione'),
        'ScontoMaggiorazione',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioLineeType_ScontoMaggiorazione',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            969,
            6),
    )

    ScontoMaggiorazione = property(
        __ScontoMaggiorazione.value, __ScontoMaggiorazione.set, None, None)

    # Element PrezzoTotale uses Python identifier PrezzoTotale
    __PrezzoTotale = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'PrezzoTotale'),
        'PrezzoTotale',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioLineeType_PrezzoTotale',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            970,
            6),
    )

    PrezzoTotale = property(
        __PrezzoTotale.value, __PrezzoTotale.set, None, None)

    # Element AliquotaIVA uses Python identifier AliquotaIVA
    __AliquotaIVA = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'AliquotaIVA'),
        'AliquotaIVA',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioLineeType_AliquotaIVA',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            971,
            6),
    )

    AliquotaIVA = property(__AliquotaIVA.value, __AliquotaIVA.set, None, None)

    # Element Ritenuta uses Python identifier Ritenuta
    __Ritenuta = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Ritenuta'),
        'Ritenuta',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioLineeType_Ritenuta',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            972,
            6),
    )

    Ritenuta = property(__Ritenuta.value, __Ritenuta.set, None, None)

    # Element Natura uses Python identifier Natura
    __Natura = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Natura'),
        'Natura',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioLineeType_Natura',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            973,
            6),
    )

    Natura = property(__Natura.value, __Natura.set, None, None)

    # Element RiferimentoAmministrazione uses Python identifier
    # RiferimentoAmministrazione
    __RiferimentoAmministrazione = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoAmministrazione'),
        'RiferimentoAmministrazione',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioLineeType_RiferimentoAmministrazione',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            974,
            6),
    )

    RiferimentoAmministrazione = property(
        __RiferimentoAmministrazione.value,
        __RiferimentoAmministrazione.set,
        None,
        None)

    # Element AltriDatiGestionali uses Python identifier AltriDatiGestionali
    __AltriDatiGestionali = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'AltriDatiGestionali'),
        'AltriDatiGestionali',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DettaglioLineeType_AltriDatiGestionali',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            975,
            6),
    )

    AltriDatiGestionali = property(
        __AltriDatiGestionali.value, __AltriDatiGestionali.set, None, None)

    _ElementMap.update({
        __NumeroLinea.name(): __NumeroLinea,
        __TipoCessionePrestazione.name(): __TipoCessionePrestazione,
        __CodiceArticolo.name(): __CodiceArticolo,
        __Descrizione.name(): __Descrizione,
        __Quantita.name(): __Quantita,
        __UnitaMisura.name(): __UnitaMisura,
        __DataInizioPeriodo.name(): __DataInizioPeriodo,
        __DataFinePeriodo.name(): __DataFinePeriodo,
        __PrezzoUnitario.name(): __PrezzoUnitario,
        __ScontoMaggiorazione.name(): __ScontoMaggiorazione,
        __PrezzoTotale.name(): __PrezzoTotale,
        __AliquotaIVA.name(): __AliquotaIVA,
        __Ritenuta.name(): __Ritenuta,
        __Natura.name(): __Natura,
        __RiferimentoAmministrazione.name(): __RiferimentoAmministrazione,
        __AltriDatiGestionali.name(): __AltriDatiGestionali
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'DettaglioLineeType', DettaglioLineeType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}CodiceArticoloType with
# content type ELEMENT_ONLY
class CodiceArticoloType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
CodiceArticoloType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'CodiceArticoloType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 978, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element CodiceTipo uses Python identifier CodiceTipo
    __CodiceTipo = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceTipo'),
        'CodiceTipo',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'CodiceArticoloType_CodiceTipo',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            980,
            6),
    )

    CodiceTipo = property(__CodiceTipo.value, __CodiceTipo.set, None, None)

    # Element CodiceValore uses Python identifier CodiceValore
    __CodiceValore = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceValore'),
        'CodiceValore',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'CodiceArticoloType_CodiceValore',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            981,
            6),
    )

    CodiceValore = property(
        __CodiceValore.value, __CodiceValore.set, None, None)

    _ElementMap.update({
        __CodiceTipo.name(): __CodiceTipo,
        __CodiceValore.name(): __CodiceValore
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'CodiceArticoloType', CodiceArticoloType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}AltriDatiGestionaliType
# with content type ELEMENT_ONLY
class AltriDatiGestionaliType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
AltriDatiGestionaliType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'AltriDatiGestionaliType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 984, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element TipoDato uses Python identifier TipoDato
    __TipoDato = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'TipoDato'),
        'TipoDato',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'AltriDatiGestionaliType_TipoDato',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            986,
            6),
    )

    TipoDato = property(__TipoDato.value, __TipoDato.set, None, None)

    # Element RiferimentoTesto uses Python identifier RiferimentoTesto
    __RiferimentoTesto = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoTesto'),
        'RiferimentoTesto',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'AltriDatiGestionaliType_RiferimentoTesto',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            987,
            6),
    )

    RiferimentoTesto = property(
        __RiferimentoTesto.value, __RiferimentoTesto.set, None, None)

    # Element RiferimentoNumero uses Python identifier RiferimentoNumero
    __RiferimentoNumero = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoNumero'),
        'RiferimentoNumero',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'AltriDatiGestionaliType_RiferimentoNumero',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            988,
            6),
    )

    RiferimentoNumero = property(
        __RiferimentoNumero.value, __RiferimentoNumero.set, None, None)

    # Element RiferimentoData uses Python identifier RiferimentoData
    __RiferimentoData = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoData'),
        'RiferimentoData',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'AltriDatiGestionaliType_RiferimentoData',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            989,
            6),
    )

    RiferimentoData = property(
        __RiferimentoData.value, __RiferimentoData.set, None, None)

    _ElementMap.update({
        __TipoDato.name(): __TipoDato,
        __RiferimentoTesto.name(): __RiferimentoTesto,
        __RiferimentoNumero.name(): __RiferimentoNumero,
        __RiferimentoData.name(): __RiferimentoData
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'AltriDatiGestionaliType', AltriDatiGestionaliType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}DatiRiepilogoType with
# content type ELEMENT_ONLY
class DatiRiepilogoType (pyxb.binding.basis.complexTypeDefinition):

    """Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}

    DatiRiepilogoType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiRiepilogoType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 1004, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element AliquotaIVA uses Python identifier AliquotaIVA
    __AliquotaIVA = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'AliquotaIVA'),
        'AliquotaIVA',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiRiepilogoType_AliquotaIVA',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1006,
            6),
    )

    AliquotaIVA = property(__AliquotaIVA.value, __AliquotaIVA.set, None, None)

    # Element Natura uses Python identifier Natura
    __Natura = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Natura'),
        'Natura',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiRiepilogoType_Natura',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1007,
            6),
    )

    Natura = property(__Natura.value, __Natura.set, None, None)

    # Element SpeseAccessorie uses Python identifier SpeseAccessorie
    __SpeseAccessorie = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'SpeseAccessorie'),
        'SpeseAccessorie',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiRiepilogoType_SpeseAccessorie',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1008,
            6),
    )

    SpeseAccessorie = property(
        __SpeseAccessorie.value, __SpeseAccessorie.set, None, None)

    # Element Arrotondamento uses Python identifier Arrotondamento
    __Arrotondamento = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Arrotondamento'),
        'Arrotondamento',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiRiepilogoType_Arrotondamento',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1009,
            6),
    )

    Arrotondamento = property(
        __Arrotondamento.value, __Arrotondamento.set, None, None)

    # Element ImponibileImporto uses Python identifier ImponibileImporto
    __ImponibileImporto = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'ImponibileImporto'),
        'ImponibileImporto',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiRiepilogoType_ImponibileImporto',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1010,
            6),
    )

    ImponibileImporto = property(
        __ImponibileImporto.value, __ImponibileImporto.set, None, None)

    # Element Imposta uses Python identifier Imposta
    __Imposta = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'Imposta'),
        'Imposta',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiRiepilogoType_Imposta',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1011,
            6),
    )

    Imposta = property(__Imposta.value, __Imposta.set, None, None)

    # Element EsigibilitaIVA uses Python identifier EsigibilitaIVA
    __EsigibilitaIVA = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'EsigibilitaIVA'),
        'EsigibilitaIVA',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'DatiRiepilogoType_EsigibilitaIVA',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1012,
            6),
    )

    EsigibilitaIVA = property(
        __EsigibilitaIVA.value, __EsigibilitaIVA.set, None, None)

    # Element RiferimentoNormativo uses Python identifier RiferimentoNormativo
    __RiferimentoNormativo = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoNormativo'),
        'RiferimentoNormativo',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1'
        '_DatiRiepilogoType_RiferimentoNormativo',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1013,
            6),
    )

    RiferimentoNormativo = property(
        __RiferimentoNormativo.value, __RiferimentoNormativo.set, None, None)

    _ElementMap.update({
        __AliquotaIVA.name(): __AliquotaIVA,
        __Natura.name(): __Natura,
        __SpeseAccessorie.name(): __SpeseAccessorie,
        __Arrotondamento.name(): __Arrotondamento,
        __ImponibileImporto.name(): __ImponibileImporto,
        __Imposta.name(): __Imposta,
        __EsigibilitaIVA.name(): __EsigibilitaIVA,
        __RiferimentoNormativo.name(): __RiferimentoNormativo
    })
    _AttributeMap.update({

    })
Namespace.addCategoryObject(
    'typeBinding', 'DatiRiepilogoType', DatiRiepilogoType)


# Complex type
# {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}FatturaElettronicaType
# with content type ELEMENT_ONLY
class FatturaElettronicaType (pyxb.binding.basis.complexTypeDefinition):

    """
    Complex type {http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}
    FatturaElettronicaType with content type ELEMENT_ONLY
    """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(
        Namespace, 'FatturaElettronicaType')
    _XSDLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 11, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element FatturaElettronicaHeader uses Python identifier
    # FatturaElettronicaHeader
    __FatturaElettronicaHeader = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'FatturaElettronicaHeader'),
        'FatturaElettronicaHeader',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1'
        '_FatturaElettronicaType_FatturaElettronicaHeader',
        False,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            13,
            6),
    )

    FatturaElettronicaHeader = property(
        __FatturaElettronicaHeader.value,
        __FatturaElettronicaHeader.set,
        None,
        None)

    # Element FatturaElettronicaBody uses Python identifier
    # FatturaElettronicaBody
    __FatturaElettronicaBody = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            None,
            'FatturaElettronicaBody'),
        'FatturaElettronicaBody',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1'
        '_FatturaElettronicaType_FatturaElettronicaBody',
        True,
        pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            14,
            6),
    )

    FatturaElettronicaBody = property(
        __FatturaElettronicaBody.value,
        __FatturaElettronicaBody.set,
        None,
        None)

    # Element {http://www.w3.org/2000/09/xmldsig#}Signature uses Python
    # identifier Signature
    __Signature = pyxb.binding.content.ElementDeclaration(
        pyxb.namespace.ExpandedName(
            _Namespace_ds,
            'Signature'),
        'Signature',
        '__httpwww_fatturapa_gov_itsdifatturapav1_1_'
        'FatturaElettronicaType_httpwww_w3_org200009xmldsigSignature',
        False,
        pyxb.utils.utility.Location(
            'http://www.w3.org/TR/2002/REC-xmldsig-'
            'core-20020212/xmldsig-core-schema.xsd',
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
        (
            '__httpwww_fatturapa_gov_itsdifatturapav1_'
            '1_FatturaElettronicaType_versione'),
        VersioneSchemaType,
        required=True)
    __versione._DeclarationLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 17, 4)
    __versione._UseLocation = pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd', 17, 4)

    versione = property(__versione.value, __versione.set, None, None)

    _ElementMap.update({
        __FatturaElettronicaHeader.name(): __FatturaElettronicaHeader,
        __FatturaElettronicaBody.name(): __FatturaElettronicaBody,
        __Signature.name(): __Signature
    })
    _AttributeMap.update({
        __versione.name(): __versione
    })
Namespace.addCategoryObject(
    'typeBinding', 'FatturaElettronicaType', FatturaElettronicaType)


FatturaElettronica = pyxb.binding.basis.element(
    pyxb.namespace.ExpandedName(
        Namespace,
        'FatturaElettronica'),
    FatturaElettronicaType,
    documentation=(
        '\n\t\t\t\tXML schema per fattura elettronica '
        'Sistema Di Interscambio SDI 1.1\n\t\t\t'),
    location=pyxb.utils.utility.Location(
        '/tmp/fatturapa_v1.1.xsd',
        4,
        2))
Namespace.addCategoryObject(
    'elementBinding',
    FatturaElettronica.name().localName(),
    FatturaElettronica)


FatturaElettronicaHeaderType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiTrasmissione'),
        DatiTrasmissioneType,
        scope=FatturaElettronicaHeaderType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            21,
            6)))

FatturaElettronicaHeaderType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CedentePrestatore'),
        CedentePrestatoreType,
        scope=FatturaElettronicaHeaderType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            22,
            6)))

FatturaElettronicaHeaderType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'RappresentanteFiscale'),
        RappresentanteFiscaleType,
        scope=FatturaElettronicaHeaderType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            23,
            6)))

FatturaElettronicaHeaderType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CessionarioCommittente'),
        CessionarioCommittenteType,
        scope=FatturaElettronicaHeaderType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            24,
            6)))

FatturaElettronicaHeaderType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None, 'TerzoIntermediarioOSoggettoEmittente'),
        TerzoIntermediarioSoggettoEmittenteType,
        scope=FatturaElettronicaHeaderType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 25, 6)))

FatturaElettronicaHeaderType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'SoggettoEmittente'),
        SoggettoEmittenteType,
        scope=FatturaElettronicaHeaderType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            26,
            6)))


def _BuildAutomaton():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            23,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            25,
            6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            26,
            6))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        FatturaElettronicaHeaderType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiTrasmissione')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 21, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        FatturaElettronicaHeaderType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CedentePrestatore')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 22, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        FatturaElettronicaHeaderType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'RappresentanteFiscale')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 23, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        FatturaElettronicaHeaderType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CessionarioCommittente')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 24, 6))
    st_3 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(
        FatturaElettronicaHeaderType._UseForTag(
            pyxb.namespace.ExpandedName(
                None,
                'TerzoIntermediarioOSoggettoEmittente')
        ), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 25, 6))
    st_4 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(
        FatturaElettronicaHeaderType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'SoggettoEmittente')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 26, 6))
    st_5 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
    ]))
    transitions.append(fac.Transition(st_3, [
    ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False)]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
    ]))
    transitions.append(fac.Transition(st_5, [
    ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False)]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True)]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
FatturaElettronicaHeaderType._Automaton = _BuildAutomaton()


FatturaElettronicaBodyType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiGenerali'),
        DatiGeneraliType,
        scope=FatturaElettronicaBodyType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            31,
            6)))

FatturaElettronicaBodyType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiBeniServizi'),
        DatiBeniServiziType,
        scope=FatturaElettronicaBodyType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            32,
            6)))

FatturaElettronicaBodyType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiVeicoli'),
        DatiVeicoliType,
        scope=FatturaElettronicaBodyType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            33,
            6)))

FatturaElettronicaBodyType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiPagamento'),
        DatiPagamentoType,
        scope=FatturaElettronicaBodyType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            34,
            6)))

FatturaElettronicaBodyType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Allegati'),
        AllegatiType,
        scope=FatturaElettronicaBodyType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            35,
            6)))


def _BuildAutomaton_():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            33,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=None,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            34,
            6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=None,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            35,
            6))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        FatturaElettronicaBodyType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiGenerali')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 31, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        FatturaElettronicaBodyType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiBeniServizi')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 32, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(
        FatturaElettronicaBodyType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiVeicoli')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 33, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(
        FatturaElettronicaBodyType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiPagamento')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 34, 6))
    st_3 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(
        FatturaElettronicaBodyType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Allegati')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 35, 6))
    st_4 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
    ]))
    transitions.append(fac.Transition(st_3, [
    ]))
    transitions.append(fac.Transition(st_4, [
    ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False)]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False)]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True)]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
FatturaElettronicaBodyType._Automaton = _BuildAutomaton_()


DatiTrasmissioneType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IdTrasmittente'),
        IdFiscaleType,
        scope=DatiTrasmissioneType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            51,
            6)))

DatiTrasmissioneType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'ProgressivoInvio'),
        String10Type,
        scope=DatiTrasmissioneType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            52,
            6)))

DatiTrasmissioneType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'FormatoTrasmissione'),
        FormatoTrasmissioneType,
        scope=DatiTrasmissioneType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            53,
            6)))

DatiTrasmissioneType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceDestinatario'),
        CodiceDestinatarioType,
        scope=DatiTrasmissioneType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            54,
            6)))

DatiTrasmissioneType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'ContattiTrasmittente'),
        ContattiTrasmittenteType,
        scope=DatiTrasmissioneType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            55,
            6)))


def _BuildAutomaton_2():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            55,
            6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiTrasmissioneType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IdTrasmittente')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 51, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiTrasmissioneType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'ProgressivoInvio')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 52, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiTrasmissioneType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'FormatoTrasmissione')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 53, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DatiTrasmissioneType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CodiceDestinatario')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 54, 6))
    st_3 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiTrasmissioneType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'ContattiTrasmittente')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 55, 6))
    st_4 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
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
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True)]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiTrasmissioneType._Automaton = _BuildAutomaton_2()


IdFiscaleType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IdPaese'),
        NazioneType,
        scope=IdFiscaleType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            65,
            6)))

IdFiscaleType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IdCodice'),
        CodiceType,
        scope=IdFiscaleType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            66,
            6)))


def _BuildAutomaton_3():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        IdFiscaleType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IdPaese')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 65, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        IdFiscaleType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IdCodice')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 66, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
IdFiscaleType._Automaton = _BuildAutomaton_3()


ContattiTrasmittenteType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Telefono'),
        TelFaxType,
        scope=ContattiTrasmittenteType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            95,
            6)))

ContattiTrasmittenteType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Email'),
        EmailType,
        scope=ContattiTrasmittenteType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            96,
            6)))


def _BuildAutomaton_4():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            95,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            96,
            6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(
        ContattiTrasmittenteType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Telefono')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 95, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(
        ContattiTrasmittenteType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Email')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 96, 6))
    st_1 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False)]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True)]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ContattiTrasmittenteType._Automaton = _BuildAutomaton_4()


DatiGeneraliType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiGeneraliDocumento'),
        DatiGeneraliDocumentoType,
        scope=DatiGeneraliType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            106,
            6)))

DatiGeneraliType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiOrdineAcquisto'),
        DatiDocumentiCorrelatiType,
        scope=DatiGeneraliType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            107,
            6)))

DatiGeneraliType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiContratto'),
        DatiDocumentiCorrelatiType,
        scope=DatiGeneraliType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            108,
            6)))

DatiGeneraliType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiConvenzione'),
        DatiDocumentiCorrelatiType,
        scope=DatiGeneraliType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            109,
            6)))

DatiGeneraliType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiRicezione'),
        DatiDocumentiCorrelatiType,
        scope=DatiGeneraliType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            110,
            6)))

DatiGeneraliType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiFattureCollegate'),
        DatiDocumentiCorrelatiType,
        scope=DatiGeneraliType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            111,
            6)))

DatiGeneraliType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiSAL'),
        DatiSALType,
        scope=DatiGeneraliType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            112,
            6)))

DatiGeneraliType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiDDT'),
        DatiDDTType,
        scope=DatiGeneraliType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            113,
            6)))

DatiGeneraliType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiTrasporto'),
        DatiTrasportoType,
        scope=DatiGeneraliType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            114,
            6)))

DatiGeneraliType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'FatturaPrincipale'),
        FatturaPrincipaleType,
        scope=DatiGeneraliType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            115,
            6)))


def _BuildAutomaton_5():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=None,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            107,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=None,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            108,
            6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=None,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            109,
            6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(
        min=0,
        max=None,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            110,
            6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(
        min=0,
        max=None,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            111,
            6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(
        min=0,
        max=None,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            112,
            6))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(
        min=0,
        max=None,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            113,
            6))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            114,
            6))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            115,
            6))
    counters.add(cc_8)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiGeneraliDocumento')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 106, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiOrdineAcquisto')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 107, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiContratto')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 108, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiConvenzione')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 109, 6))
    st_3 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiRicezione')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 110, 6))
    st_4 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiFattureCollegate')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 111, 6))
    st_5 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiSAL')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 112, 6))
    st_6 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiDDT')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 113, 6))
    st_7 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiTrasporto')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 114, 6))
    st_8 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'FatturaPrincipale')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 115, 6))
    st_9 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    transitions.append(fac.Transition(st_2, [
    ]))
    transitions.append(fac.Transition(st_3, [
    ]))
    transitions.append(fac.Transition(st_4, [
    ]))
    transitions.append(fac.Transition(st_5, [
    ]))
    transitions.append(fac.Transition(st_6, [
    ]))
    transitions.append(fac.Transition(st_7, [
    ]))
    transitions.append(fac.Transition(st_8, [
    ]))
    transitions.append(fac.Transition(st_9, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False)]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False)]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False)]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False)]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False)]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False)]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, True)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False)]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False)]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, True)]))
    st_9._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiGeneraliType._Automaton = _BuildAutomaton_5()


DatiGeneraliDocumentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'TipoDocumento'),
        TipoDocumentoType,
        scope=DatiGeneraliDocumentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            120,
            6)))

DatiGeneraliDocumentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Divisa'),
        DivisaType,
        scope=DatiGeneraliDocumentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            121,
            6)))

DatiGeneraliDocumentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Data'),
        DataFatturaType,
        scope=DatiGeneraliDocumentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            122,
            6)))

DatiGeneraliDocumentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Numero'),
        String20Type,
        scope=DatiGeneraliDocumentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            123,
            6)))

DatiGeneraliDocumentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiRitenuta'),
        DatiRitenutaType,
        scope=DatiGeneraliDocumentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            124,
            6)))

DatiGeneraliDocumentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiBollo'),
        DatiBolloType,
        scope=DatiGeneraliDocumentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            125,
            6)))

DatiGeneraliDocumentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiCassaPrevidenziale'),
        DatiCassaPrevidenzialeType,
        scope=DatiGeneraliDocumentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            126,
            6)))

DatiGeneraliDocumentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'ScontoMaggiorazione'),
        ScontoMaggiorazioneType,
        scope=DatiGeneraliDocumentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            127,
            6)))

DatiGeneraliDocumentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'ImportoTotaleDocumento'),
        Amount2DecimalType,
        scope=DatiGeneraliDocumentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            128,
            6)))

DatiGeneraliDocumentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Arrotondamento'),
        Amount2DecimalType,
        scope=DatiGeneraliDocumentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            129,
            6)))

DatiGeneraliDocumentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Causale'),
        String200LatinType,
        scope=DatiGeneraliDocumentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            130,
            6)))

DatiGeneraliDocumentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Art73'),
        Art73Type,
        scope=DatiGeneraliDocumentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            131,
            6)))


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
            '/tmp/fatturapa_v1.1.xsd',
            124,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            125,
            6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=None,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            126,
            6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(
        min=0,
        max=None,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            127,
            6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            128,
            6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            129,
            6))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(
        min=0,
        max=None,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            130,
            6))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            131,
            6))
    counters.add(cc_7)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliDocumentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'TipoDocumento')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 120, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliDocumentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Divisa')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 121, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliDocumentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Data')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 122, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliDocumentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Numero')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 123, 6))
    st_3 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliDocumentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiRitenuta')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 124, 6))
    st_4 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliDocumentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiBollo')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 125, 6))
    st_5 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliDocumentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiCassaPrevidenziale')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 126, 6))
    st_6 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliDocumentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'ScontoMaggiorazione')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 127, 6))
    st_7 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliDocumentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'ImportoTotaleDocumento')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 128, 6))
    st_8 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliDocumentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Arrotondamento')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 129, 6))
    st_9 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliDocumentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Causale')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 130, 6))
    st_10 = fac.State(symbol, is_initial=False,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiGeneraliDocumentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Art73')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 131, 6))
    st_11 = fac.State(symbol, is_initial=False,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
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
    transitions.append(fac.Transition(st_7, [
    ]))
    transitions.append(fac.Transition(st_8, [
    ]))
    transitions.append(fac.Transition(st_9, [
    ]))
    transitions.append(fac.Transition(st_10, [
    ]))
    transitions.append(fac.Transition(st_11, [
    ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False)]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, False)]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, True)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False)]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, False)]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, True)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False)]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, True)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False)]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, True)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False)]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, True)]))
    st_11._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiGeneraliDocumentoType._Automaton = _BuildAutomaton_6()


DatiRitenutaType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'TipoRitenuta'),
        TipoRitenutaType,
        scope=DatiRitenutaType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            136,
            6)))

DatiRitenutaType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'ImportoRitenuta'),
        Amount2DecimalType,
        scope=DatiRitenutaType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            137,
            6)))

DatiRitenutaType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'AliquotaRitenuta'),
        RateType,
        scope=DatiRitenutaType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            138,
            6)))

DatiRitenutaType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CausalePagamento'),
        CausalePagamentoType,
        scope=DatiRitenutaType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            139,
            6)))


def _BuildAutomaton_7():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiRitenutaType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'TipoRitenuta')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 136, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiRitenutaType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'ImportoRitenuta')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 137, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiRitenutaType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'AliquotaRitenuta')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 138, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DatiRitenutaType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CausalePagamento')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 139, 6))
    st_3 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
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
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiRitenutaType._Automaton = _BuildAutomaton_7()


DatiBolloType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'BolloVirtuale'),
        BolloVirtualeType,
        scope=DatiBolloType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            144,
            6)))

DatiBolloType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'ImportoBollo'),
        Amount2DecimalType,
        scope=DatiBolloType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            145,
            6)))


def _BuildAutomaton_8():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiBolloType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'BolloVirtuale')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 144, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DatiBolloType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'ImportoBollo')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 145, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiBolloType._Automaton = _BuildAutomaton_8()


DatiCassaPrevidenzialeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'TipoCassa'),
        TipoCassaType,
        scope=DatiCassaPrevidenzialeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            150,
            6)))

DatiCassaPrevidenzialeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'AlCassa'),
        RateType,
        scope=DatiCassaPrevidenzialeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            151,
            6)))

DatiCassaPrevidenzialeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'ImportoContributoCassa'),
        Amount2DecimalType,
        scope=DatiCassaPrevidenzialeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            152,
            6)))

DatiCassaPrevidenzialeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'ImponibileCassa'),
        Amount2DecimalType,
        scope=DatiCassaPrevidenzialeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            153,
            6)))

DatiCassaPrevidenzialeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'AliquotaIVA'),
        RateType,
        scope=DatiCassaPrevidenzialeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            154,
            6)))

DatiCassaPrevidenzialeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Ritenuta'),
        RitenutaType,
        scope=DatiCassaPrevidenzialeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            155,
            6)))

DatiCassaPrevidenzialeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Natura'),
        NaturaType,
        scope=DatiCassaPrevidenzialeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            156,
            6)))

DatiCassaPrevidenzialeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoAmministrazione'),
        String20Type,
        scope=DatiCassaPrevidenzialeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            157,
            6)))


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
            '/tmp/fatturapa_v1.1.xsd',
            153,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            155,
            6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            156,
            6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            157,
            6))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiCassaPrevidenzialeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'TipoCassa')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 150, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiCassaPrevidenzialeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'AlCassa')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 151, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiCassaPrevidenzialeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'ImportoContributoCassa')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 152, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiCassaPrevidenzialeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'ImponibileCassa')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 153, 6))
    st_3 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DatiCassaPrevidenzialeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'AliquotaIVA')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 154, 6))
    st_4 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiCassaPrevidenzialeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Ritenuta')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 155, 6))
    st_5 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiCassaPrevidenzialeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Natura')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 156, 6))
    st_6 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiCassaPrevidenzialeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None,
                'RiferimentoAmministrazione')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 157, 6))
    st_7 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
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
    transitions.append(fac.Transition(st_6, [
    ]))
    transitions.append(fac.Transition(st_7, [
    ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False)]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, True)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False)]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True)]))
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiCassaPrevidenzialeType._Automaton = _BuildAutomaton_9()


ScontoMaggiorazioneType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Tipo'),
        TipoScontoMaggiorazioneType,
        scope=ScontoMaggiorazioneType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            162,
            6)))

ScontoMaggiorazioneType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Percentuale'),
        RateType,
        scope=ScontoMaggiorazioneType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            163,
            6)))

ScontoMaggiorazioneType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Importo'),
        Amount2DecimalType,
        scope=ScontoMaggiorazioneType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            164,
            6)))


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
            '/tmp/fatturapa_v1.1.xsd',
            163,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            164,
            6))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        ScontoMaggiorazioneType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Tipo')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 162, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(
        ScontoMaggiorazioneType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Percentuale')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 163, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(
        ScontoMaggiorazioneType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Importo')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 164, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
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
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True)]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ScontoMaggiorazioneType._Automaton = _BuildAutomaton_10()


DatiSALType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoFase'),
        RiferimentoFaseType,
        scope=DatiSALType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            441,
            6)))


def _BuildAutomaton_11():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DatiSALType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'RiferimentoFase')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 441, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiSALType._Automaton = _BuildAutomaton_11()


DatiDocumentiCorrelatiType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoNumeroLinea'),
        RiferimentoNumeroLineaType,
        scope=DatiDocumentiCorrelatiType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            446,
            6)))

DatiDocumentiCorrelatiType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IdDocumento'),
        String20Type,
        scope=DatiDocumentiCorrelatiType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            447,
            6)))

DatiDocumentiCorrelatiType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Data'),
        pyxb.binding.datatypes.date,
        scope=DatiDocumentiCorrelatiType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            448,
            6)))

DatiDocumentiCorrelatiType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NumItem'),
        String20Type,
        scope=DatiDocumentiCorrelatiType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            449,
            6)))

DatiDocumentiCorrelatiType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceCommessaConvenzione'),
        String100LatinType,
        scope=DatiDocumentiCorrelatiType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            450,
            6)))

DatiDocumentiCorrelatiType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceCUP'),
        String15Type,
        scope=DatiDocumentiCorrelatiType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            451,
            6)))

DatiDocumentiCorrelatiType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceCIG'),
        String15Type,
        scope=DatiDocumentiCorrelatiType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            452,
            6)))


def _BuildAutomaton_12():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=None,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            446,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            448,
            6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            449,
            6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            450,
            6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            451,
            6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            452,
            6))
    counters.add(cc_5)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiDocumentiCorrelatiType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'RiferimentoNumeroLinea')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 446, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DatiDocumentiCorrelatiType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IdDocumento')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 447, 6))
    st_1 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiDocumentiCorrelatiType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Data')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 448, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiDocumentiCorrelatiType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NumItem')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 449, 6))
    st_3 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiDocumentiCorrelatiType._UseForTag(
            pyxb.namespace.ExpandedName(
                None,
                'CodiceCommessaConvenzione')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 450, 6))
    st_4 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiDocumentiCorrelatiType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CodiceCUP')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 451, 6))
    st_5 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiDocumentiCorrelatiType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CodiceCIG')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 452, 6))
    st_6 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False)]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
    ]))
    transitions.append(fac.Transition(st_3, [
    ]))
    transitions.append(fac.Transition(st_4, [
    ]))
    transitions.append(fac.Transition(st_5, [
    ]))
    transitions.append(fac.Transition(st_6, [
    ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False)]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False)]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False)]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False)]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True)]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiDocumentiCorrelatiType._Automaton = _BuildAutomaton_12()


DatiDDTType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NumeroDDT'),
        String20Type,
        scope=DatiDDTType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            463,
            6)))

DatiDDTType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DataDDT'),
        pyxb.binding.datatypes.date,
        scope=DatiDDTType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            464,
            6)))

DatiDDTType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoNumeroLinea'),
        RiferimentoNumeroLineaType,
        scope=DatiDDTType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            465,
            6)))


def _BuildAutomaton_13():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=None,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            465,
            6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiDDTType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NumeroDDT')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 463, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DatiDDTType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DataDDT')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 464, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiDDTType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'RiferimentoNumeroLinea')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 465, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
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
DatiDDTType._Automaton = _BuildAutomaton_13()


DatiTrasportoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiAnagraficiVettore'),
        DatiAnagraficiVettoreType,
        scope=DatiTrasportoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            470,
            6)))

DatiTrasportoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'MezzoTrasporto'),
        String80LatinType,
        scope=DatiTrasportoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            471,
            6)))

DatiTrasportoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CausaleTrasporto'),
        String100LatinType,
        scope=DatiTrasportoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            472,
            6)))

DatiTrasportoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NumeroColli'),
        NumeroColliType,
        scope=DatiTrasportoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            473,
            6)))

DatiTrasportoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Descrizione'),
        String100LatinType,
        scope=DatiTrasportoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            474,
            6)))

DatiTrasportoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'UnitaMisuraPeso'),
        String10Type,
        scope=DatiTrasportoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            475,
            6)))

DatiTrasportoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'PesoLordo'),
        PesoType,
        scope=DatiTrasportoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            476,
            6)))

DatiTrasportoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'PesoNetto'),
        PesoType,
        scope=DatiTrasportoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            477,
            6)))

DatiTrasportoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DataOraRitiro'),
        pyxb.binding.datatypes.dateTime,
        scope=DatiTrasportoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            478,
            6)))

DatiTrasportoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DataInizioTrasporto'),
        pyxb.binding.datatypes.date,
        scope=DatiTrasportoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            479,
            6)))

DatiTrasportoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'TipoResa'),
        TipoResaType,
        scope=DatiTrasportoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            480,
            6)))

DatiTrasportoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IndirizzoResa'),
        IndirizzoType,
        scope=DatiTrasportoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            481,
            6)))

DatiTrasportoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DataOraConsegna'),
        pyxb.binding.datatypes.dateTime,
        scope=DatiTrasportoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            482,
            6)))


def _BuildAutomaton_14():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            470,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            471,
            6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            472,
            6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            473,
            6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            474,
            6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            475,
            6))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            476,
            6))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            477,
            6))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            478,
            6))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            479,
            6))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            480,
            6))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            481,
            6))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            482,
            6))
    counters.add(cc_12)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiTrasportoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiAnagraficiVettore')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 470, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiTrasportoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'MezzoTrasporto')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 471, 6))
    st_1 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiTrasportoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CausaleTrasporto')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 472, 6))
    st_2 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiTrasportoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NumeroColli')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 473, 6))
    st_3 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiTrasportoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Descrizione')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 474, 6))
    st_4 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiTrasportoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'UnitaMisuraPeso')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 475, 6))
    st_5 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiTrasportoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'PesoLordo')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 476, 6))
    st_6 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiTrasportoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'PesoNetto')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 477, 6))
    st_7 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiTrasportoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DataOraRitiro')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 478, 6))
    st_8 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiTrasportoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DataInizioTrasporto')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 479, 6))
    st_9 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiTrasportoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'TipoResa')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 480, 6))
    st_10 = fac.State(symbol, is_initial=True,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiTrasportoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IndirizzoResa')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 481, 6))
    st_11 = fac.State(symbol, is_initial=True,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiTrasportoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DataOraConsegna')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 482, 6))
    st_12 = fac.State(symbol, is_initial=True,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, False)]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_1, False)]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True)]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False)]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_3, False)]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False)]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False)]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False)]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False)]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False)]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False)]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False)]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False)]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_9, True)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_9, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, False)]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, False)]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_10, True)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_10, False)]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_10, False)]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_11, True)]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_11, False)]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True)]))
    st_12._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
DatiTrasportoType._Automaton = _BuildAutomaton_14()


IndirizzoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Indirizzo'),
        String60LatinType,
        scope=IndirizzoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            487,
            6)))

IndirizzoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NumeroCivico'),
        NumeroCivicoType,
        scope=IndirizzoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            488,
            6)))

IndirizzoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CAP'),
        CAPType,
        scope=IndirizzoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            489,
            6)))

IndirizzoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Comune'),
        String60LatinType,
        scope=IndirizzoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            490,
            6)))

IndirizzoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Provincia'),
        ProvinciaType,
        scope=IndirizzoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            491,
            6)))

IndirizzoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Nazione'),
        NazioneType,
        scope=IndirizzoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            492,
            6),
        unicode_default='IT'))


def _BuildAutomaton_15():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            488,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            491,
            6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        IndirizzoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Indirizzo')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 487, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        IndirizzoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NumeroCivico')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 488, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        IndirizzoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CAP')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 489, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        IndirizzoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Comune')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 490, 6))
    st_3 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        IndirizzoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Provincia')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 491, 6))
    st_4 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        IndirizzoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Nazione')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 492, 6))
    st_5 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
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
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
    ]))
    transitions.append(fac.Transition(st_5, [
    ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False)]))
    st_4._set_transitionSet(transitions)
    transitions = []
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
IndirizzoType._Automaton = _BuildAutomaton_15()


FatturaPrincipaleType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NumeroFatturaPrincipale'),
        String20Type,
        scope=FatturaPrincipaleType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            497,
            6)))

FatturaPrincipaleType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DataFatturaPrincipale'),
        pyxb.binding.datatypes.date,
        scope=FatturaPrincipaleType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            498,
            6)))


def _BuildAutomaton_16():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        FatturaPrincipaleType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NumeroFatturaPrincipale')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 497, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        FatturaPrincipaleType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DataFatturaPrincipale')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 498, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
FatturaPrincipaleType._Automaton = _BuildAutomaton_16()


CedentePrestatoreType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiAnagrafici'),
        DatiAnagraficiCedenteType,
        scope=CedentePrestatoreType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            523,
            6)))

CedentePrestatoreType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Sede'),
        IndirizzoType,
        scope=CedentePrestatoreType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            524,
            6)))

CedentePrestatoreType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'StabileOrganizzazione'),
        IndirizzoType,
        scope=CedentePrestatoreType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            525,
            6)))

CedentePrestatoreType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IscrizioneREA'),
        IscrizioneREAType,
        scope=CedentePrestatoreType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            526,
            6)))

CedentePrestatoreType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Contatti'),
        ContattiType,
        scope=CedentePrestatoreType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            527,
            6)))

CedentePrestatoreType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoAmministrazione'),
        String20Type,
        scope=CedentePrestatoreType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            528,
            6)))


def _BuildAutomaton_17():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            525,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            526,
            6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            527,
            6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            528,
            6))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        CedentePrestatoreType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiAnagrafici')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 523, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        CedentePrestatoreType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Sede')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 524, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(
        CedentePrestatoreType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'StabileOrganizzazione')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 525, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(
        CedentePrestatoreType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IscrizioneREA')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 526, 6))
    st_3 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(
        CedentePrestatoreType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Contatti')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 527, 6))
    st_4 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(
        CedentePrestatoreType._UseForTag(
            pyxb.namespace.ExpandedName(
                None,
                'RiferimentoAmministrazione')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 528, 6))
    st_5 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
    ]))
    transitions.append(fac.Transition(st_3, [
    ]))
    transitions.append(fac.Transition(st_4, [
    ]))
    transitions.append(fac.Transition(st_5, [
    ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False)]))
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
CedentePrestatoreType._Automaton = _BuildAutomaton_17()


DatiAnagraficiCedenteType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IdFiscaleIVA'),
        IdFiscaleType,
        scope=DatiAnagraficiCedenteType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            533,
            6)))

DatiAnagraficiCedenteType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceFiscale'),
        CodiceFiscaleType,
        scope=DatiAnagraficiCedenteType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            534,
            6)))

DatiAnagraficiCedenteType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Anagrafica'),
        AnagraficaType,
        scope=DatiAnagraficiCedenteType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            535,
            6)))

DatiAnagraficiCedenteType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'AlboProfessionale'),
        String60LatinType,
        scope=DatiAnagraficiCedenteType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            536,
            6)))

DatiAnagraficiCedenteType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'ProvinciaAlbo'),
        ProvinciaType,
        scope=DatiAnagraficiCedenteType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            537,
            6)))

DatiAnagraficiCedenteType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NumeroIscrizioneAlbo'),
        String60Type,
        scope=DatiAnagraficiCedenteType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            538,
            6)))

DatiAnagraficiCedenteType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DataIscrizioneAlbo'),
        pyxb.binding.datatypes.date,
        scope=DatiAnagraficiCedenteType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            539,
            6)))

DatiAnagraficiCedenteType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'RegimeFiscale'),
        RegimeFiscaleType,
        scope=DatiAnagraficiCedenteType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            540,
            6)))


def _BuildAutomaton_18():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            534,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            536,
            6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            537,
            6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            538,
            6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            539,
            6))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiCedenteType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IdFiscaleIVA')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 533, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiCedenteType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CodiceFiscale')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 534, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiCedenteType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Anagrafica')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 535, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiCedenteType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'AlboProfessionale')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 536, 6))
    st_3 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiCedenteType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'ProvinciaAlbo')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 537, 6))
    st_4 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiCedenteType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NumeroIscrizioneAlbo')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 538, 6))
    st_5 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiCedenteType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DataIscrizioneAlbo')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 539, 6))
    st_6 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiCedenteType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'RegimeFiscale')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 540, 6))
    st_7 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
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
    transitions.append(fac.Transition(st_5, [
    ]))
    transitions.append(fac.Transition(st_6, [
    ]))
    transitions.append(fac.Transition(st_7, [
    ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False)]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False)]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False)]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False)]))
    st_6._set_transitionSet(transitions)
    transitions = []
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiAnagraficiCedenteType._Automaton = _BuildAutomaton_18()


AnagraficaType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Denominazione'),
        String80LatinType,
        scope=AnagraficaType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            653,
            10)))

AnagraficaType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Nome'),
        String60LatinType,
        scope=AnagraficaType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            656,
            10)))

AnagraficaType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Cognome'),
        String60LatinType,
        scope=AnagraficaType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            657,
            10)))

AnagraficaType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Titolo'),
        TitoloType,
        scope=AnagraficaType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            660,
            6)))

AnagraficaType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CodEORI'),
        CodEORIType,
        scope=AnagraficaType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            661,
            6)))


def _BuildAutomaton_19():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            660,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            661,
            6))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        AnagraficaType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Denominazione')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 653, 10))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        AnagraficaType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Nome')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 656, 10))
    st_1 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        AnagraficaType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Cognome')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 657, 10))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(
        AnagraficaType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Titolo')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 660, 6))
    st_3 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(
        AnagraficaType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CodEORI')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 661, 6))
    st_4 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_3, [
    ]))
    transitions.append(fac.Transition(st_4, [
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
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True)]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AnagraficaType._Automaton = _BuildAutomaton_19()


DatiAnagraficiVettoreType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IdFiscaleIVA'),
        IdFiscaleType,
        scope=DatiAnagraficiVettoreType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            666,
            6)))

DatiAnagraficiVettoreType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceFiscale'),
        CodiceFiscaleType,
        scope=DatiAnagraficiVettoreType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            667,
            6)))

DatiAnagraficiVettoreType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Anagrafica'),
        AnagraficaType,
        scope=DatiAnagraficiVettoreType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            668,
            6)))

DatiAnagraficiVettoreType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NumeroLicenzaGuida'),
        String20Type,
        scope=DatiAnagraficiVettoreType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            669,
            6)))


def _BuildAutomaton_20():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            667,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            669,
            6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiVettoreType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IdFiscaleIVA')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 666, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiVettoreType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CodiceFiscale')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 667, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiVettoreType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Anagrafica')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 668, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiVettoreType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NumeroLicenzaGuida')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 669, 6))
    st_3 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
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
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True)]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiAnagraficiVettoreType._Automaton = _BuildAutomaton_20()


IscrizioneREAType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Ufficio'),
        ProvinciaType,
        scope=IscrizioneREAType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            674,
            6)))

IscrizioneREAType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NumeroREA'),
        String20Type,
        scope=IscrizioneREAType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            675,
            6)))

IscrizioneREAType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CapitaleSociale'),
        Amount2DecimalType,
        scope=IscrizioneREAType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            676,
            6)))

IscrizioneREAType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'SocioUnico'),
        SocioUnicoType,
        scope=IscrizioneREAType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            677,
            6)))

IscrizioneREAType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'StatoLiquidazione'),
        StatoLiquidazioneType,
        scope=IscrizioneREAType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            678,
            6)))


def _BuildAutomaton_21():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            676,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            677,
            6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        IscrizioneREAType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Ufficio')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 674, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        IscrizioneREAType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NumeroREA')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 675, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        IscrizioneREAType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CapitaleSociale')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 676, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        IscrizioneREAType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'SocioUnico')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 677, 6))
    st_3 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        IscrizioneREAType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'StatoLiquidazione')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 678, 6))
    st_4 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
    ]))
    transitions.append(fac.Transition(st_3, [
    ]))
    transitions.append(fac.Transition(st_4, [
    ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False)]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False)]))
    st_3._set_transitionSet(transitions)
    transitions = []
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
IscrizioneREAType._Automaton = _BuildAutomaton_21()


ContattiType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Telefono'),
        TelFaxType,
        scope=ContattiType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            683,
            6)))

ContattiType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Fax'),
        TelFaxType,
        scope=ContattiType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            684,
            6)))

ContattiType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Email'),
        EmailType,
        scope=ContattiType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            685,
            6)))


def _BuildAutomaton_22():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            683,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            684,
            6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            685,
            6))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(
        ContattiType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Telefono')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 683, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(
        ContattiType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Fax')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 684, 6))
    st_1 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(
        ContattiType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Email')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 685, 6))
    st_2 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False)]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False)]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True)]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ContattiType._Automaton = _BuildAutomaton_22()


RappresentanteFiscaleType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiAnagrafici'),
        DatiAnagraficiRappresentanteType,
        scope=RappresentanteFiscaleType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            695,
            6)))


def _BuildAutomaton_23():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_23
    del _BuildAutomaton_23
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        RappresentanteFiscaleType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiAnagrafici')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 695, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
RappresentanteFiscaleType._Automaton = _BuildAutomaton_23()


DatiAnagraficiRappresentanteType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IdFiscaleIVA'),
        IdFiscaleType,
        scope=DatiAnagraficiRappresentanteType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            700,
            6)))

DatiAnagraficiRappresentanteType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceFiscale'),
        CodiceFiscaleType,
        scope=DatiAnagraficiRappresentanteType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            701,
            6)))

DatiAnagraficiRappresentanteType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Anagrafica'),
        AnagraficaType,
        scope=DatiAnagraficiRappresentanteType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            702,
            6)))


def _BuildAutomaton_24():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_24
    del _BuildAutomaton_24
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            701,
            6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiRappresentanteType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IdFiscaleIVA')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 700, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiRappresentanteType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CodiceFiscale')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 701, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiRappresentanteType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Anagrafica')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 702, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
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
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiAnagraficiRappresentanteType._Automaton = _BuildAutomaton_24()


CessionarioCommittenteType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiAnagrafici'),
        DatiAnagraficiCessionarioType,
        scope=CessionarioCommittenteType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            712,
            6)))

CessionarioCommittenteType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Sede'),
        IndirizzoType,
        scope=CessionarioCommittenteType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            713,
            6)))


def _BuildAutomaton_25():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_25
    del _BuildAutomaton_25
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        CessionarioCommittenteType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiAnagrafici')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 712, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        CessionarioCommittenteType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Sede')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 713, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CessionarioCommittenteType._Automaton = _BuildAutomaton_25()


DatiAnagraficiCessionarioType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IdFiscaleIVA'),
        IdFiscaleType,
        scope=DatiAnagraficiCessionarioType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            718,
            6)))

DatiAnagraficiCessionarioType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceFiscale'),
        CodiceFiscaleType,
        scope=DatiAnagraficiCessionarioType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            719,
            6)))

DatiAnagraficiCessionarioType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Anagrafica'),
        AnagraficaType,
        scope=DatiAnagraficiCessionarioType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            720,
            6)))


def _BuildAutomaton_26():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_26
    del _BuildAutomaton_26
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            718,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            719,
            6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiCessionarioType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IdFiscaleIVA')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 718, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiCessionarioType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CodiceFiscale')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 719, 6))
    st_1 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiCessionarioType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Anagrafica')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 720, 6))
    st_2 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False)]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False)]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiAnagraficiCessionarioType._Automaton = _BuildAutomaton_26()


DatiBeniServiziType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DettaglioLinee'),
        DettaglioLineeType,
        scope=DatiBeniServiziType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            730,
            6)))

DatiBeniServiziType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DatiRiepilogo'),
        DatiRiepilogoType,
        scope=DatiBeniServiziType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            731,
            6)))


def _BuildAutomaton_27():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_27
    del _BuildAutomaton_27
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiBeniServiziType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DettaglioLinee')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 730, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DatiBeniServiziType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiRiepilogo')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 731, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
    ]))
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiBeniServiziType._Automaton = _BuildAutomaton_27()


DatiVeicoliType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Data'),
        pyxb.binding.datatypes.date,
        scope=DatiVeicoliType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            744,
            6)))

DatiVeicoliType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'TotalePercorso'),
        String15Type,
        scope=DatiVeicoliType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            745,
            6)))


def _BuildAutomaton_28():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_28
    del _BuildAutomaton_28
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiVeicoliType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Data')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 744, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DatiVeicoliType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'TotalePercorso')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 745, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiVeicoliType._Automaton = _BuildAutomaton_28()


DatiPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CondizioniPagamento'),
        CondizioniPagamentoType,
        scope=DatiPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            755,
            6)))

DatiPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DettaglioPagamento'),
        DettaglioPagamentoType,
        scope=DatiPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            756,
            6)))


def _BuildAutomaton_29():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_29
    del _BuildAutomaton_29
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CondizioniPagamento')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 755, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DatiPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DettaglioPagamento')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 756, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiPagamentoType._Automaton = _BuildAutomaton_29()


DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Beneficiario'),
        String200LatinType,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            782,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'ModalitaPagamento'),
        ModalitaPagamentoType,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            783,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DataRiferimentoTerminiPagamento'),
        pyxb.binding.datatypes.date,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            784,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'GiorniTerminiPagamento'),
        GiorniTerminePagamentoType,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            785,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DataScadenzaPagamento'),
        pyxb.binding.datatypes.date,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            786,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'ImportoPagamento'),
        Amount2DecimalType,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            787,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CodUfficioPostale'),
        String20Type,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            788,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CognomeQuietanzante'),
        String60LatinType,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            789,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NomeQuietanzante'),
        String60LatinType,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            790,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CFQuietanzante'),
        CodiceFiscalePFType,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            791,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'TitoloQuietanzante'),
        TitoloType,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            792,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IstitutoFinanziario'),
        String80LatinType,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            793,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IBAN'),
        IBANType,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            794,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'ABI'),
        ABIType,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            795,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CAB'),
        CABType,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            796,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'BIC'),
        BICType,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            797,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'ScontoPagamentoAnticipato'),
        Amount2DecimalType,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            798,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DataLimitePagamentoAnticipato'),
        pyxb.binding.datatypes.date,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            799,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'PenalitaPagamentiRitardati'),
        Amount2DecimalType,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            800,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DataDecorrenzaPenale'),
        pyxb.binding.datatypes.date,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            801,
            6)))

DettaglioPagamentoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CodicePagamento'),
        String60Type,
        scope=DettaglioPagamentoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            802,
            6)))


def _BuildAutomaton_30():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_30
    del _BuildAutomaton_30
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            782,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            784,
            6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            785,
            6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            786,
            6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            788,
            6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            789,
            6))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            790,
            6))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            791,
            6))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            792,
            6))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            793,
            6))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            794,
            6))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            795,
            6))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            796,
            6))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            797,
            6))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            798,
            6))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            799,
            6))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            800,
            6))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            801,
            6))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            802,
            6))
    counters.add(cc_18)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Beneficiario')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 782, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'ModalitaPagamento')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 783, 6))
    st_1 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None,
                'DataRiferimentoTerminiPagamento')
        ), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 784, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'GiorniTerminiPagamento')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 785, 6))
    st_3 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DataScadenzaPagamento')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 786, 6))
    st_4 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'ImportoPagamento')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 787, 6))
    st_5 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CodUfficioPostale')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 788, 6))
    st_6 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CognomeQuietanzante')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 789, 6))
    st_7 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NomeQuietanzante')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 790, 6))
    st_8 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CFQuietanzante')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 791, 6))
    st_9 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'TitoloQuietanzante')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 792, 6))
    st_10 = fac.State(symbol, is_initial=False,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IstitutoFinanziario')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 793, 6))
    st_11 = fac.State(symbol, is_initial=False,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IBAN')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 794, 6))
    st_12 = fac.State(symbol, is_initial=False,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'ABI')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 795, 6))
    st_13 = fac.State(symbol, is_initial=False,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CAB')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 796, 6))
    st_14 = fac.State(symbol, is_initial=False,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'BIC')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 797, 6))
    st_15 = fac.State(symbol, is_initial=False,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None,
                'ScontoPagamentoAnticipato')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 798, 6))
    st_16 = fac.State(symbol, is_initial=False,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None,
                'DataLimitePagamentoAnticipato')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 799, 6))
    st_17 = fac.State(symbol, is_initial=False,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None,
                'PenalitaPagamentiRitardati')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 800, 6))
    st_18 = fac.State(symbol, is_initial=False,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DataDecorrenzaPenale')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 801, 6))
    st_19 = fac.State(symbol, is_initial=False,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_18, False))
    symbol = pyxb.binding.content.ElementUse(
        DettaglioPagamentoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CodicePagamento')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 802, 6))
    st_20 = fac.State(symbol, is_initial=False,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_20)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False)]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
    ]))
    transitions.append(fac.Transition(st_3, [
    ]))
    transitions.append(fac.Transition(st_4, [
    ]))
    transitions.append(fac.Transition(st_5, [
    ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False)]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False)]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False)]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
    ]))
    transitions.append(fac.Transition(st_7, [
    ]))
    transitions.append(fac.Transition(st_8, [
    ]))
    transitions.append(fac.Transition(st_9, [
    ]))
    transitions.append(fac.Transition(st_10, [
    ]))
    transitions.append(fac.Transition(st_11, [
    ]))
    transitions.append(fac.Transition(st_12, [
    ]))
    transitions.append(fac.Transition(st_13, [
    ]))
    transitions.append(fac.Transition(st_14, [
    ]))
    transitions.append(fac.Transition(st_15, [
    ]))
    transitions.append(fac.Transition(st_16, [
    ]))
    transitions.append(fac.Transition(st_17, [
    ]))
    transitions.append(fac.Transition(st_18, [
    ]))
    transitions.append(fac.Transition(st_19, [
    ]))
    transitions.append(fac.Transition(st_20, [
    ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_4, False)]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, True)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_5, False)]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_5, False)]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, True)]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False)]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False)]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False)]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_6, False)]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_6, False)]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_6, False)]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_6, False)]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_6, False)]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_6, False)]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_6, False)]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False)]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False)]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False)]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False)]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, False)]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_7, False)]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_7, False)]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_7, False)]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_7, False)]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_7, False)]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, True)]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False)]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False)]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False)]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False)]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False)]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_8, False)]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_8, False)]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_8, False)]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_8, False)]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_8, False)]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, True)]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, False)]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, False)]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, False)]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False)]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, False)]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_9, False)]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_9, False)]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_9, False)]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_9, False)]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_10, True)]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_10, False)]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_10, False)]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, False)]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_10, False)]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_10, False)]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_10, False)]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_10, False)]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_10, False)]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_11, True)]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_11, False)]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_11, False)]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_11, False)]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_11, False)]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_11, False)]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_11, False)]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_11, False)]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_12, True)]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_12, False)]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_12, False)]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_12, False)]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_12, False)]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_12, False)]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_12, False)]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_13, True)]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_13, False)]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_13, False)]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_13, False)]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_13, False)]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_13, False)]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_14, True)]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_14, False)]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_14, False)]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_14, False)]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_14, False)]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_15, True)]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_15, False)]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_15, False)]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_15, False)]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_16, True)]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_16, False)]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_16, False)]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_17, True)]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_17, False)]))
    st_19._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_18, True)]))
    st_20._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DettaglioPagamentoType._Automaton = _BuildAutomaton_30()


TerzoIntermediarioSoggettoEmittenteType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(None, 'DatiAnagrafici'),
        DatiAnagraficiTerzoIntermediarioType,
        scope=TerzoIntermediarioSoggettoEmittenteType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 934, 6)))


def _BuildAutomaton_31():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_31
    del _BuildAutomaton_31
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        TerzoIntermediarioSoggettoEmittenteType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DatiAnagrafici')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 934, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
TerzoIntermediarioSoggettoEmittenteType._Automaton = _BuildAutomaton_31()


DatiAnagraficiTerzoIntermediarioType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'IdFiscaleIVA'),
        IdFiscaleType,
        scope=DatiAnagraficiTerzoIntermediarioType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            939,
            6)))

DatiAnagraficiTerzoIntermediarioType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceFiscale'),
        CodiceFiscaleType,
        scope=DatiAnagraficiTerzoIntermediarioType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            940,
            6)))

DatiAnagraficiTerzoIntermediarioType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Anagrafica'),
        AnagraficaType,
        scope=DatiAnagraficiTerzoIntermediarioType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            941,
            6)))


def _BuildAutomaton_32():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_32
    del _BuildAutomaton_32
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            939,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            940,
            6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiTerzoIntermediarioType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'IdFiscaleIVA')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 939, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiTerzoIntermediarioType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CodiceFiscale')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 940, 6))
    st_1 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DatiAnagraficiTerzoIntermediarioType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Anagrafica')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 941, 6))
    st_2 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False)]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False)]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiAnagraficiTerzoIntermediarioType._Automaton = _BuildAutomaton_32()


AllegatiType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NomeAttachment'),
        String60LatinType,
        scope=AllegatiType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            951,
            6)))

AllegatiType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'AlgoritmoCompressione'),
        String10Type,
        scope=AllegatiType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            952,
            6)))

AllegatiType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'FormatoAttachment'),
        String10Type,
        scope=AllegatiType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            953,
            6)))

AllegatiType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DescrizioneAttachment'),
        String100LatinType,
        scope=AllegatiType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            954,
            6)))

AllegatiType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Attachment'),
        pyxb.binding.datatypes.base64Binary,
        scope=AllegatiType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            955,
            6)))


def _BuildAutomaton_33():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_33
    del _BuildAutomaton_33
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            952,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            953,
            6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            954,
            6))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        AllegatiType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NomeAttachment')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 951, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        AllegatiType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'AlgoritmoCompressione')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 952, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        AllegatiType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'FormatoAttachment')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 953, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        AllegatiType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DescrizioneAttachment')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 954, 6))
    st_3 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        AllegatiType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Attachment')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 955, 6))
    st_4 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    transitions.append(fac.Transition(st_2, [
    ]))
    transitions.append(fac.Transition(st_3, [
    ]))
    transitions.append(fac.Transition(st_4, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False)]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False)]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False)]))
    st_3._set_transitionSet(transitions)
    transitions = []
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AllegatiType._Automaton = _BuildAutomaton_33()


DettaglioLineeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'NumeroLinea'),
        NumeroLineaType,
        scope=DettaglioLineeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            960,
            6)))

DettaglioLineeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'TipoCessionePrestazione'),
        TipoCessionePrestazioneType,
        scope=DettaglioLineeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            961,
            6)))

DettaglioLineeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceArticolo'),
        CodiceArticoloType,
        scope=DettaglioLineeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            962,
            6)))

DettaglioLineeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Descrizione'),
        String1000LatinType,
        scope=DettaglioLineeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            963,
            6)))

DettaglioLineeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Quantita'),
        QuantitaType,
        scope=DettaglioLineeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            964,
            6)))

DettaglioLineeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'UnitaMisura'),
        String10Type,
        scope=DettaglioLineeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            965,
            6)))

DettaglioLineeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DataInizioPeriodo'),
        pyxb.binding.datatypes.date,
        scope=DettaglioLineeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            966,
            6)))

DettaglioLineeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'DataFinePeriodo'),
        pyxb.binding.datatypes.date,
        scope=DettaglioLineeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            967,
            6)))

DettaglioLineeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'PrezzoUnitario'),
        Amount8DecimalType,
        scope=DettaglioLineeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            968,
            6)))

DettaglioLineeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'ScontoMaggiorazione'),
        ScontoMaggiorazioneType,
        scope=DettaglioLineeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            969,
            6)))

DettaglioLineeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'PrezzoTotale'),
        Amount8DecimalType,
        scope=DettaglioLineeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            970,
            6)))

DettaglioLineeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'AliquotaIVA'),
        RateType,
        scope=DettaglioLineeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            971,
            6)))

DettaglioLineeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Ritenuta'),
        RitenutaType,
        scope=DettaglioLineeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            972,
            6)))

DettaglioLineeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Natura'),
        NaturaType,
        scope=DettaglioLineeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            973,
            6)))

DettaglioLineeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoAmministrazione'),
        String20Type,
        scope=DettaglioLineeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            974,
            6)))

DettaglioLineeType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'AltriDatiGestionali'),
        AltriDatiGestionaliType,
        scope=DettaglioLineeType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            975,
            6)))


def _BuildAutomaton_34():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_34
    del _BuildAutomaton_34
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            961,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=None,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            962,
            6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            964,
            6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            965,
            6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            966,
            6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            967,
            6))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(
        min=0,
        max=None,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            969,
            6))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            972,
            6))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            973,
            6))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            974,
            6))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(
        min=0,
        max=None,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            975,
            6))
    counters.add(cc_10)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DettaglioLineeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'NumeroLinea')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 960, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DettaglioLineeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'TipoCessionePrestazione')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 961, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DettaglioLineeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CodiceArticolo')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 962, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DettaglioLineeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Descrizione')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 963, 6))
    st_3 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DettaglioLineeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Quantita')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 964, 6))
    st_4 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DettaglioLineeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'UnitaMisura')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 965, 6))
    st_5 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DettaglioLineeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DataInizioPeriodo')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 966, 6))
    st_6 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DettaglioLineeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'DataFinePeriodo')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 967, 6))
    st_7 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DettaglioLineeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'PrezzoUnitario')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 968, 6))
    st_8 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DettaglioLineeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'ScontoMaggiorazione')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 969, 6))
    st_9 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DettaglioLineeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'PrezzoTotale')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 970, 6))
    st_10 = fac.State(symbol, is_initial=False,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DettaglioLineeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'AliquotaIVA')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 971, 6))
    st_11 = fac.State(symbol, is_initial=False,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(
        DettaglioLineeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Ritenuta')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 972, 6))
    st_12 = fac.State(symbol, is_initial=False,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(
        DettaglioLineeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Natura')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 973, 6))
    st_13 = fac.State(symbol, is_initial=False,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(
        DettaglioLineeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None,
                'RiferimentoAmministrazione')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 974, 6))
    st_14 = fac.State(symbol, is_initial=False,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(
        DettaglioLineeType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'AltriDatiGestionali')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 975, 6))
    st_15 = fac.State(symbol, is_initial=False,
                      final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    transitions.append(fac.Transition(st_2, [
    ]))
    transitions.append(fac.Transition(st_3, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False)]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False)]))
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
    transitions.append(fac.Transition(st_8, [
    ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True)]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False)]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True)]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False)]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False)]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, True)]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False)]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
    ]))
    transitions.append(fac.Transition(st_10, [
    ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, True)]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False)]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
    ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
    ]))
    transitions.append(fac.Transition(st_13, [
    ]))
    transitions.append(fac.Transition(st_14, [
    ]))
    transitions.append(fac.Transition(st_15, [
    ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, True)]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False)]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False)]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, False)]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, True)]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False)]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False)]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, True)]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False)]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, True)]))
    st_15._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DettaglioLineeType._Automaton = _BuildAutomaton_34()


CodiceArticoloType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceTipo'),
        String35Type,
        scope=CodiceArticoloType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            980,
            6)))

CodiceArticoloType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'CodiceValore'),
        String35Type,
        scope=CodiceArticoloType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            981,
            6)))


def _BuildAutomaton_35():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_35
    del _BuildAutomaton_35
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        CodiceArticoloType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CodiceTipo')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 980, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        CodiceArticoloType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'CodiceValore')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 981, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CodiceArticoloType._Automaton = _BuildAutomaton_35()


AltriDatiGestionaliType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'TipoDato'),
        String10Type,
        scope=AltriDatiGestionaliType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            986,
            6)))

AltriDatiGestionaliType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoTesto'),
        String60LatinType,
        scope=AltriDatiGestionaliType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            987,
            6)))

AltriDatiGestionaliType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoNumero'),
        Amount8DecimalType,
        scope=AltriDatiGestionaliType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            988,
            6)))

AltriDatiGestionaliType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoData'),
        pyxb.binding.datatypes.date,
        scope=AltriDatiGestionaliType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            989,
            6)))


def _BuildAutomaton_36():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_36
    del _BuildAutomaton_36
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            987,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            988,
            6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            989,
            6))
    counters.add(cc_2)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        AltriDatiGestionaliType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'TipoDato')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 986, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(
        AltriDatiGestionaliType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'RiferimentoTesto')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 987, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(
        AltriDatiGestionaliType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'RiferimentoNumero')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 988, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(
        AltriDatiGestionaliType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'RiferimentoData')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 989, 6))
    st_3 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    transitions.append(fac.Transition(st_2, [
    ]))
    transitions.append(fac.Transition(st_3, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False)]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False)]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True)]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AltriDatiGestionaliType._Automaton = _BuildAutomaton_36()


DatiRiepilogoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'AliquotaIVA'),
        RateType,
        scope=DatiRiepilogoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1006,
            6)))

DatiRiepilogoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Natura'),
        NaturaType,
        scope=DatiRiepilogoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1007,
            6)))

DatiRiepilogoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'SpeseAccessorie'),
        Amount2DecimalType,
        scope=DatiRiepilogoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1008,
            6)))

DatiRiepilogoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Arrotondamento'),
        Amount8DecimalType,
        scope=DatiRiepilogoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1009,
            6)))

DatiRiepilogoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'ImponibileImporto'),
        Amount2DecimalType,
        scope=DatiRiepilogoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1010,
            6)))

DatiRiepilogoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'Imposta'),
        Amount2DecimalType,
        scope=DatiRiepilogoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1011,
            6)))

DatiRiepilogoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'EsigibilitaIVA'),
        EsigibilitaIVAType,
        scope=DatiRiepilogoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1012,
            6)))

DatiRiepilogoType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'RiferimentoNormativo'),
        String100LatinType,
        scope=DatiRiepilogoType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1013,
            6)))


def _BuildAutomaton_37():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_37
    del _BuildAutomaton_37
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1007,
            6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1008,
            6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1009,
            6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1012,
            6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            1013,
            6))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiRiepilogoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'AliquotaIVA')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 1006, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiRiepilogoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Natura')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 1007, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiRiepilogoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'SpeseAccessorie')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 1008, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiRiepilogoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Arrotondamento')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 1009, 6))
    st_3 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        DatiRiepilogoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'ImponibileImporto')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 1010, 6))
    st_4 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        DatiRiepilogoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'Imposta')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 1011, 6))
    st_5 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiRiepilogoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'EsigibilitaIVA')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 1012, 6))
    st_6 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(
        DatiRiepilogoType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'RiferimentoNormativo')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 1013, 6))
    st_7 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    transitions.append(fac.Transition(st_2, [
    ]))
    transitions.append(fac.Transition(st_3, [
    ]))
    transitions.append(fac.Transition(st_4, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True)]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False)]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True)]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False)]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True)]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False)]))
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
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True)]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False)]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True)]))
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiRiepilogoType._Automaton = _BuildAutomaton_37()


FatturaElettronicaType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'FatturaElettronicaHeader'),
        FatturaElettronicaHeaderType,
        scope=FatturaElettronicaType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            13,
            6)))

FatturaElettronicaType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            None,
            'FatturaElettronicaBody'),
        FatturaElettronicaBodyType,
        scope=FatturaElettronicaType,
        location=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            14,
            6)))

FatturaElettronicaType._AddElement(
    pyxb.binding.basis.element(
        pyxb.namespace.ExpandedName(
            _Namespace_ds,
            'Signature'),
        _ImportedBinding__ds.SignatureType,
        scope=FatturaElettronicaType,
        location=pyxb.utils.utility.Location(
            (
                'http://www.w3.org/TR/2002/REC-xmldsig-core-'
                '20020212/xmldsig-core-schema.xsd'
            ),
            43,
            0)))


def _BuildAutomaton_38():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_38
    del _BuildAutomaton_38
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(
        min=0,
        max=1,
        metadata=pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd',
            15,
            6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(
        FatturaElettronicaType._UseForTag(
            pyxb.namespace.ExpandedName(
                None,
                'FatturaElettronicaHeader')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 13, 6))
    st_0 = fac.State(symbol, is_initial=True,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(
        FatturaElettronicaType._UseForTag(
            pyxb.namespace.ExpandedName(
                None, 'FatturaElettronicaBody')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 14, 6))
    st_1 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(
        FatturaElettronicaType._UseForTag(
            pyxb.namespace.ExpandedName(
                _Namespace_ds, 'Signature')), pyxb.utils.utility.Location(
            '/tmp/fatturapa_v1.1.xsd', 15, 6))
    st_2 = fac.State(symbol, is_initial=False,
                     final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
    ]))
    transitions.append(fac.Transition(st_2, [
    ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True)]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
FatturaElettronicaType._Automaton = _BuildAutomaton_38()
