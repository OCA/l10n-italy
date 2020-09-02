# Copyright 2020 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

_field_renames = [
    ('stock.picking.package.preparation', 'stock_picking_package_preparation',
     'show_price', 'ddt_show_price'),
]


@openupgrade.migrate()
def migrate(env, version):
    if not version:
        return
    openupgrade.rename_fields(env, _field_renames)
    # Remove old view that still contains reference to 'show_price'
    # otherwise the method '_check_xml' of 'ir.ui.view' raises an error
    # on calling 'postprocess_and_fields' method.
    openupgrade.delete_records_safely_by_xml_id(env, [
        'l10n_it_ddt.ddt_stock_picking_package_preparation_form',
    ])
