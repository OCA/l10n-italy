# Copyright 2020 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_field_renames = [
    ('stock.picking.package.preparation', 'stock_picking_package_preparation',
     'show_price', 'ddt_show_price'),
]


def delete_inherits_safely_by_id(env, xml):
    for xml_child in xml.inherit_children_ids:
        if xml_child.inherit_children_ids:
            delete_inherits_safely_by_id(env, xml_child)
        else:
            delete_records_safely_by_id(env, xml_child)
    delete_records_safely_by_id(env, xml)


def delete_records_safely_by_id(env, xml_ids):
    for xml_id in xml_ids:
        _logger.debug('Deleting record for ID %s', xml_id)
        try:
            with env.cr.savepoint():
                if xml_id and xml_id.exists():
                    xml_id.unlink()
        except Exception as e:
            _logger.error('Error deleting XML-ID %s: %s', xml_id, repr(e))


@openupgrade.migrate()
def migrate(env, version):
    if not version:
        return
    openupgrade.rename_fields(env, _field_renames)
    # Remove old view that still contains reference to 'show_price'
    # otherwise the method '_check_xml' of 'ir.ui.view' raises an error
    # on calling 'postprocess_and_fields' method.
    xml = env.ref('l10n_it_ddt.ddt_stock_picking_package_preparation_form',
                  raise_if_not_found=False)
    delete_inherits_safely_by_id(env, xml)
