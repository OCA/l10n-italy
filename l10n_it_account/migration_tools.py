# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Common methods for migrations
from openupgradelib import openupgrade


def _remove_module(env, module_name):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_module_module
        SET
            state = 'to remove'
        WHERE
            name = %(module_name)s
            AND state NOT IN ('to remove', 'uninstalled')
        """,
        dict(
            module_name=module_name,
        ),
    )


def remove_modules_views(cr, modules):
    """Remove the views and menus registered by the given modules.

    Also removes any view inheriting the removed views and any menu that is a
    child of a removed menu.

    ``modules`` can be a single module name or a list of module names.

    Uses recursive CTEs so that:
     - inherited views / child menus are deleted before their parents (no FK
       violation)
     - all ir_model_data rows for deleted views and menus are removed (no
       orphans)
    """
    if isinstance(modules, str):
        modules = [modules]
    if not modules:
        return
    openupgrade.logged_query(
        cr,
        """
        WITH RECURSIVE views_to_delete AS (
            SELECT v.id
            FROM ir_ui_view v
            JOIN ir_model_data imd
                ON imd.model = 'ir.ui.view'
               AND imd.res_id = v.id
               AND imd.module = ANY(%s)
            UNION ALL
            SELECT v.id
            FROM ir_ui_view v
            JOIN views_to_delete vtd ON v.inherit_id = vtd.id
        ),
        deleted_imd AS (
            DELETE FROM ir_model_data
            WHERE model = 'ir.ui.view'
              AND res_id IN (SELECT id FROM views_to_delete)
        )
        DELETE FROM ir_ui_view
        WHERE id IN (SELECT id FROM views_to_delete)
        """,
        (list(modules),),
    )
    openupgrade.logged_query(
        cr,
        """
        WITH RECURSIVE menus_to_delete AS (
            SELECT m.id
            FROM ir_ui_menu m
            JOIN ir_model_data imd
                ON imd.model = 'ir.ui.menu'
               AND imd.res_id = m.id
               AND imd.module = ANY(%s)
            UNION ALL
            SELECT m.id
            FROM ir_ui_menu m
            JOIN menus_to_delete mtd ON m.parent_id = mtd.id
        ),
        deleted_imd AS (
            DELETE FROM ir_model_data
            WHERE model = 'ir.ui.menu'
              AND res_id IN (SELECT id FROM menus_to_delete)
        )
        DELETE FROM ir_ui_menu
        WHERE id IN (SELECT id FROM menus_to_delete)
        """,
        (list(modules),),
    )
