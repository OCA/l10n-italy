import logging
import re

import xmlschema
from lxml import etree

from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

# compiled reg expression for whitespace characters substitution
reg_whitespace = re.compile(r"\s+")


def encode_for_export(string_to_encode, max_chars, encoding="latin"):
    return (
        reg_whitespace.sub(" ", string_to_encode)
        .encode(encoding, errors="replace")
        .decode(encoding)[:max_chars]
    )


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

_old_xsd_specs = get_module_resource(
    "l10n_it_account", "tools", "xsd", "xmldsig-core-schema.xsd"
)

_fpa_schema_file = get_module_resource(
    "l10n_it_account",
    "tools",
    "xsd",
    "Schema_del_file_xml_FatturaPA_v1.2.2.xsd",
)

fpa_schema = xmlschema.XMLSchema(
    _fpa_schema_file,
    locations={"http://www.w3.org/2000/09/xmldsig#": _old_xsd_specs},
    validation="lax",
    allow="local",
    loglevel=20,
)


def fpa_schema_etree():
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
    return etree.parse(_fpa_schema_file, parser)


# Funzione per leggere i possibili valori dei tipi enumeration
def fpa_schema_get_enum(type_name):
    enum = fpa_schema.types[type_name].get_facet(xmlschema.names.XSD_ENUMERATION)
    return tuple(
        (e.get("value"), enum.get_annotation(i) or "") for i, e in enumerate(enum)
    )
