# ./bindings/vat_settlement_v_1_0.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:4f059617657cbf045796906b94fd6da476500108
# Generated 2018-11-22 12:18:13.668082 by PyXB version 1.2.5 using Python 2.7.15.candidate.1
# Namespace urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp

from __future__ import unicode_literals
import logging
import io
import sys
_logger = logging.getLogger(__name__)
try:
    import pyxb
    import pyxb.binding
    import pyxb.binding.saxer
    import pyxb.utils.utility
    import pyxb.utils.domutils
    import pyxb.utils.six as _six
    # Import bindings for namespaces imported into schema
    import pyxb.binding.datatypes
except ImportError as err:
    _logger.debug(err)

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:4409401a-ee48-11e8-b673-b05adae3c683')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.5'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
# import _ds as _ImportedBinding__ds
import pyxb.binding.datatypes
import _cm as _ImportedBinding__cm
from openerp.addons.l10n_it_fatturapa.bindings import _ds as _ImportedBinding__ds

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp', create_if_missing=True)
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


# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}Eventi_Ecc_Type
class Eventi_Ecc_Type (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Eventi_Ecc_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 141, 1)
    _Documentation = None
Eventi_Ecc_Type._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=Eventi_Ecc_Type, enum_prefix=None)
Eventi_Ecc_Type.n1 = Eventi_Ecc_Type._CF_enumeration.addEnumeration(unicode_value='1', tag='n1')
Eventi_Ecc_Type.n9 = Eventi_Ecc_Type._CF_enumeration.addEnumeration(unicode_value='9', tag='n9')
Eventi_Ecc_Type._InitializeFacetMap(Eventi_Ecc_Type._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'Eventi_Ecc_Type', Eventi_Ecc_Type)
_module_typeBindings.Eventi_Ecc_Type = Eventi_Ecc_Type

# Atomic simple type: {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}DatoVN_Type
class DatoVN_Type (pyxb.binding.datatypes.string):

    """Tipo semplice che identifica numeri positivi con 2 cifre decimali. La lunghezza massima prevista è di 16 caratteri, il separatore decimale previsto è la virgola."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatoVN_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 147, 1)
    _Documentation = 'Tipo semplice che identifica numeri positivi con 2 cifre decimali. La lunghezza massima prevista \xe8 di 16 caratteri, il separatore decimale previsto \xe8 la virgola.'
DatoVN_Type._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(16))
DatoVN_Type._CF_pattern = pyxb.binding.facets.CF_pattern()
DatoVN_Type._CF_pattern.addPattern(pattern='[\\-]{0,1}[0-9]+,[0-9]{2}')
DatoVN_Type._InitializeFacetMap(DatoVN_Type._CF_maxLength,
   DatoVN_Type._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'DatoVN_Type', DatoVN_Type)
_module_typeBindings.DatoVN_Type = DatoVN_Type

# Atomic simple type: [anonymous]
class STD_ANON (_ImportedBinding__cm.DatoNP_Type, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 27, 4)
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.n1 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='1', tag='n1')
STD_ANON.n2 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='2', tag='n2')
STD_ANON.n3 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='3', tag='n3')
STD_ANON.n4 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='4', tag='n4')
STD_ANON.n5 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='5', tag='n5')
STD_ANON.n6 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='6', tag='n6')
STD_ANON.n7 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='7', tag='n7')
STD_ANON.n8 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='8', tag='n8')
STD_ANON.n9 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='9', tag='n9')
STD_ANON.n10 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='10', tag='n10')
STD_ANON.n11 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='11', tag='n11')
STD_ANON.n12 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='12', tag='n12')
STD_ANON.n13 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='13', tag='n13')
STD_ANON.n99 = STD_ANON._CF_enumeration.addEnumeration(unicode_value='99', tag='n99')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)
_module_typeBindings.STD_ANON = STD_ANON

# Atomic simple type: [anonymous]
class STD_ANON_ (_ImportedBinding__cm.DatoNP_Type, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 49, 4)
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.n1 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='1', tag='n1')
STD_ANON_.n2 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='2', tag='n2')
STD_ANON_.n3 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='3', tag='n3')
STD_ANON_.n4 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='4', tag='n4')
STD_ANON_.n5 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='5', tag='n5')
STD_ANON_.n6 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='6', tag='n6')
STD_ANON_.n7 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='7', tag='n7')
STD_ANON_.n8 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='8', tag='n8')
STD_ANON_.n9 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='9', tag='n9')
STD_ANON_.n11 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='11', tag='n11')
STD_ANON_.n12 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='12', tag='n12')
STD_ANON_.n13 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='13', tag='n13')
STD_ANON_.n14 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='14', tag='n14')
STD_ANON_.n15 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='15', tag='n15')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)
_module_typeBindings.STD_ANON_ = STD_ANON_

# Atomic simple type: [anonymous]
class STD_ANON_2 (_ImportedBinding__cm.DatoN1_Type, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 72, 4)
    _Documentation = None
STD_ANON_2._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_2, enum_prefix=None)
STD_ANON_2.n1 = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='1', tag='n1')
STD_ANON_2.n2 = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='2', tag='n2')
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_enumeration)
_module_typeBindings.STD_ANON_2 = STD_ANON_2

# Atomic simple type: [anonymous]
class STD_ANON_3 (_ImportedBinding__cm.DatoNP_Type, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 91, 7)
    _Documentation = None
STD_ANON_3._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_3, enum_prefix=None)
STD_ANON_3.n1 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='1', tag='n1')
STD_ANON_3.n2 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='2', tag='n2')
STD_ANON_3.n3 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='3', tag='n3')
STD_ANON_3.n4 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='4', tag='n4')
STD_ANON_3.n5 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='5', tag='n5')
STD_ANON_3.n6 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='6', tag='n6')
STD_ANON_3.n7 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='7', tag='n7')
STD_ANON_3.n8 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='8', tag='n8')
STD_ANON_3.n9 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='9', tag='n9')
STD_ANON_3.n10 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='10', tag='n10')
STD_ANON_3.n11 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='11', tag='n11')
STD_ANON_3.n12 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='12', tag='n12')
STD_ANON_3._InitializeFacetMap(STD_ANON_3._CF_enumeration)
_module_typeBindings.STD_ANON_3 = STD_ANON_3

# Atomic simple type: [anonymous]
class STD_ANON_4 (_ImportedBinding__cm.DatoN1_Type, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 109, 7)
    _Documentation = None
STD_ANON_4._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_4, enum_prefix=None)
STD_ANON_4.n1 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='1', tag='n1')
STD_ANON_4.n2 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='2', tag='n2')
STD_ANON_4.n3 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='3', tag='n3')
STD_ANON_4.n4 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='4', tag='n4')
STD_ANON_4.n5 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='5', tag='n5')
STD_ANON_4._InitializeFacetMap(STD_ANON_4._CF_enumeration)
_module_typeBindings.STD_ANON_4 = STD_ANON_4

# Atomic simple type: [anonymous]
class STD_ANON_5 (_ImportedBinding__cm.DatoAN_Type, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('../common/main/intestazioneIvp_2017_v1.xsd', 14, 4)
    _Documentation = None
STD_ANON_5._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_5, enum_prefix=None)
STD_ANON_5.IVP17 = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value='IVP17', tag='IVP17')
STD_ANON_5._InitializeFacetMap(STD_ANON_5._CF_enumeration)
_module_typeBindings.STD_ANON_5 = STD_ANON_5

# Atomic simple type: [anonymous]
class STD_ANON_6 (_ImportedBinding__cm.DatoNP_Type, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('../common/main/intestazioneIvp_2017_v1.xsd', 22, 4)
    _Documentation = None
STD_ANON_6._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_6, enum_prefix=None)
STD_ANON_6.n1 = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='1', tag='n1')
STD_ANON_6.n2 = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='2', tag='n2')
STD_ANON_6.n3 = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='3', tag='n3')
STD_ANON_6.n4 = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='4', tag='n4')
STD_ANON_6.n5 = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='5', tag='n5')
STD_ANON_6.n6 = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='6', tag='n6')
STD_ANON_6.n7 = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='7', tag='n7')
STD_ANON_6.n8 = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='8', tag='n8')
STD_ANON_6.n9 = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='9', tag='n9')
STD_ANON_6.n11 = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='11', tag='n11')
STD_ANON_6.n12 = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='12', tag='n12')
STD_ANON_6.n13 = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='13', tag='n13')
STD_ANON_6.n14 = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='14', tag='n14')
STD_ANON_6.n15 = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='15', tag='n15')
STD_ANON_6._InitializeFacetMap(STD_ANON_6._CF_enumeration)
_module_typeBindings.STD_ANON_6 = STD_ANON_6

# Complex type {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}Frontespizio_IVP_Type with content type ELEMENT_ONLY
class Frontespizio_IVP_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}Frontespizio_IVP_Type with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Frontespizio_IVP_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 20, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}CodiceFiscale uses Python identifier CodiceFiscale
    __CodiceFiscale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CodiceFiscale'), 'CodiceFiscale', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Frontespizio_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpCodiceFiscale', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 22, 3), )

    
    CodiceFiscale = property(__CodiceFiscale.value, __CodiceFiscale.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}AnnoImposta uses Python identifier AnnoImposta
    __AnnoImposta = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'AnnoImposta'), 'AnnoImposta', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Frontespizio_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpAnnoImposta', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 23, 3), )

    
    AnnoImposta = property(__AnnoImposta.value, __AnnoImposta.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}PartitaIVA uses Python identifier PartitaIVA
    __PartitaIVA = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PartitaIVA'), 'PartitaIVA', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Frontespizio_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpPartitaIVA', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 24, 3), )

    
    PartitaIVA = property(__PartitaIVA.value, __PartitaIVA.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}PIVAControllante uses Python identifier PIVAControllante
    __PIVAControllante = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'PIVAControllante'), 'PIVAControllante', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Frontespizio_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpPIVAControllante', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 25, 3), )

    
    PIVAControllante = property(__PIVAControllante.value, __PIVAControllante.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}UltimoMese uses Python identifier UltimoMese
    __UltimoMese = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'UltimoMese'), 'UltimoMese', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Frontespizio_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpUltimoMese', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 26, 3), )

    
    UltimoMese = property(__UltimoMese.value, __UltimoMese.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}LiquidazioneGruppo uses Python identifier LiquidazioneGruppo
    __LiquidazioneGruppo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'LiquidazioneGruppo'), 'LiquidazioneGruppo', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Frontespizio_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpLiquidazioneGruppo', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 46, 3), )

    
    LiquidazioneGruppo = property(__LiquidazioneGruppo.value, __LiquidazioneGruppo.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}CFDichiarante uses Python identifier CFDichiarante
    __CFDichiarante = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CFDichiarante'), 'CFDichiarante', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Frontespizio_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpCFDichiarante', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 47, 3), )

    
    CFDichiarante = property(__CFDichiarante.value, __CFDichiarante.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}CodiceCaricaDichiarante uses Python identifier CodiceCaricaDichiarante
    __CodiceCaricaDichiarante = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CodiceCaricaDichiarante'), 'CodiceCaricaDichiarante', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Frontespizio_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpCodiceCaricaDichiarante', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 48, 3), )

    
    CodiceCaricaDichiarante = property(__CodiceCaricaDichiarante.value, __CodiceCaricaDichiarante.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}CodiceFiscaleSocieta uses Python identifier CodiceFiscaleSocieta
    __CodiceFiscaleSocieta = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CodiceFiscaleSocieta'), 'CodiceFiscaleSocieta', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Frontespizio_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpCodiceFiscaleSocieta', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 68, 3), )

    
    CodiceFiscaleSocieta = property(__CodiceFiscaleSocieta.value, __CodiceFiscaleSocieta.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}FirmaDichiarazione uses Python identifier FirmaDichiarazione
    __FirmaDichiarazione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FirmaDichiarazione'), 'FirmaDichiarazione', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Frontespizio_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpFirmaDichiarazione', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 69, 3), )

    
    FirmaDichiarazione = property(__FirmaDichiarazione.value, __FirmaDichiarazione.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}CFIntermediario uses Python identifier CFIntermediario
    __CFIntermediario = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CFIntermediario'), 'CFIntermediario', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Frontespizio_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpCFIntermediario', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 70, 3), )

    
    CFIntermediario = property(__CFIntermediario.value, __CFIntermediario.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}ImpegnoPresentazione uses Python identifier ImpegnoPresentazione
    __ImpegnoPresentazione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ImpegnoPresentazione'), 'ImpegnoPresentazione', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Frontespizio_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpImpegnoPresentazione', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 71, 3), )

    
    ImpegnoPresentazione = property(__ImpegnoPresentazione.value, __ImpegnoPresentazione.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}DataImpegno uses Python identifier DataImpegno
    __DataImpegno = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DataImpegno'), 'DataImpegno', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Frontespizio_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpDataImpegno', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 79, 3), )

    
    DataImpegno = property(__DataImpegno.value, __DataImpegno.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}FirmaIntermediario uses Python identifier FirmaIntermediario
    __FirmaIntermediario = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FirmaIntermediario'), 'FirmaIntermediario', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Frontespizio_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpFirmaIntermediario', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 80, 3), )

    
    FirmaIntermediario = property(__FirmaIntermediario.value, __FirmaIntermediario.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}FlagConferma uses Python identifier FlagConferma
    __FlagConferma = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FlagConferma'), 'FlagConferma', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Frontespizio_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpFlagConferma', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 81, 3), )

    
    FlagConferma = property(__FlagConferma.value, __FlagConferma.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}IdentificativoProdSoftware uses Python identifier IdentificativoProdSoftware
    __IdentificativoProdSoftware = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IdentificativoProdSoftware'), 'IdentificativoProdSoftware', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Frontespizio_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpIdentificativoProdSoftware', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 82, 3), )

    
    IdentificativoProdSoftware = property(__IdentificativoProdSoftware.value, __IdentificativoProdSoftware.set, None, None)

    _ElementMap.update({
        __CodiceFiscale.name() : __CodiceFiscale,
        __AnnoImposta.name() : __AnnoImposta,
        __PartitaIVA.name() : __PartitaIVA,
        __PIVAControllante.name() : __PIVAControllante,
        __UltimoMese.name() : __UltimoMese,
        __LiquidazioneGruppo.name() : __LiquidazioneGruppo,
        __CFDichiarante.name() : __CFDichiarante,
        __CodiceCaricaDichiarante.name() : __CodiceCaricaDichiarante,
        __CodiceFiscaleSocieta.name() : __CodiceFiscaleSocieta,
        __FirmaDichiarazione.name() : __FirmaDichiarazione,
        __CFIntermediario.name() : __CFIntermediario,
        __ImpegnoPresentazione.name() : __ImpegnoPresentazione,
        __DataImpegno.name() : __DataImpegno,
        __FirmaIntermediario.name() : __FirmaIntermediario,
        __FlagConferma.name() : __FlagConferma,
        __IdentificativoProdSoftware.name() : __IdentificativoProdSoftware
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Frontespizio_IVP_Type = Frontespizio_IVP_Type
Namespace.addCategoryObject('typeBinding', 'Frontespizio_IVP_Type', Frontespizio_IVP_Type)


# Complex type {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}DatiContabili_IVP_Type with content type ELEMENT_ONLY
class DatiContabili_IVP_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}DatiContabili_IVP_Type with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DatiContabili_IVP_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 85, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}Modulo uses Python identifier Modulo
    __Modulo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Modulo'), 'Modulo', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_DatiContabili_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpModulo', True, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 87, 3), )

    
    Modulo = property(__Modulo.value, __Modulo.set, None, None)

    _ElementMap.update({
        __Modulo.name() : __Modulo
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.DatiContabili_IVP_Type = DatiContabili_IVP_Type
Namespace.addCategoryObject('typeBinding', 'DatiContabili_IVP_Type', DatiContabili_IVP_Type)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 88, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}Mese uses Python identifier Mese
    __Mese = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Mese'), 'Mese', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpMese', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 90, 6), )

    
    Mese = property(__Mese.value, __Mese.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}Trimestre uses Python identifier Trimestre
    __Trimestre = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Trimestre'), 'Trimestre', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpTrimestre', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 108, 6), )

    
    Trimestre = property(__Trimestre.value, __Trimestre.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}Subfornitura uses Python identifier Subfornitura
    __Subfornitura = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Subfornitura'), 'Subfornitura', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpSubfornitura', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 119, 6), )

    
    Subfornitura = property(__Subfornitura.value, __Subfornitura.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}EventiEccezionali uses Python identifier EventiEccezionali
    __EventiEccezionali = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'EventiEccezionali'), 'EventiEccezionali', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpEventiEccezionali', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 120, 6), )

    
    EventiEccezionali = property(__EventiEccezionali.value, __EventiEccezionali.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}TotaleOperazioniAttive uses Python identifier TotaleOperazioniAttive
    __TotaleOperazioniAttive = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TotaleOperazioniAttive'), 'TotaleOperazioniAttive', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpTotaleOperazioniAttive', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 121, 6), )

    
    TotaleOperazioniAttive = property(__TotaleOperazioniAttive.value, __TotaleOperazioniAttive.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}TotaleOperazioniPassive uses Python identifier TotaleOperazioniPassive
    __TotaleOperazioniPassive = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'TotaleOperazioniPassive'), 'TotaleOperazioniPassive', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpTotaleOperazioniPassive', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 122, 6), )

    
    TotaleOperazioniPassive = property(__TotaleOperazioniPassive.value, __TotaleOperazioniPassive.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}IvaEsigibile uses Python identifier IvaEsigibile
    __IvaEsigibile = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IvaEsigibile'), 'IvaEsigibile', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpIvaEsigibile', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 123, 6), )

    
    IvaEsigibile = property(__IvaEsigibile.value, __IvaEsigibile.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}IvaDetratta uses Python identifier IvaDetratta
    __IvaDetratta = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IvaDetratta'), 'IvaDetratta', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpIvaDetratta', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 124, 6), )

    
    IvaDetratta = property(__IvaDetratta.value, __IvaDetratta.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}IvaDovuta uses Python identifier IvaDovuta
    __IvaDovuta = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IvaDovuta'), 'IvaDovuta', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpIvaDovuta', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 125, 6), )

    
    IvaDovuta = property(__IvaDovuta.value, __IvaDovuta.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}IvaCredito uses Python identifier IvaCredito
    __IvaCredito = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IvaCredito'), 'IvaCredito', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpIvaCredito', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 126, 6), )

    
    IvaCredito = property(__IvaCredito.value, __IvaCredito.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}DebitoPrecedente uses Python identifier DebitoPrecedente
    __DebitoPrecedente = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DebitoPrecedente'), 'DebitoPrecedente', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpDebitoPrecedente', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 127, 6), )

    
    DebitoPrecedente = property(__DebitoPrecedente.value, __DebitoPrecedente.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}CreditoPeriodoPrecedente uses Python identifier CreditoPeriodoPrecedente
    __CreditoPeriodoPrecedente = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CreditoPeriodoPrecedente'), 'CreditoPeriodoPrecedente', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpCreditoPeriodoPrecedente', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 128, 6), )

    
    CreditoPeriodoPrecedente = property(__CreditoPeriodoPrecedente.value, __CreditoPeriodoPrecedente.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}CreditoAnnoPrecedente uses Python identifier CreditoAnnoPrecedente
    __CreditoAnnoPrecedente = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CreditoAnnoPrecedente'), 'CreditoAnnoPrecedente', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpCreditoAnnoPrecedente', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 129, 6), )

    
    CreditoAnnoPrecedente = property(__CreditoAnnoPrecedente.value, __CreditoAnnoPrecedente.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}VersamentiAutoUE uses Python identifier VersamentiAutoUE
    __VersamentiAutoUE = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'VersamentiAutoUE'), 'VersamentiAutoUE', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpVersamentiAutoUE', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 130, 6), )

    
    VersamentiAutoUE = property(__VersamentiAutoUE.value, __VersamentiAutoUE.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}CreditiImposta uses Python identifier CreditiImposta
    __CreditiImposta = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CreditiImposta'), 'CreditiImposta', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpCreditiImposta', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 131, 6), )

    
    CreditiImposta = property(__CreditiImposta.value, __CreditiImposta.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}InteressiDovuti uses Python identifier InteressiDovuti
    __InteressiDovuti = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'InteressiDovuti'), 'InteressiDovuti', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpInteressiDovuti', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 132, 6), )

    
    InteressiDovuti = property(__InteressiDovuti.value, __InteressiDovuti.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}Acconto uses Python identifier Acconto
    __Acconto = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Acconto'), 'Acconto', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpAcconto', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 133, 6), )

    
    Acconto = property(__Acconto.value, __Acconto.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}ImportoDaVersare uses Python identifier ImportoDaVersare
    __ImportoDaVersare = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ImportoDaVersare'), 'ImportoDaVersare', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpImportoDaVersare', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 134, 6), )

    
    ImportoDaVersare = property(__ImportoDaVersare.value, __ImportoDaVersare.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}ImportoACredito uses Python identifier ImportoACredito
    __ImportoACredito = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ImportoACredito'), 'ImportoACredito', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpImportoACredito', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 135, 6), )

    
    ImportoACredito = property(__ImportoACredito.value, __ImportoACredito.set, None, None)

    _ElementMap.update({
        __Mese.name() : __Mese,
        __Trimestre.name() : __Trimestre,
        __Subfornitura.name() : __Subfornitura,
        __EventiEccezionali.name() : __EventiEccezionali,
        __TotaleOperazioniAttive.name() : __TotaleOperazioniAttive,
        __TotaleOperazioniPassive.name() : __TotaleOperazioniPassive,
        __IvaEsigibile.name() : __IvaEsigibile,
        __IvaDetratta.name() : __IvaDetratta,
        __IvaDovuta.name() : __IvaDovuta,
        __IvaCredito.name() : __IvaCredito,
        __DebitoPrecedente.name() : __DebitoPrecedente,
        __CreditoPeriodoPrecedente.name() : __CreditoPeriodoPrecedente,
        __CreditoAnnoPrecedente.name() : __CreditoAnnoPrecedente,
        __VersamentiAutoUE.name() : __VersamentiAutoUE,
        __CreditiImposta.name() : __CreditiImposta,
        __InteressiDovuti.name() : __InteressiDovuti,
        __Acconto.name() : __Acconto,
        __ImportoDaVersare.name() : __ImportoDaVersare,
        __ImportoACredito.name() : __ImportoACredito
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('../common/main/fornituraIvp_2017_v1.xsd', 23, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.w3.org/2000/09/xmldsig#}Signature uses Python identifier Signature
    __Signature = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(_Namespace_ds, 'Signature'), 'Signature', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON__httpwww_w3_org200009xmldsigSignature', False, pyxb.utils.utility.Location('http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd', 43, 0), )

    
    Signature = property(__Signature.value, __Signature.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}Intestazione uses Python identifier Intestazione
    __Intestazione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Intestazione'), 'Intestazione', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON__urnwww_agenziaentrate_gov_itspecificheTecnichescoivpIntestazione', False, pyxb.utils.utility.Location('../common/main/fornituraIvp_2017_v1.xsd', 25, 4), )

    
    Intestazione = property(__Intestazione.value, __Intestazione.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}Comunicazione uses Python identifier Comunicazione
    __Comunicazione = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Comunicazione'), 'Comunicazione', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_CTD_ANON__urnwww_agenziaentrate_gov_itspecificheTecnichescoivpComunicazione', False, pyxb.utils.utility.Location('../common/main/fornituraIvp_2017_v1.xsd', 26, 4), )

    
    Comunicazione = property(__Comunicazione.value, __Comunicazione.set, None, None)

    _ElementMap.update({
        __Signature.name() : __Signature,
        __Intestazione.name() : __Intestazione,
        __Comunicazione.name() : __Comunicazione
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_ = CTD_ANON_


# Complex type {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}Intestazione_IVP_Type with content type ELEMENT_ONLY
class Intestazione_IVP_Type (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}Intestazione_IVP_Type with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Intestazione_IVP_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/main/intestazioneIvp_2017_v1.xsd', 11, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}CodiceFornitura uses Python identifier CodiceFornitura
    __CodiceFornitura = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CodiceFornitura'), 'CodiceFornitura', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Intestazione_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpCodiceFornitura', False, pyxb.utils.utility.Location('../common/main/intestazioneIvp_2017_v1.xsd', 13, 3), )

    
    CodiceFornitura = property(__CodiceFornitura.value, __CodiceFornitura.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}CodiceFiscaleDichiarante uses Python identifier CodiceFiscaleDichiarante
    __CodiceFiscaleDichiarante = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CodiceFiscaleDichiarante'), 'CodiceFiscaleDichiarante', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Intestazione_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpCodiceFiscaleDichiarante', False, pyxb.utils.utility.Location('../common/main/intestazioneIvp_2017_v1.xsd', 20, 3), )

    
    CodiceFiscaleDichiarante = property(__CodiceFiscaleDichiarante.value, __CodiceFiscaleDichiarante.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}CodiceCarica uses Python identifier CodiceCarica
    __CodiceCarica = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'CodiceCarica'), 'CodiceCarica', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Intestazione_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpCodiceCarica', False, pyxb.utils.utility.Location('../common/main/intestazioneIvp_2017_v1.xsd', 21, 3), )

    
    CodiceCarica = property(__CodiceCarica.value, __CodiceCarica.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}IdSistema uses Python identifier IdSistema
    __IdSistema = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IdSistema'), 'IdSistema', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Intestazione_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpIdSistema', False, pyxb.utils.utility.Location('../common/main/intestazioneIvp_2017_v1.xsd', 41, 3), )

    
    IdSistema = property(__IdSistema.value, __IdSistema.set, None, None)

    _ElementMap.update({
        __CodiceFornitura.name() : __CodiceFornitura,
        __CodiceFiscaleDichiarante.name() : __CodiceFiscaleDichiarante,
        __CodiceCarica.name() : __CodiceCarica,
        __IdSistema.name() : __IdSistema
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Intestazione_IVP_Type = Intestazione_IVP_Type
Namespace.addCategoryObject('typeBinding', 'Intestazione_IVP_Type', Intestazione_IVP_Type)


# Complex type {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}Comunicazione_IVP_Type with content type ELEMENT_ONLY
class Comunicazione_IVP_Type (_ImportedBinding__cm.Documento_Type):
    """Complex type {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}Comunicazione_IVP_Type with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Comunicazione_IVP_Type')
    _XSDLocation = pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 10, 1)
    _ElementMap = _ImportedBinding__cm.Documento_Type._ElementMap.copy()
    _AttributeMap = _ImportedBinding__cm.Documento_Type._AttributeMap.copy()
    # Base type is _ImportedBinding__cm.Documento_Type
    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}Frontespizio uses Python identifier Frontespizio
    __Frontespizio = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Frontespizio'), 'Frontespizio', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Comunicazione_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpFrontespizio', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 14, 5), )

    
    Frontespizio = property(__Frontespizio.value, __Frontespizio.set, None, None)

    
    # Element {urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp}DatiContabili uses Python identifier DatiContabili
    __DatiContabili = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'DatiContabili'), 'DatiContabili', '__urnwww_agenziaentrate_gov_itspecificheTecnichescoivp_Comunicazione_IVP_Type_urnwww_agenziaentrate_gov_itspecificheTecnichescoivpDatiContabili', False, pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 15, 5), )

    
    DatiContabili = property(__DatiContabili.value, __DatiContabili.set, None, None)

    
    # Attribute identificativo inherited from {urn:www.agenziaentrate.gov.it:specificheTecniche:common}Documento_Type
    _ElementMap.update({
        __Frontespizio.name() : __Frontespizio,
        __DatiContabili.name() : __DatiContabili
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Comunicazione_IVP_Type = Comunicazione_IVP_Type
Namespace.addCategoryObject('typeBinding', 'Comunicazione_IVP_Type', Comunicazione_IVP_Type)


Intestazione = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intestazione'), pyxb.binding.datatypes.anyType, location=pyxb.utils.utility.Location('../common/main/intestazioneIvp_2017_v1.xsd', 10, 1))
Namespace.addCategoryObject('elementBinding', Intestazione.name().localName(), Intestazione)

Fornitura = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Fornitura'), CTD_ANON_, location=pyxb.utils.utility.Location('../common/main/fornituraIvp_2017_v1.xsd', 22, 1))
Namespace.addCategoryObject('elementBinding', Fornitura.name().localName(), Fornitura)

Comunicazione = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Comunicazione'), Comunicazione_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 9, 1))
Namespace.addCategoryObject('elementBinding', Comunicazione.name().localName(), Comunicazione)



Frontespizio_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CodiceFiscale'), _ImportedBinding__cm.DatoCF_Type, scope=Frontespizio_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 22, 3)))

Frontespizio_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'AnnoImposta'), _ImportedBinding__cm.DatoDA_Type, scope=Frontespizio_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 23, 3)))

Frontespizio_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PartitaIVA'), _ImportedBinding__cm.DatoPI_Type, scope=Frontespizio_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 24, 3)))

Frontespizio_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'PIVAControllante'), _ImportedBinding__cm.DatoPI_Type, scope=Frontespizio_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 25, 3)))

Frontespizio_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'UltimoMese'), STD_ANON, scope=Frontespizio_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 26, 3)))

Frontespizio_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'LiquidazioneGruppo'), _ImportedBinding__cm.DatoCB_Type, scope=Frontespizio_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 46, 3)))

Frontespizio_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CFDichiarante'), _ImportedBinding__cm.DatoCF_Type, scope=Frontespizio_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 47, 3)))

Frontespizio_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CodiceCaricaDichiarante'), STD_ANON_, scope=Frontespizio_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 48, 3)))

Frontespizio_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CodiceFiscaleSocieta'), _ImportedBinding__cm.DatoCN_Type, scope=Frontespizio_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 68, 3)))

Frontespizio_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FirmaDichiarazione'), _ImportedBinding__cm.DatoCB_Type, scope=Frontespizio_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 69, 3)))

Frontespizio_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CFIntermediario'), _ImportedBinding__cm.DatoCF_Type, scope=Frontespizio_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 70, 3)))

Frontespizio_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ImpegnoPresentazione'), STD_ANON_2, scope=Frontespizio_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 71, 3)))

Frontespizio_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DataImpegno'), _ImportedBinding__cm.DatoDT_Type, scope=Frontespizio_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 79, 3)))

Frontespizio_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FirmaIntermediario'), _ImportedBinding__cm.DatoCB_Type, scope=Frontespizio_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 80, 3)))

Frontespizio_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FlagConferma'), _ImportedBinding__cm.DatoCB_Type, scope=Frontespizio_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 81, 3)))

Frontespizio_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IdentificativoProdSoftware'), _ImportedBinding__cm.DatoAN_Type, scope=Frontespizio_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 82, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 25, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 26, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 46, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 47, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 48, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 68, 3))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 70, 3))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 71, 3))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 79, 3))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 80, 3))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 81, 3))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 82, 3))
    counters.add(cc_11)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Frontespizio_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CodiceFiscale')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 22, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Frontespizio_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'AnnoImposta')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 23, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Frontespizio_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PartitaIVA')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 24, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Frontespizio_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'PIVAControllante')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 25, 3))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Frontespizio_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'UltimoMese')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 26, 3))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Frontespizio_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'LiquidazioneGruppo')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 46, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Frontespizio_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CFDichiarante')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 47, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Frontespizio_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CodiceCaricaDichiarante')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 48, 3))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Frontespizio_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CodiceFiscaleSocieta')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 68, 3))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Frontespizio_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FirmaDichiarazione')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 69, 3))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(Frontespizio_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CFIntermediario')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 70, 3))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(Frontespizio_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ImpegnoPresentazione')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 71, 3))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(Frontespizio_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DataImpegno')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 79, 3))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(Frontespizio_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FirmaIntermediario')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 80, 3))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(Frontespizio_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FlagConferma')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 81, 3))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(Frontespizio_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IdentificativoProdSoftware')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 82, 3))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
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
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
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
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
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
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
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
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, True) ]))
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
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_11, True) ]))
    st_15._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Frontespizio_IVP_Type._Automaton = _BuildAutomaton()




DatiContabili_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Modulo'), CTD_ANON, scope=DatiContabili_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 87, 3)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=1, max=5, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 87, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(DatiContabili_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Modulo')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 87, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
DatiContabili_IVP_Type._Automaton = _BuildAutomaton_()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Mese'), STD_ANON_3, scope=CTD_ANON, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 90, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Trimestre'), STD_ANON_4, scope=CTD_ANON, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 108, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Subfornitura'), _ImportedBinding__cm.DatoCB_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 119, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'EventiEccezionali'), Eventi_Ecc_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 120, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TotaleOperazioniAttive'), DatoVN_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 121, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'TotaleOperazioniPassive'), DatoVN_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 122, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IvaEsigibile'), DatoVN_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 123, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IvaDetratta'), DatoVN_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 124, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IvaDovuta'), _ImportedBinding__cm.DatoVP_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 125, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IvaCredito'), _ImportedBinding__cm.DatoVP_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 126, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DebitoPrecedente'), _ImportedBinding__cm.DatoVP_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 127, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CreditoPeriodoPrecedente'), _ImportedBinding__cm.DatoVP_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 128, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CreditoAnnoPrecedente'), DatoVN_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 129, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'VersamentiAutoUE'), _ImportedBinding__cm.DatoVP_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 130, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CreditiImposta'), _ImportedBinding__cm.DatoVP_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 131, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'InteressiDovuti'), _ImportedBinding__cm.DatoVP_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 132, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Acconto'), _ImportedBinding__cm.DatoVP_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 133, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ImportoDaVersare'), _ImportedBinding__cm.DatoVP_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 134, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ImportoACredito'), _ImportedBinding__cm.DatoVP_Type, scope=CTD_ANON, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 135, 6)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 90, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 108, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 119, 6))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 120, 6))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 121, 6))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 122, 6))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 123, 6))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 124, 6))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 125, 6))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 126, 6))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 127, 6))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 128, 6))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 129, 6))
    counters.add(cc_12)
    cc_13 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 130, 6))
    counters.add(cc_13)
    cc_14 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 131, 6))
    counters.add(cc_14)
    cc_15 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 132, 6))
    counters.add(cc_15)
    cc_16 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 133, 6))
    counters.add(cc_16)
    cc_17 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 134, 6))
    counters.add(cc_17)
    cc_18 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 135, 6))
    counters.add(cc_18)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Mese')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 90, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Trimestre')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 108, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Subfornitura')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 119, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'EventiEccezionali')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 120, 6))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TotaleOperazioniAttive')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 121, 6))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'TotaleOperazioniPassive')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 122, 6))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IvaEsigibile')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 123, 6))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IvaDetratta')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 124, 6))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IvaDovuta')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 125, 6))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IvaCredito')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 126, 6))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DebitoPrecedente')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 127, 6))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CreditoPeriodoPrecedente')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 128, 6))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CreditoAnnoPrecedente')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 129, 6))
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_13, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'VersamentiAutoUE')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 130, 6))
    st_13 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_14, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CreditiImposta')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 131, 6))
    st_14 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_15, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'InteressiDovuti')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 132, 6))
    st_15 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_16, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Acconto')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 133, 6))
    st_16 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_17, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ImportoDaVersare')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 134, 6))
    st_17 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_18, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ImportoACredito')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 135, 6))
    st_18 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_18, [
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_18, [
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_18, [
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
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_18, [
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
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_10, False) ]))
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
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_11, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_11, False) ]))
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
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_12, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_12, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_13, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_13, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_13, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_14, True) ]))
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_14, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_14, False) ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
        fac.UpdateInstruction(cc_15, True) ]))
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_15, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_15, False) ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
        fac.UpdateInstruction(cc_16, True) ]))
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_16, False) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_16, False) ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
        fac.UpdateInstruction(cc_17, True) ]))
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_17, False) ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_18, [
        fac.UpdateInstruction(cc_18, True) ]))
    st_18._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_2()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(_Namespace_ds, 'Signature'), _ImportedBinding__ds.SignatureType, scope=CTD_ANON_, location=pyxb.utils.utility.Location('http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd', 43, 0)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Intestazione'), Intestazione_IVP_Type, scope=CTD_ANON_, location=pyxb.utils.utility.Location('../common/main/fornituraIvp_2017_v1.xsd', 25, 4)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Comunicazione'), Comunicazione_IVP_Type, scope=CTD_ANON_, location=pyxb.utils.utility.Location('../common/main/fornituraIvp_2017_v1.xsd', 26, 4)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/fornituraIvp_2017_v1.xsd', 27, 4))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Intestazione')), pyxb.utils.utility.Location('../common/main/fornituraIvp_2017_v1.xsd', 25, 4))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Comunicazione')), pyxb.utils.utility.Location('../common/main/fornituraIvp_2017_v1.xsd', 26, 4))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(_Namespace_ds, 'Signature')), pyxb.utils.utility.Location('../common/main/fornituraIvp_2017_v1.xsd', 27, 4))
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
CTD_ANON_._Automaton = _BuildAutomaton_3()




Intestazione_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CodiceFornitura'), STD_ANON_5, scope=Intestazione_IVP_Type, location=pyxb.utils.utility.Location('../common/main/intestazioneIvp_2017_v1.xsd', 13, 3)))

Intestazione_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CodiceFiscaleDichiarante'), _ImportedBinding__cm.DatoCF_Type, scope=Intestazione_IVP_Type, location=pyxb.utils.utility.Location('../common/main/intestazioneIvp_2017_v1.xsd', 20, 3)))

Intestazione_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CodiceCarica'), STD_ANON_6, scope=Intestazione_IVP_Type, location=pyxb.utils.utility.Location('../common/main/intestazioneIvp_2017_v1.xsd', 21, 3)))

Intestazione_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IdSistema'), _ImportedBinding__cm.DatoCF_Type, scope=Intestazione_IVP_Type, location=pyxb.utils.utility.Location('../common/main/intestazioneIvp_2017_v1.xsd', 41, 3)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/intestazioneIvp_2017_v1.xsd', 20, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/intestazioneIvp_2017_v1.xsd', 21, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('../common/main/intestazioneIvp_2017_v1.xsd', 41, 3))
    counters.add(cc_2)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Intestazione_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CodiceFornitura')), pyxb.utils.utility.Location('../common/main/intestazioneIvp_2017_v1.xsd', 13, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Intestazione_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CodiceFiscaleDichiarante')), pyxb.utils.utility.Location('../common/main/intestazioneIvp_2017_v1.xsd', 20, 3))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Intestazione_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'CodiceCarica')), pyxb.utils.utility.Location('../common/main/intestazioneIvp_2017_v1.xsd', 21, 3))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(Intestazione_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IdSistema')), pyxb.utils.utility.Location('../common/main/intestazioneIvp_2017_v1.xsd', 41, 3))
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
Intestazione_IVP_Type._Automaton = _BuildAutomaton_4()




Comunicazione_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Frontespizio'), Frontespizio_IVP_Type, scope=Comunicazione_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 14, 5)))

Comunicazione_IVP_Type._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'DatiContabili'), DatiContabili_IVP_Type, scope=Comunicazione_IVP_Type, location=pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 15, 5)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Comunicazione_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Frontespizio')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 14, 5))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Comunicazione_IVP_Type._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'DatiContabili')), pyxb.utils.utility.Location('../common/main/comunicazioneIvp_2017_v1.xsd', 15, 5))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Comunicazione_IVP_Type._Automaton = _BuildAutomaton_5()

