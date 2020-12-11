# -*- coding: utf-8 -*-
# flake8: noqa`
# PyXB bindings for NM:32e521a6da5b62d07147ea75b23acb0fb9726893
# Generated 2020-06-11 15:53:54.097929 by PyXB version 1.2.6 using Python 3.6.9.final.0
# Namespace http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2

from __future__ import unicode_literals
import io

import logging

_logger = logging.getLogger(__name__)
try:
    import pyxb
    import pyxb.binding
    import pyxb.binding.datatypes
    import pyxb.binding.saxer
    import pyxb.utils.utility
    import pyxb.utils.domutils
    import pyxb.utils.six as _six
    # Import bindings for namespaces imported into schema
    import pyxb.binding.datatypes
except (ImportError) as err:
    _logger.debug(err)

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:f33a6cc4-abea-11ea-89e6-e09467884037')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
from . import _ds as _ImportedBinding__ds

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])
_Namespace_ds = _ImportedBinding__ds.Namespace
_Namespace_ds.configureCategories(['typeBinding', 'elementBinding'])

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


# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}CodiceDestinatarioType
class CodiceDestinatarioType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CodiceDestinatarioType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 57, 2)
    _Documentation = None
CodiceDestinatarioType._CF_pattern = pyxb.binding.facets.CF_pattern()
CodiceDestinatarioType._CF_pattern.addPattern(pattern='[A-Z0-9]{6,7}')
CodiceDestinatarioType._InitializeFacetMap(CodiceDestinatarioType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'CodiceDestinatarioType', CodiceDestinatarioType)
_module_typeBindings.CodiceDestinatarioType = CodiceDestinatarioType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}CodiceType
class CodiceType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CodiceType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 68, 2)
    _Documentation = None
CodiceType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(28))
CodiceType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
CodiceType._InitializeFacetMap(CodiceType._CF_maxLength,
   CodiceType._CF_minLength)
Namespace.addCategoryObject('typeBinding', 'CodiceType', CodiceType)
_module_typeBindings.CodiceType = CodiceType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}FormatoTrasmissioneType
class FormatoTrasmissioneType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FormatoTrasmissioneType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 74, 2)
    _Documentation = None
FormatoTrasmissioneType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=FormatoTrasmissioneType)
FormatoTrasmissioneType.FPA12 = FormatoTrasmissioneType._CF_enumeration.addEnumeration(unicode_value='FPA12', tag='FPA12')
FormatoTrasmissioneType.FPR12 = FormatoTrasmissioneType._CF_enumeration.addEnumeration(unicode_value='FPR12', tag='FPR12')
FormatoTrasmissioneType._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(5))
FormatoTrasmissioneType._InitializeFacetMap(FormatoTrasmissioneType._CF_enumeration,
   FormatoTrasmissioneType._CF_length)
Namespace.addCategoryObject('typeBinding', 'FormatoTrasmissioneType', FormatoTrasmissioneType)
_module_typeBindings.FormatoTrasmissioneType = FormatoTrasmissioneType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}CausalePagamentoType
class CausalePagamentoType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CausalePagamentoType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 163, 2)
    _Documentation = None
CausalePagamentoType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=CausalePagamentoType)
CausalePagamentoType.A = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='A', tag='A')
CausalePagamentoType.B = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='B', tag='B')
CausalePagamentoType.C = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='C', tag='C')
CausalePagamentoType.D = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='D', tag='D')
CausalePagamentoType.E = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='E', tag='E')
CausalePagamentoType.G = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='G', tag='G')
CausalePagamentoType.H = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='H', tag='H')
CausalePagamentoType.I = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='I', tag='I')
CausalePagamentoType.L = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='L', tag='L')
CausalePagamentoType.M = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='M', tag='M')
CausalePagamentoType.N = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='N', tag='N')
CausalePagamentoType.O = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='O', tag='O')
CausalePagamentoType.P = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='P', tag='P')
CausalePagamentoType.Q = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='Q', tag='Q')
CausalePagamentoType.R = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='R', tag='R')
CausalePagamentoType.S = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='S', tag='S')
CausalePagamentoType.T = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='T', tag='T')
CausalePagamentoType.U = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='U', tag='U')
CausalePagamentoType.V = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='V', tag='V')
CausalePagamentoType.W = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='W', tag='W')
CausalePagamentoType.X = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='X', tag='X')
CausalePagamentoType.Y = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='Y', tag='Y')
CausalePagamentoType.L1 = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='L1', tag='L1')
CausalePagamentoType.M1 = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='M1', tag='M1')
CausalePagamentoType.M2 = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='M2', tag='M2')
CausalePagamentoType.O1 = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='O1', tag='O1')
CausalePagamentoType.V1 = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='V1', tag='V1')
CausalePagamentoType.ZO = CausalePagamentoType._CF_enumeration.addEnumeration(unicode_value='ZO', tag='ZO')
CausalePagamentoType._InitializeFacetMap(CausalePagamentoType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'CausalePagamentoType', CausalePagamentoType)
_module_typeBindings.CausalePagamentoType = CausalePagamentoType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}TipoScontoMaggiorazioneType
class TipoScontoMaggiorazioneType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TipoScontoMaggiorazioneType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 196, 2)
    _Documentation = None
TipoScontoMaggiorazioneType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=TipoScontoMaggiorazioneType)
TipoScontoMaggiorazioneType.SC = TipoScontoMaggiorazioneType._CF_enumeration.addEnumeration(unicode_value='SC', tag='SC')
TipoScontoMaggiorazioneType.MG = TipoScontoMaggiorazioneType._CF_enumeration.addEnumeration(unicode_value='MG', tag='MG')
TipoScontoMaggiorazioneType._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(2))
TipoScontoMaggiorazioneType._InitializeFacetMap(TipoScontoMaggiorazioneType._CF_enumeration,
   TipoScontoMaggiorazioneType._CF_length)
Namespace.addCategoryObject('typeBinding', 'TipoScontoMaggiorazioneType', TipoScontoMaggiorazioneType)
_module_typeBindings.TipoScontoMaggiorazioneType = TipoScontoMaggiorazioneType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}Art73Type
class Art73Type (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Art73Type')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 211, 2)
    _Documentation = None
Art73Type._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=Art73Type)
Art73Type.SI = Art73Type._CF_enumeration.addEnumeration(unicode_value='SI', tag='SI')
Art73Type._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(2))
Art73Type._InitializeFacetMap(Art73Type._CF_enumeration,
   Art73Type._CF_length)
Namespace.addCategoryObject('typeBinding', 'Art73Type', Art73Type)
_module_typeBindings.Art73Type = Art73Type

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}TipoCassaType
class TipoCassaType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TipoCassaType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 221, 2)
    _Documentation = None
TipoCassaType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=TipoCassaType)
TipoCassaType.TC01 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC01', tag='TC01')
TipoCassaType.TC02 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC02', tag='TC02')
TipoCassaType.TC03 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC03', tag='TC03')
TipoCassaType.TC04 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC04', tag='TC04')
TipoCassaType.TC05 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC05', tag='TC05')
TipoCassaType.TC06 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC06', tag='TC06')
TipoCassaType.TC07 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC07', tag='TC07')
TipoCassaType.TC08 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC08', tag='TC08')
TipoCassaType.TC09 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC09', tag='TC09')
TipoCassaType.TC10 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC10', tag='TC10')
TipoCassaType.TC11 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC11', tag='TC11')
TipoCassaType.TC12 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC12', tag='TC12')
TipoCassaType.TC13 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC13', tag='TC13')
TipoCassaType.TC14 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC14', tag='TC14')
TipoCassaType.TC15 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC15', tag='TC15')
TipoCassaType.TC16 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC16', tag='TC16')
TipoCassaType.TC17 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC17', tag='TC17')
TipoCassaType.TC18 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC18', tag='TC18')
TipoCassaType.TC19 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC19', tag='TC19')
TipoCassaType.TC20 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC20', tag='TC20')
TipoCassaType.TC21 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC21', tag='TC21')
TipoCassaType.TC22 = TipoCassaType._CF_enumeration.addEnumeration(unicode_value='TC22', tag='TC22')
TipoCassaType._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(4))
TipoCassaType._InitializeFacetMap(TipoCassaType._CF_enumeration,
   TipoCassaType._CF_length)
Namespace.addCategoryObject('typeBinding', 'TipoCassaType', TipoCassaType)
_module_typeBindings.TipoCassaType = TipoCassaType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}TipoDocumentoType
class TipoDocumentoType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TipoDocumentoType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 336, 2)
    _Documentation = None
TipoDocumentoType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=TipoDocumentoType)
TipoDocumentoType.TD01 = TipoDocumentoType._CF_enumeration.addEnumeration(unicode_value='TD01', tag='TD01')
TipoDocumentoType.TD02 = TipoDocumentoType._CF_enumeration.addEnumeration(unicode_value='TD02', tag='TD02')
TipoDocumentoType.TD03 = TipoDocumentoType._CF_enumeration.addEnumeration(unicode_value='TD03', tag='TD03')
TipoDocumentoType.TD04 = TipoDocumentoType._CF_enumeration.addEnumeration(unicode_value='TD04', tag='TD04')
TipoDocumentoType.TD05 = TipoDocumentoType._CF_enumeration.addEnumeration(unicode_value='TD05', tag='TD05')
TipoDocumentoType.TD06 = TipoDocumentoType._CF_enumeration.addEnumeration(unicode_value='TD06', tag='TD06')
TipoDocumentoType.TD16 = TipoDocumentoType._CF_enumeration.addEnumeration(unicode_value='TD16', tag='TD16')
TipoDocumentoType.TD17 = TipoDocumentoType._CF_enumeration.addEnumeration(unicode_value='TD17', tag='TD17')
TipoDocumentoType.TD18 = TipoDocumentoType._CF_enumeration.addEnumeration(unicode_value='TD18', tag='TD18')
TipoDocumentoType.TD19 = TipoDocumentoType._CF_enumeration.addEnumeration(unicode_value='TD19', tag='TD19')
TipoDocumentoType.TD20 = TipoDocumentoType._CF_enumeration.addEnumeration(unicode_value='TD20', tag='TD20')
TipoDocumentoType.TD21 = TipoDocumentoType._CF_enumeration.addEnumeration(unicode_value='TD21', tag='TD21')
TipoDocumentoType.TD22 = TipoDocumentoType._CF_enumeration.addEnumeration(unicode_value='TD22', tag='TD22')
TipoDocumentoType.TD23 = TipoDocumentoType._CF_enumeration.addEnumeration(unicode_value='TD23', tag='TD23')
TipoDocumentoType.TD24 = TipoDocumentoType._CF_enumeration.addEnumeration(unicode_value='TD24', tag='TD24')
TipoDocumentoType.TD25 = TipoDocumentoType._CF_enumeration.addEnumeration(unicode_value='TD25', tag='TD25')
TipoDocumentoType.TD26 = TipoDocumentoType._CF_enumeration.addEnumeration(unicode_value='TD26', tag='TD26')
TipoDocumentoType.TD27 = TipoDocumentoType._CF_enumeration.addEnumeration(unicode_value='TD27', tag='TD27')
TipoDocumentoType._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(4))
TipoDocumentoType._InitializeFacetMap(TipoDocumentoType._CF_enumeration,
   TipoDocumentoType._CF_length)
Namespace.addCategoryObject('typeBinding', 'TipoDocumentoType', TipoDocumentoType)
_module_typeBindings.TipoDocumentoType = TipoDocumentoType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}TipoRitenutaType
class TipoRitenutaType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TipoRitenutaType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 431, 2)
    _Documentation = None
TipoRitenutaType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=TipoRitenutaType)
TipoRitenutaType.RT01 = TipoRitenutaType._CF_enumeration.addEnumeration(unicode_value='RT01', tag='RT01')
TipoRitenutaType.RT02 = TipoRitenutaType._CF_enumeration.addEnumeration(unicode_value='RT02', tag='RT02')
TipoRitenutaType.RT03 = TipoRitenutaType._CF_enumeration.addEnumeration(unicode_value='RT03', tag='RT03')
TipoRitenutaType.RT04 = TipoRitenutaType._CF_enumeration.addEnumeration(unicode_value='RT04', tag='RT04')
TipoRitenutaType.RT05 = TipoRitenutaType._CF_enumeration.addEnumeration(unicode_value='RT05', tag='RT05')
TipoRitenutaType.RT06 = TipoRitenutaType._CF_enumeration.addEnumeration(unicode_value='RT06', tag='RT06')
TipoRitenutaType._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(4))
TipoRitenutaType._InitializeFacetMap(TipoRitenutaType._CF_enumeration,
   TipoRitenutaType._CF_length)
Namespace.addCategoryObject('typeBinding', 'TipoRitenutaType', TipoRitenutaType)
_module_typeBindings.TipoRitenutaType = TipoRitenutaType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}RiferimentoNumeroLineaType
class RiferimentoNumeroLineaType (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'RiferimentoNumeroLineaType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 482, 2)
    _Documentation = None
RiferimentoNumeroLineaType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.integer(9999), value_datatype=RiferimentoNumeroLineaType)
RiferimentoNumeroLineaType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.integer(1), value_datatype=RiferimentoNumeroLineaType)
RiferimentoNumeroLineaType._InitializeFacetMap(RiferimentoNumeroLineaType._CF_maxInclusive,
   RiferimentoNumeroLineaType._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'RiferimentoNumeroLineaType', RiferimentoNumeroLineaType)
_module_typeBindings.RiferimentoNumeroLineaType = RiferimentoNumeroLineaType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}SoggettoEmittenteType
class SoggettoEmittenteType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SoggettoEmittenteType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 528, 2)
    _Documentation = None
SoggettoEmittenteType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=SoggettoEmittenteType)
SoggettoEmittenteType.CC = SoggettoEmittenteType._CF_enumeration.addEnumeration(unicode_value='CC', tag='CC')
SoggettoEmittenteType.TZ = SoggettoEmittenteType._CF_enumeration.addEnumeration(unicode_value='TZ', tag='TZ')
SoggettoEmittenteType._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(2))
SoggettoEmittenteType._InitializeFacetMap(SoggettoEmittenteType._CF_enumeration,
   SoggettoEmittenteType._CF_length)
Namespace.addCategoryObject('typeBinding', 'SoggettoEmittenteType', SoggettoEmittenteType)
_module_typeBindings.SoggettoEmittenteType = SoggettoEmittenteType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}RegimeFiscaleType
class RegimeFiscaleType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'RegimeFiscaleType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 568, 2)
    _Documentation = None
RegimeFiscaleType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=RegimeFiscaleType)
RegimeFiscaleType.RF01 = RegimeFiscaleType._CF_enumeration.addEnumeration(unicode_value='RF01', tag='RF01')
RegimeFiscaleType.RF02 = RegimeFiscaleType._CF_enumeration.addEnumeration(unicode_value='RF02', tag='RF02')
RegimeFiscaleType.RF04 = RegimeFiscaleType._CF_enumeration.addEnumeration(unicode_value='RF04', tag='RF04')
RegimeFiscaleType.RF05 = RegimeFiscaleType._CF_enumeration.addEnumeration(unicode_value='RF05', tag='RF05')
RegimeFiscaleType.RF06 = RegimeFiscaleType._CF_enumeration.addEnumeration(unicode_value='RF06', tag='RF06')
RegimeFiscaleType.RF07 = RegimeFiscaleType._CF_enumeration.addEnumeration(unicode_value='RF07', tag='RF07')
RegimeFiscaleType.RF08 = RegimeFiscaleType._CF_enumeration.addEnumeration(unicode_value='RF08', tag='RF08')
RegimeFiscaleType.RF09 = RegimeFiscaleType._CF_enumeration.addEnumeration(unicode_value='RF09', tag='RF09')
RegimeFiscaleType.RF10 = RegimeFiscaleType._CF_enumeration.addEnumeration(unicode_value='RF10', tag='RF10')
RegimeFiscaleType.RF11 = RegimeFiscaleType._CF_enumeration.addEnumeration(unicode_value='RF11', tag='RF11')
RegimeFiscaleType.RF12 = RegimeFiscaleType._CF_enumeration.addEnumeration(unicode_value='RF12', tag='RF12')
RegimeFiscaleType.RF13 = RegimeFiscaleType._CF_enumeration.addEnumeration(unicode_value='RF13', tag='RF13')
RegimeFiscaleType.RF14 = RegimeFiscaleType._CF_enumeration.addEnumeration(unicode_value='RF14', tag='RF14')
RegimeFiscaleType.RF15 = RegimeFiscaleType._CF_enumeration.addEnumeration(unicode_value='RF15', tag='RF15')
RegimeFiscaleType.RF16 = RegimeFiscaleType._CF_enumeration.addEnumeration(unicode_value='RF16', tag='RF16')
RegimeFiscaleType.RF17 = RegimeFiscaleType._CF_enumeration.addEnumeration(unicode_value='RF17', tag='RF17')
RegimeFiscaleType.RF19 = RegimeFiscaleType._CF_enumeration.addEnumeration(unicode_value='RF19', tag='RF19')
RegimeFiscaleType.RF18 = RegimeFiscaleType._CF_enumeration.addEnumeration(unicode_value='RF18', tag='RF18')
RegimeFiscaleType._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(4))
RegimeFiscaleType._InitializeFacetMap(RegimeFiscaleType._CF_enumeration,
   RegimeFiscaleType._CF_length)
Namespace.addCategoryObject('typeBinding', 'RegimeFiscaleType', RegimeFiscaleType)
_module_typeBindings.RegimeFiscaleType = RegimeFiscaleType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}CondizioniPagamentoType
class CondizioniPagamentoType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CondizioniPagamentoType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 780, 2)
    _Documentation = None
CondizioniPagamentoType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=CondizioniPagamentoType)
CondizioniPagamentoType.TP01 = CondizioniPagamentoType._CF_enumeration.addEnumeration(unicode_value='TP01', tag='TP01')
CondizioniPagamentoType.TP02 = CondizioniPagamentoType._CF_enumeration.addEnumeration(unicode_value='TP02', tag='TP02')
CondizioniPagamentoType.TP03 = CondizioniPagamentoType._CF_enumeration.addEnumeration(unicode_value='TP03', tag='TP03')
CondizioniPagamentoType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(4))
CondizioniPagamentoType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(4))
CondizioniPagamentoType._InitializeFacetMap(CondizioniPagamentoType._CF_enumeration,
   CondizioniPagamentoType._CF_maxLength,
   CondizioniPagamentoType._CF_minLength)
Namespace.addCategoryObject('typeBinding', 'CondizioniPagamentoType', CondizioniPagamentoType)
_module_typeBindings.CondizioniPagamentoType = CondizioniPagamentoType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}ModalitaPagamentoType
class ModalitaPagamentoType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ModalitaPagamentoType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 826, 2)
    _Documentation = None
ModalitaPagamentoType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=ModalitaPagamentoType)
ModalitaPagamentoType.MP01 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP01', tag='MP01')
ModalitaPagamentoType.MP02 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP02', tag='MP02')
ModalitaPagamentoType.MP03 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP03', tag='MP03')
ModalitaPagamentoType.MP04 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP04', tag='MP04')
ModalitaPagamentoType.MP05 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP05', tag='MP05')
ModalitaPagamentoType.MP06 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP06', tag='MP06')
ModalitaPagamentoType.MP07 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP07', tag='MP07')
ModalitaPagamentoType.MP08 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP08', tag='MP08')
ModalitaPagamentoType.MP09 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP09', tag='MP09')
ModalitaPagamentoType.MP10 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP10', tag='MP10')
ModalitaPagamentoType.MP11 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP11', tag='MP11')
ModalitaPagamentoType.MP12 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP12', tag='MP12')
ModalitaPagamentoType.MP13 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP13', tag='MP13')
ModalitaPagamentoType.MP14 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP14', tag='MP14')
ModalitaPagamentoType.MP15 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP15', tag='MP15')
ModalitaPagamentoType.MP16 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP16', tag='MP16')
ModalitaPagamentoType.MP17 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP17', tag='MP17')
ModalitaPagamentoType.MP18 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP18', tag='MP18')
ModalitaPagamentoType.MP19 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP19', tag='MP19')
ModalitaPagamentoType.MP20 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP20', tag='MP20')
ModalitaPagamentoType.MP21 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP21', tag='MP21')
ModalitaPagamentoType.MP22 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP22', tag='MP22')
ModalitaPagamentoType.MP23 = ModalitaPagamentoType._CF_enumeration.addEnumeration(unicode_value='MP23', tag='MP23')
ModalitaPagamentoType._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(4))
ModalitaPagamentoType._InitializeFacetMap(ModalitaPagamentoType._CF_enumeration,
   ModalitaPagamentoType._CF_length)
Namespace.addCategoryObject('typeBinding', 'ModalitaPagamentoType', ModalitaPagamentoType)
_module_typeBindings.ModalitaPagamentoType = ModalitaPagamentoType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}IBANType
class IBANType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IBANType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 946, 2)
    _Documentation = None
IBANType._CF_pattern = pyxb.binding.facets.CF_pattern()
IBANType._CF_pattern.addPattern(pattern='[a-zA-Z]{2}[0-9]{2}[a-zA-Z0-9]{11,30}')
IBANType._InitializeFacetMap(IBANType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'IBANType', IBANType)
_module_typeBindings.IBANType = IBANType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}BICType
class BICType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'BICType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 951, 2)
    _Documentation = None
BICType._CF_pattern = pyxb.binding.facets.CF_pattern()
BICType._CF_pattern.addPattern(pattern='[A-Z]{6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3}){0,1}')
BICType._InitializeFacetMap(BICType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'BICType', BICType)
_module_typeBindings.BICType = BICType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}RitenutaType
class RitenutaType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'RitenutaType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1017, 2)
    _Documentation = None
RitenutaType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=RitenutaType)
RitenutaType.SI = RitenutaType._CF_enumeration.addEnumeration(unicode_value='SI', tag='SI')
RitenutaType._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(2))
RitenutaType._InitializeFacetMap(RitenutaType._CF_enumeration,
   RitenutaType._CF_length)
Namespace.addCategoryObject('typeBinding', 'RitenutaType', RitenutaType)
_module_typeBindings.RitenutaType = RitenutaType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}EsigibilitaIVAType
class EsigibilitaIVAType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'EsigibilitaIVAType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1039, 2)
    _Documentation = None
EsigibilitaIVAType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=EsigibilitaIVAType)
EsigibilitaIVAType.D = EsigibilitaIVAType._CF_enumeration.addEnumeration(unicode_value='D', tag='D')
EsigibilitaIVAType.I = EsigibilitaIVAType._CF_enumeration.addEnumeration(unicode_value='I', tag='I')
EsigibilitaIVAType.S = EsigibilitaIVAType._CF_enumeration.addEnumeration(unicode_value='S', tag='S')
EsigibilitaIVAType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
EsigibilitaIVAType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
EsigibilitaIVAType._InitializeFacetMap(EsigibilitaIVAType._CF_enumeration,
   EsigibilitaIVAType._CF_maxLength,
   EsigibilitaIVAType._CF_minLength)
Namespace.addCategoryObject('typeBinding', 'EsigibilitaIVAType', EsigibilitaIVAType)
_module_typeBindings.EsigibilitaIVAType = EsigibilitaIVAType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}NaturaType
class NaturaType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NaturaType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1060, 2)
    _Documentation = None
NaturaType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=NaturaType)
NaturaType.N1 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N1', tag='N1')
NaturaType.N2 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N2', tag='N2')
NaturaType.N2_1 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N2.1', tag='N2_1')
NaturaType.N2_2 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N2.2', tag='N2_2')
NaturaType.N3 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N3', tag='N3')
NaturaType.N3_1 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N3.1', tag='N3_1')
NaturaType.N3_2 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N3.2', tag='N3_2')
NaturaType.N3_3 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N3.3', tag='N3_3')
NaturaType.N3_4 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N3.4', tag='N3_4')
NaturaType.N3_5 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N3.5', tag='N3_5')
NaturaType.N3_6 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N3.6', tag='N3_6')
NaturaType.N4 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N4', tag='N4')
NaturaType.N5 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N5', tag='N5')
NaturaType.N6 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N6', tag='N6')
NaturaType.N6_1 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N6.1', tag='N6_1')
NaturaType.N6_2 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N6.2', tag='N6_2')
NaturaType.N6_3 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N6.3', tag='N6_3')
NaturaType.N6_4 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N6.4', tag='N6_4')
NaturaType.N6_5 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N6.5', tag='N6_5')
NaturaType.N6_6 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N6.6', tag='N6_6')
NaturaType.N6_7 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N6.7', tag='N6_7')
NaturaType.N6_8 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N6.8', tag='N6_8')
NaturaType.N6_9 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N6.9', tag='N6_9')
NaturaType.N7 = NaturaType._CF_enumeration.addEnumeration(unicode_value='N7', tag='N7')
NaturaType._InitializeFacetMap(NaturaType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'NaturaType', NaturaType)
_module_typeBindings.NaturaType = NaturaType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}CodiceFiscaleType
class CodiceFiscaleType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CodiceFiscaleType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1187, 2)
    _Documentation = None
CodiceFiscaleType._CF_pattern = pyxb.binding.facets.CF_pattern()
CodiceFiscaleType._CF_pattern.addPattern(pattern='[A-Z0-9]{11,16}')
CodiceFiscaleType._InitializeFacetMap(CodiceFiscaleType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'CodiceFiscaleType', CodiceFiscaleType)
_module_typeBindings.CodiceFiscaleType = CodiceFiscaleType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}CodiceFiscalePFType
class CodiceFiscalePFType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CodiceFiscalePFType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1192, 2)
    _Documentation = None
CodiceFiscalePFType._CF_pattern = pyxb.binding.facets.CF_pattern()
CodiceFiscalePFType._CF_pattern.addPattern(pattern='[A-Z0-9]{16}')
CodiceFiscalePFType._InitializeFacetMap(CodiceFiscalePFType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'CodiceFiscalePFType', CodiceFiscalePFType)
_module_typeBindings.CodiceFiscalePFType = CodiceFiscalePFType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}CodEORIType
class CodEORIType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CodEORIType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1197, 2)
    _Documentation = None
CodEORIType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(17))
CodEORIType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(13))
CodEORIType._InitializeFacetMap(CodEORIType._CF_maxLength,
   CodEORIType._CF_minLength)
Namespace.addCategoryObject('typeBinding', 'CodEORIType', CodEORIType)
_module_typeBindings.CodEORIType = CodEORIType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}SocioUnicoType
class SocioUnicoType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SocioUnicoType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1203, 2)
    _Documentation = None
SocioUnicoType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=SocioUnicoType)
SocioUnicoType.SU = SocioUnicoType._CF_enumeration.addEnumeration(unicode_value='SU', tag='SU')
SocioUnicoType.SM = SocioUnicoType._CF_enumeration.addEnumeration(unicode_value='SM', tag='SM')
SocioUnicoType._InitializeFacetMap(SocioUnicoType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'SocioUnicoType', SocioUnicoType)
_module_typeBindings.SocioUnicoType = SocioUnicoType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}StatoLiquidazioneType
class StatoLiquidazioneType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'StatoLiquidazioneType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1217, 2)
    _Documentation = None
StatoLiquidazioneType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=StatoLiquidazioneType)
StatoLiquidazioneType.LS = StatoLiquidazioneType._CF_enumeration.addEnumeration(unicode_value='LS', tag='LS')
StatoLiquidazioneType.LN = StatoLiquidazioneType._CF_enumeration.addEnumeration(unicode_value='LN', tag='LN')
StatoLiquidazioneType._InitializeFacetMap(StatoLiquidazioneType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'StatoLiquidazioneType', StatoLiquidazioneType)
_module_typeBindings.StatoLiquidazioneType = StatoLiquidazioneType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}TipoCessionePrestazioneType
class TipoCessionePrestazioneType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TipoCessionePrestazioneType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1231, 2)
    _Documentation = None
TipoCessionePrestazioneType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=TipoCessionePrestazioneType)
TipoCessionePrestazioneType.SC = TipoCessionePrestazioneType._CF_enumeration.addEnumeration(unicode_value='SC', tag='SC')
TipoCessionePrestazioneType.PR = TipoCessionePrestazioneType._CF_enumeration.addEnumeration(unicode_value='PR', tag='PR')
TipoCessionePrestazioneType.AB = TipoCessionePrestazioneType._CF_enumeration.addEnumeration(unicode_value='AB', tag='AB')
TipoCessionePrestazioneType.AC = TipoCessionePrestazioneType._CF_enumeration.addEnumeration(unicode_value='AC', tag='AC')
TipoCessionePrestazioneType._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(2))
TipoCessionePrestazioneType._InitializeFacetMap(TipoCessionePrestazioneType._CF_enumeration,
   TipoCessionePrestazioneType._CF_length)
Namespace.addCategoryObject('typeBinding', 'TipoCessionePrestazioneType', TipoCessionePrestazioneType)
_module_typeBindings.TipoCessionePrestazioneType = TipoCessionePrestazioneType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}TitoloType
class TitoloType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TitoloType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1256, 2)
    _Documentation = None
TitoloType._CF_whiteSpace = pyxb.binding.facets.CF_whiteSpace(value=pyxb.binding.facets._WhiteSpace_enum.collapse)
TitoloType._CF_pattern = pyxb.binding.facets.CF_pattern()
TitoloType._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{2,10})')
TitoloType._InitializeFacetMap(TitoloType._CF_whiteSpace,
   TitoloType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'TitoloType', TitoloType)
_module_typeBindings.TitoloType = TitoloType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}String10Type
class String10Type (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String10Type')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1262, 2)
    _Documentation = None
String10Type._CF_pattern = pyxb.binding.facets.CF_pattern()
String10Type._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{1,10})')
String10Type._InitializeFacetMap(String10Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'String10Type', String10Type)
_module_typeBindings.String10Type = String10Type

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}String15Type
class String15Type (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String15Type')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1267, 2)
    _Documentation = None
String15Type._CF_pattern = pyxb.binding.facets.CF_pattern()
String15Type._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{1,15})')
String15Type._InitializeFacetMap(String15Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'String15Type', String15Type)
_module_typeBindings.String15Type = String15Type

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}String20Type
class String20Type (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String20Type')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1272, 2)
    _Documentation = None
String20Type._CF_pattern = pyxb.binding.facets.CF_pattern()
String20Type._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{1,20})')
String20Type._InitializeFacetMap(String20Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'String20Type', String20Type)
_module_typeBindings.String20Type = String20Type

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}String35Type
class String35Type (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String35Type')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1277, 2)
    _Documentation = None
String35Type._CF_pattern = pyxb.binding.facets.CF_pattern()
String35Type._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{1,35})')
String35Type._InitializeFacetMap(String35Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'String35Type', String35Type)
_module_typeBindings.String35Type = String35Type

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}String35LatinExtType
class String35LatinExtType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String35LatinExtType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1282, 2)
    _Documentation = None
String35LatinExtType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(35))
String35LatinExtType._CF_minLength = pyxb.binding.facets.CF_minLength(value=pyxb.binding.datatypes.nonNegativeInteger(1))
String35LatinExtType._InitializeFacetMap(String35LatinExtType._CF_maxLength,
   String35LatinExtType._CF_minLength)
Namespace.addCategoryObject('typeBinding', 'String35LatinExtType', String35LatinExtType)
_module_typeBindings.String35LatinExtType = String35LatinExtType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}String60Type
class String60Type (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String60Type')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1288, 2)
    _Documentation = None
String60Type._CF_pattern = pyxb.binding.facets.CF_pattern()
String60Type._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{1,60})')
String60Type._InitializeFacetMap(String60Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'String60Type', String60Type)
_module_typeBindings.String60Type = String60Type

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}String80Type
class String80Type (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String80Type')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1293, 2)
    _Documentation = None
String80Type._CF_pattern = pyxb.binding.facets.CF_pattern()
String80Type._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{1,80})')
String80Type._InitializeFacetMap(String80Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'String80Type', String80Type)
_module_typeBindings.String80Type = String80Type

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}String100Type
class String100Type (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String100Type')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1298, 2)
    _Documentation = None
String100Type._CF_pattern = pyxb.binding.facets.CF_pattern()
String100Type._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{1,100})')
String100Type._InitializeFacetMap(String100Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'String100Type', String100Type)
_module_typeBindings.String100Type = String100Type

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}String60LatinType
class String60LatinType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String60LatinType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1303, 2)
    _Documentation = None
String60LatinType._CF_pattern = pyxb.binding.facets.CF_pattern()
String60LatinType._CF_pattern.addPattern(pattern='[\\p{IsBasicLatin}\\p{IsLatin-1Supplement}]{1,60}')
String60LatinType._InitializeFacetMap(String60LatinType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'String60LatinType', String60LatinType)
_module_typeBindings.String60LatinType = String60LatinType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}String80LatinType
class String80LatinType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String80LatinType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1308, 2)
    _Documentation = None
String80LatinType._CF_pattern = pyxb.binding.facets.CF_pattern()
String80LatinType._CF_pattern.addPattern(pattern='[\\p{IsBasicLatin}\\p{IsLatin-1Supplement}]{1,80}')
String80LatinType._InitializeFacetMap(String80LatinType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'String80LatinType', String80LatinType)
_module_typeBindings.String80LatinType = String80LatinType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}String100LatinType
class String100LatinType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String100LatinType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1313, 2)
    _Documentation = None
String100LatinType._CF_pattern = pyxb.binding.facets.CF_pattern()
String100LatinType._CF_pattern.addPattern(pattern='[\\p{IsBasicLatin}\\p{IsLatin-1Supplement}]{1,100}')
String100LatinType._InitializeFacetMap(String100LatinType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'String100LatinType', String100LatinType)
_module_typeBindings.String100LatinType = String100LatinType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}String200LatinType
class String200LatinType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String200LatinType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1318, 2)
    _Documentation = None
String200LatinType._CF_pattern = pyxb.binding.facets.CF_pattern()
String200LatinType._CF_pattern.addPattern(pattern='[\\p{IsBasicLatin}\\p{IsLatin-1Supplement}]{1,200}')
String200LatinType._InitializeFacetMap(String200LatinType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'String200LatinType', String200LatinType)
_module_typeBindings.String200LatinType = String200LatinType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}String1000LatinType
class String1000LatinType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'String1000LatinType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1323, 2)
    _Documentation = None
String1000LatinType._CF_pattern = pyxb.binding.facets.CF_pattern()
String1000LatinType._CF_pattern.addPattern(pattern='[\\p{IsBasicLatin}\\p{IsLatin-1Supplement}]{1,1000}')
String1000LatinType._InitializeFacetMap(String1000LatinType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'String1000LatinType', String1000LatinType)
_module_typeBindings.String1000LatinType = String1000LatinType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}ProvinciaType
class ProvinciaType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ProvinciaType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1328, 2)
    _Documentation = None
ProvinciaType._CF_pattern = pyxb.binding.facets.CF_pattern()
ProvinciaType._CF_pattern.addPattern(pattern='[A-Z]{2}')
ProvinciaType._InitializeFacetMap(ProvinciaType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'ProvinciaType', ProvinciaType)
_module_typeBindings.ProvinciaType = ProvinciaType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}NazioneType
class NazioneType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NazioneType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1333, 2)
    _Documentation = None
NazioneType._CF_pattern = pyxb.binding.facets.CF_pattern()
NazioneType._CF_pattern.addPattern(pattern='[A-Z]{2}')
NazioneType._InitializeFacetMap(NazioneType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'NazioneType', NazioneType)
_module_typeBindings.NazioneType = NazioneType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DivisaType
class DivisaType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DivisaType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1338, 2)
    _Documentation = None
DivisaType._CF_pattern = pyxb.binding.facets.CF_pattern()
DivisaType._CF_pattern.addPattern(pattern='[A-Z]{3}')
DivisaType._InitializeFacetMap(DivisaType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DivisaType', DivisaType)
_module_typeBindings.DivisaType = DivisaType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}TipoResaType
class TipoResaType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TipoResaType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1343, 2)
    _Documentation = None
TipoResaType._CF_pattern = pyxb.binding.facets.CF_pattern()
TipoResaType._CF_pattern.addPattern(pattern='[A-Z]{3}')
TipoResaType._InitializeFacetMap(TipoResaType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'TipoResaType', TipoResaType)
_module_typeBindings.TipoResaType = TipoResaType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}NumeroCivicoType
class NumeroCivicoType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NumeroCivicoType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1348, 2)
    _Documentation = None
NumeroCivicoType._CF_pattern = pyxb.binding.facets.CF_pattern()
NumeroCivicoType._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{1,8})')
NumeroCivicoType._InitializeFacetMap(NumeroCivicoType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'NumeroCivicoType', NumeroCivicoType)
_module_typeBindings.NumeroCivicoType = NumeroCivicoType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}BolloVirtualeType
class BolloVirtualeType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'BolloVirtualeType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1353, 2)
    _Documentation = None
BolloVirtualeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(enum_prefix=None, value_datatype=BolloVirtualeType)
BolloVirtualeType.SI = BolloVirtualeType._CF_enumeration.addEnumeration(unicode_value='SI', tag='SI')
BolloVirtualeType._InitializeFacetMap(BolloVirtualeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'BolloVirtualeType', BolloVirtualeType)
_module_typeBindings.BolloVirtualeType = BolloVirtualeType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}TelFaxType
class TelFaxType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TelFaxType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1358, 2)
    _Documentation = None
TelFaxType._CF_pattern = pyxb.binding.facets.CF_pattern()
TelFaxType._CF_pattern.addPattern(pattern='(\\p{IsBasicLatin}{5,12})')
TelFaxType._InitializeFacetMap(TelFaxType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'TelFaxType', TelFaxType)
_module_typeBindings.TelFaxType = TelFaxType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}EmailType
class EmailType (pyxb.binding.datatypes.normalizedString):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'EmailType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1363, 2)
    _Documentation = None
EmailType._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(256))
EmailType._CF_pattern = pyxb.binding.facets.CF_pattern()
EmailType._CF_pattern.addPattern(pattern='([!#-\'*+/-9=?A-Z^-~-]+(\\.[!#-\'*+/-9=?A-Z^-~-]+)*|"(\\[\\]!#-[^-~ \\t]|(\\\\[\\t -~]))+")@([!#-\'*+/-9=?A-Z^-~-]+(\\.[!#-\'*+/-9=?A-Z^-~-]+)*|\\[[\\t -Z^-~]*\\])')
EmailType._InitializeFacetMap(EmailType._CF_maxLength,
   EmailType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'EmailType', EmailType)
_module_typeBindings.EmailType = EmailType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}PesoType
class PesoType (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PesoType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1370, 2)
    _Documentation = None
PesoType._CF_pattern = pyxb.binding.facets.CF_pattern()
PesoType._CF_pattern.addPattern(pattern='[0-9]{1,4}\\.[0-9]{1,2}')
PesoType._InitializeFacetMap(PesoType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'PesoType', PesoType)
_module_typeBindings.PesoType = PesoType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}Amount8DecimalType
class Amount8DecimalType (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Amount8DecimalType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1375, 2)
    _Documentation = None
Amount8DecimalType._CF_pattern = pyxb.binding.facets.CF_pattern()
Amount8DecimalType._CF_pattern.addPattern(pattern='[\\-]?[0-9]{1,11}\\.[0-9]{2,8}')
Amount8DecimalType._InitializeFacetMap(Amount8DecimalType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'Amount8DecimalType', Amount8DecimalType)
_module_typeBindings.Amount8DecimalType = Amount8DecimalType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}Amount2DecimalType
class Amount2DecimalType (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Amount2DecimalType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1380, 2)
    _Documentation = None
Amount2DecimalType._CF_pattern = pyxb.binding.facets.CF_pattern()
Amount2DecimalType._CF_pattern.addPattern(pattern='[\\-]?[0-9]{1,11}\\.[0-9]{2}')
Amount2DecimalType._InitializeFacetMap(Amount2DecimalType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'Amount2DecimalType', Amount2DecimalType)
_module_typeBindings.Amount2DecimalType = Amount2DecimalType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}RateType
class RateType (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'RateType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1385, 2)
    _Documentation = None
RateType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.decimal('100.0'), value_datatype=RateType)
RateType._CF_pattern = pyxb.binding.facets.CF_pattern()
RateType._CF_pattern.addPattern(pattern='[0-9]{1,3}\\.[0-9]{2}')
RateType._InitializeFacetMap(RateType._CF_maxInclusive,
   RateType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'RateType', RateType)
_module_typeBindings.RateType = RateType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}RiferimentoFaseType
class RiferimentoFaseType (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'RiferimentoFaseType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1391, 2)
    _Documentation = None
RiferimentoFaseType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.integer(999), value_datatype=RiferimentoFaseType)
RiferimentoFaseType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.integer(1), value_datatype=RiferimentoFaseType)
RiferimentoFaseType._InitializeFacetMap(RiferimentoFaseType._CF_maxInclusive,
   RiferimentoFaseType._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'RiferimentoFaseType', RiferimentoFaseType)
_module_typeBindings.RiferimentoFaseType = RiferimentoFaseType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}NumeroColliType
class NumeroColliType (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NumeroColliType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1397, 2)
    _Documentation = None
NumeroColliType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.integer(9999), value_datatype=NumeroColliType)
NumeroColliType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.integer(1), value_datatype=NumeroColliType)
NumeroColliType._InitializeFacetMap(NumeroColliType._CF_maxInclusive,
   NumeroColliType._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'NumeroColliType', NumeroColliType)
_module_typeBindings.NumeroColliType = NumeroColliType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}NumeroLineaType
class NumeroLineaType (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'NumeroLineaType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1403, 2)
    _Documentation = None
NumeroLineaType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.integer(9999), value_datatype=NumeroLineaType)
NumeroLineaType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.integer(1), value_datatype=NumeroLineaType)
NumeroLineaType._InitializeFacetMap(NumeroLineaType._CF_maxInclusive,
   NumeroLineaType._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'NumeroLineaType', NumeroLineaType)
_module_typeBindings.NumeroLineaType = NumeroLineaType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}CAPType
class CAPType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CAPType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1409, 2)
    _Documentation = None
CAPType._CF_pattern = pyxb.binding.facets.CF_pattern()
CAPType._CF_pattern.addPattern(pattern='[0-9][0-9][0-9][0-9][0-9]')
CAPType._InitializeFacetMap(CAPType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'CAPType', CAPType)
_module_typeBindings.CAPType = CAPType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}ABIType
class ABIType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ABIType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1414, 2)
    _Documentation = None
ABIType._CF_pattern = pyxb.binding.facets.CF_pattern()
ABIType._CF_pattern.addPattern(pattern='[0-9][0-9][0-9][0-9][0-9]')
ABIType._InitializeFacetMap(ABIType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'ABIType', ABIType)
_module_typeBindings.ABIType = ABIType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}CABType
class CABType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CABType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1419, 2)
    _Documentation = None
CABType._CF_pattern = pyxb.binding.facets.CF_pattern()
CABType._CF_pattern.addPattern(pattern='[0-9][0-9][0-9][0-9][0-9]')
CABType._InitializeFacetMap(CABType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'CABType', CABType)
_module_typeBindings.CABType = CABType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}GiorniTerminePagamentoType
class GiorniTerminePagamentoType (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'GiorniTerminePagamentoType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1424, 2)
    _Documentation = None
GiorniTerminePagamentoType._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value=pyxb.binding.datatypes.integer(999), value_datatype=GiorniTerminePagamentoType)
GiorniTerminePagamentoType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.integer(0), value_datatype=GiorniTerminePagamentoType)
GiorniTerminePagamentoType._InitializeFacetMap(GiorniTerminePagamentoType._CF_maxInclusive,
   GiorniTerminePagamentoType._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'GiorniTerminePagamentoType', GiorniTerminePagamentoType)
_module_typeBindings.GiorniTerminePagamentoType = GiorniTerminePagamentoType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}QuantitaType
class QuantitaType (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'QuantitaType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1430, 2)
    _Documentation = None
QuantitaType._CF_pattern = pyxb.binding.facets.CF_pattern()
QuantitaType._CF_pattern.addPattern(pattern='[0-9]{1,12}\\.[0-9]{2,8}')
QuantitaType._InitializeFacetMap(QuantitaType._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'QuantitaType', QuantitaType)
_module_typeBindings.QuantitaType = QuantitaType

# Atomic simple type: {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DataFatturaType
class DataFatturaType (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DataFatturaType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1435, 2)
    _Documentation = None
DataFatturaType._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value=pyxb.binding.datatypes.date('1970-01-01'), value_datatype=DataFatturaType)
DataFatturaType._InitializeFacetMap(DataFatturaType._CF_minInclusive)
Namespace.addCategoryObject('typeBinding', 'DataFatturaType', DataFatturaType)
_module_typeBindings.DataFatturaType = DataFatturaType

# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}FatturaElettronicaHeaderType with content type ELEMENT_ONLY
class FatturaElettronicaHeaderType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}FatturaElettronicaHeaderType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FatturaElettronicaHeaderType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 25, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element DatiTrasmissione uses Python identifier DatiTrasmissione
    __DatiTrasmissione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiTrasmissione'), 'DatiTrasmissione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_FatturaElettronicaHeaderType_DatiTrasmissione', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 27, 6), )


    DatiTrasmissione = property(__DatiTrasmissione.value, __DatiTrasmissione.set, None, None)


    # Element CedentePrestatore uses Python identifier CedentePrestatore
    __CedentePrestatore = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CedentePrestatore'), 'CedentePrestatore', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_FatturaElettronicaHeaderType_CedentePrestatore', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 28, 6), )


    CedentePrestatore = property(__CedentePrestatore.value, __CedentePrestatore.set, None, None)


    # Element RappresentanteFiscale uses Python identifier RappresentanteFiscale
    __RappresentanteFiscale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RappresentanteFiscale'), 'RappresentanteFiscale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_FatturaElettronicaHeaderType_RappresentanteFiscale', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 29, 6), )


    RappresentanteFiscale = property(__RappresentanteFiscale.value, __RappresentanteFiscale.set, None, None)


    # Element CessionarioCommittente uses Python identifier CessionarioCommittente
    __CessionarioCommittente = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CessionarioCommittente'), 'CessionarioCommittente', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_FatturaElettronicaHeaderType_CessionarioCommittente', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 30, 6), )


    CessionarioCommittente = property(__CessionarioCommittente.value, __CessionarioCommittente.set, None, None)


    # Element TerzoIntermediarioOSoggettoEmittente uses Python identifier TerzoIntermediarioOSoggettoEmittente
    __TerzoIntermediarioOSoggettoEmittente = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'TerzoIntermediarioOSoggettoEmittente'), 'TerzoIntermediarioOSoggettoEmittente', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_FatturaElettronicaHeaderType_TerzoIntermediarioOSoggettoEmittente', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 31, 6), )


    TerzoIntermediarioOSoggettoEmittente = property(__TerzoIntermediarioOSoggettoEmittente.value, __TerzoIntermediarioOSoggettoEmittente.set, None, None)


    # Element SoggettoEmittente uses Python identifier SoggettoEmittente
    __SoggettoEmittente = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SoggettoEmittente'), 'SoggettoEmittente', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_FatturaElettronicaHeaderType_SoggettoEmittente', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 32, 6), )


    SoggettoEmittente = property(__SoggettoEmittente.value, __SoggettoEmittente.set, None, None)

    _ElementMap.update({
        __DatiTrasmissione.name() : __DatiTrasmissione,
        __CedentePrestatore.name() : __CedentePrestatore,
        __RappresentanteFiscale.name() : __RappresentanteFiscale,
        __CessionarioCommittente.name() : __CessionarioCommittente,
        __TerzoIntermediarioOSoggettoEmittente.name() : __TerzoIntermediarioOSoggettoEmittente,
        __SoggettoEmittente.name() : __SoggettoEmittente
    })
    _AttributeMap.update({

    })
_module_typeBindings.FatturaElettronicaHeaderType = FatturaElettronicaHeaderType
Namespace.addCategoryObject('typeBinding', 'FatturaElettronicaHeaderType', FatturaElettronicaHeaderType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}FatturaElettronicaBodyType with content type ELEMENT_ONLY
class FatturaElettronicaBodyType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}FatturaElettronicaBodyType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FatturaElettronicaBodyType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 35, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element DatiGenerali uses Python identifier DatiGenerali
    __DatiGenerali = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiGenerali'), 'DatiGenerali', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_FatturaElettronicaBodyType_DatiGenerali', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 37, 6), )


    DatiGenerali = property(__DatiGenerali.value, __DatiGenerali.set, None, None)


    # Element DatiBeniServizi uses Python identifier DatiBeniServizi
    __DatiBeniServizi = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiBeniServizi'), 'DatiBeniServizi', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_FatturaElettronicaBodyType_DatiBeniServizi', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 38, 6), )


    DatiBeniServizi = property(__DatiBeniServizi.value, __DatiBeniServizi.set, None, None)


    # Element DatiVeicoli uses Python identifier DatiVeicoli
    __DatiVeicoli = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiVeicoli'), 'DatiVeicoli', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_FatturaElettronicaBodyType_DatiVeicoli', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 39, 6), )


    DatiVeicoli = property(__DatiVeicoli.value, __DatiVeicoli.set, None, None)


    # Element DatiPagamento uses Python identifier DatiPagamento
    __DatiPagamento = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiPagamento'), 'DatiPagamento', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_FatturaElettronicaBodyType_DatiPagamento', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 40, 6), )


    DatiPagamento = property(__DatiPagamento.value, __DatiPagamento.set, None, None)


    # Element Allegati uses Python identifier Allegati
    __Allegati = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Allegati'), 'Allegati', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_FatturaElettronicaBodyType_Allegati', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 41, 6), )


    Allegati = property(__Allegati.value, __Allegati.set, None, None)

    _ElementMap.update({
        __DatiGenerali.name() : __DatiGenerali,
        __DatiBeniServizi.name() : __DatiBeniServizi,
        __DatiVeicoli.name() : __DatiVeicoli,
        __DatiPagamento.name() : __DatiPagamento,
        __Allegati.name() : __Allegati
    })
    _AttributeMap.update({

    })
_module_typeBindings.FatturaElettronicaBodyType = FatturaElettronicaBodyType
Namespace.addCategoryObject('typeBinding', 'FatturaElettronicaBodyType', FatturaElettronicaBodyType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiTrasmissioneType with content type ELEMENT_ONLY
class DatiTrasmissioneType (pyxb.binding.basis.complexTypeDefinition):
    """Blocco relativo ai dati di trasmissione della Fattura Elettronica"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiTrasmissioneType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 44, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdTrasmittente uses Python identifier IdTrasmittente
    __IdTrasmittente = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IdTrasmittente'), 'IdTrasmittente', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiTrasmissioneType_IdTrasmittente', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 49, 6), )


    IdTrasmittente = property(__IdTrasmittente.value, __IdTrasmittente.set, None, None)


    # Element ProgressivoInvio uses Python identifier ProgressivoInvio
    __ProgressivoInvio = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ProgressivoInvio'), 'ProgressivoInvio', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiTrasmissioneType_ProgressivoInvio', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 50, 6), )


    ProgressivoInvio = property(__ProgressivoInvio.value, __ProgressivoInvio.set, None, None)


    # Element FormatoTrasmissione uses Python identifier FormatoTrasmissione
    __FormatoTrasmissione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'FormatoTrasmissione'), 'FormatoTrasmissione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiTrasmissioneType_FormatoTrasmissione', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 51, 6), )


    FormatoTrasmissione = property(__FormatoTrasmissione.value, __FormatoTrasmissione.set, None, None)


    # Element CodiceDestinatario uses Python identifier CodiceDestinatario
    __CodiceDestinatario = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CodiceDestinatario'), 'CodiceDestinatario', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiTrasmissioneType_CodiceDestinatario', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 52, 6), )


    CodiceDestinatario = property(__CodiceDestinatario.value, __CodiceDestinatario.set, None, None)


    # Element ContattiTrasmittente uses Python identifier ContattiTrasmittente
    __ContattiTrasmittente = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ContattiTrasmittente'), 'ContattiTrasmittente', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiTrasmissioneType_ContattiTrasmittente', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 53, 6), )


    ContattiTrasmittente = property(__ContattiTrasmittente.value, __ContattiTrasmittente.set, None, None)


    # Element PECDestinatario uses Python identifier PECDestinatario
    __PECDestinatario = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PECDestinatario'), 'PECDestinatario', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiTrasmissioneType_PECDestinatario', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 54, 6), )


    PECDestinatario = property(__PECDestinatario.value, __PECDestinatario.set, None, None)

    _ElementMap.update({
        __IdTrasmittente.name() : __IdTrasmittente,
        __ProgressivoInvio.name() : __ProgressivoInvio,
        __FormatoTrasmissione.name() : __FormatoTrasmissione,
        __CodiceDestinatario.name() : __CodiceDestinatario,
        __ContattiTrasmittente.name() : __ContattiTrasmittente,
        __PECDestinatario.name() : __PECDestinatario
    })
    _AttributeMap.update({

    })
_module_typeBindings.DatiTrasmissioneType = DatiTrasmissioneType
Namespace.addCategoryObject('typeBinding', 'DatiTrasmissioneType', DatiTrasmissioneType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}IdFiscaleType with content type ELEMENT_ONLY
class IdFiscaleType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}IdFiscaleType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IdFiscaleType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 62, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdPaese uses Python identifier IdPaese
    __IdPaese = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IdPaese'), 'IdPaese', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_IdFiscaleType_IdPaese', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 64, 6), )


    IdPaese = property(__IdPaese.value, __IdPaese.set, None, None)


    # Element IdCodice uses Python identifier IdCodice
    __IdCodice = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IdCodice'), 'IdCodice', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_IdFiscaleType_IdCodice', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 65, 6), )


    IdCodice = property(__IdCodice.value, __IdCodice.set, None, None)

    _ElementMap.update({
        __IdPaese.name() : __IdPaese,
        __IdCodice.name() : __IdCodice
    })
    _AttributeMap.update({

    })
_module_typeBindings.IdFiscaleType = IdFiscaleType
Namespace.addCategoryObject('typeBinding', 'IdFiscaleType', IdFiscaleType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}ContattiTrasmittenteType with content type ELEMENT_ONLY
class ContattiTrasmittenteType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}ContattiTrasmittenteType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ContattiTrasmittenteType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 89, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element Telefono uses Python identifier Telefono
    __Telefono = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Telefono'), 'Telefono', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_ContattiTrasmittenteType_Telefono', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 91, 6), )


    Telefono = property(__Telefono.value, __Telefono.set, None, None)


    # Element Email uses Python identifier Email
    __Email = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Email'), 'Email', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_ContattiTrasmittenteType_Email', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 92, 6), )


    Email = property(__Email.value, __Email.set, None, None)

    _ElementMap.update({
        __Telefono.name() : __Telefono,
        __Email.name() : __Email
    })
    _AttributeMap.update({

    })
_module_typeBindings.ContattiTrasmittenteType = ContattiTrasmittenteType
Namespace.addCategoryObject('typeBinding', 'ContattiTrasmittenteType', ContattiTrasmittenteType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiGeneraliType with content type ELEMENT_ONLY
class DatiGeneraliType (pyxb.binding.basis.complexTypeDefinition):
    """
				Blocco relativo ai Dati Generali della Fattura Elettronica
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiGeneraliType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 95, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element DatiGeneraliDocumento uses Python identifier DatiGeneraliDocumento
    __DatiGeneraliDocumento = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiGeneraliDocumento'), 'DatiGeneraliDocumento', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliType_DatiGeneraliDocumento', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 102, 6), )


    DatiGeneraliDocumento = property(__DatiGeneraliDocumento.value, __DatiGeneraliDocumento.set, None, None)


    # Element DatiOrdineAcquisto uses Python identifier DatiOrdineAcquisto
    __DatiOrdineAcquisto = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiOrdineAcquisto'), 'DatiOrdineAcquisto', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliType_DatiOrdineAcquisto', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 103, 6), )


    DatiOrdineAcquisto = property(__DatiOrdineAcquisto.value, __DatiOrdineAcquisto.set, None, None)


    # Element DatiContratto uses Python identifier DatiContratto
    __DatiContratto = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiContratto'), 'DatiContratto', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliType_DatiContratto', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 104, 6), )


    DatiContratto = property(__DatiContratto.value, __DatiContratto.set, None, None)


    # Element DatiConvenzione uses Python identifier DatiConvenzione
    __DatiConvenzione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiConvenzione'), 'DatiConvenzione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliType_DatiConvenzione', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 105, 6), )


    DatiConvenzione = property(__DatiConvenzione.value, __DatiConvenzione.set, None, None)


    # Element DatiRicezione uses Python identifier DatiRicezione
    __DatiRicezione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiRicezione'), 'DatiRicezione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliType_DatiRicezione', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 106, 6), )


    DatiRicezione = property(__DatiRicezione.value, __DatiRicezione.set, None, None)


    # Element DatiFattureCollegate uses Python identifier DatiFattureCollegate
    __DatiFattureCollegate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiFattureCollegate'), 'DatiFattureCollegate', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliType_DatiFattureCollegate', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 107, 6), )


    DatiFattureCollegate = property(__DatiFattureCollegate.value, __DatiFattureCollegate.set, None, None)


    # Element DatiSAL uses Python identifier DatiSAL
    __DatiSAL = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiSAL'), 'DatiSAL', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliType_DatiSAL', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 108, 6), )


    DatiSAL = property(__DatiSAL.value, __DatiSAL.set, None, None)


    # Element DatiDDT uses Python identifier DatiDDT
    __DatiDDT = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiDDT'), 'DatiDDT', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliType_DatiDDT', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 109, 6), )


    DatiDDT = property(__DatiDDT.value, __DatiDDT.set, None, None)


    # Element DatiTrasporto uses Python identifier DatiTrasporto
    __DatiTrasporto = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiTrasporto'), 'DatiTrasporto', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliType_DatiTrasporto', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 110, 6), )


    DatiTrasporto = property(__DatiTrasporto.value, __DatiTrasporto.set, None, None)


    # Element FatturaPrincipale uses Python identifier FatturaPrincipale
    __FatturaPrincipale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'FatturaPrincipale'), 'FatturaPrincipale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliType_FatturaPrincipale', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 111, 6), )


    FatturaPrincipale = property(__FatturaPrincipale.value, __FatturaPrincipale.set, None, None)

    _ElementMap.update({
        __DatiGeneraliDocumento.name() : __DatiGeneraliDocumento,
        __DatiOrdineAcquisto.name() : __DatiOrdineAcquisto,
        __DatiContratto.name() : __DatiContratto,
        __DatiConvenzione.name() : __DatiConvenzione,
        __DatiRicezione.name() : __DatiRicezione,
        __DatiFattureCollegate.name() : __DatiFattureCollegate,
        __DatiSAL.name() : __DatiSAL,
        __DatiDDT.name() : __DatiDDT,
        __DatiTrasporto.name() : __DatiTrasporto,
        __FatturaPrincipale.name() : __FatturaPrincipale
    })
    _AttributeMap.update({

    })
_module_typeBindings.DatiGeneraliType = DatiGeneraliType
Namespace.addCategoryObject('typeBinding', 'DatiGeneraliType', DatiGeneraliType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiGeneraliDocumentoType with content type ELEMENT_ONLY
class DatiGeneraliDocumentoType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiGeneraliDocumentoType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiGeneraliDocumentoType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 114, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element TipoDocumento uses Python identifier TipoDocumento
    __TipoDocumento = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'TipoDocumento'), 'TipoDocumento', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliDocumentoType_TipoDocumento', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 116, 6), )


    TipoDocumento = property(__TipoDocumento.value, __TipoDocumento.set, None, None)


    # Element Divisa uses Python identifier Divisa
    __Divisa = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Divisa'), 'Divisa', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliDocumentoType_Divisa', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 117, 6), )


    Divisa = property(__Divisa.value, __Divisa.set, None, None)


    # Element Data uses Python identifier Data
    __Data = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Data'), 'Data', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliDocumentoType_Data', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 118, 6), )


    Data = property(__Data.value, __Data.set, None, None)


    # Element Numero uses Python identifier Numero
    __Numero = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Numero'), 'Numero', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliDocumentoType_Numero', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 119, 6), )


    Numero = property(__Numero.value, __Numero.set, None, None)


    # Element DatiRitenuta uses Python identifier DatiRitenuta
    __DatiRitenuta = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiRitenuta'), 'DatiRitenuta', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliDocumentoType_DatiRitenuta', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 120, 6), )


    DatiRitenuta = property(__DatiRitenuta.value, __DatiRitenuta.set, None, None)


    # Element DatiBollo uses Python identifier DatiBollo
    __DatiBollo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiBollo'), 'DatiBollo', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliDocumentoType_DatiBollo', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 121, 6), )


    DatiBollo = property(__DatiBollo.value, __DatiBollo.set, None, None)


    # Element DatiCassaPrevidenziale uses Python identifier DatiCassaPrevidenziale
    __DatiCassaPrevidenziale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiCassaPrevidenziale'), 'DatiCassaPrevidenziale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliDocumentoType_DatiCassaPrevidenziale', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 122, 6), )


    DatiCassaPrevidenziale = property(__DatiCassaPrevidenziale.value, __DatiCassaPrevidenziale.set, None, None)


    # Element ScontoMaggiorazione uses Python identifier ScontoMaggiorazione
    __ScontoMaggiorazione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ScontoMaggiorazione'), 'ScontoMaggiorazione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliDocumentoType_ScontoMaggiorazione', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 123, 6), )


    ScontoMaggiorazione = property(__ScontoMaggiorazione.value, __ScontoMaggiorazione.set, None, None)


    # Element ImportoTotaleDocumento uses Python identifier ImportoTotaleDocumento
    __ImportoTotaleDocumento = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ImportoTotaleDocumento'), 'ImportoTotaleDocumento', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliDocumentoType_ImportoTotaleDocumento', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 124, 6), )


    ImportoTotaleDocumento = property(__ImportoTotaleDocumento.value, __ImportoTotaleDocumento.set, None, None)


    # Element Arrotondamento uses Python identifier Arrotondamento
    __Arrotondamento = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Arrotondamento'), 'Arrotondamento', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliDocumentoType_Arrotondamento', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 125, 6), )


    Arrotondamento = property(__Arrotondamento.value, __Arrotondamento.set, None, None)


    # Element Causale uses Python identifier Causale
    __Causale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Causale'), 'Causale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliDocumentoType_Causale', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 126, 6), )


    Causale = property(__Causale.value, __Causale.set, None, None)


    # Element Art73 uses Python identifier Art73
    __Art73 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Art73'), 'Art73', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiGeneraliDocumentoType_Art73', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 127, 6), )


    Art73 = property(__Art73.value, __Art73.set, None, None)

    _ElementMap.update({
        __TipoDocumento.name() : __TipoDocumento,
        __Divisa.name() : __Divisa,
        __Data.name() : __Data,
        __Numero.name() : __Numero,
        __DatiRitenuta.name() : __DatiRitenuta,
        __DatiBollo.name() : __DatiBollo,
        __DatiCassaPrevidenziale.name() : __DatiCassaPrevidenziale,
        __ScontoMaggiorazione.name() : __ScontoMaggiorazione,
        __ImportoTotaleDocumento.name() : __ImportoTotaleDocumento,
        __Arrotondamento.name() : __Arrotondamento,
        __Causale.name() : __Causale,
        __Art73.name() : __Art73
    })
    _AttributeMap.update({

    })
_module_typeBindings.DatiGeneraliDocumentoType = DatiGeneraliDocumentoType
Namespace.addCategoryObject('typeBinding', 'DatiGeneraliDocumentoType', DatiGeneraliDocumentoType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiRitenutaType with content type ELEMENT_ONLY
class DatiRitenutaType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiRitenutaType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiRitenutaType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 130, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element TipoRitenuta uses Python identifier TipoRitenuta
    __TipoRitenuta = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'TipoRitenuta'), 'TipoRitenuta', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiRitenutaType_TipoRitenuta', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 132, 6), )


    TipoRitenuta = property(__TipoRitenuta.value, __TipoRitenuta.set, None, None)


    # Element ImportoRitenuta uses Python identifier ImportoRitenuta
    __ImportoRitenuta = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ImportoRitenuta'), 'ImportoRitenuta', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiRitenutaType_ImportoRitenuta', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 133, 6), )


    ImportoRitenuta = property(__ImportoRitenuta.value, __ImportoRitenuta.set, None, None)


    # Element AliquotaRitenuta uses Python identifier AliquotaRitenuta
    __AliquotaRitenuta = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'AliquotaRitenuta'), 'AliquotaRitenuta', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiRitenutaType_AliquotaRitenuta', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 134, 6), )


    AliquotaRitenuta = property(__AliquotaRitenuta.value, __AliquotaRitenuta.set, None, None)


    # Element CausalePagamento uses Python identifier CausalePagamento
    __CausalePagamento = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CausalePagamento'), 'CausalePagamento', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiRitenutaType_CausalePagamento', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 135, 6), )


    CausalePagamento = property(__CausalePagamento.value, __CausalePagamento.set, None, None)

    _ElementMap.update({
        __TipoRitenuta.name() : __TipoRitenuta,
        __ImportoRitenuta.name() : __ImportoRitenuta,
        __AliquotaRitenuta.name() : __AliquotaRitenuta,
        __CausalePagamento.name() : __CausalePagamento
    })
    _AttributeMap.update({

    })
_module_typeBindings.DatiRitenutaType = DatiRitenutaType
Namespace.addCategoryObject('typeBinding', 'DatiRitenutaType', DatiRitenutaType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiBolloType with content type ELEMENT_ONLY
class DatiBolloType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiBolloType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiBolloType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 138, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element BolloVirtuale uses Python identifier BolloVirtuale
    __BolloVirtuale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'BolloVirtuale'), 'BolloVirtuale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiBolloType_BolloVirtuale', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 140, 6), )


    BolloVirtuale = property(__BolloVirtuale.value, __BolloVirtuale.set, None, None)


    # Element ImportoBollo uses Python identifier ImportoBollo
    __ImportoBollo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ImportoBollo'), 'ImportoBollo', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiBolloType_ImportoBollo', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 141, 6), )


    ImportoBollo = property(__ImportoBollo.value, __ImportoBollo.set, None, None)

    _ElementMap.update({
        __BolloVirtuale.name() : __BolloVirtuale,
        __ImportoBollo.name() : __ImportoBollo
    })
    _AttributeMap.update({

    })
_module_typeBindings.DatiBolloType = DatiBolloType
Namespace.addCategoryObject('typeBinding', 'DatiBolloType', DatiBolloType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiCassaPrevidenzialeType with content type ELEMENT_ONLY
class DatiCassaPrevidenzialeType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiCassaPrevidenzialeType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiCassaPrevidenzialeType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 144, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element TipoCassa uses Python identifier TipoCassa
    __TipoCassa = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'TipoCassa'), 'TipoCassa', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiCassaPrevidenzialeType_TipoCassa', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 146, 6), )


    TipoCassa = property(__TipoCassa.value, __TipoCassa.set, None, None)


    # Element AlCassa uses Python identifier AlCassa
    __AlCassa = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'AlCassa'), 'AlCassa', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiCassaPrevidenzialeType_AlCassa', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 147, 6), )


    AlCassa = property(__AlCassa.value, __AlCassa.set, None, None)


    # Element ImportoContributoCassa uses Python identifier ImportoContributoCassa
    __ImportoContributoCassa = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ImportoContributoCassa'), 'ImportoContributoCassa', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiCassaPrevidenzialeType_ImportoContributoCassa', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 148, 6), )


    ImportoContributoCassa = property(__ImportoContributoCassa.value, __ImportoContributoCassa.set, None, None)


    # Element ImponibileCassa uses Python identifier ImponibileCassa
    __ImponibileCassa = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ImponibileCassa'), 'ImponibileCassa', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiCassaPrevidenzialeType_ImponibileCassa', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 149, 6), )


    ImponibileCassa = property(__ImponibileCassa.value, __ImponibileCassa.set, None, None)


    # Element AliquotaIVA uses Python identifier AliquotaIVA
    __AliquotaIVA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'AliquotaIVA'), 'AliquotaIVA', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiCassaPrevidenzialeType_AliquotaIVA', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 150, 6), )


    AliquotaIVA = property(__AliquotaIVA.value, __AliquotaIVA.set, None, None)


    # Element Ritenuta uses Python identifier Ritenuta
    __Ritenuta = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Ritenuta'), 'Ritenuta', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiCassaPrevidenzialeType_Ritenuta', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 151, 6), )


    Ritenuta = property(__Ritenuta.value, __Ritenuta.set, None, None)


    # Element Natura uses Python identifier Natura
    __Natura = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Natura'), 'Natura', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiCassaPrevidenzialeType_Natura', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 152, 6), )


    Natura = property(__Natura.value, __Natura.set, None, None)


    # Element RiferimentoAmministrazione uses Python identifier RiferimentoAmministrazione
    __RiferimentoAmministrazione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RiferimentoAmministrazione'), 'RiferimentoAmministrazione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiCassaPrevidenzialeType_RiferimentoAmministrazione', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 153, 6), )


    RiferimentoAmministrazione = property(__RiferimentoAmministrazione.value, __RiferimentoAmministrazione.set, None, None)

    _ElementMap.update({
        __TipoCassa.name() : __TipoCassa,
        __AlCassa.name() : __AlCassa,
        __ImportoContributoCassa.name() : __ImportoContributoCassa,
        __ImponibileCassa.name() : __ImponibileCassa,
        __AliquotaIVA.name() : __AliquotaIVA,
        __Ritenuta.name() : __Ritenuta,
        __Natura.name() : __Natura,
        __RiferimentoAmministrazione.name() : __RiferimentoAmministrazione
    })
    _AttributeMap.update({

    })
_module_typeBindings.DatiCassaPrevidenzialeType = DatiCassaPrevidenzialeType
Namespace.addCategoryObject('typeBinding', 'DatiCassaPrevidenzialeType', DatiCassaPrevidenzialeType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}ScontoMaggiorazioneType with content type ELEMENT_ONLY
class ScontoMaggiorazioneType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}ScontoMaggiorazioneType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ScontoMaggiorazioneType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 156, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element Tipo uses Python identifier Tipo
    __Tipo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Tipo'), 'Tipo', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_ScontoMaggiorazioneType_Tipo', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 158, 6), )


    Tipo = property(__Tipo.value, __Tipo.set, None, None)


    # Element Percentuale uses Python identifier Percentuale
    __Percentuale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Percentuale'), 'Percentuale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_ScontoMaggiorazioneType_Percentuale', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 159, 6), )


    Percentuale = property(__Percentuale.value, __Percentuale.set, None, None)


    # Element Importo uses Python identifier Importo
    __Importo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Importo'), 'Importo', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_ScontoMaggiorazioneType_Importo', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 160, 6), )


    Importo = property(__Importo.value, __Importo.set, None, None)

    _ElementMap.update({
        __Tipo.name() : __Tipo,
        __Percentuale.name() : __Percentuale,
        __Importo.name() : __Importo
    })
    _AttributeMap.update({

    })
_module_typeBindings.ScontoMaggiorazioneType = ScontoMaggiorazioneType
Namespace.addCategoryObject('typeBinding', 'ScontoMaggiorazioneType', ScontoMaggiorazioneType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiSALType with content type ELEMENT_ONLY
class DatiSALType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiSALType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiSALType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 466, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element RiferimentoFase uses Python identifier RiferimentoFase
    __RiferimentoFase = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RiferimentoFase'), 'RiferimentoFase', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiSALType_RiferimentoFase', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 468, 6), )


    RiferimentoFase = property(__RiferimentoFase.value, __RiferimentoFase.set, None, None)

    _ElementMap.update({
        __RiferimentoFase.name() : __RiferimentoFase
    })
    _AttributeMap.update({

    })
_module_typeBindings.DatiSALType = DatiSALType
Namespace.addCategoryObject('typeBinding', 'DatiSALType', DatiSALType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiDocumentiCorrelatiType with content type ELEMENT_ONLY
class DatiDocumentiCorrelatiType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiDocumentiCorrelatiType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiDocumentiCorrelatiType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 471, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element RiferimentoNumeroLinea uses Python identifier RiferimentoNumeroLinea
    __RiferimentoNumeroLinea = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RiferimentoNumeroLinea'), 'RiferimentoNumeroLinea', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiDocumentiCorrelatiType_RiferimentoNumeroLinea', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 473, 6), )


    RiferimentoNumeroLinea = property(__RiferimentoNumeroLinea.value, __RiferimentoNumeroLinea.set, None, None)


    # Element IdDocumento uses Python identifier IdDocumento
    __IdDocumento = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IdDocumento'), 'IdDocumento', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiDocumentiCorrelatiType_IdDocumento', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 474, 6), )


    IdDocumento = property(__IdDocumento.value, __IdDocumento.set, None, None)


    # Element Data uses Python identifier Data
    __Data = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Data'), 'Data', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiDocumentiCorrelatiType_Data', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 475, 6), )


    Data = property(__Data.value, __Data.set, None, None)


    # Element NumItem uses Python identifier NumItem
    __NumItem = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'NumItem'), 'NumItem', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiDocumentiCorrelatiType_NumItem', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 476, 6), )


    NumItem = property(__NumItem.value, __NumItem.set, None, None)


    # Element CodiceCommessaConvenzione uses Python identifier CodiceCommessaConvenzione
    __CodiceCommessaConvenzione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CodiceCommessaConvenzione'), 'CodiceCommessaConvenzione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiDocumentiCorrelatiType_CodiceCommessaConvenzione', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 477, 6), )


    CodiceCommessaConvenzione = property(__CodiceCommessaConvenzione.value, __CodiceCommessaConvenzione.set, None, None)


    # Element CodiceCUP uses Python identifier CodiceCUP
    __CodiceCUP = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CodiceCUP'), 'CodiceCUP', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiDocumentiCorrelatiType_CodiceCUP', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 478, 6), )


    CodiceCUP = property(__CodiceCUP.value, __CodiceCUP.set, None, None)


    # Element CodiceCIG uses Python identifier CodiceCIG
    __CodiceCIG = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CodiceCIG'), 'CodiceCIG', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiDocumentiCorrelatiType_CodiceCIG', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 479, 6), )


    CodiceCIG = property(__CodiceCIG.value, __CodiceCIG.set, None, None)

    _ElementMap.update({
        __RiferimentoNumeroLinea.name() : __RiferimentoNumeroLinea,
        __IdDocumento.name() : __IdDocumento,
        __Data.name() : __Data,
        __NumItem.name() : __NumItem,
        __CodiceCommessaConvenzione.name() : __CodiceCommessaConvenzione,
        __CodiceCUP.name() : __CodiceCUP,
        __CodiceCIG.name() : __CodiceCIG
    })
    _AttributeMap.update({

    })
_module_typeBindings.DatiDocumentiCorrelatiType = DatiDocumentiCorrelatiType
Namespace.addCategoryObject('typeBinding', 'DatiDocumentiCorrelatiType', DatiDocumentiCorrelatiType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiDDTType with content type ELEMENT_ONLY
class DatiDDTType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiDDTType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiDDTType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 488, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element NumeroDDT uses Python identifier NumeroDDT
    __NumeroDDT = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'NumeroDDT'), 'NumeroDDT', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiDDTType_NumeroDDT', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 490, 6), )


    NumeroDDT = property(__NumeroDDT.value, __NumeroDDT.set, None, None)


    # Element DataDDT uses Python identifier DataDDT
    __DataDDT = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DataDDT'), 'DataDDT', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiDDTType_DataDDT', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 491, 6), )


    DataDDT = property(__DataDDT.value, __DataDDT.set, None, None)


    # Element RiferimentoNumeroLinea uses Python identifier RiferimentoNumeroLinea
    __RiferimentoNumeroLinea = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RiferimentoNumeroLinea'), 'RiferimentoNumeroLinea', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiDDTType_RiferimentoNumeroLinea', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 492, 6), )


    RiferimentoNumeroLinea = property(__RiferimentoNumeroLinea.value, __RiferimentoNumeroLinea.set, None, None)

    _ElementMap.update({
        __NumeroDDT.name() : __NumeroDDT,
        __DataDDT.name() : __DataDDT,
        __RiferimentoNumeroLinea.name() : __RiferimentoNumeroLinea
    })
    _AttributeMap.update({

    })
_module_typeBindings.DatiDDTType = DatiDDTType
Namespace.addCategoryObject('typeBinding', 'DatiDDTType', DatiDDTType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiTrasportoType with content type ELEMENT_ONLY
class DatiTrasportoType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiTrasportoType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiTrasportoType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 495, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element DatiAnagraficiVettore uses Python identifier DatiAnagraficiVettore
    __DatiAnagraficiVettore = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiAnagraficiVettore'), 'DatiAnagraficiVettore', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiTrasportoType_DatiAnagraficiVettore', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 497, 6), )


    DatiAnagraficiVettore = property(__DatiAnagraficiVettore.value, __DatiAnagraficiVettore.set, None, None)


    # Element MezzoTrasporto uses Python identifier MezzoTrasporto
    __MezzoTrasporto = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'MezzoTrasporto'), 'MezzoTrasporto', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiTrasportoType_MezzoTrasporto', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 498, 6), )


    MezzoTrasporto = property(__MezzoTrasporto.value, __MezzoTrasporto.set, None, None)


    # Element CausaleTrasporto uses Python identifier CausaleTrasporto
    __CausaleTrasporto = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CausaleTrasporto'), 'CausaleTrasporto', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiTrasportoType_CausaleTrasporto', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 499, 6), )


    CausaleTrasporto = property(__CausaleTrasporto.value, __CausaleTrasporto.set, None, None)


    # Element NumeroColli uses Python identifier NumeroColli
    __NumeroColli = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'NumeroColli'), 'NumeroColli', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiTrasportoType_NumeroColli', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 500, 6), )


    NumeroColli = property(__NumeroColli.value, __NumeroColli.set, None, None)


    # Element Descrizione uses Python identifier Descrizione
    __Descrizione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Descrizione'), 'Descrizione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiTrasportoType_Descrizione', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 501, 6), )


    Descrizione = property(__Descrizione.value, __Descrizione.set, None, None)


    # Element UnitaMisuraPeso uses Python identifier UnitaMisuraPeso
    __UnitaMisuraPeso = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'UnitaMisuraPeso'), 'UnitaMisuraPeso', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiTrasportoType_UnitaMisuraPeso', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 502, 6), )


    UnitaMisuraPeso = property(__UnitaMisuraPeso.value, __UnitaMisuraPeso.set, None, None)


    # Element PesoLordo uses Python identifier PesoLordo
    __PesoLordo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PesoLordo'), 'PesoLordo', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiTrasportoType_PesoLordo', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 503, 6), )


    PesoLordo = property(__PesoLordo.value, __PesoLordo.set, None, None)


    # Element PesoNetto uses Python identifier PesoNetto
    __PesoNetto = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PesoNetto'), 'PesoNetto', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiTrasportoType_PesoNetto', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 504, 6), )


    PesoNetto = property(__PesoNetto.value, __PesoNetto.set, None, None)


    # Element DataOraRitiro uses Python identifier DataOraRitiro
    __DataOraRitiro = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DataOraRitiro'), 'DataOraRitiro', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiTrasportoType_DataOraRitiro', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 505, 6), )


    DataOraRitiro = property(__DataOraRitiro.value, __DataOraRitiro.set, None, None)


    # Element DataInizioTrasporto uses Python identifier DataInizioTrasporto
    __DataInizioTrasporto = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DataInizioTrasporto'), 'DataInizioTrasporto', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiTrasportoType_DataInizioTrasporto', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 506, 6), )


    DataInizioTrasporto = property(__DataInizioTrasporto.value, __DataInizioTrasporto.set, None, None)


    # Element TipoResa uses Python identifier TipoResa
    __TipoResa = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'TipoResa'), 'TipoResa', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiTrasportoType_TipoResa', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 507, 6), )


    TipoResa = property(__TipoResa.value, __TipoResa.set, None, None)


    # Element IndirizzoResa uses Python identifier IndirizzoResa
    __IndirizzoResa = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IndirizzoResa'), 'IndirizzoResa', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiTrasportoType_IndirizzoResa', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 508, 6), )


    IndirizzoResa = property(__IndirizzoResa.value, __IndirizzoResa.set, None, None)


    # Element DataOraConsegna uses Python identifier DataOraConsegna
    __DataOraConsegna = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DataOraConsegna'), 'DataOraConsegna', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiTrasportoType_DataOraConsegna', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 509, 6), )


    DataOraConsegna = property(__DataOraConsegna.value, __DataOraConsegna.set, None, None)

    _ElementMap.update({
        __DatiAnagraficiVettore.name() : __DatiAnagraficiVettore,
        __MezzoTrasporto.name() : __MezzoTrasporto,
        __CausaleTrasporto.name() : __CausaleTrasporto,
        __NumeroColli.name() : __NumeroColli,
        __Descrizione.name() : __Descrizione,
        __UnitaMisuraPeso.name() : __UnitaMisuraPeso,
        __PesoLordo.name() : __PesoLordo,
        __PesoNetto.name() : __PesoNetto,
        __DataOraRitiro.name() : __DataOraRitiro,
        __DataInizioTrasporto.name() : __DataInizioTrasporto,
        __TipoResa.name() : __TipoResa,
        __IndirizzoResa.name() : __IndirizzoResa,
        __DataOraConsegna.name() : __DataOraConsegna
    })
    _AttributeMap.update({

    })
_module_typeBindings.DatiTrasportoType = DatiTrasportoType
Namespace.addCategoryObject('typeBinding', 'DatiTrasportoType', DatiTrasportoType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}IndirizzoType with content type ELEMENT_ONLY
class IndirizzoType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}IndirizzoType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IndirizzoType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 512, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element Indirizzo uses Python identifier Indirizzo
    __Indirizzo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Indirizzo'), 'Indirizzo', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_IndirizzoType_Indirizzo', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 514, 6), )


    Indirizzo = property(__Indirizzo.value, __Indirizzo.set, None, None)


    # Element NumeroCivico uses Python identifier NumeroCivico
    __NumeroCivico = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'NumeroCivico'), 'NumeroCivico', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_IndirizzoType_NumeroCivico', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 515, 6), )


    NumeroCivico = property(__NumeroCivico.value, __NumeroCivico.set, None, None)


    # Element CAP uses Python identifier CAP
    __CAP = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CAP'), 'CAP', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_IndirizzoType_CAP', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 516, 6), )


    CAP = property(__CAP.value, __CAP.set, None, None)


    # Element Comune uses Python identifier Comune
    __Comune = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Comune'), 'Comune', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_IndirizzoType_Comune', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 517, 6), )


    Comune = property(__Comune.value, __Comune.set, None, None)


    # Element Provincia uses Python identifier Provincia
    __Provincia = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Provincia'), 'Provincia', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_IndirizzoType_Provincia', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 518, 6), )


    Provincia = property(__Provincia.value, __Provincia.set, None, None)


    # Element Nazione uses Python identifier Nazione
    __Nazione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Nazione'), 'Nazione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_IndirizzoType_Nazione', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 519, 6), )


    Nazione = property(__Nazione.value, __Nazione.set, None, None)

    _ElementMap.update({
        __Indirizzo.name() : __Indirizzo,
        __NumeroCivico.name() : __NumeroCivico,
        __CAP.name() : __CAP,
        __Comune.name() : __Comune,
        __Provincia.name() : __Provincia,
        __Nazione.name() : __Nazione
    })
    _AttributeMap.update({

    })
_module_typeBindings.IndirizzoType = IndirizzoType
Namespace.addCategoryObject('typeBinding', 'IndirizzoType', IndirizzoType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}FatturaPrincipaleType with content type ELEMENT_ONLY
class FatturaPrincipaleType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}FatturaPrincipaleType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FatturaPrincipaleType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 522, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element NumeroFatturaPrincipale uses Python identifier NumeroFatturaPrincipale
    __NumeroFatturaPrincipale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'NumeroFatturaPrincipale'), 'NumeroFatturaPrincipale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_FatturaPrincipaleType_NumeroFatturaPrincipale', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 524, 6), )


    NumeroFatturaPrincipale = property(__NumeroFatturaPrincipale.value, __NumeroFatturaPrincipale.set, None, None)


    # Element DataFatturaPrincipale uses Python identifier DataFatturaPrincipale
    __DataFatturaPrincipale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DataFatturaPrincipale'), 'DataFatturaPrincipale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_FatturaPrincipaleType_DataFatturaPrincipale', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 525, 6), )


    DataFatturaPrincipale = property(__DataFatturaPrincipale.value, __DataFatturaPrincipale.set, None, None)

    _ElementMap.update({
        __NumeroFatturaPrincipale.name() : __NumeroFatturaPrincipale,
        __DataFatturaPrincipale.name() : __DataFatturaPrincipale
    })
    _AttributeMap.update({

    })
_module_typeBindings.FatturaPrincipaleType = FatturaPrincipaleType
Namespace.addCategoryObject('typeBinding', 'FatturaPrincipaleType', FatturaPrincipaleType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}CedentePrestatoreType with content type ELEMENT_ONLY
class CedentePrestatoreType (pyxb.binding.basis.complexTypeDefinition):
    """Blocco relativo ai dati del Cedente / Prestatore"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CedentePrestatoreType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 543, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element DatiAnagrafici uses Python identifier DatiAnagrafici
    __DatiAnagrafici = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiAnagrafici'), 'DatiAnagrafici', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_CedentePrestatoreType_DatiAnagrafici', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 548, 6), )


    DatiAnagrafici = property(__DatiAnagrafici.value, __DatiAnagrafici.set, None, None)


    # Element Sede uses Python identifier Sede
    __Sede = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Sede'), 'Sede', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_CedentePrestatoreType_Sede', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 549, 6), )


    Sede = property(__Sede.value, __Sede.set, None, None)


    # Element StabileOrganizzazione uses Python identifier StabileOrganizzazione
    __StabileOrganizzazione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'StabileOrganizzazione'), 'StabileOrganizzazione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_CedentePrestatoreType_StabileOrganizzazione', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 550, 6), )


    StabileOrganizzazione = property(__StabileOrganizzazione.value, __StabileOrganizzazione.set, None, None)


    # Element IscrizioneREA uses Python identifier IscrizioneREA
    __IscrizioneREA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IscrizioneREA'), 'IscrizioneREA', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_CedentePrestatoreType_IscrizioneREA', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 551, 6), )


    IscrizioneREA = property(__IscrizioneREA.value, __IscrizioneREA.set, None, None)


    # Element Contatti uses Python identifier Contatti
    __Contatti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Contatti'), 'Contatti', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_CedentePrestatoreType_Contatti', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 552, 6), )


    Contatti = property(__Contatti.value, __Contatti.set, None, None)


    # Element RiferimentoAmministrazione uses Python identifier RiferimentoAmministrazione
    __RiferimentoAmministrazione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RiferimentoAmministrazione'), 'RiferimentoAmministrazione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_CedentePrestatoreType_RiferimentoAmministrazione', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 553, 6), )


    RiferimentoAmministrazione = property(__RiferimentoAmministrazione.value, __RiferimentoAmministrazione.set, None, None)

    _ElementMap.update({
        __DatiAnagrafici.name() : __DatiAnagrafici,
        __Sede.name() : __Sede,
        __StabileOrganizzazione.name() : __StabileOrganizzazione,
        __IscrizioneREA.name() : __IscrizioneREA,
        __Contatti.name() : __Contatti,
        __RiferimentoAmministrazione.name() : __RiferimentoAmministrazione
    })
    _AttributeMap.update({

    })
_module_typeBindings.CedentePrestatoreType = CedentePrestatoreType
Namespace.addCategoryObject('typeBinding', 'CedentePrestatoreType', CedentePrestatoreType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiAnagraficiCedenteType with content type ELEMENT_ONLY
class DatiAnagraficiCedenteType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiAnagraficiCedenteType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiAnagraficiCedenteType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 556, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdFiscaleIVA uses Python identifier IdFiscaleIVA
    __IdFiscaleIVA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IdFiscaleIVA'), 'IdFiscaleIVA', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiCedenteType_IdFiscaleIVA', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 558, 6), )


    IdFiscaleIVA = property(__IdFiscaleIVA.value, __IdFiscaleIVA.set, None, None)


    # Element CodiceFiscale uses Python identifier CodiceFiscale
    __CodiceFiscale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CodiceFiscale'), 'CodiceFiscale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiCedenteType_CodiceFiscale', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 559, 6), )


    CodiceFiscale = property(__CodiceFiscale.value, __CodiceFiscale.set, None, None)


    # Element Anagrafica uses Python identifier Anagrafica
    __Anagrafica = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Anagrafica'), 'Anagrafica', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiCedenteType_Anagrafica', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 560, 6), )


    Anagrafica = property(__Anagrafica.value, __Anagrafica.set, None, None)


    # Element AlboProfessionale uses Python identifier AlboProfessionale
    __AlboProfessionale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'AlboProfessionale'), 'AlboProfessionale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiCedenteType_AlboProfessionale', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 561, 6), )


    AlboProfessionale = property(__AlboProfessionale.value, __AlboProfessionale.set, None, None)


    # Element ProvinciaAlbo uses Python identifier ProvinciaAlbo
    __ProvinciaAlbo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ProvinciaAlbo'), 'ProvinciaAlbo', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiCedenteType_ProvinciaAlbo', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 562, 6), )


    ProvinciaAlbo = property(__ProvinciaAlbo.value, __ProvinciaAlbo.set, None, None)


    # Element NumeroIscrizioneAlbo uses Python identifier NumeroIscrizioneAlbo
    __NumeroIscrizioneAlbo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'NumeroIscrizioneAlbo'), 'NumeroIscrizioneAlbo', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiCedenteType_NumeroIscrizioneAlbo', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 563, 6), )


    NumeroIscrizioneAlbo = property(__NumeroIscrizioneAlbo.value, __NumeroIscrizioneAlbo.set, None, None)


    # Element DataIscrizioneAlbo uses Python identifier DataIscrizioneAlbo
    __DataIscrizioneAlbo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DataIscrizioneAlbo'), 'DataIscrizioneAlbo', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiCedenteType_DataIscrizioneAlbo', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 564, 6), )


    DataIscrizioneAlbo = property(__DataIscrizioneAlbo.value, __DataIscrizioneAlbo.set, None, None)


    # Element RegimeFiscale uses Python identifier RegimeFiscale
    __RegimeFiscale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RegimeFiscale'), 'RegimeFiscale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiCedenteType_RegimeFiscale', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 565, 6), )


    RegimeFiscale = property(__RegimeFiscale.value, __RegimeFiscale.set, None, None)

    _ElementMap.update({
        __IdFiscaleIVA.name() : __IdFiscaleIVA,
        __CodiceFiscale.name() : __CodiceFiscale,
        __Anagrafica.name() : __Anagrafica,
        __AlboProfessionale.name() : __AlboProfessionale,
        __ProvinciaAlbo.name() : __ProvinciaAlbo,
        __NumeroIscrizioneAlbo.name() : __NumeroIscrizioneAlbo,
        __DataIscrizioneAlbo.name() : __DataIscrizioneAlbo,
        __RegimeFiscale.name() : __RegimeFiscale
    })
    _AttributeMap.update({

    })
_module_typeBindings.DatiAnagraficiCedenteType = DatiAnagraficiCedenteType
Namespace.addCategoryObject('typeBinding', 'DatiAnagraficiCedenteType', DatiAnagraficiCedenteType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}AnagraficaType with content type ELEMENT_ONLY
class AnagraficaType (pyxb.binding.basis.complexTypeDefinition):
    """Il campo Denominazione è in alternativa ai campi Nome e Cognome"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AnagraficaType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 663, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element Denominazione uses Python identifier Denominazione
    __Denominazione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Denominazione'), 'Denominazione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_AnagraficaType_Denominazione', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 670, 10), )


    Denominazione = property(__Denominazione.value, __Denominazione.set, None, None)


    # Element Nome uses Python identifier Nome
    __Nome = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Nome'), 'Nome', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_AnagraficaType_Nome', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 673, 10), )


    Nome = property(__Nome.value, __Nome.set, None, None)


    # Element Cognome uses Python identifier Cognome
    __Cognome = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Cognome'), 'Cognome', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_AnagraficaType_Cognome', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 674, 10), )


    Cognome = property(__Cognome.value, __Cognome.set, None, None)


    # Element Titolo uses Python identifier Titolo
    __Titolo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Titolo'), 'Titolo', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_AnagraficaType_Titolo', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 677, 6), )


    Titolo = property(__Titolo.value, __Titolo.set, None, None)


    # Element CodEORI uses Python identifier CodEORI
    __CodEORI = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CodEORI'), 'CodEORI', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_AnagraficaType_CodEORI', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 678, 6), )


    CodEORI = property(__CodEORI.value, __CodEORI.set, None, None)

    _ElementMap.update({
        __Denominazione.name() : __Denominazione,
        __Nome.name() : __Nome,
        __Cognome.name() : __Cognome,
        __Titolo.name() : __Titolo,
        __CodEORI.name() : __CodEORI
    })
    _AttributeMap.update({

    })
_module_typeBindings.AnagraficaType = AnagraficaType
Namespace.addCategoryObject('typeBinding', 'AnagraficaType', AnagraficaType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiAnagraficiVettoreType with content type ELEMENT_ONLY
class DatiAnagraficiVettoreType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiAnagraficiVettoreType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiAnagraficiVettoreType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 681, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdFiscaleIVA uses Python identifier IdFiscaleIVA
    __IdFiscaleIVA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IdFiscaleIVA'), 'IdFiscaleIVA', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiVettoreType_IdFiscaleIVA', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 683, 6), )


    IdFiscaleIVA = property(__IdFiscaleIVA.value, __IdFiscaleIVA.set, None, None)


    # Element CodiceFiscale uses Python identifier CodiceFiscale
    __CodiceFiscale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CodiceFiscale'), 'CodiceFiscale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiVettoreType_CodiceFiscale', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 684, 6), )


    CodiceFiscale = property(__CodiceFiscale.value, __CodiceFiscale.set, None, None)


    # Element Anagrafica uses Python identifier Anagrafica
    __Anagrafica = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Anagrafica'), 'Anagrafica', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiVettoreType_Anagrafica', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 685, 6), )


    Anagrafica = property(__Anagrafica.value, __Anagrafica.set, None, None)


    # Element NumeroLicenzaGuida uses Python identifier NumeroLicenzaGuida
    __NumeroLicenzaGuida = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'NumeroLicenzaGuida'), 'NumeroLicenzaGuida', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiVettoreType_NumeroLicenzaGuida', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 686, 6), )


    NumeroLicenzaGuida = property(__NumeroLicenzaGuida.value, __NumeroLicenzaGuida.set, None, None)

    _ElementMap.update({
        __IdFiscaleIVA.name() : __IdFiscaleIVA,
        __CodiceFiscale.name() : __CodiceFiscale,
        __Anagrafica.name() : __Anagrafica,
        __NumeroLicenzaGuida.name() : __NumeroLicenzaGuida
    })
    _AttributeMap.update({

    })
_module_typeBindings.DatiAnagraficiVettoreType = DatiAnagraficiVettoreType
Namespace.addCategoryObject('typeBinding', 'DatiAnagraficiVettoreType', DatiAnagraficiVettoreType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}IscrizioneREAType with content type ELEMENT_ONLY
class IscrizioneREAType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}IscrizioneREAType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IscrizioneREAType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 689, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element Ufficio uses Python identifier Ufficio
    __Ufficio = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Ufficio'), 'Ufficio', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_IscrizioneREAType_Ufficio', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 691, 6), )


    Ufficio = property(__Ufficio.value, __Ufficio.set, None, None)


    # Element NumeroREA uses Python identifier NumeroREA
    __NumeroREA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'NumeroREA'), 'NumeroREA', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_IscrizioneREAType_NumeroREA', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 692, 6), )


    NumeroREA = property(__NumeroREA.value, __NumeroREA.set, None, None)


    # Element CapitaleSociale uses Python identifier CapitaleSociale
    __CapitaleSociale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CapitaleSociale'), 'CapitaleSociale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_IscrizioneREAType_CapitaleSociale', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 693, 6), )


    CapitaleSociale = property(__CapitaleSociale.value, __CapitaleSociale.set, None, None)


    # Element SocioUnico uses Python identifier SocioUnico
    __SocioUnico = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SocioUnico'), 'SocioUnico', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_IscrizioneREAType_SocioUnico', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 694, 6), )


    SocioUnico = property(__SocioUnico.value, __SocioUnico.set, None, None)


    # Element StatoLiquidazione uses Python identifier StatoLiquidazione
    __StatoLiquidazione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'StatoLiquidazione'), 'StatoLiquidazione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_IscrizioneREAType_StatoLiquidazione', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 695, 6), )


    StatoLiquidazione = property(__StatoLiquidazione.value, __StatoLiquidazione.set, None, None)

    _ElementMap.update({
        __Ufficio.name() : __Ufficio,
        __NumeroREA.name() : __NumeroREA,
        __CapitaleSociale.name() : __CapitaleSociale,
        __SocioUnico.name() : __SocioUnico,
        __StatoLiquidazione.name() : __StatoLiquidazione
    })
    _AttributeMap.update({

    })
_module_typeBindings.IscrizioneREAType = IscrizioneREAType
Namespace.addCategoryObject('typeBinding', 'IscrizioneREAType', IscrizioneREAType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}ContattiType with content type ELEMENT_ONLY
class ContattiType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}ContattiType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ContattiType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 698, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element Telefono uses Python identifier Telefono
    __Telefono = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Telefono'), 'Telefono', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_ContattiType_Telefono', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 700, 6), )


    Telefono = property(__Telefono.value, __Telefono.set, None, None)


    # Element Fax uses Python identifier Fax
    __Fax = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Fax'), 'Fax', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_ContattiType_Fax', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 701, 6), )


    Fax = property(__Fax.value, __Fax.set, None, None)


    # Element Email uses Python identifier Email
    __Email = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Email'), 'Email', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_ContattiType_Email', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 702, 6), )


    Email = property(__Email.value, __Email.set, None, None)

    _ElementMap.update({
        __Telefono.name() : __Telefono,
        __Fax.name() : __Fax,
        __Email.name() : __Email
    })
    _AttributeMap.update({

    })
_module_typeBindings.ContattiType = ContattiType
Namespace.addCategoryObject('typeBinding', 'ContattiType', ContattiType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}RappresentanteFiscaleType with content type ELEMENT_ONLY
class RappresentanteFiscaleType (pyxb.binding.basis.complexTypeDefinition):
    """Blocco relativo ai dati del Rappresentante Fiscale"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'RappresentanteFiscaleType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 705, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element DatiAnagrafici uses Python identifier DatiAnagrafici
    __DatiAnagrafici = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiAnagrafici'), 'DatiAnagrafici', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_RappresentanteFiscaleType_DatiAnagrafici', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 710, 6), )


    DatiAnagrafici = property(__DatiAnagrafici.value, __DatiAnagrafici.set, None, None)

    _ElementMap.update({
        __DatiAnagrafici.name() : __DatiAnagrafici
    })
    _AttributeMap.update({

    })
_module_typeBindings.RappresentanteFiscaleType = RappresentanteFiscaleType
Namespace.addCategoryObject('typeBinding', 'RappresentanteFiscaleType', RappresentanteFiscaleType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiAnagraficiRappresentanteType with content type ELEMENT_ONLY
class DatiAnagraficiRappresentanteType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiAnagraficiRappresentanteType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiAnagraficiRappresentanteType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 713, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdFiscaleIVA uses Python identifier IdFiscaleIVA
    __IdFiscaleIVA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IdFiscaleIVA'), 'IdFiscaleIVA', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiRappresentanteType_IdFiscaleIVA', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 715, 6), )


    IdFiscaleIVA = property(__IdFiscaleIVA.value, __IdFiscaleIVA.set, None, None)


    # Element CodiceFiscale uses Python identifier CodiceFiscale
    __CodiceFiscale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CodiceFiscale'), 'CodiceFiscale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiRappresentanteType_CodiceFiscale', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 716, 6), )


    CodiceFiscale = property(__CodiceFiscale.value, __CodiceFiscale.set, None, None)


    # Element Anagrafica uses Python identifier Anagrafica
    __Anagrafica = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Anagrafica'), 'Anagrafica', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiRappresentanteType_Anagrafica', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 717, 6), )


    Anagrafica = property(__Anagrafica.value, __Anagrafica.set, None, None)

    _ElementMap.update({
        __IdFiscaleIVA.name() : __IdFiscaleIVA,
        __CodiceFiscale.name() : __CodiceFiscale,
        __Anagrafica.name() : __Anagrafica
    })
    _AttributeMap.update({

    })
_module_typeBindings.DatiAnagraficiRappresentanteType = DatiAnagraficiRappresentanteType
Namespace.addCategoryObject('typeBinding', 'DatiAnagraficiRappresentanteType', DatiAnagraficiRappresentanteType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}CessionarioCommittenteType with content type ELEMENT_ONLY
class CessionarioCommittenteType (pyxb.binding.basis.complexTypeDefinition):
    """Blocco relativo ai dati del Cessionario / Committente"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CessionarioCommittenteType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 720, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element DatiAnagrafici uses Python identifier DatiAnagrafici
    __DatiAnagrafici = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiAnagrafici'), 'DatiAnagrafici', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_CessionarioCommittenteType_DatiAnagrafici', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 725, 6), )


    DatiAnagrafici = property(__DatiAnagrafici.value, __DatiAnagrafici.set, None, None)


    # Element Sede uses Python identifier Sede
    __Sede = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Sede'), 'Sede', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_CessionarioCommittenteType_Sede', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 726, 6), )


    Sede = property(__Sede.value, __Sede.set, None, None)


    # Element StabileOrganizzazione uses Python identifier StabileOrganizzazione
    __StabileOrganizzazione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'StabileOrganizzazione'), 'StabileOrganizzazione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_CessionarioCommittenteType_StabileOrganizzazione', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 727, 3), )


    StabileOrganizzazione = property(__StabileOrganizzazione.value, __StabileOrganizzazione.set, None, None)


    # Element RappresentanteFiscale uses Python identifier RappresentanteFiscale
    __RappresentanteFiscale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RappresentanteFiscale'), 'RappresentanteFiscale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_CessionarioCommittenteType_RappresentanteFiscale', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 728, 6), )


    RappresentanteFiscale = property(__RappresentanteFiscale.value, __RappresentanteFiscale.set, None, None)

    _ElementMap.update({
        __DatiAnagrafici.name() : __DatiAnagrafici,
        __Sede.name() : __Sede,
        __StabileOrganizzazione.name() : __StabileOrganizzazione,
        __RappresentanteFiscale.name() : __RappresentanteFiscale
    })
    _AttributeMap.update({

    })
_module_typeBindings.CessionarioCommittenteType = CessionarioCommittenteType
Namespace.addCategoryObject('typeBinding', 'CessionarioCommittenteType', CessionarioCommittenteType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}RappresentanteFiscaleCessionarioType with content type ELEMENT_ONLY
class RappresentanteFiscaleCessionarioType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}RappresentanteFiscaleCessionarioType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'RappresentanteFiscaleCessionarioType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 731, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdFiscaleIVA uses Python identifier IdFiscaleIVA
    __IdFiscaleIVA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IdFiscaleIVA'), 'IdFiscaleIVA', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_RappresentanteFiscaleCessionarioType_IdFiscaleIVA', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 733, 3), )


    IdFiscaleIVA = property(__IdFiscaleIVA.value, __IdFiscaleIVA.set, None, None)


    # Element Denominazione uses Python identifier Denominazione
    __Denominazione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Denominazione'), 'Denominazione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_RappresentanteFiscaleCessionarioType_Denominazione', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 736, 10), )


    Denominazione = property(__Denominazione.value, __Denominazione.set, None, None)


    # Element Nome uses Python identifier Nome
    __Nome = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Nome'), 'Nome', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_RappresentanteFiscaleCessionarioType_Nome', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 739, 10), )


    Nome = property(__Nome.value, __Nome.set, None, None)


    # Element Cognome uses Python identifier Cognome
    __Cognome = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Cognome'), 'Cognome', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_RappresentanteFiscaleCessionarioType_Cognome', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 740, 10), )


    Cognome = property(__Cognome.value, __Cognome.set, None, None)

    _ElementMap.update({
        __IdFiscaleIVA.name() : __IdFiscaleIVA,
        __Denominazione.name() : __Denominazione,
        __Nome.name() : __Nome,
        __Cognome.name() : __Cognome
    })
    _AttributeMap.update({

    })
_module_typeBindings.RappresentanteFiscaleCessionarioType = RappresentanteFiscaleCessionarioType
Namespace.addCategoryObject('typeBinding', 'RappresentanteFiscaleCessionarioType', RappresentanteFiscaleCessionarioType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiAnagraficiCessionarioType with content type ELEMENT_ONLY
class DatiAnagraficiCessionarioType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiAnagraficiCessionarioType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiAnagraficiCessionarioType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 745, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdFiscaleIVA uses Python identifier IdFiscaleIVA
    __IdFiscaleIVA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IdFiscaleIVA'), 'IdFiscaleIVA', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiCessionarioType_IdFiscaleIVA', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 747, 6), )


    IdFiscaleIVA = property(__IdFiscaleIVA.value, __IdFiscaleIVA.set, None, None)


    # Element CodiceFiscale uses Python identifier CodiceFiscale
    __CodiceFiscale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CodiceFiscale'), 'CodiceFiscale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiCessionarioType_CodiceFiscale', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 748, 6), )


    CodiceFiscale = property(__CodiceFiscale.value, __CodiceFiscale.set, None, None)


    # Element Anagrafica uses Python identifier Anagrafica
    __Anagrafica = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Anagrafica'), 'Anagrafica', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiCessionarioType_Anagrafica', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 749, 6), )


    Anagrafica = property(__Anagrafica.value, __Anagrafica.set, None, None)

    _ElementMap.update({
        __IdFiscaleIVA.name() : __IdFiscaleIVA,
        __CodiceFiscale.name() : __CodiceFiscale,
        __Anagrafica.name() : __Anagrafica
    })
    _AttributeMap.update({

    })
_module_typeBindings.DatiAnagraficiCessionarioType = DatiAnagraficiCessionarioType
Namespace.addCategoryObject('typeBinding', 'DatiAnagraficiCessionarioType', DatiAnagraficiCessionarioType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiBeniServiziType with content type ELEMENT_ONLY
class DatiBeniServiziType (pyxb.binding.basis.complexTypeDefinition):
    """Blocco relativo ai dati di Beni Servizi della Fattura	Elettronica"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiBeniServiziType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 752, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element DettaglioLinee uses Python identifier DettaglioLinee
    __DettaglioLinee = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DettaglioLinee'), 'DettaglioLinee', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiBeniServiziType_DettaglioLinee', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 757, 6), )


    DettaglioLinee = property(__DettaglioLinee.value, __DettaglioLinee.set, None, None)


    # Element DatiRiepilogo uses Python identifier DatiRiepilogo
    __DatiRiepilogo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiRiepilogo'), 'DatiRiepilogo', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiBeniServiziType_DatiRiepilogo', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 758, 6), )


    DatiRiepilogo = property(__DatiRiepilogo.value, __DatiRiepilogo.set, None, None)

    _ElementMap.update({
        __DettaglioLinee.name() : __DettaglioLinee,
        __DatiRiepilogo.name() : __DatiRiepilogo
    })
    _AttributeMap.update({

    })
_module_typeBindings.DatiBeniServiziType = DatiBeniServiziType
Namespace.addCategoryObject('typeBinding', 'DatiBeniServiziType', DatiBeniServiziType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiVeicoliType with content type ELEMENT_ONLY
class DatiVeicoliType (pyxb.binding.basis.complexTypeDefinition):
    """Blocco relativo ai dati dei Veicoli della Fattura Elettronica (da indicare nei casi di cessioni tra Paesi
			membri di mezzi di trasporto nuovi, in base all'art. 38, comma 4 del dl 331 del 1993)"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiVeicoliType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 761, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element Data uses Python identifier Data
    __Data = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Data'), 'Data', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiVeicoliType_Data', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 767, 6), )


    Data = property(__Data.value, __Data.set, None, None)


    # Element TotalePercorso uses Python identifier TotalePercorso
    __TotalePercorso = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'TotalePercorso'), 'TotalePercorso', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiVeicoliType_TotalePercorso', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 768, 6), )


    TotalePercorso = property(__TotalePercorso.value, __TotalePercorso.set, None, None)

    _ElementMap.update({
        __Data.name() : __Data,
        __TotalePercorso.name() : __TotalePercorso
    })
    _AttributeMap.update({

    })
_module_typeBindings.DatiVeicoliType = DatiVeicoliType
Namespace.addCategoryObject('typeBinding', 'DatiVeicoliType', DatiVeicoliType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiPagamentoType with content type ELEMENT_ONLY
class DatiPagamentoType (pyxb.binding.basis.complexTypeDefinition):
    """Blocco relativo ai dati di Pagamento della Fattura Elettronica"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiPagamentoType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 771, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element CondizioniPagamento uses Python identifier CondizioniPagamento
    __CondizioniPagamento = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CondizioniPagamento'), 'CondizioniPagamento', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiPagamentoType_CondizioniPagamento', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 776, 6), )


    CondizioniPagamento = property(__CondizioniPagamento.value, __CondizioniPagamento.set, None, None)


    # Element DettaglioPagamento uses Python identifier DettaglioPagamento
    __DettaglioPagamento = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DettaglioPagamento'), 'DettaglioPagamento', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiPagamentoType_DettaglioPagamento', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 777, 6), )


    DettaglioPagamento = property(__DettaglioPagamento.value, __DettaglioPagamento.set, None, None)

    _ElementMap.update({
        __CondizioniPagamento.name() : __CondizioniPagamento,
        __DettaglioPagamento.name() : __DettaglioPagamento
    })
    _AttributeMap.update({

    })
_module_typeBindings.DatiPagamentoType = DatiPagamentoType
Namespace.addCategoryObject('typeBinding', 'DatiPagamentoType', DatiPagamentoType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DettaglioPagamentoType with content type ELEMENT_ONLY
class DettaglioPagamentoType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DettaglioPagamentoType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DettaglioPagamentoType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 801, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element Beneficiario uses Python identifier Beneficiario
    __Beneficiario = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Beneficiario'), 'Beneficiario', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_Beneficiario', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 803, 6), )


    Beneficiario = property(__Beneficiario.value, __Beneficiario.set, None, None)


    # Element ModalitaPagamento uses Python identifier ModalitaPagamento
    __ModalitaPagamento = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ModalitaPagamento'), 'ModalitaPagamento', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_ModalitaPagamento', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 804, 6), )


    ModalitaPagamento = property(__ModalitaPagamento.value, __ModalitaPagamento.set, None, None)


    # Element DataRiferimentoTerminiPagamento uses Python identifier DataRiferimentoTerminiPagamento
    __DataRiferimentoTerminiPagamento = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DataRiferimentoTerminiPagamento'), 'DataRiferimentoTerminiPagamento', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_DataRiferimentoTerminiPagamento', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 805, 6), )


    DataRiferimentoTerminiPagamento = property(__DataRiferimentoTerminiPagamento.value, __DataRiferimentoTerminiPagamento.set, None, None)


    # Element GiorniTerminiPagamento uses Python identifier GiorniTerminiPagamento
    __GiorniTerminiPagamento = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'GiorniTerminiPagamento'), 'GiorniTerminiPagamento', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_GiorniTerminiPagamento', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 806, 6), )


    GiorniTerminiPagamento = property(__GiorniTerminiPagamento.value, __GiorniTerminiPagamento.set, None, None)


    # Element DataScadenzaPagamento uses Python identifier DataScadenzaPagamento
    __DataScadenzaPagamento = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DataScadenzaPagamento'), 'DataScadenzaPagamento', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_DataScadenzaPagamento', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 807, 6), )


    DataScadenzaPagamento = property(__DataScadenzaPagamento.value, __DataScadenzaPagamento.set, None, None)


    # Element ImportoPagamento uses Python identifier ImportoPagamento
    __ImportoPagamento = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ImportoPagamento'), 'ImportoPagamento', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_ImportoPagamento', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 808, 6), )


    ImportoPagamento = property(__ImportoPagamento.value, __ImportoPagamento.set, None, None)


    # Element CodUfficioPostale uses Python identifier CodUfficioPostale
    __CodUfficioPostale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CodUfficioPostale'), 'CodUfficioPostale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_CodUfficioPostale', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 809, 6), )


    CodUfficioPostale = property(__CodUfficioPostale.value, __CodUfficioPostale.set, None, None)


    # Element CognomeQuietanzante uses Python identifier CognomeQuietanzante
    __CognomeQuietanzante = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CognomeQuietanzante'), 'CognomeQuietanzante', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_CognomeQuietanzante', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 810, 6), )


    CognomeQuietanzante = property(__CognomeQuietanzante.value, __CognomeQuietanzante.set, None, None)


    # Element NomeQuietanzante uses Python identifier NomeQuietanzante
    __NomeQuietanzante = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'NomeQuietanzante'), 'NomeQuietanzante', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_NomeQuietanzante', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 811, 6), )


    NomeQuietanzante = property(__NomeQuietanzante.value, __NomeQuietanzante.set, None, None)


    # Element CFQuietanzante uses Python identifier CFQuietanzante
    __CFQuietanzante = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CFQuietanzante'), 'CFQuietanzante', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_CFQuietanzante', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 812, 6), )


    CFQuietanzante = property(__CFQuietanzante.value, __CFQuietanzante.set, None, None)


    # Element TitoloQuietanzante uses Python identifier TitoloQuietanzante
    __TitoloQuietanzante = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'TitoloQuietanzante'), 'TitoloQuietanzante', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_TitoloQuietanzante', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 813, 6), )


    TitoloQuietanzante = property(__TitoloQuietanzante.value, __TitoloQuietanzante.set, None, None)


    # Element IstitutoFinanziario uses Python identifier IstitutoFinanziario
    __IstitutoFinanziario = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IstitutoFinanziario'), 'IstitutoFinanziario', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_IstitutoFinanziario', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 814, 6), )


    IstitutoFinanziario = property(__IstitutoFinanziario.value, __IstitutoFinanziario.set, None, None)


    # Element IBAN uses Python identifier IBAN
    __IBAN = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IBAN'), 'IBAN', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_IBAN', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 815, 6), )


    IBAN = property(__IBAN.value, __IBAN.set, None, None)


    # Element ABI uses Python identifier ABI
    __ABI = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ABI'), 'ABI', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_ABI', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 816, 6), )


    ABI = property(__ABI.value, __ABI.set, None, None)


    # Element CAB uses Python identifier CAB
    __CAB = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CAB'), 'CAB', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_CAB', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 817, 6), )


    CAB = property(__CAB.value, __CAB.set, None, None)


    # Element BIC uses Python identifier BIC
    __BIC = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'BIC'), 'BIC', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_BIC', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 818, 6), )


    BIC = property(__BIC.value, __BIC.set, None, None)


    # Element ScontoPagamentoAnticipato uses Python identifier ScontoPagamentoAnticipato
    __ScontoPagamentoAnticipato = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ScontoPagamentoAnticipato'), 'ScontoPagamentoAnticipato', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_ScontoPagamentoAnticipato', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 819, 6), )


    ScontoPagamentoAnticipato = property(__ScontoPagamentoAnticipato.value, __ScontoPagamentoAnticipato.set, None, None)


    # Element DataLimitePagamentoAnticipato uses Python identifier DataLimitePagamentoAnticipato
    __DataLimitePagamentoAnticipato = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DataLimitePagamentoAnticipato'), 'DataLimitePagamentoAnticipato', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_DataLimitePagamentoAnticipato', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 820, 6), )


    DataLimitePagamentoAnticipato = property(__DataLimitePagamentoAnticipato.value, __DataLimitePagamentoAnticipato.set, None, None)


    # Element PenalitaPagamentiRitardati uses Python identifier PenalitaPagamentiRitardati
    __PenalitaPagamentiRitardati = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PenalitaPagamentiRitardati'), 'PenalitaPagamentiRitardati', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_PenalitaPagamentiRitardati', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 821, 6), )


    PenalitaPagamentiRitardati = property(__PenalitaPagamentiRitardati.value, __PenalitaPagamentiRitardati.set, None, None)


    # Element DataDecorrenzaPenale uses Python identifier DataDecorrenzaPenale
    __DataDecorrenzaPenale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DataDecorrenzaPenale'), 'DataDecorrenzaPenale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_DataDecorrenzaPenale', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 822, 6), )


    DataDecorrenzaPenale = property(__DataDecorrenzaPenale.value, __DataDecorrenzaPenale.set, None, None)


    # Element CodicePagamento uses Python identifier CodicePagamento
    __CodicePagamento = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CodicePagamento'), 'CodicePagamento', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioPagamentoType_CodicePagamento', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 823, 6), )


    CodicePagamento = property(__CodicePagamento.value, __CodicePagamento.set, None, None)

    _ElementMap.update({
        __Beneficiario.name() : __Beneficiario,
        __ModalitaPagamento.name() : __ModalitaPagamento,
        __DataRiferimentoTerminiPagamento.name() : __DataRiferimentoTerminiPagamento,
        __GiorniTerminiPagamento.name() : __GiorniTerminiPagamento,
        __DataScadenzaPagamento.name() : __DataScadenzaPagamento,
        __ImportoPagamento.name() : __ImportoPagamento,
        __CodUfficioPostale.name() : __CodUfficioPostale,
        __CognomeQuietanzante.name() : __CognomeQuietanzante,
        __NomeQuietanzante.name() : __NomeQuietanzante,
        __CFQuietanzante.name() : __CFQuietanzante,
        __TitoloQuietanzante.name() : __TitoloQuietanzante,
        __IstitutoFinanziario.name() : __IstitutoFinanziario,
        __IBAN.name() : __IBAN,
        __ABI.name() : __ABI,
        __CAB.name() : __CAB,
        __BIC.name() : __BIC,
        __ScontoPagamentoAnticipato.name() : __ScontoPagamentoAnticipato,
        __DataLimitePagamentoAnticipato.name() : __DataLimitePagamentoAnticipato,
        __PenalitaPagamentiRitardati.name() : __PenalitaPagamentiRitardati,
        __DataDecorrenzaPenale.name() : __DataDecorrenzaPenale,
        __CodicePagamento.name() : __CodicePagamento
    })
    _AttributeMap.update({

    })
_module_typeBindings.DettaglioPagamentoType = DettaglioPagamentoType
Namespace.addCategoryObject('typeBinding', 'DettaglioPagamentoType', DettaglioPagamentoType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}TerzoIntermediarioSoggettoEmittenteType with content type ELEMENT_ONLY
class TerzoIntermediarioSoggettoEmittenteType (pyxb.binding.basis.complexTypeDefinition):
    """Blocco relativo ai dati del Terzo Intermediario che emette fattura elettronica per conto del Cedente/Prestatore"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TerzoIntermediarioSoggettoEmittenteType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 956, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element DatiAnagrafici uses Python identifier DatiAnagrafici
    __DatiAnagrafici = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DatiAnagrafici'), 'DatiAnagrafici', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_TerzoIntermediarioSoggettoEmittenteType_DatiAnagrafici', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 961, 6), )


    DatiAnagrafici = property(__DatiAnagrafici.value, __DatiAnagrafici.set, None, None)

    _ElementMap.update({
        __DatiAnagrafici.name() : __DatiAnagrafici
    })
    _AttributeMap.update({

    })
_module_typeBindings.TerzoIntermediarioSoggettoEmittenteType = TerzoIntermediarioSoggettoEmittenteType
Namespace.addCategoryObject('typeBinding', 'TerzoIntermediarioSoggettoEmittenteType', TerzoIntermediarioSoggettoEmittenteType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiAnagraficiTerzoIntermediarioType with content type ELEMENT_ONLY
class DatiAnagraficiTerzoIntermediarioType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiAnagraficiTerzoIntermediarioType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiAnagraficiTerzoIntermediarioType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 964, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element IdFiscaleIVA uses Python identifier IdFiscaleIVA
    __IdFiscaleIVA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'IdFiscaleIVA'), 'IdFiscaleIVA', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiTerzoIntermediarioType_IdFiscaleIVA', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 966, 6), )


    IdFiscaleIVA = property(__IdFiscaleIVA.value, __IdFiscaleIVA.set, None, None)


    # Element CodiceFiscale uses Python identifier CodiceFiscale
    __CodiceFiscale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CodiceFiscale'), 'CodiceFiscale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiTerzoIntermediarioType_CodiceFiscale', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 967, 6), )


    CodiceFiscale = property(__CodiceFiscale.value, __CodiceFiscale.set, None, None)


    # Element Anagrafica uses Python identifier Anagrafica
    __Anagrafica = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Anagrafica'), 'Anagrafica', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiAnagraficiTerzoIntermediarioType_Anagrafica', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 968, 6), )


    Anagrafica = property(__Anagrafica.value, __Anagrafica.set, None, None)

    _ElementMap.update({
        __IdFiscaleIVA.name() : __IdFiscaleIVA,
        __CodiceFiscale.name() : __CodiceFiscale,
        __Anagrafica.name() : __Anagrafica
    })
    _AttributeMap.update({

    })
_module_typeBindings.DatiAnagraficiTerzoIntermediarioType = DatiAnagraficiTerzoIntermediarioType
Namespace.addCategoryObject('typeBinding', 'DatiAnagraficiTerzoIntermediarioType', DatiAnagraficiTerzoIntermediarioType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}AllegatiType with content type ELEMENT_ONLY
class AllegatiType (pyxb.binding.basis.complexTypeDefinition):
    """Blocco relativo ai dati di eventuali allegati"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AllegatiType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 971, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element NomeAttachment uses Python identifier NomeAttachment
    __NomeAttachment = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'NomeAttachment'), 'NomeAttachment', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_AllegatiType_NomeAttachment', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 976, 6), )


    NomeAttachment = property(__NomeAttachment.value, __NomeAttachment.set, None, None)


    # Element AlgoritmoCompressione uses Python identifier AlgoritmoCompressione
    __AlgoritmoCompressione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'AlgoritmoCompressione'), 'AlgoritmoCompressione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_AllegatiType_AlgoritmoCompressione', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 977, 6), )


    AlgoritmoCompressione = property(__AlgoritmoCompressione.value, __AlgoritmoCompressione.set, None, None)


    # Element FormatoAttachment uses Python identifier FormatoAttachment
    __FormatoAttachment = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'FormatoAttachment'), 'FormatoAttachment', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_AllegatiType_FormatoAttachment', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 978, 6), )


    FormatoAttachment = property(__FormatoAttachment.value, __FormatoAttachment.set, None, None)


    # Element DescrizioneAttachment uses Python identifier DescrizioneAttachment
    __DescrizioneAttachment = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DescrizioneAttachment'), 'DescrizioneAttachment', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_AllegatiType_DescrizioneAttachment', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 979, 6), )


    DescrizioneAttachment = property(__DescrizioneAttachment.value, __DescrizioneAttachment.set, None, None)


    # Element Attachment uses Python identifier Attachment
    __Attachment = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Attachment'), 'Attachment', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_AllegatiType_Attachment', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 980, 6), )


    Attachment = property(__Attachment.value, __Attachment.set, None, None)

    _ElementMap.update({
        __NomeAttachment.name() : __NomeAttachment,
        __AlgoritmoCompressione.name() : __AlgoritmoCompressione,
        __FormatoAttachment.name() : __FormatoAttachment,
        __DescrizioneAttachment.name() : __DescrizioneAttachment,
        __Attachment.name() : __Attachment
    })
    _AttributeMap.update({

    })
_module_typeBindings.AllegatiType = AllegatiType
Namespace.addCategoryObject('typeBinding', 'AllegatiType', AllegatiType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DettaglioLineeType with content type ELEMENT_ONLY
class DettaglioLineeType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DettaglioLineeType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DettaglioLineeType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 983, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element NumeroLinea uses Python identifier NumeroLinea
    __NumeroLinea = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'NumeroLinea'), 'NumeroLinea', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioLineeType_NumeroLinea', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 985, 6), )


    NumeroLinea = property(__NumeroLinea.value, __NumeroLinea.set, None, None)


    # Element TipoCessionePrestazione uses Python identifier TipoCessionePrestazione
    __TipoCessionePrestazione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'TipoCessionePrestazione'), 'TipoCessionePrestazione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioLineeType_TipoCessionePrestazione', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 986, 6), )


    TipoCessionePrestazione = property(__TipoCessionePrestazione.value, __TipoCessionePrestazione.set, None, None)


    # Element CodiceArticolo uses Python identifier CodiceArticolo
    __CodiceArticolo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CodiceArticolo'), 'CodiceArticolo', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioLineeType_CodiceArticolo', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 987, 6), )


    CodiceArticolo = property(__CodiceArticolo.value, __CodiceArticolo.set, None, None)


    # Element Descrizione uses Python identifier Descrizione
    __Descrizione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Descrizione'), 'Descrizione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioLineeType_Descrizione', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 988, 6), )


    Descrizione = property(__Descrizione.value, __Descrizione.set, None, None)


    # Element Quantita uses Python identifier Quantita
    __Quantita = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Quantita'), 'Quantita', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioLineeType_Quantita', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 989, 6), )


    Quantita = property(__Quantita.value, __Quantita.set, None, None)


    # Element UnitaMisura uses Python identifier UnitaMisura
    __UnitaMisura = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'UnitaMisura'), 'UnitaMisura', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioLineeType_UnitaMisura', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 990, 6), )


    UnitaMisura = property(__UnitaMisura.value, __UnitaMisura.set, None, None)


    # Element DataInizioPeriodo uses Python identifier DataInizioPeriodo
    __DataInizioPeriodo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DataInizioPeriodo'), 'DataInizioPeriodo', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioLineeType_DataInizioPeriodo', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 991, 6), )


    DataInizioPeriodo = property(__DataInizioPeriodo.value, __DataInizioPeriodo.set, None, None)


    # Element DataFinePeriodo uses Python identifier DataFinePeriodo
    __DataFinePeriodo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'DataFinePeriodo'), 'DataFinePeriodo', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioLineeType_DataFinePeriodo', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 992, 6), )


    DataFinePeriodo = property(__DataFinePeriodo.value, __DataFinePeriodo.set, None, None)


    # Element PrezzoUnitario uses Python identifier PrezzoUnitario
    __PrezzoUnitario = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PrezzoUnitario'), 'PrezzoUnitario', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioLineeType_PrezzoUnitario', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 993, 6), )


    PrezzoUnitario = property(__PrezzoUnitario.value, __PrezzoUnitario.set, None, None)


    # Element ScontoMaggiorazione uses Python identifier ScontoMaggiorazione
    __ScontoMaggiorazione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ScontoMaggiorazione'), 'ScontoMaggiorazione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioLineeType_ScontoMaggiorazione', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 994, 6), )


    ScontoMaggiorazione = property(__ScontoMaggiorazione.value, __ScontoMaggiorazione.set, None, None)


    # Element PrezzoTotale uses Python identifier PrezzoTotale
    __PrezzoTotale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'PrezzoTotale'), 'PrezzoTotale', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioLineeType_PrezzoTotale', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 995, 6), )


    PrezzoTotale = property(__PrezzoTotale.value, __PrezzoTotale.set, None, None)


    # Element AliquotaIVA uses Python identifier AliquotaIVA
    __AliquotaIVA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'AliquotaIVA'), 'AliquotaIVA', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioLineeType_AliquotaIVA', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 996, 6), )


    AliquotaIVA = property(__AliquotaIVA.value, __AliquotaIVA.set, None, None)


    # Element Ritenuta uses Python identifier Ritenuta
    __Ritenuta = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Ritenuta'), 'Ritenuta', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioLineeType_Ritenuta', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 997, 6), )


    Ritenuta = property(__Ritenuta.value, __Ritenuta.set, None, None)


    # Element Natura uses Python identifier Natura
    __Natura = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Natura'), 'Natura', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioLineeType_Natura', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 998, 6), )


    Natura = property(__Natura.value, __Natura.set, None, None)


    # Element RiferimentoAmministrazione uses Python identifier RiferimentoAmministrazione
    __RiferimentoAmministrazione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RiferimentoAmministrazione'), 'RiferimentoAmministrazione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioLineeType_RiferimentoAmministrazione', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 999, 6), )


    RiferimentoAmministrazione = property(__RiferimentoAmministrazione.value, __RiferimentoAmministrazione.set, None, None)


    # Element AltriDatiGestionali uses Python identifier AltriDatiGestionali
    __AltriDatiGestionali = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'AltriDatiGestionali'), 'AltriDatiGestionali', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DettaglioLineeType_AltriDatiGestionali', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1000, 6), )


    AltriDatiGestionali = property(__AltriDatiGestionali.value, __AltriDatiGestionali.set, None, None)

    _ElementMap.update({
        __NumeroLinea.name() : __NumeroLinea,
        __TipoCessionePrestazione.name() : __TipoCessionePrestazione,
        __CodiceArticolo.name() : __CodiceArticolo,
        __Descrizione.name() : __Descrizione,
        __Quantita.name() : __Quantita,
        __UnitaMisura.name() : __UnitaMisura,
        __DataInizioPeriodo.name() : __DataInizioPeriodo,
        __DataFinePeriodo.name() : __DataFinePeriodo,
        __PrezzoUnitario.name() : __PrezzoUnitario,
        __ScontoMaggiorazione.name() : __ScontoMaggiorazione,
        __PrezzoTotale.name() : __PrezzoTotale,
        __AliquotaIVA.name() : __AliquotaIVA,
        __Ritenuta.name() : __Ritenuta,
        __Natura.name() : __Natura,
        __RiferimentoAmministrazione.name() : __RiferimentoAmministrazione,
        __AltriDatiGestionali.name() : __AltriDatiGestionali
    })
    _AttributeMap.update({

    })
_module_typeBindings.DettaglioLineeType = DettaglioLineeType
Namespace.addCategoryObject('typeBinding', 'DettaglioLineeType', DettaglioLineeType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}CodiceArticoloType with content type ELEMENT_ONLY
class CodiceArticoloType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}CodiceArticoloType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CodiceArticoloType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1003, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element CodiceTipo uses Python identifier CodiceTipo
    __CodiceTipo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CodiceTipo'), 'CodiceTipo', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_CodiceArticoloType_CodiceTipo', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1005, 6), )


    CodiceTipo = property(__CodiceTipo.value, __CodiceTipo.set, None, None)


    # Element CodiceValore uses Python identifier CodiceValore
    __CodiceValore = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'CodiceValore'), 'CodiceValore', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_CodiceArticoloType_CodiceValore', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1006, 6), )


    CodiceValore = property(__CodiceValore.value, __CodiceValore.set, None, None)

    _ElementMap.update({
        __CodiceTipo.name() : __CodiceTipo,
        __CodiceValore.name() : __CodiceValore
    })
    _AttributeMap.update({

    })
_module_typeBindings.CodiceArticoloType = CodiceArticoloType
Namespace.addCategoryObject('typeBinding', 'CodiceArticoloType', CodiceArticoloType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}AltriDatiGestionaliType with content type ELEMENT_ONLY
class AltriDatiGestionaliType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}AltriDatiGestionaliType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'AltriDatiGestionaliType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1009, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element TipoDato uses Python identifier TipoDato
    __TipoDato = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'TipoDato'), 'TipoDato', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_AltriDatiGestionaliType_TipoDato', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1011, 6), )


    TipoDato = property(__TipoDato.value, __TipoDato.set, None, None)


    # Element RiferimentoTesto uses Python identifier RiferimentoTesto
    __RiferimentoTesto = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RiferimentoTesto'), 'RiferimentoTesto', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_AltriDatiGestionaliType_RiferimentoTesto', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1012, 6), )


    RiferimentoTesto = property(__RiferimentoTesto.value, __RiferimentoTesto.set, None, None)


    # Element RiferimentoNumero uses Python identifier RiferimentoNumero
    __RiferimentoNumero = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RiferimentoNumero'), 'RiferimentoNumero', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_AltriDatiGestionaliType_RiferimentoNumero', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1013, 6), )


    RiferimentoNumero = property(__RiferimentoNumero.value, __RiferimentoNumero.set, None, None)


    # Element RiferimentoData uses Python identifier RiferimentoData
    __RiferimentoData = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RiferimentoData'), 'RiferimentoData', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_AltriDatiGestionaliType_RiferimentoData', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1014, 6), )


    RiferimentoData = property(__RiferimentoData.value, __RiferimentoData.set, None, None)

    _ElementMap.update({
        __TipoDato.name() : __TipoDato,
        __RiferimentoTesto.name() : __RiferimentoTesto,
        __RiferimentoNumero.name() : __RiferimentoNumero,
        __RiferimentoData.name() : __RiferimentoData
    })
    _AttributeMap.update({

    })
_module_typeBindings.AltriDatiGestionaliType = AltriDatiGestionaliType
Namespace.addCategoryObject('typeBinding', 'AltriDatiGestionaliType', AltriDatiGestionaliType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiRiepilogoType with content type ELEMENT_ONLY
class DatiRiepilogoType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}DatiRiepilogoType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiRiepilogoType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1027, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element AliquotaIVA uses Python identifier AliquotaIVA
    __AliquotaIVA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'AliquotaIVA'), 'AliquotaIVA', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiRiepilogoType_AliquotaIVA', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1029, 6), )


    AliquotaIVA = property(__AliquotaIVA.value, __AliquotaIVA.set, None, None)


    # Element Natura uses Python identifier Natura
    __Natura = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Natura'), 'Natura', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiRiepilogoType_Natura', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1030, 6), )


    Natura = property(__Natura.value, __Natura.set, None, None)


    # Element SpeseAccessorie uses Python identifier SpeseAccessorie
    __SpeseAccessorie = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'SpeseAccessorie'), 'SpeseAccessorie', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiRiepilogoType_SpeseAccessorie', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1031, 6), )


    SpeseAccessorie = property(__SpeseAccessorie.value, __SpeseAccessorie.set, None, None)


    # Element Arrotondamento uses Python identifier Arrotondamento
    __Arrotondamento = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Arrotondamento'), 'Arrotondamento', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiRiepilogoType_Arrotondamento', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1032, 6), )


    Arrotondamento = property(__Arrotondamento.value, __Arrotondamento.set, None, None)


    # Element ImponibileImporto uses Python identifier ImponibileImporto
    __ImponibileImporto = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ImponibileImporto'), 'ImponibileImporto', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiRiepilogoType_ImponibileImporto', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1033, 6), )


    ImponibileImporto = property(__ImponibileImporto.value, __ImponibileImporto.set, None, None)


    # Element Imposta uses Python identifier Imposta
    __Imposta = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'Imposta'), 'Imposta', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiRiepilogoType_Imposta', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1034, 6), )


    Imposta = property(__Imposta.value, __Imposta.set, None, None)


    # Element EsigibilitaIVA uses Python identifier EsigibilitaIVA
    __EsigibilitaIVA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'EsigibilitaIVA'), 'EsigibilitaIVA', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiRiepilogoType_EsigibilitaIVA', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1035, 6), )


    EsigibilitaIVA = property(__EsigibilitaIVA.value, __EsigibilitaIVA.set, None, None)


    # Element RiferimentoNormativo uses Python identifier RiferimentoNormativo
    __RiferimentoNormativo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'RiferimentoNormativo'), 'RiferimentoNormativo', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_DatiRiepilogoType_RiferimentoNormativo', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1036, 6), )


    RiferimentoNormativo = property(__RiferimentoNormativo.value, __RiferimentoNormativo.set, None, None)

    _ElementMap.update({
        __AliquotaIVA.name() : __AliquotaIVA,
        __Natura.name() : __Natura,
        __SpeseAccessorie.name() : __SpeseAccessorie,
        __Arrotondamento.name() : __Arrotondamento,
        __ImponibileImporto.name() : __ImponibileImporto,
        __Imposta.name() : __Imposta,
        __EsigibilitaIVA.name() : __EsigibilitaIVA,
        __RiferimentoNormativo.name() : __RiferimentoNormativo
    })
    _AttributeMap.update({

    })
_module_typeBindings.DatiRiepilogoType = DatiRiepilogoType
Namespace.addCategoryObject('typeBinding', 'DatiRiepilogoType', DatiRiepilogoType)


# Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}FatturaElettronicaType with content type ELEMENT_ONLY
class FatturaElettronicaType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2}FatturaElettronicaType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FatturaElettronicaType')
    _XSDLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 16, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType

    # Element FatturaElettronicaHeader uses Python identifier FatturaElettronicaHeader
    __FatturaElettronicaHeader = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'FatturaElettronicaHeader'), 'FatturaElettronicaHeader', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_FatturaElettronicaType_FatturaElettronicaHeader', False, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 18, 6), )


    FatturaElettronicaHeader = property(__FatturaElettronicaHeader.value, __FatturaElettronicaHeader.set, None, None)


    # Element FatturaElettronicaBody uses Python identifier FatturaElettronicaBody
    __FatturaElettronicaBody = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'FatturaElettronicaBody'), 'FatturaElettronicaBody', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_FatturaElettronicaType_FatturaElettronicaBody', True, pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 19, 6), )


    FatturaElettronicaBody = property(__FatturaElettronicaBody.value, __FatturaElettronicaBody.set, None, None)


    # Element {http://www.w3.org/2000/09/xmldsig#}Signature uses Python identifier Signature
    __Signature = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_ds, 'Signature'), 'Signature', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_FatturaElettronicaType_httpwww_w3_org200009xmldsigSignature', False, pyxb.utils.utility.Location('http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd', 43, 0), )


    Signature = property(__Signature.value, __Signature.set, None, None)


    # Attribute versione uses Python identifier versione
    __versione = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'versione'), 'versione', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_FatturaElettronicaType_versione', _module_typeBindings.FormatoTrasmissioneType, required=True)
    __versione._DeclarationLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 22, 4)
    __versione._UseLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 22, 4)

    versione = property(__versione.value, __versione.set, None, None)


    # Attribute SistemaEmittente uses Python identifier SistemaEmittente
    __SistemaEmittente = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'SistemaEmittente'), 'SistemaEmittente', '__httpivaservizi_agenziaentrate_gov_itdocsxsdfatturev1_2_FatturaElettronicaType_SistemaEmittente', _module_typeBindings.String10Type)
    __SistemaEmittente._DeclarationLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 23, 4)
    __SistemaEmittente._UseLocation = pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 23, 4)

    SistemaEmittente = property(__SistemaEmittente.value, __SistemaEmittente.set, None, None)

    _ElementMap.update({
        __FatturaElettronicaHeader.name() : __FatturaElettronicaHeader,
        __FatturaElettronicaBody.name() : __FatturaElettronicaBody,
        __Signature.name() : __Signature
    })
    _AttributeMap.update({
        __versione.name() : __versione,
        __SistemaEmittente.name() : __SistemaEmittente
    })
_module_typeBindings.FatturaElettronicaType = FatturaElettronicaType
Namespace.addCategoryObject('typeBinding', 'FatturaElettronicaType', FatturaElettronicaType)


FatturaElettronica = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FatturaElettronica'), FatturaElettronicaType, documentation='XML schema fatture destinate a PA e privati in forma ordinaria 1.2.1', location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 10, 2))
Namespace.addCategoryObject('elementBinding', FatturaElettronica.name().localName(), FatturaElettronica)



FatturaElettronicaHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiTrasmissione'), DatiTrasmissioneType, scope=FatturaElettronicaHeaderType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 27, 6)))

FatturaElettronicaHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CedentePrestatore'), CedentePrestatoreType, scope=FatturaElettronicaHeaderType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 28, 6)))

FatturaElettronicaHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RappresentanteFiscale'), RappresentanteFiscaleType, scope=FatturaElettronicaHeaderType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 29, 6)))

FatturaElettronicaHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CessionarioCommittente'), CessionarioCommittenteType, scope=FatturaElettronicaHeaderType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 30, 6)))

FatturaElettronicaHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'TerzoIntermediarioOSoggettoEmittente'), TerzoIntermediarioSoggettoEmittenteType, scope=FatturaElettronicaHeaderType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 31, 6)))

FatturaElettronicaHeaderType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SoggettoEmittente'), SoggettoEmittenteType, scope=FatturaElettronicaHeaderType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 32, 6)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 29, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 31, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 32, 6))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(FatturaElettronicaHeaderType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiTrasmissione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 27, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(FatturaElettronicaHeaderType._UseForTag(pyxb.namespace.ExpandedName(None, 'CedentePrestatore')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 28, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(FatturaElettronicaHeaderType._UseForTag(pyxb.namespace.ExpandedName(None, 'RappresentanteFiscale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 29, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(FatturaElettronicaHeaderType._UseForTag(pyxb.namespace.ExpandedName(None, 'CessionarioCommittente')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 30, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(FatturaElettronicaHeaderType._UseForTag(pyxb.namespace.ExpandedName(None, 'TerzoIntermediarioOSoggettoEmittente')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 31, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(FatturaElettronicaHeaderType._UseForTag(pyxb.namespace.ExpandedName(None, 'SoggettoEmittente')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 32, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
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
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
FatturaElettronicaHeaderType._Automaton = _BuildAutomaton()




FatturaElettronicaBodyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiGenerali'), DatiGeneraliType, scope=FatturaElettronicaBodyType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 37, 6)))

FatturaElettronicaBodyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiBeniServizi'), DatiBeniServiziType, scope=FatturaElettronicaBodyType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 38, 6)))

FatturaElettronicaBodyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiVeicoli'), DatiVeicoliType, scope=FatturaElettronicaBodyType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 39, 6)))

FatturaElettronicaBodyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiPagamento'), DatiPagamentoType, scope=FatturaElettronicaBodyType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 40, 6)))

FatturaElettronicaBodyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Allegati'), AllegatiType, scope=FatturaElettronicaBodyType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 41, 6)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 39, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 40, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 41, 6))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(FatturaElettronicaBodyType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiGenerali')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 37, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(FatturaElettronicaBodyType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiBeniServizi')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 38, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FatturaElettronicaBodyType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiVeicoli')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 39, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(FatturaElettronicaBodyType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiPagamento')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 40, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(FatturaElettronicaBodyType._UseForTag(pyxb.namespace.ExpandedName(None, 'Allegati')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 41, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
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
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
FatturaElettronicaBodyType._Automaton = _BuildAutomaton_()




DatiTrasmissioneType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IdTrasmittente'), IdFiscaleType, scope=DatiTrasmissioneType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 49, 6)))

DatiTrasmissioneType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ProgressivoInvio'), String10Type, scope=DatiTrasmissioneType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 50, 6)))

DatiTrasmissioneType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'FormatoTrasmissione'), FormatoTrasmissioneType, scope=DatiTrasmissioneType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 51, 6)))

DatiTrasmissioneType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CodiceDestinatario'), CodiceDestinatarioType, scope=DatiTrasmissioneType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 52, 6)))

DatiTrasmissioneType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ContattiTrasmittente'), ContattiTrasmittenteType, scope=DatiTrasmissioneType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 53, 6)))

DatiTrasmissioneType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PECDestinatario'), EmailType, scope=DatiTrasmissioneType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 54, 6)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 53, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 54, 6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiTrasmissioneType._UseForTag(pyxb.namespace.ExpandedName(None, 'IdTrasmittente')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 49, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiTrasmissioneType._UseForTag(pyxb.namespace.ExpandedName(None, 'ProgressivoInvio')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 50, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiTrasmissioneType._UseForTag(pyxb.namespace.ExpandedName(None, 'FormatoTrasmissione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 51, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DatiTrasmissioneType._UseForTag(pyxb.namespace.ExpandedName(None, 'CodiceDestinatario')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 52, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(DatiTrasmissioneType._UseForTag(pyxb.namespace.ExpandedName(None, 'ContattiTrasmittente')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 53, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(DatiTrasmissioneType._UseForTag(pyxb.namespace.ExpandedName(None, 'PECDestinatario')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 54, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiTrasmissioneType._Automaton = _BuildAutomaton_2()




IdFiscaleType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IdPaese'), NazioneType, scope=IdFiscaleType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 64, 6)))

IdFiscaleType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IdCodice'), CodiceType, scope=IdFiscaleType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 65, 6)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(IdFiscaleType._UseForTag(pyxb.namespace.ExpandedName(None, 'IdPaese')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 64, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(IdFiscaleType._UseForTag(pyxb.namespace.ExpandedName(None, 'IdCodice')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 65, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
IdFiscaleType._Automaton = _BuildAutomaton_3()




ContattiTrasmittenteType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Telefono'), TelFaxType, scope=ContattiTrasmittenteType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 91, 6)))

ContattiTrasmittenteType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Email'), EmailType, scope=ContattiTrasmittenteType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 92, 6)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 91, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 92, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ContattiTrasmittenteType._UseForTag(pyxb.namespace.ExpandedName(None, 'Telefono')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 91, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(ContattiTrasmittenteType._UseForTag(pyxb.namespace.ExpandedName(None, 'Email')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 92, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ContattiTrasmittenteType._Automaton = _BuildAutomaton_4()




DatiGeneraliType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiGeneraliDocumento'), DatiGeneraliDocumentoType, scope=DatiGeneraliType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 102, 6)))

DatiGeneraliType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiOrdineAcquisto'), DatiDocumentiCorrelatiType, scope=DatiGeneraliType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 103, 6)))

DatiGeneraliType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiContratto'), DatiDocumentiCorrelatiType, scope=DatiGeneraliType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 104, 6)))

DatiGeneraliType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiConvenzione'), DatiDocumentiCorrelatiType, scope=DatiGeneraliType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 105, 6)))

DatiGeneraliType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiRicezione'), DatiDocumentiCorrelatiType, scope=DatiGeneraliType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 106, 6)))

DatiGeneraliType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiFattureCollegate'), DatiDocumentiCorrelatiType, scope=DatiGeneraliType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 107, 6)))

DatiGeneraliType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiSAL'), DatiSALType, scope=DatiGeneraliType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 108, 6)))

DatiGeneraliType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiDDT'), DatiDDTType, scope=DatiGeneraliType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 109, 6)))

DatiGeneraliType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiTrasporto'), DatiTrasportoType, scope=DatiGeneraliType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 110, 6)))

DatiGeneraliType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'FatturaPrincipale'), FatturaPrincipaleType, scope=DatiGeneraliType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 111, 6)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 103, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 104, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 105, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 106, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 107, 6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 108, 6))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 109, 6))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 110, 6))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 111, 6))
    counters.add(cc_8)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiGeneraliDocumento')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 102, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiOrdineAcquisto')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 103, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiContratto')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 104, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiConvenzione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 105, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiRicezione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 106, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiFattureCollegate')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 107, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiSAL')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 108, 6))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiDDT')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 109, 6))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiTrasporto')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 110, 6))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliType._UseForTag(pyxb.namespace.ExpandedName(None, 'FatturaPrincipale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 111, 6))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
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
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, True) ]))
    st_9._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiGeneraliType._Automaton = _BuildAutomaton_5()




DatiGeneraliDocumentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'TipoDocumento'), TipoDocumentoType, scope=DatiGeneraliDocumentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 116, 6)))

DatiGeneraliDocumentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Divisa'), DivisaType, scope=DatiGeneraliDocumentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 117, 6)))

DatiGeneraliDocumentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Data'), DataFatturaType, scope=DatiGeneraliDocumentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 118, 6)))

DatiGeneraliDocumentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Numero'), String20Type, scope=DatiGeneraliDocumentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 119, 6)))

DatiGeneraliDocumentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiRitenuta'), DatiRitenutaType, scope=DatiGeneraliDocumentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 120, 6)))

DatiGeneraliDocumentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiBollo'), DatiBolloType, scope=DatiGeneraliDocumentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 121, 6)))

DatiGeneraliDocumentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiCassaPrevidenziale'), DatiCassaPrevidenzialeType, scope=DatiGeneraliDocumentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 122, 6)))

DatiGeneraliDocumentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ScontoMaggiorazione'), ScontoMaggiorazioneType, scope=DatiGeneraliDocumentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 123, 6)))

DatiGeneraliDocumentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ImportoTotaleDocumento'), Amount2DecimalType, scope=DatiGeneraliDocumentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 124, 6)))

DatiGeneraliDocumentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Arrotondamento'), Amount2DecimalType, scope=DatiGeneraliDocumentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 125, 6)))

DatiGeneraliDocumentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Causale'), String200LatinType, scope=DatiGeneraliDocumentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 126, 6)))

DatiGeneraliDocumentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Art73'), Art73Type, scope=DatiGeneraliDocumentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 127, 6)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 120, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 121, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 122, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 123, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 124, 6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 125, 6))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 126, 6))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 127, 6))
    counters.add(cc_7)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliDocumentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'TipoDocumento')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 116, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliDocumentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'Divisa')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 117, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliDocumentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'Data')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 118, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliDocumentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'Numero')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 119, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliDocumentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiRitenuta')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 120, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliDocumentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiBollo')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 121, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliDocumentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiCassaPrevidenziale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 122, 6))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliDocumentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'ScontoMaggiorazione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 123, 6))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliDocumentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'ImportoTotaleDocumento')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 124, 6))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliDocumentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'Arrotondamento')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 125, 6))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliDocumentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'Causale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 126, 6))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(DatiGeneraliDocumentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'Art73')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 127, 6))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
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
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, True) ]))
    st_11._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiGeneraliDocumentoType._Automaton = _BuildAutomaton_6()




DatiRitenutaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'TipoRitenuta'), TipoRitenutaType, scope=DatiRitenutaType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 132, 6)))

DatiRitenutaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ImportoRitenuta'), Amount2DecimalType, scope=DatiRitenutaType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 133, 6)))

DatiRitenutaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'AliquotaRitenuta'), RateType, scope=DatiRitenutaType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 134, 6)))

DatiRitenutaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CausalePagamento'), CausalePagamentoType, scope=DatiRitenutaType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 135, 6)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiRitenutaType._UseForTag(pyxb.namespace.ExpandedName(None, 'TipoRitenuta')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 132, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiRitenutaType._UseForTag(pyxb.namespace.ExpandedName(None, 'ImportoRitenuta')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 133, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiRitenutaType._UseForTag(pyxb.namespace.ExpandedName(None, 'AliquotaRitenuta')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 134, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DatiRitenutaType._UseForTag(pyxb.namespace.ExpandedName(None, 'CausalePagamento')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 135, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
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




DatiBolloType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'BolloVirtuale'), BolloVirtualeType, scope=DatiBolloType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 140, 6)))

DatiBolloType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ImportoBollo'), Amount2DecimalType, scope=DatiBolloType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 141, 6)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 141, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DatiBolloType._UseForTag(pyxb.namespace.ExpandedName(None, 'BolloVirtuale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 140, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(DatiBolloType._UseForTag(pyxb.namespace.ExpandedName(None, 'ImportoBollo')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 141, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiBolloType._Automaton = _BuildAutomaton_8()




DatiCassaPrevidenzialeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'TipoCassa'), TipoCassaType, scope=DatiCassaPrevidenzialeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 146, 6)))

DatiCassaPrevidenzialeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'AlCassa'), RateType, scope=DatiCassaPrevidenzialeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 147, 6)))

DatiCassaPrevidenzialeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ImportoContributoCassa'), Amount2DecimalType, scope=DatiCassaPrevidenzialeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 148, 6)))

DatiCassaPrevidenzialeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ImponibileCassa'), Amount2DecimalType, scope=DatiCassaPrevidenzialeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 149, 6)))

DatiCassaPrevidenzialeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'AliquotaIVA'), RateType, scope=DatiCassaPrevidenzialeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 150, 6)))

DatiCassaPrevidenzialeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Ritenuta'), RitenutaType, scope=DatiCassaPrevidenzialeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 151, 6)))

DatiCassaPrevidenzialeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Natura'), NaturaType, scope=DatiCassaPrevidenzialeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 152, 6)))

DatiCassaPrevidenzialeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RiferimentoAmministrazione'), String20Type, scope=DatiCassaPrevidenzialeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 153, 6)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 149, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 151, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 152, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 153, 6))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiCassaPrevidenzialeType._UseForTag(pyxb.namespace.ExpandedName(None, 'TipoCassa')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 146, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiCassaPrevidenzialeType._UseForTag(pyxb.namespace.ExpandedName(None, 'AlCassa')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 147, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiCassaPrevidenzialeType._UseForTag(pyxb.namespace.ExpandedName(None, 'ImportoContributoCassa')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 148, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiCassaPrevidenzialeType._UseForTag(pyxb.namespace.ExpandedName(None, 'ImponibileCassa')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 149, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DatiCassaPrevidenzialeType._UseForTag(pyxb.namespace.ExpandedName(None, 'AliquotaIVA')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 150, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(DatiCassaPrevidenzialeType._UseForTag(pyxb.namespace.ExpandedName(None, 'Ritenuta')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 151, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(DatiCassaPrevidenzialeType._UseForTag(pyxb.namespace.ExpandedName(None, 'Natura')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 152, 6))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(DatiCassaPrevidenzialeType._UseForTag(pyxb.namespace.ExpandedName(None, 'RiferimentoAmministrazione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 153, 6))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
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
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
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
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiCassaPrevidenzialeType._Automaton = _BuildAutomaton_9()




ScontoMaggiorazioneType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Tipo'), TipoScontoMaggiorazioneType, scope=ScontoMaggiorazioneType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 158, 6)))

ScontoMaggiorazioneType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Percentuale'), RateType, scope=ScontoMaggiorazioneType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 159, 6)))

ScontoMaggiorazioneType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Importo'), Amount8DecimalType, scope=ScontoMaggiorazioneType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 160, 6)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 159, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 160, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ScontoMaggiorazioneType._UseForTag(pyxb.namespace.ExpandedName(None, 'Tipo')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 158, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ScontoMaggiorazioneType._UseForTag(pyxb.namespace.ExpandedName(None, 'Percentuale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 159, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(ScontoMaggiorazioneType._UseForTag(pyxb.namespace.ExpandedName(None, 'Importo')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 160, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ScontoMaggiorazioneType._Automaton = _BuildAutomaton_10()




DatiSALType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RiferimentoFase'), RiferimentoFaseType, scope=DatiSALType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 468, 6)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DatiSALType._UseForTag(pyxb.namespace.ExpandedName(None, 'RiferimentoFase')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 468, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiSALType._Automaton = _BuildAutomaton_11()




DatiDocumentiCorrelatiType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RiferimentoNumeroLinea'), RiferimentoNumeroLineaType, scope=DatiDocumentiCorrelatiType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 473, 6)))

DatiDocumentiCorrelatiType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IdDocumento'), String20Type, scope=DatiDocumentiCorrelatiType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 474, 6)))

DatiDocumentiCorrelatiType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Data'), pyxb.binding.datatypes.date, scope=DatiDocumentiCorrelatiType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 475, 6)))

DatiDocumentiCorrelatiType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'NumItem'), String20Type, scope=DatiDocumentiCorrelatiType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 476, 6)))

DatiDocumentiCorrelatiType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CodiceCommessaConvenzione'), String100LatinType, scope=DatiDocumentiCorrelatiType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 477, 6)))

DatiDocumentiCorrelatiType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CodiceCUP'), String15Type, scope=DatiDocumentiCorrelatiType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 478, 6)))

DatiDocumentiCorrelatiType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CodiceCIG'), String15Type, scope=DatiDocumentiCorrelatiType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 479, 6)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 473, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 475, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 476, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 477, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 478, 6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 479, 6))
    counters.add(cc_5)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiDocumentiCorrelatiType._UseForTag(pyxb.namespace.ExpandedName(None, 'RiferimentoNumeroLinea')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 473, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DatiDocumentiCorrelatiType._UseForTag(pyxb.namespace.ExpandedName(None, 'IdDocumento')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 474, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(DatiDocumentiCorrelatiType._UseForTag(pyxb.namespace.ExpandedName(None, 'Data')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 475, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(DatiDocumentiCorrelatiType._UseForTag(pyxb.namespace.ExpandedName(None, 'NumItem')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 476, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(DatiDocumentiCorrelatiType._UseForTag(pyxb.namespace.ExpandedName(None, 'CodiceCommessaConvenzione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 477, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(DatiDocumentiCorrelatiType._UseForTag(pyxb.namespace.ExpandedName(None, 'CodiceCUP')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 478, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(DatiDocumentiCorrelatiType._UseForTag(pyxb.namespace.ExpandedName(None, 'CodiceCIG')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 479, 6))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
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
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiDocumentiCorrelatiType._Automaton = _BuildAutomaton_12()




DatiDDTType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'NumeroDDT'), String20Type, scope=DatiDDTType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 490, 6)))

DatiDDTType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DataDDT'), pyxb.binding.datatypes.date, scope=DatiDDTType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 491, 6)))

DatiDDTType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RiferimentoNumeroLinea'), RiferimentoNumeroLineaType, scope=DatiDDTType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 492, 6)))

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 492, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiDDTType._UseForTag(pyxb.namespace.ExpandedName(None, 'NumeroDDT')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 490, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DatiDDTType._UseForTag(pyxb.namespace.ExpandedName(None, 'DataDDT')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 491, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(DatiDDTType._UseForTag(pyxb.namespace.ExpandedName(None, 'RiferimentoNumeroLinea')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 492, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
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
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiDDTType._Automaton = _BuildAutomaton_13()




DatiTrasportoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiAnagraficiVettore'), DatiAnagraficiVettoreType, scope=DatiTrasportoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 497, 6)))

DatiTrasportoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'MezzoTrasporto'), String80LatinType, scope=DatiTrasportoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 498, 6)))

DatiTrasportoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CausaleTrasporto'), String100LatinType, scope=DatiTrasportoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 499, 6)))

DatiTrasportoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'NumeroColli'), NumeroColliType, scope=DatiTrasportoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 500, 6)))

DatiTrasportoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Descrizione'), String100LatinType, scope=DatiTrasportoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 501, 6)))

DatiTrasportoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'UnitaMisuraPeso'), String10Type, scope=DatiTrasportoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 502, 6)))

DatiTrasportoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PesoLordo'), PesoType, scope=DatiTrasportoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 503, 6)))

DatiTrasportoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PesoNetto'), PesoType, scope=DatiTrasportoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 504, 6)))

DatiTrasportoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DataOraRitiro'), pyxb.binding.datatypes.dateTime, scope=DatiTrasportoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 505, 6)))

DatiTrasportoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DataInizioTrasporto'), pyxb.binding.datatypes.date, scope=DatiTrasportoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 506, 6)))

DatiTrasportoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'TipoResa'), TipoResaType, scope=DatiTrasportoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 507, 6)))

DatiTrasportoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IndirizzoResa'), IndirizzoType, scope=DatiTrasportoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 508, 6)))

DatiTrasportoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DataOraConsegna'), pyxb.binding.datatypes.dateTime, scope=DatiTrasportoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 509, 6)))

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 497, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 498, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 499, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 500, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 501, 6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 502, 6))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 503, 6))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 504, 6))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 505, 6))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 506, 6))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 507, 6))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 508, 6))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 509, 6))
    counters.add(cc_12)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(DatiTrasportoType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiAnagraficiVettore')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 497, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(DatiTrasportoType._UseForTag(pyxb.namespace.ExpandedName(None, 'MezzoTrasporto')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 498, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(DatiTrasportoType._UseForTag(pyxb.namespace.ExpandedName(None, 'CausaleTrasporto')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 499, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(DatiTrasportoType._UseForTag(pyxb.namespace.ExpandedName(None, 'NumeroColli')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 500, 6))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(DatiTrasportoType._UseForTag(pyxb.namespace.ExpandedName(None, 'Descrizione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 501, 6))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(DatiTrasportoType._UseForTag(pyxb.namespace.ExpandedName(None, 'UnitaMisuraPeso')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 502, 6))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(DatiTrasportoType._UseForTag(pyxb.namespace.ExpandedName(None, 'PesoLordo')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 503, 6))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(DatiTrasportoType._UseForTag(pyxb.namespace.ExpandedName(None, 'PesoNetto')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 504, 6))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(DatiTrasportoType._UseForTag(pyxb.namespace.ExpandedName(None, 'DataOraRitiro')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 505, 6))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(DatiTrasportoType._UseForTag(pyxb.namespace.ExpandedName(None, 'DataInizioTrasporto')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 506, 6))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(DatiTrasportoType._UseForTag(pyxb.namespace.ExpandedName(None, 'TipoResa')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 507, 6))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(DatiTrasportoType._UseForTag(pyxb.namespace.ExpandedName(None, 'IndirizzoResa')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 508, 6))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(DatiTrasportoType._UseForTag(pyxb.namespace.ExpandedName(None, 'DataOraConsegna')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 509, 6))
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True) ]))
    st_12._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
DatiTrasportoType._Automaton = _BuildAutomaton_14()




IndirizzoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Indirizzo'), String60LatinType, scope=IndirizzoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 514, 6)))

IndirizzoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'NumeroCivico'), NumeroCivicoType, scope=IndirizzoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 515, 6)))

IndirizzoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CAP'), CAPType, scope=IndirizzoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 516, 6)))

IndirizzoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Comune'), String60LatinType, scope=IndirizzoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 517, 6)))

IndirizzoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Provincia'), ProvinciaType, scope=IndirizzoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 518, 6)))

IndirizzoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Nazione'), NazioneType, scope=IndirizzoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 519, 6), unicode_default='IT'))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 515, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 518, 6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(IndirizzoType._UseForTag(pyxb.namespace.ExpandedName(None, 'Indirizzo')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 514, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(IndirizzoType._UseForTag(pyxb.namespace.ExpandedName(None, 'NumeroCivico')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 515, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(IndirizzoType._UseForTag(pyxb.namespace.ExpandedName(None, 'CAP')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 516, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(IndirizzoType._UseForTag(pyxb.namespace.ExpandedName(None, 'Comune')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 517, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(IndirizzoType._UseForTag(pyxb.namespace.ExpandedName(None, 'Provincia')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 518, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(IndirizzoType._UseForTag(pyxb.namespace.ExpandedName(None, 'Nazione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 519, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
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
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
IndirizzoType._Automaton = _BuildAutomaton_15()




FatturaPrincipaleType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'NumeroFatturaPrincipale'), String20Type, scope=FatturaPrincipaleType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 524, 6)))

FatturaPrincipaleType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DataFatturaPrincipale'), pyxb.binding.datatypes.date, scope=FatturaPrincipaleType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 525, 6)))

def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(FatturaPrincipaleType._UseForTag(pyxb.namespace.ExpandedName(None, 'NumeroFatturaPrincipale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 524, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(FatturaPrincipaleType._UseForTag(pyxb.namespace.ExpandedName(None, 'DataFatturaPrincipale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 525, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
FatturaPrincipaleType._Automaton = _BuildAutomaton_16()




CedentePrestatoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiAnagrafici'), DatiAnagraficiCedenteType, scope=CedentePrestatoreType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 548, 6)))

CedentePrestatoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Sede'), IndirizzoType, scope=CedentePrestatoreType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 549, 6)))

CedentePrestatoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'StabileOrganizzazione'), IndirizzoType, scope=CedentePrestatoreType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 550, 6)))

CedentePrestatoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IscrizioneREA'), IscrizioneREAType, scope=CedentePrestatoreType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 551, 6)))

CedentePrestatoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Contatti'), ContattiType, scope=CedentePrestatoreType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 552, 6)))

CedentePrestatoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RiferimentoAmministrazione'), String20Type, scope=CedentePrestatoreType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 553, 6)))

def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 550, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 551, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 552, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 553, 6))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CedentePrestatoreType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiAnagrafici')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 548, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CedentePrestatoreType._UseForTag(pyxb.namespace.ExpandedName(None, 'Sede')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 549, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CedentePrestatoreType._UseForTag(pyxb.namespace.ExpandedName(None, 'StabileOrganizzazione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 550, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CedentePrestatoreType._UseForTag(pyxb.namespace.ExpandedName(None, 'IscrizioneREA')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 551, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CedentePrestatoreType._UseForTag(pyxb.namespace.ExpandedName(None, 'Contatti')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 552, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CedentePrestatoreType._UseForTag(pyxb.namespace.ExpandedName(None, 'RiferimentoAmministrazione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 553, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
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
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CedentePrestatoreType._Automaton = _BuildAutomaton_17()




DatiAnagraficiCedenteType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IdFiscaleIVA'), IdFiscaleType, scope=DatiAnagraficiCedenteType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 558, 6)))

DatiAnagraficiCedenteType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CodiceFiscale'), CodiceFiscaleType, scope=DatiAnagraficiCedenteType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 559, 6)))

DatiAnagraficiCedenteType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Anagrafica'), AnagraficaType, scope=DatiAnagraficiCedenteType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 560, 6)))

DatiAnagraficiCedenteType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'AlboProfessionale'), String60LatinType, scope=DatiAnagraficiCedenteType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 561, 6)))

DatiAnagraficiCedenteType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ProvinciaAlbo'), ProvinciaType, scope=DatiAnagraficiCedenteType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 562, 6)))

DatiAnagraficiCedenteType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'NumeroIscrizioneAlbo'), String60Type, scope=DatiAnagraficiCedenteType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 563, 6)))

DatiAnagraficiCedenteType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DataIscrizioneAlbo'), pyxb.binding.datatypes.date, scope=DatiAnagraficiCedenteType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 564, 6)))

DatiAnagraficiCedenteType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RegimeFiscale'), RegimeFiscaleType, scope=DatiAnagraficiCedenteType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 565, 6)))

def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 559, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 561, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 562, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 563, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 564, 6))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiCedenteType._UseForTag(pyxb.namespace.ExpandedName(None, 'IdFiscaleIVA')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 558, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiCedenteType._UseForTag(pyxb.namespace.ExpandedName(None, 'CodiceFiscale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 559, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiCedenteType._UseForTag(pyxb.namespace.ExpandedName(None, 'Anagrafica')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 560, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiCedenteType._UseForTag(pyxb.namespace.ExpandedName(None, 'AlboProfessionale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 561, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiCedenteType._UseForTag(pyxb.namespace.ExpandedName(None, 'ProvinciaAlbo')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 562, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiCedenteType._UseForTag(pyxb.namespace.ExpandedName(None, 'NumeroIscrizioneAlbo')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 563, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiCedenteType._UseForTag(pyxb.namespace.ExpandedName(None, 'DataIscrizioneAlbo')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 564, 6))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiCedenteType._UseForTag(pyxb.namespace.ExpandedName(None, 'RegimeFiscale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 565, 6))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
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
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiAnagraficiCedenteType._Automaton = _BuildAutomaton_18()




AnagraficaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Denominazione'), String80LatinType, scope=AnagraficaType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 670, 10)))

AnagraficaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Nome'), String60LatinType, scope=AnagraficaType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 673, 10)))

AnagraficaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Cognome'), String60LatinType, scope=AnagraficaType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 674, 10)))

AnagraficaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Titolo'), TitoloType, scope=AnagraficaType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 677, 6)))

AnagraficaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CodEORI'), CodEORIType, scope=AnagraficaType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 678, 6)))

def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 677, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 678, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AnagraficaType._UseForTag(pyxb.namespace.ExpandedName(None, 'Denominazione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 670, 10))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AnagraficaType._UseForTag(pyxb.namespace.ExpandedName(None, 'Nome')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 673, 10))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AnagraficaType._UseForTag(pyxb.namespace.ExpandedName(None, 'Cognome')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 674, 10))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(AnagraficaType._UseForTag(pyxb.namespace.ExpandedName(None, 'Titolo')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 677, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(AnagraficaType._UseForTag(pyxb.namespace.ExpandedName(None, 'CodEORI')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 678, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
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
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AnagraficaType._Automaton = _BuildAutomaton_19()




DatiAnagraficiVettoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IdFiscaleIVA'), IdFiscaleType, scope=DatiAnagraficiVettoreType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 683, 6)))

DatiAnagraficiVettoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CodiceFiscale'), CodiceFiscaleType, scope=DatiAnagraficiVettoreType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 684, 6)))

DatiAnagraficiVettoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Anagrafica'), AnagraficaType, scope=DatiAnagraficiVettoreType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 685, 6)))

DatiAnagraficiVettoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'NumeroLicenzaGuida'), String20Type, scope=DatiAnagraficiVettoreType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 686, 6)))

def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 684, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 686, 6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiVettoreType._UseForTag(pyxb.namespace.ExpandedName(None, 'IdFiscaleIVA')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 683, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiVettoreType._UseForTag(pyxb.namespace.ExpandedName(None, 'CodiceFiscale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 684, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiVettoreType._UseForTag(pyxb.namespace.ExpandedName(None, 'Anagrafica')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 685, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiVettoreType._UseForTag(pyxb.namespace.ExpandedName(None, 'NumeroLicenzaGuida')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 686, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiAnagraficiVettoreType._Automaton = _BuildAutomaton_20()




IscrizioneREAType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Ufficio'), ProvinciaType, scope=IscrizioneREAType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 691, 6)))

IscrizioneREAType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'NumeroREA'), String20Type, scope=IscrizioneREAType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 692, 6)))

IscrizioneREAType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CapitaleSociale'), Amount2DecimalType, scope=IscrizioneREAType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 693, 6)))

IscrizioneREAType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SocioUnico'), SocioUnicoType, scope=IscrizioneREAType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 694, 6)))

IscrizioneREAType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'StatoLiquidazione'), StatoLiquidazioneType, scope=IscrizioneREAType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 695, 6)))

def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 693, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 694, 6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(IscrizioneREAType._UseForTag(pyxb.namespace.ExpandedName(None, 'Ufficio')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 691, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(IscrizioneREAType._UseForTag(pyxb.namespace.ExpandedName(None, 'NumeroREA')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 692, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(IscrizioneREAType._UseForTag(pyxb.namespace.ExpandedName(None, 'CapitaleSociale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 693, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(IscrizioneREAType._UseForTag(pyxb.namespace.ExpandedName(None, 'SocioUnico')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 694, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(IscrizioneREAType._UseForTag(pyxb.namespace.ExpandedName(None, 'StatoLiquidazione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 695, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
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
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
IscrizioneREAType._Automaton = _BuildAutomaton_21()




ContattiType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Telefono'), TelFaxType, scope=ContattiType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 700, 6)))

ContattiType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Fax'), TelFaxType, scope=ContattiType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 701, 6)))

ContattiType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Email'), EmailType, scope=ContattiType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 702, 6)))

def _BuildAutomaton_22 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 700, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 701, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 702, 6))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ContattiType._UseForTag(pyxb.namespace.ExpandedName(None, 'Telefono')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 700, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(ContattiType._UseForTag(pyxb.namespace.ExpandedName(None, 'Fax')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 701, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(ContattiType._UseForTag(pyxb.namespace.ExpandedName(None, 'Email')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 702, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
ContattiType._Automaton = _BuildAutomaton_22()




RappresentanteFiscaleType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiAnagrafici'), DatiAnagraficiRappresentanteType, scope=RappresentanteFiscaleType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 710, 6)))

def _BuildAutomaton_23 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_23
    del _BuildAutomaton_23
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(RappresentanteFiscaleType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiAnagrafici')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 710, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
RappresentanteFiscaleType._Automaton = _BuildAutomaton_23()




DatiAnagraficiRappresentanteType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IdFiscaleIVA'), IdFiscaleType, scope=DatiAnagraficiRappresentanteType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 715, 6)))

DatiAnagraficiRappresentanteType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CodiceFiscale'), CodiceFiscaleType, scope=DatiAnagraficiRappresentanteType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 716, 6)))

DatiAnagraficiRappresentanteType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Anagrafica'), AnagraficaType, scope=DatiAnagraficiRappresentanteType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 717, 6)))

def _BuildAutomaton_24 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_24
    del _BuildAutomaton_24
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 716, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiRappresentanteType._UseForTag(pyxb.namespace.ExpandedName(None, 'IdFiscaleIVA')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 715, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiRappresentanteType._UseForTag(pyxb.namespace.ExpandedName(None, 'CodiceFiscale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 716, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiRappresentanteType._UseForTag(pyxb.namespace.ExpandedName(None, 'Anagrafica')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 717, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiAnagraficiRappresentanteType._Automaton = _BuildAutomaton_24()




CessionarioCommittenteType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiAnagrafici'), DatiAnagraficiCessionarioType, scope=CessionarioCommittenteType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 725, 6)))

CessionarioCommittenteType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Sede'), IndirizzoType, scope=CessionarioCommittenteType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 726, 6)))

CessionarioCommittenteType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'StabileOrganizzazione'), IndirizzoType, scope=CessionarioCommittenteType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 727, 3)))

CessionarioCommittenteType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RappresentanteFiscale'), RappresentanteFiscaleCessionarioType, scope=CessionarioCommittenteType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 728, 6)))

def _BuildAutomaton_25 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_25
    del _BuildAutomaton_25
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 727, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 728, 6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CessionarioCommittenteType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiAnagrafici')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 725, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CessionarioCommittenteType._UseForTag(pyxb.namespace.ExpandedName(None, 'Sede')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 726, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CessionarioCommittenteType._UseForTag(pyxb.namespace.ExpandedName(None, 'StabileOrganizzazione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 727, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CessionarioCommittenteType._UseForTag(pyxb.namespace.ExpandedName(None, 'RappresentanteFiscale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 728, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
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
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CessionarioCommittenteType._Automaton = _BuildAutomaton_25()




RappresentanteFiscaleCessionarioType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IdFiscaleIVA'), IdFiscaleType, scope=RappresentanteFiscaleCessionarioType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 733, 3)))

RappresentanteFiscaleCessionarioType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Denominazione'), String80LatinType, scope=RappresentanteFiscaleCessionarioType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 736, 10)))

RappresentanteFiscaleCessionarioType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Nome'), String60LatinType, scope=RappresentanteFiscaleCessionarioType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 739, 10)))

RappresentanteFiscaleCessionarioType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Cognome'), String60LatinType, scope=RappresentanteFiscaleCessionarioType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 740, 10)))

def _BuildAutomaton_26 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_26
    del _BuildAutomaton_26
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RappresentanteFiscaleCessionarioType._UseForTag(pyxb.namespace.ExpandedName(None, 'IdFiscaleIVA')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 733, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(RappresentanteFiscaleCessionarioType._UseForTag(pyxb.namespace.ExpandedName(None, 'Denominazione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 736, 10))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RappresentanteFiscaleCessionarioType._UseForTag(pyxb.namespace.ExpandedName(None, 'Nome')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 739, 10))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(RappresentanteFiscaleCessionarioType._UseForTag(pyxb.namespace.ExpandedName(None, 'Cognome')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 740, 10))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
RappresentanteFiscaleCessionarioType._Automaton = _BuildAutomaton_26()




DatiAnagraficiCessionarioType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IdFiscaleIVA'), IdFiscaleType, scope=DatiAnagraficiCessionarioType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 747, 6)))

DatiAnagraficiCessionarioType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CodiceFiscale'), CodiceFiscaleType, scope=DatiAnagraficiCessionarioType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 748, 6)))

DatiAnagraficiCessionarioType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Anagrafica'), AnagraficaType, scope=DatiAnagraficiCessionarioType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 749, 6)))

def _BuildAutomaton_27 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_27
    del _BuildAutomaton_27
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 747, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 748, 6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiCessionarioType._UseForTag(pyxb.namespace.ExpandedName(None, 'IdFiscaleIVA')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 747, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiCessionarioType._UseForTag(pyxb.namespace.ExpandedName(None, 'CodiceFiscale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 748, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiCessionarioType._UseForTag(pyxb.namespace.ExpandedName(None, 'Anagrafica')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 749, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiAnagraficiCessionarioType._Automaton = _BuildAutomaton_27()




DatiBeniServiziType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DettaglioLinee'), DettaglioLineeType, scope=DatiBeniServiziType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 757, 6)))

DatiBeniServiziType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiRiepilogo'), DatiRiepilogoType, scope=DatiBeniServiziType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 758, 6)))

def _BuildAutomaton_28 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_28
    del _BuildAutomaton_28
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiBeniServiziType._UseForTag(pyxb.namespace.ExpandedName(None, 'DettaglioLinee')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 757, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DatiBeniServiziType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiRiepilogo')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 758, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
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
DatiBeniServiziType._Automaton = _BuildAutomaton_28()




DatiVeicoliType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Data'), pyxb.binding.datatypes.date, scope=DatiVeicoliType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 767, 6)))

DatiVeicoliType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'TotalePercorso'), String15Type, scope=DatiVeicoliType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 768, 6)))

def _BuildAutomaton_29 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_29
    del _BuildAutomaton_29
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiVeicoliType._UseForTag(pyxb.namespace.ExpandedName(None, 'Data')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 767, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DatiVeicoliType._UseForTag(pyxb.namespace.ExpandedName(None, 'TotalePercorso')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 768, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiVeicoliType._Automaton = _BuildAutomaton_29()




DatiPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CondizioniPagamento'), CondizioniPagamentoType, scope=DatiPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 776, 6)))

DatiPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DettaglioPagamento'), DettaglioPagamentoType, scope=DatiPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 777, 6)))

def _BuildAutomaton_30 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_30
    del _BuildAutomaton_30
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'CondizioniPagamento')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 776, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DatiPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'DettaglioPagamento')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 777, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
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
DatiPagamentoType._Automaton = _BuildAutomaton_30()




DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Beneficiario'), String200LatinType, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 803, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ModalitaPagamento'), ModalitaPagamentoType, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 804, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DataRiferimentoTerminiPagamento'), pyxb.binding.datatypes.date, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 805, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'GiorniTerminiPagamento'), GiorniTerminePagamentoType, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 806, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DataScadenzaPagamento'), pyxb.binding.datatypes.date, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 807, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ImportoPagamento'), Amount2DecimalType, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 808, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CodUfficioPostale'), String20Type, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 809, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CognomeQuietanzante'), String60LatinType, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 810, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'NomeQuietanzante'), String60LatinType, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 811, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CFQuietanzante'), CodiceFiscalePFType, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 812, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'TitoloQuietanzante'), TitoloType, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 813, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IstitutoFinanziario'), String80LatinType, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 814, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IBAN'), IBANType, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 815, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ABI'), ABIType, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 816, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CAB'), CABType, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 817, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'BIC'), BICType, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 818, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ScontoPagamentoAnticipato'), Amount2DecimalType, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 819, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DataLimitePagamentoAnticipato'), pyxb.binding.datatypes.date, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 820, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PenalitaPagamentiRitardati'), Amount2DecimalType, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 821, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DataDecorrenzaPenale'), pyxb.binding.datatypes.date, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 822, 6)))

DettaglioPagamentoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CodicePagamento'), String60Type, scope=DettaglioPagamentoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 823, 6)))

def _BuildAutomaton_31 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_31
    del _BuildAutomaton_31
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 803, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 805, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 806, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 807, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 809, 6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 810, 6))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 811, 6))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 812, 6))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 813, 6))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 814, 6))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 815, 6))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 816, 6))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 817, 6))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 818, 6))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 819, 6))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 820, 6))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 821, 6))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 822, 6))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 823, 6))
    counters.add(cc_18)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'Beneficiario')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 803, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'ModalitaPagamento')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 804, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'DataRiferimentoTerminiPagamento')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 805, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'GiorniTerminiPagamento')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 806, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'DataScadenzaPagamento')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 807, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'ImportoPagamento')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 808, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'CodUfficioPostale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 809, 6))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'CognomeQuietanzante')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 810, 6))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'NomeQuietanzante')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 811, 6))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'CFQuietanzante')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 812, 6))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'TitoloQuietanzante')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 813, 6))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'IstitutoFinanziario')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 814, 6))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'IBAN')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 815, 6))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'ABI')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 816, 6))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'CAB')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 817, 6))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'BIC')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 818, 6))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'ScontoPagamentoAnticipato')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 819, 6))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'DataLimitePagamentoAnticipato')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 820, 6))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'PenalitaPagamentiRitardati')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 821, 6))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'DataDecorrenzaPenale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 822, 6))
    st_19 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_18, False))
    symbol = pyxb.binding.content.ElementUse(DettaglioPagamentoType._UseForTag(pyxb.namespace.ExpandedName(None, 'CodicePagamento')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 823, 6))
    st_20 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_20)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
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
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
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
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_14, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_15, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_15, False) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_16, True) ]))
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_16, False) ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
        fac.UpdateInstruction(cc_17, True) ]))
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_17, False) ]))
    st_19._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_20, [
        fac.UpdateInstruction(cc_18, True) ]))
    st_20._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DettaglioPagamentoType._Automaton = _BuildAutomaton_31()




TerzoIntermediarioSoggettoEmittenteType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DatiAnagrafici'), DatiAnagraficiTerzoIntermediarioType, scope=TerzoIntermediarioSoggettoEmittenteType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 961, 6)))

def _BuildAutomaton_32 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_32
    del _BuildAutomaton_32
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(TerzoIntermediarioSoggettoEmittenteType._UseForTag(pyxb.namespace.ExpandedName(None, 'DatiAnagrafici')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 961, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
TerzoIntermediarioSoggettoEmittenteType._Automaton = _BuildAutomaton_32()




DatiAnagraficiTerzoIntermediarioType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'IdFiscaleIVA'), IdFiscaleType, scope=DatiAnagraficiTerzoIntermediarioType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 966, 6)))

DatiAnagraficiTerzoIntermediarioType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CodiceFiscale'), CodiceFiscaleType, scope=DatiAnagraficiTerzoIntermediarioType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 967, 6)))

DatiAnagraficiTerzoIntermediarioType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Anagrafica'), AnagraficaType, scope=DatiAnagraficiTerzoIntermediarioType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 968, 6)))

def _BuildAutomaton_33 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_33
    del _BuildAutomaton_33
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 966, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 967, 6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiTerzoIntermediarioType._UseForTag(pyxb.namespace.ExpandedName(None, 'IdFiscaleIVA')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 966, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiTerzoIntermediarioType._UseForTag(pyxb.namespace.ExpandedName(None, 'CodiceFiscale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 967, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DatiAnagraficiTerzoIntermediarioType._UseForTag(pyxb.namespace.ExpandedName(None, 'Anagrafica')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 968, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiAnagraficiTerzoIntermediarioType._Automaton = _BuildAutomaton_33()




AllegatiType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'NomeAttachment'), String60LatinType, scope=AllegatiType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 976, 6)))

AllegatiType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'AlgoritmoCompressione'), String10Type, scope=AllegatiType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 977, 6)))

AllegatiType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'FormatoAttachment'), String10Type, scope=AllegatiType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 978, 6)))

AllegatiType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DescrizioneAttachment'), String100LatinType, scope=AllegatiType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 979, 6)))

AllegatiType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Attachment'), pyxb.binding.datatypes.base64Binary, scope=AllegatiType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 980, 6)))

def _BuildAutomaton_34 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_34
    del _BuildAutomaton_34
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 977, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 978, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 979, 6))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AllegatiType._UseForTag(pyxb.namespace.ExpandedName(None, 'NomeAttachment')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 976, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AllegatiType._UseForTag(pyxb.namespace.ExpandedName(None, 'AlgoritmoCompressione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 977, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AllegatiType._UseForTag(pyxb.namespace.ExpandedName(None, 'FormatoAttachment')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 978, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(AllegatiType._UseForTag(pyxb.namespace.ExpandedName(None, 'DescrizioneAttachment')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 979, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AllegatiType._UseForTag(pyxb.namespace.ExpandedName(None, 'Attachment')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 980, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
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
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AllegatiType._Automaton = _BuildAutomaton_34()




DettaglioLineeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'NumeroLinea'), NumeroLineaType, scope=DettaglioLineeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 985, 6)))

DettaglioLineeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'TipoCessionePrestazione'), TipoCessionePrestazioneType, scope=DettaglioLineeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 986, 6)))

DettaglioLineeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CodiceArticolo'), CodiceArticoloType, scope=DettaglioLineeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 987, 6)))

DettaglioLineeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Descrizione'), String1000LatinType, scope=DettaglioLineeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 988, 6)))

DettaglioLineeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Quantita'), QuantitaType, scope=DettaglioLineeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 989, 6)))

DettaglioLineeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'UnitaMisura'), String10Type, scope=DettaglioLineeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 990, 6)))

DettaglioLineeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DataInizioPeriodo'), pyxb.binding.datatypes.date, scope=DettaglioLineeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 991, 6)))

DettaglioLineeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'DataFinePeriodo'), pyxb.binding.datatypes.date, scope=DettaglioLineeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 992, 6)))

DettaglioLineeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PrezzoUnitario'), Amount8DecimalType, scope=DettaglioLineeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 993, 6)))

DettaglioLineeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ScontoMaggiorazione'), ScontoMaggiorazioneType, scope=DettaglioLineeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 994, 6)))

DettaglioLineeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'PrezzoTotale'), Amount8DecimalType, scope=DettaglioLineeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 995, 6)))

DettaglioLineeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'AliquotaIVA'), RateType, scope=DettaglioLineeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 996, 6)))

DettaglioLineeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Ritenuta'), RitenutaType, scope=DettaglioLineeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 997, 6)))

DettaglioLineeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Natura'), NaturaType, scope=DettaglioLineeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 998, 6)))

DettaglioLineeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RiferimentoAmministrazione'), String20Type, scope=DettaglioLineeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 999, 6)))

DettaglioLineeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'AltriDatiGestionali'), AltriDatiGestionaliType, scope=DettaglioLineeType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1000, 6)))

def _BuildAutomaton_35 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_35
    del _BuildAutomaton_35
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 986, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 987, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 989, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 990, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 991, 6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 992, 6))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 994, 6))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 997, 6))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 998, 6))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 999, 6))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1000, 6))
    counters.add(cc_10)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DettaglioLineeType._UseForTag(pyxb.namespace.ExpandedName(None, 'NumeroLinea')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 985, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DettaglioLineeType._UseForTag(pyxb.namespace.ExpandedName(None, 'TipoCessionePrestazione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 986, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DettaglioLineeType._UseForTag(pyxb.namespace.ExpandedName(None, 'CodiceArticolo')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 987, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DettaglioLineeType._UseForTag(pyxb.namespace.ExpandedName(None, 'Descrizione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 988, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DettaglioLineeType._UseForTag(pyxb.namespace.ExpandedName(None, 'Quantita')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 989, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DettaglioLineeType._UseForTag(pyxb.namespace.ExpandedName(None, 'UnitaMisura')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 990, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DettaglioLineeType._UseForTag(pyxb.namespace.ExpandedName(None, 'DataInizioPeriodo')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 991, 6))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DettaglioLineeType._UseForTag(pyxb.namespace.ExpandedName(None, 'DataFinePeriodo')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 992, 6))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DettaglioLineeType._UseForTag(pyxb.namespace.ExpandedName(None, 'PrezzoUnitario')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 993, 6))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DettaglioLineeType._UseForTag(pyxb.namespace.ExpandedName(None, 'ScontoMaggiorazione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 994, 6))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DettaglioLineeType._UseForTag(pyxb.namespace.ExpandedName(None, 'PrezzoTotale')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 995, 6))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DettaglioLineeType._UseForTag(pyxb.namespace.ExpandedName(None, 'AliquotaIVA')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 996, 6))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(DettaglioLineeType._UseForTag(pyxb.namespace.ExpandedName(None, 'Ritenuta')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 997, 6))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(DettaglioLineeType._UseForTag(pyxb.namespace.ExpandedName(None, 'Natura')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 998, 6))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(DettaglioLineeType._UseForTag(pyxb.namespace.ExpandedName(None, 'RiferimentoAmministrazione')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 999, 6))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(DettaglioLineeType._UseForTag(pyxb.namespace.ExpandedName(None, 'AltriDatiGestionali')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1000, 6))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
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
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
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
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
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
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, True) ]))
    st_15._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DettaglioLineeType._Automaton = _BuildAutomaton_35()




CodiceArticoloType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CodiceTipo'), String35Type, scope=CodiceArticoloType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1005, 6)))

CodiceArticoloType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'CodiceValore'), String35LatinExtType, scope=CodiceArticoloType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1006, 6)))

def _BuildAutomaton_36 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_36
    del _BuildAutomaton_36
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CodiceArticoloType._UseForTag(pyxb.namespace.ExpandedName(None, 'CodiceTipo')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1005, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CodiceArticoloType._UseForTag(pyxb.namespace.ExpandedName(None, 'CodiceValore')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1006, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CodiceArticoloType._Automaton = _BuildAutomaton_36()




AltriDatiGestionaliType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'TipoDato'), String10Type, scope=AltriDatiGestionaliType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1011, 6)))

AltriDatiGestionaliType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RiferimentoTesto'), String60LatinType, scope=AltriDatiGestionaliType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1012, 6)))

AltriDatiGestionaliType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RiferimentoNumero'), Amount8DecimalType, scope=AltriDatiGestionaliType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1013, 6)))

AltriDatiGestionaliType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RiferimentoData'), pyxb.binding.datatypes.date, scope=AltriDatiGestionaliType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1014, 6)))

def _BuildAutomaton_37 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_37
    del _BuildAutomaton_37
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1012, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1013, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1014, 6))
    counters.add(cc_2)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(AltriDatiGestionaliType._UseForTag(pyxb.namespace.ExpandedName(None, 'TipoDato')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1011, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(AltriDatiGestionaliType._UseForTag(pyxb.namespace.ExpandedName(None, 'RiferimentoTesto')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1012, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(AltriDatiGestionaliType._UseForTag(pyxb.namespace.ExpandedName(None, 'RiferimentoNumero')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1013, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(AltriDatiGestionaliType._UseForTag(pyxb.namespace.ExpandedName(None, 'RiferimentoData')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1014, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
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
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
AltriDatiGestionaliType._Automaton = _BuildAutomaton_37()




DatiRiepilogoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'AliquotaIVA'), RateType, scope=DatiRiepilogoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1029, 6)))

DatiRiepilogoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Natura'), NaturaType, scope=DatiRiepilogoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1030, 6)))

DatiRiepilogoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'SpeseAccessorie'), Amount2DecimalType, scope=DatiRiepilogoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1031, 6)))

DatiRiepilogoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Arrotondamento'), Amount8DecimalType, scope=DatiRiepilogoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1032, 6)))

DatiRiepilogoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ImponibileImporto'), Amount2DecimalType, scope=DatiRiepilogoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1033, 6)))

DatiRiepilogoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'Imposta'), Amount2DecimalType, scope=DatiRiepilogoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1034, 6)))

DatiRiepilogoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'EsigibilitaIVA'), EsigibilitaIVAType, scope=DatiRiepilogoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1035, 6)))

DatiRiepilogoType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'RiferimentoNormativo'), String100LatinType, scope=DatiRiepilogoType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1036, 6)))

def _BuildAutomaton_38 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_38
    del _BuildAutomaton_38
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1030, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1031, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1032, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1035, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1036, 6))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiRiepilogoType._UseForTag(pyxb.namespace.ExpandedName(None, 'AliquotaIVA')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1029, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiRiepilogoType._UseForTag(pyxb.namespace.ExpandedName(None, 'Natura')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1030, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiRiepilogoType._UseForTag(pyxb.namespace.ExpandedName(None, 'SpeseAccessorie')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1031, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiRiepilogoType._UseForTag(pyxb.namespace.ExpandedName(None, 'Arrotondamento')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1032, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(DatiRiepilogoType._UseForTag(pyxb.namespace.ExpandedName(None, 'ImponibileImporto')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1033, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(DatiRiepilogoType._UseForTag(pyxb.namespace.ExpandedName(None, 'Imposta')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1034, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(DatiRiepilogoType._UseForTag(pyxb.namespace.ExpandedName(None, 'EsigibilitaIVA')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1035, 6))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(DatiRiepilogoType._UseForTag(pyxb.namespace.ExpandedName(None, 'RiferimentoNormativo')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 1036, 6))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
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
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
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
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiRiepilogoType._Automaton = _BuildAutomaton_38()




FatturaElettronicaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'FatturaElettronicaHeader'), FatturaElettronicaHeaderType, scope=FatturaElettronicaType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 18, 6)))

FatturaElettronicaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'FatturaElettronicaBody'), FatturaElettronicaBodyType, scope=FatturaElettronicaType, location=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 19, 6)))

FatturaElettronicaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_ds, 'Signature'), _ImportedBinding__ds.SignatureType, scope=FatturaElettronicaType, location=pyxb.utils.utility.Location('http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd', 43, 0)))

def _BuildAutomaton_39 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_39
    del _BuildAutomaton_39
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 20, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(FatturaElettronicaType._UseForTag(pyxb.namespace.ExpandedName(None, 'FatturaElettronicaHeader')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 18, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(FatturaElettronicaType._UseForTag(pyxb.namespace.ExpandedName(None, 'FatturaElettronicaBody')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 19, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(FatturaElettronicaType._UseForTag(pyxb.namespace.ExpandedName(_Namespace_ds, 'Signature')), pyxb.utils.utility.Location('https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.3/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd', 20, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
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
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
FatturaElettronicaType._Automaton = _BuildAutomaton_39()

