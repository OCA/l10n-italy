# Copyright 2026 Nextev Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import json

from openupgradelib import openupgrade
from psycopg2 import sql

_OLD_MODULE = "l10n_it_declaration_of_intent"


# Table and model name constants for migration
_OLD_TABLE = "l10n_it_declaration_of_intent_declaration"
_NEW_TABLE = "l10n_it_edi_doi_declaration_of_intent"
_OLD_MODEL = "l10n_it_declaration_of_intent.declaration"
_NEW_MODEL = "l10n_it_edi_doi.declaration_of_intent"


_REL_TABLE = "account_move_l10n_it_declaration_of_intent_declaration_rel"


def _get_rel_table_name(env):
    """Return the old m2m relation table name if it exists, else None."""
    if openupgrade.table_exists(env.cr, _REL_TABLE):
        return _REL_TABLE
    return None


def _migrate_old_declarations_into_new(env):
    """INSERT old declaration records into the new table created by l10n_it_edi_doi.

    A temporary old_id column tracks the old→new ID mapping so that all
    relation/reference tables can be updated with a JOIN instead of arithmetic
    offsets. The sequence is managed automatically by the INSERT.
    """
    # Ensure extension-only columns and the temporary old_id tracker exist
    # (l10n_it_edi_doi_extension hasn't init'd yet at this point)
    for col, col_type in (
        ("type", "varchar"),
        ("number", "varchar"),
        ("old_id", "integer"),
    ):
        if not openupgrade.column_exists(env.cr, _NEW_TABLE, col):
            openupgrade.logged_query(
                env.cr,
                sql.SQL("ALTER TABLE {} ADD COLUMN {} {}").format(
                    sql.Identifier(_NEW_TABLE),
                    sql.Identifier(col),
                    sql.SQL(col_type),
                ),
            )

    # Insert old records; sequence assigns new IDs, old ID is stored in old_id
    openupgrade.logged_query(
        env.cr,
        sql.SQL("""
            INSERT INTO {new_table}
                (old_id, partner_id, company_id, currency_id,
                 issue_date, start_date, end_date, threshold,
                 protocol_number_part1, protocol_number_part2,
                 state, type, number,
                 invoiced, not_yet_invoiced, remaining,
                 create_uid, create_date, write_uid, write_date)
            SELECT
                old.id,
                old.partner_id, old.company_id, old.currency_id,
                old.date, old.date_start, old.date_end, old.limit_amount,
                SPLIT_PART(
                    SPLIT_PART(COALESCE(old.telematic_protocol, ''), '-', 1),
                    '/', 1
                ),
                CASE
                    WHEN old.telematic_protocol LIKE '%%-%%'
                        THEN SPLIT_PART(old.telematic_protocol, '-', 2)
                    WHEN old.telematic_protocol LIKE '%%/%%'
                        THEN SPLIT_PART(old.telematic_protocol, '/', 2)
                    ELSE ''
                END,
                CASE old.state
                    WHEN 'valid' THEN 'active'
                    WHEN 'expired' THEN 'terminated'
                    WHEN 'close' THEN 'revoked'
                    ELSE old.state
                END,
                COALESCE(old.type, 'in'),
                old.number,
                COALESCE(old.used_amount, 0),
                0,
                old.limit_amount - COALESCE(old.used_amount, 0),
                old.create_uid, old.create_date, old.write_uid, old.write_date
            FROM {old_table} old
        """).format(
            new_table=sql.Identifier(_NEW_TABLE),
            old_table=sql.Identifier(_OLD_TABLE),
        ),
    )

    # Update many2many relation table using old_id mapping
    rel_table = _get_rel_table_name(env)
    if rel_table:
        # Drop FK constraints pointing to the old table before updating IDs.
        # The rel table's FK references l10n_it_declaration_of_intent_declaration,
        # but we're setting values that exist only in
        # l10n_it_edi_doi_declaration_of_intent.
        env.cr.execute(
            """
            SELECT conname FROM pg_constraint c
            JOIN pg_class t ON t.oid = c.conrelid
            JOIN pg_class f ON f.oid = c.confrelid
            WHERE t.relname = %s AND f.relname = %s AND c.contype = 'f'
            """,
            (rel_table, _OLD_TABLE),
        )
        for (conname,) in env.cr.fetchall():
            openupgrade.logged_query(
                env.cr,
                sql.SQL("ALTER TABLE {} DROP CONSTRAINT {}").format(
                    sql.Identifier(rel_table),
                    sql.Identifier(conname),
                ),
            )
        # Update rel_table in two steps to avoid PK issues
        openupgrade.logged_query(
            env.cr,
            sql.SQL(
                """
                UPDATE {rel_table} rel
                SET l10n_it_declaration_of_intent_declaration_id = -new.id
                FROM {new_table} new
                WHERE rel.l10n_it_declaration_of_intent_declaration_id = new.old_id
            """
            ).format(
                rel_table=sql.Identifier(rel_table),
                new_table=sql.Identifier(_NEW_TABLE),
            ),
        )
        openupgrade.logged_query(
            env.cr,
            sql.SQL(
                """
                UPDATE {rel_table} rel
                SET l10n_it_declaration_of_intent_declaration_id = new.id
                FROM {new_table} new
                WHERE rel.l10n_it_declaration_of_intent_declaration_id = -new.id
            """
            ).format(
                rel_table=sql.Identifier(rel_table),
                new_table=sql.Identifier(_NEW_TABLE),
            ),
        )

    # Update all model references with new model name, using old_id for matching
    _model_refs = [
        ("ir_model_data", "model", "res_id"),
        ("ir_attachment", "res_model", "res_id"),
    ]
    _optional_model_refs = [
        ("mail_message", "model", "res_id"),
        ("mail_followers", "res_model", "res_id"),
    ]
    for table, model_col, id_col in _model_refs + [
        r for r in _optional_model_refs if openupgrade.table_exists(env.cr, r[0])
    ]:
        openupgrade.logged_query(
            env.cr,
            sql.SQL("""
                UPDATE {table} ref
                SET {model_col} = %s, {id_col} = new.id
                FROM {new_table} new
                WHERE ref.{model_col} = %s AND ref.{id_col} = new.old_id
            """).format(
                table=sql.Identifier(table),
                model_col=sql.Identifier(model_col),
                id_col=sql.Identifier(id_col),
                new_table=sql.Identifier(_NEW_TABLE),
            ),
            (_NEW_MODEL, _OLD_MODEL),
        )

    # Update ir_model_fields.relation (model name only, no record IDs)
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_model_fields
        SET relation = %s
        WHERE relation = %s
        """,
        (_NEW_MODEL, _OLD_MODEL),
    )

    # Drop old declaration table (data has been migrated)
    # Note: old_id column is kept until post-migration (used to map IDs
    # when populating account_move_doi from declaration lines).
    openupgrade.logged_query(
        env.cr,
        sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(sql.Identifier(_OLD_TABLE)),
    )


def _l10n_it_declaration_of_intent_pre_migration(env):
    """
    Migrate data from l10n_it_declaration_of_intent to l10n_it_edi_doi.

    This function handles the migration of:
    - Declaration of Intent records (main model)
    - Many2many relations with account.move
    - State values mapping
    - Database cleanup for Odoo 18 compatibility
    """
    # Check if "l10n_it_declaration_of_intent_declaration" table exists
    if not openupgrade.table_exists(env.cr, _OLD_TABLE):
        # Migration already done or old module never installed
        return

    # Remove views from the old module before Odoo tries to render them.
    # The old module may still be in state 'installed' (not 'to remove'),
    # so Odoo won't clean up its views automatically. They must be deleted
    # here because they use Odoo 16 XPath syntax (e.g. /tree/) that is
    # incompatible with Odoo 18 (renamed to /list/) and would cause a
    # ValueError when opening the invoice form view.
    #
    # The recursive CTE also collects any inherited views that extend
    # the module's views (from any module), so that:
    #  - inherited views are deleted before their parents (no FK violation)
    #  - all ir_model_data rows for deleted views are removed (no orphans)
    openupgrade.logged_query(
        env.cr,
        """
        WITH RECURSIVE views_to_delete AS (
            SELECT v.id
            FROM ir_ui_view v
            JOIN ir_model_data imd
                ON imd.model = 'ir.ui.view'
               AND imd.res_id = v.id
               AND imd.module = 'l10n_it_declaration_of_intent'
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
    )

    # Mark old module for removal so Odoo's cleanup handles the rest
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_module_module
        SET state = 'to remove'
        WHERE name = 'l10n_it_declaration_of_intent'
          AND state NOT IN ('uninstalled', 'to remove')
        """,
    )

    # l10n_it_edi_doi (dependency) is always installed first and always
    # creates the new table. Migrate old records into it; the offset ensures
    # no PK conflicts whether the table is empty (offset=0) or not.
    _migrate_old_declarations_into_new(env)

    # Check for the relation table
    rel_table = _get_rel_table_name(env)

    if rel_table:
        # Migrate invoice-DOI links from many2many to many2one
        # In v16, invoices could have multiple DOIs (many2many)
        # In v18, invoices can only have one DOI (many2one)
        # We migrate the first/oldest DOI for each invoice
        openupgrade.logged_query(
            env.cr,
            sql.SQL("""
                UPDATE account_move am
                SET l10n_it_edi_doi_id = subq.doi_id
                FROM (
                    SELECT
                        rel.account_move_id,
                        MIN(rel.l10n_it_declaration_of_intent_declaration_id) as doi_id
                    FROM {rel_table} rel
                    GROUP BY rel.account_move_id
                ) subq
                WHERE am.id = subq.account_move_id
                AND am.l10n_it_edi_doi_id IS NULL
            """).format(rel_table=sql.Identifier(rel_table)),
        )

    # Drop old tables that are no longer needed
    # (lines migrated to account_move_doi in post-migration)
    tables_to_drop = [
        "l10n_it_declaration_of_intent_yearly_limit",  # Yearly limits no longer managed
        "move_line_declaration_line_rel",  # Old M2M relation
        "account_tax_l10n_it_declaration_of_intent_declaration_rel",  # Tax↔DOI M2M
        "declaration_select_manually_rel",  # Manually selected DOIs M2M
    ]

    # Drop orphan column on account_move_line (no equivalent in l10n_it_edi_doi)
    if openupgrade.column_exists(
        env.cr, "account_move_line", "force_declaration_of_intent_id"
    ):
        openupgrade.logged_query(
            env.cr,
            "ALTER TABLE account_move_line DROP COLUMN force_declaration_of_intent_id",
        )

    for table in tables_to_drop:
        if openupgrade.table_exists(env.cr, table):
            openupgrade.logged_query(
                env.cr,
                sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(
                    sql.Identifier(table)
                ),
            )


def _log_migration_choices(env):
    """Post chatter notes on invoices and admin partner about migration decisions.

    For each invoice that was linked to multiple DOIs in v16, post a note
    listing all linked declarations and which one was automatically selected
    as primary (l10n_it_edi_doi_id). Also post a summary with links on the
    admin partner so that the relevant invoices can be found at a glance.
    """
    env.cr.execute(
        """
        SELECT
            amd.move_id,
            am.name,
            am.l10n_it_edi_doi_id,
            json_agg(
                json_build_object(
                    'id',       amd.declaration_id,
                    'number',   doi.number,
                    'protocol', CONCAT_WS(
                        '-',
                        NULLIF(doi.protocol_number_part1, ''),
                        NULLIF(doi.protocol_number_part2, '')
                    )
                )
                ORDER BY amd.declaration_id
            ) AS declarations
        FROM account_move_doi amd
        JOIN account_move am ON am.id = amd.move_id
        JOIN l10n_it_edi_doi_declaration_of_intent doi ON doi.id = amd.declaration_id
        GROUP BY amd.move_id, am.name, am.l10n_it_edi_doi_id
        HAVING COUNT(*) > 1
        """
    )
    rows = env.cr.fetchall()
    if not rows:
        return

    base_url = (
        env["ir.config_parameter"].sudo().get_param("web.base.url", "").rstrip("/")
    )

    def _doi_label(d):
        label = d.get("number") or d.get("protocol") or f"ID {d['id']}"
        return f"<strong>{label}</strong>"

    affected_links = []
    for move_id, move_name, primary_doi_id, declarations_json in rows:
        declarations = (
            json.loads(declarations_json)
            if isinstance(declarations_json, str)
            else declarations_json
        )
        primary = next((d for d in declarations if d["id"] == primary_doi_id), None)
        others = [d for d in declarations if d["id"] != primary_doi_id]

        primary_label = _doi_label(primary) if primary else f"ID {primary_doi_id}"
        others_labels = ", ".join(_doi_label(d) for d in others)

        body = (
            "<p><strong>Migrazione da Odoo 16:</strong> "
            f"questa fattura era collegata a {len(declarations)} "
            "Dichiarazioni di Intento. "
            f"La DI impostata come riferimento primario è {primary_label}."
        )
        if others:
            body += (
                f" Le altre DI collegate ({others_labels}) sono visibili "
                "nel tab <em>Dichiarazioni di Intento</em>: "
                "verificare e correggere gli importi se necessario."
            )
        body += "</p>"

        env["account.move"].browse(move_id).message_post(
            body=body,
            message_type="comment",
            subtype_xmlid="mail.mt_note",
        )

        display_name = move_name or f"ID {move_id}"
        if base_url:
            url = f"{base_url}/web#model=account.move&id={move_id}&view_type=form"
            affected_links.append(f'<a href="{url}">{display_name}</a>')
        else:
            affected_links.append(display_name)

    admin_partner = env.ref("base.partner_admin", raise_if_not_found=False)
    if admin_partner:
        body = (
            f"<p><strong>Migrazione DI – {len(affected_links)} fatture "
            "con più dichiarazioni di intento in Odoo 16:</strong><br/>"
            "Per ciascuna fattura la DI primaria è stata selezionata "
            "automaticamente (quella con ID minore). "
            "Verificare e correggere gli importi nel tab "
            "<em>Dichiarazioni di Intento</em>:</p>"
            "<ul>" + "".join(f"<li>{link}</li>" for link in affected_links) + "</ul>"
        )
        admin_partner.message_post(
            body=body,
            message_type="comment",
            subtype_xmlid="mail.mt_note",
        )


def _l10n_it_declaration_of_intent_post_migration(env):
    """
    Post-migration tasks for l10n_it_declaration_of_intent.

    This handles data that needs ORM access or depends on loaded modules.
    """
    # Populate account_move_doi from v16 declaration lines.
    # The line table always exists at this point: pre_migration returns early
    # if the old module was not installed, so we only reach here after a full
    # migration where the line table is guaranteed to be present.
    _LINE_TABLE = "l10n_it_declaration_of_intent_declaration_line"
    openupgrade.logged_query(
        env.cr,
        sql.SQL("""
            INSERT INTO account_move_doi
                (move_id, declaration_id, amount, sequence,
                 currency_id, company_id,
                 create_uid, create_date, write_uid, write_date)
            SELECT
                line.invoice_id,
                new_doi.id,
                COALESCE(line.amount, 0),
                ROW_NUMBER() OVER (
                    PARTITION BY line.invoice_id
                    ORDER BY new_doi.id
                ) * 10,
                am.currency_id,
                am.company_id,
                1, NOW() AT TIME ZONE 'UTC',
                1, NOW() AT TIME ZONE 'UTC'
            FROM {line_table} line
            JOIN {new_table} new_doi ON new_doi.old_id = line.declaration_id
            JOIN account_move am ON am.id = line.invoice_id
            WHERE line.invoice_id IS NOT NULL
        """).format(
            line_table=sql.Identifier(_LINE_TABLE),
            new_table=sql.Identifier(_NEW_TABLE),
        ),
    )
    openupgrade.logged_query(
        env.cr,
        sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(sql.Identifier(_LINE_TABLE)),
    )

    _log_migration_choices(env)

    # Populate l10n_it_edi_doi_amount from account_move_doi.
    # account_move_doi is populated, so we can use the real per-invoice
    # amounts from v16 declaration lines (when available) rather than the
    # approximate ABS(amount_untaxed).
    # Primary: sum of amounts from account_move_doi (accurate when populated
    # from declaration lines; stays 0 when populated from the m2m fallback).
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_move am
        SET l10n_it_edi_doi_amount = doi_sum.total
        FROM (
            SELECT move_id, SUM(amount) AS total
            FROM account_move_doi
            GROUP BY move_id
        ) doi_sum
        WHERE am.id = doi_sum.move_id
          AND doi_sum.total > 0
          AND am.l10n_it_edi_doi_amount = 0
        """,
    )
    # Fallback: invoices still at 0 (m2m path had no amounts).
    # In v18, l10n_it_edi_doi_amount is always positive: sum(price_total) *
    # -direction_sign. ABS(amount_untaxed) is a reasonable proxy.
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_move am
        SET l10n_it_edi_doi_amount = ABS(am.amount_untaxed)
        WHERE am.l10n_it_edi_doi_id IS NOT NULL
          AND am.l10n_it_edi_doi_amount = 0
        """,
    )

    # Drop the temporary old_id column now that account_move_doi is populated
    openupgrade.logged_query(
        env.cr,
        sql.SQL("ALTER TABLE {} DROP COLUMN IF EXISTS old_id").format(
            sql.Identifier(_NEW_TABLE)
        ),
    )

    # Sync the new ir.sequence so that the next assigned number doesn't
    # collide with numbers migrated from the old module.
    #
    # Primary source: the old sequence record (code "declaration_of_intent")
    # still lives in ir_sequence at this point — its number_next already holds
    # the correct next value and is deleted here to avoid leaving a stale
    # duplicate around.
    # Fallback: derive next from MAX(number)+1 of the migrated records in case
    # the old sequence was already removed by a previous run or manual cleanup.
    env.cr.execute(
        "SELECT number_next FROM ir_sequence WHERE code = %s",
        ("declaration_of_intent",),
    )
    row = env.cr.fetchone()
    if row:
        next_number = row[0]
    else:
        # Fallback: reconstruct from the trailing digit group of each number
        # value (handles plain integers like "42" and prefixed ones like
        # "DOI/2025/00042").
        env.cr.execute(
            r"""
            SELECT COALESCE(
                MAX(
                    (regexp_matches(number, '(\d+)[^0-9]*$'))[1]::integer
                ), 0
            )
            FROM l10n_it_edi_doi_declaration_of_intent
            WHERE number IS NOT NULL
              AND number ~ '\d'
            """
        )
        max_number = env.cr.fetchone()[0]
        next_number = max_number + 1 if max_number > 0 else 1

    seq = env.ref(
        "l10n_it_edi_doi_extension.declaration_of_intent_seq",
        raise_if_not_found=False,
    )
    if seq and seq.number_next < next_number:
        seq.number_next = next_number

    # Remove the old sequence now that the new one has been updated,
    # so it doesn't linger as a stale duplicate after migration.
    if row:
        env.cr.execute(
            "DELETE FROM ir_sequence WHERE code = %s",
            ("declaration_of_intent",),
        )

    # Update ir.model.data for proper module reference (main DOI model)
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_model_data
        SET module = 'l10n_it_edi_doi_extension'
        WHERE model = 'l10n_it_edi_doi.declaration_of_intent'
        AND module = 'l10n_it_declaration_of_intent'
        """,
    )

    # ---- Clean up all remnants of the old module ----
    old_module = _OLD_MODULE
    old_model_prefix = f"{_OLD_MODULE}.%"

    # Delete actions pointing to old models
    openupgrade.logged_query(
        env.cr,
        "DELETE FROM ir_act_window WHERE res_model LIKE %s",
        (old_model_prefix,),
    )

    # Delete menus owned by old module
    openupgrade.logged_query(
        env.cr,
        """
        DELETE FROM ir_ui_menu m
        USING ir_model_data imd
        WHERE imd.model = 'ir.ui.menu'
          AND imd.res_id = m.id
          AND imd.module = %s
        """,
        (old_module,),
    )

    # Delete views owned by old module (if any survived pre-migration)
    openupgrade.logged_query(
        env.cr,
        """
        DELETE FROM ir_ui_view v
        USING ir_model_data imd
        WHERE imd.model = 'ir.ui.view'
          AND imd.res_id = v.id
          AND imd.module = %s
        """,
        (old_module,),
    )

    # Delete access rules for old models
    openupgrade.logged_query(
        env.cr,
        """
        DELETE FROM ir_model_access
        WHERE model_id IN (SELECT id FROM ir_model WHERE model LIKE %s)
        """,
        (old_model_prefix,),
    )

    # Delete record rules for old models
    openupgrade.logged_query(
        env.cr,
        """
        DELETE FROM ir_rule
        WHERE model_id IN (SELECT id FROM ir_model WHERE model LIKE %s)
        """,
        (old_model_prefix,),
    )

    # Delete field selections for old model fields
    openupgrade.logged_query(
        env.cr,
        """
        DELETE FROM ir_model_fields_selection
        WHERE field_id IN (
            SELECT id FROM ir_model_fields WHERE model LIKE %s
        )
        """,
        (old_model_prefix,),
    )

    # Delete fields belonging to old models
    openupgrade.logged_query(
        env.cr,
        "DELETE FROM ir_model_fields WHERE model LIKE %s",
        (old_model_prefix,),
    )

    # Delete fields added by old module to existing models
    # (e.g. valid_for_declaration_of_intent on account.fiscal.position)
    openupgrade.logged_query(
        env.cr,
        """
        DELETE FROM ir_model_fields f
        USING ir_model_data imd
        WHERE imd.model = 'ir.model.fields'
          AND imd.res_id = f.id
          AND imd.module = %s
          AND f.model NOT LIKE %s
        """,
        (old_module, old_model_prefix),
    )

    # Delete old ir.model records
    openupgrade.logged_query(
        env.cr,
        "DELETE FROM ir_model WHERE model LIKE %s",
        (old_model_prefix,),
    )

    # Delete all remaining ir_model_data for old module
    openupgrade.logged_query(
        env.cr,
        "DELETE FROM ir_model_data WHERE module = %s",
        (old_module,),
    )

    # Remove old module record entirely (already marked 'to remove' in pre-migration)
    openupgrade.logged_query(
        env.cr,
        """
        DELETE FROM ir_module_module
        WHERE name = %s
        """,
        (old_module,),
    )


def _l10n_it_edi_doi_extension_pre_init_hook(env):
    if openupgrade.is_module_installed(env.cr, _OLD_MODULE):
        _l10n_it_declaration_of_intent_pre_migration(env)


def _l10n_it_edi_doi_extension_post_init_hook(env):
    env.cr.execute("SELECT state FROM ir_module_module WHERE name = %s", (_OLD_MODULE,))
    row = env.cr.fetchone()
    # Run post-migration if the old module was installed or is being removed
    # (pre-migration sets state to 'to remove', so is_module_installed = False)
    if row and row[0] in ("installed", "to remove"):
        _l10n_it_declaration_of_intent_post_migration(env)
