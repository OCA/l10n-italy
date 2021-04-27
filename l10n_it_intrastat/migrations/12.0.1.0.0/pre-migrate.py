#  Copyright 2021 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade
from psycopg2 import sql


def restore_intrastat_codes(cr):
    """
    Module report_intrastat from core moved to account_intrastat in Enterprise,
    so the table report_intrastat_code has been renamed account_intrastat_code.

    This migration copies back the data from account_intrastat_code
    to report_intrastat_code.
    Note also that data of column "name" has been moved to column "code".
    """

    # Restore table report_intrastat_code
    # that has been renamed to account_intrastat_code
    enterprise_table_name = "account_intrastat_code"
    oca_table_name = "report_intrastat_code"
    if not openupgrade.table_exists(
        cr, enterprise_table_name
    ) and openupgrade.table_exists(cr, oca_table_name):
        # Enterprise did not move your data, lucky you!
        return

    enterprise_table_name = sql.Identifier(enterprise_table_name)
    oca_table_name = sql.Identifier(oca_table_name)
    # Create table that will be updated by module
    query = sql.SQL(
        """
CREATE TABLE {oca_table_name} AS (SELECT * FROM {enterprise_table_name});
ALTER TABLE {oca_table_name} ADD PRIMARY KEY (id);
"""
    )
    openupgrade.logged_query(
        cr,
        query.format(
            oca_table_name=oca_table_name,
            enterprise_table_name=enterprise_table_name,
        ),
    )

    # "name" column has been moved to "code",
    # move it back and drop "code" column
    openupgrade.logged_query(
        cr,
        sql.SQL(
            """
UPDATE {oca_table_name} SET name = code
"""
        ).format(
            oca_table_name=oca_table_name,
        ),
    )
    openupgrade.logged_query(
        cr,
        sql.SQL(
            """
ALTER TABLE {oca_table_name} DROP COLUMN "code"
"""
        ).format(
            oca_table_name=oca_table_name,
        ),
    )

    # Update module data linked to this module to have the correct model
    openupgrade.logged_query(
        cr,
        sql.SQL(
            """
UPDATE ir_model_data
SET
    model = 'report.intrastat.code'
WHERE
    module = 'l10n_it_intrastat'
    AND model = 'account.intrastat.code'
    AND res_id in (SELECT id FROM {oca_table_name})
    """
        ).format(
            oca_table_name=oca_table_name,
        ),
    )


@openupgrade.migrate()
def migrate(env, version):
    views_xmlids = [
        "view_form_report_intrastat_code",
        "view_tree_report_intrastat_code",
    ]
    for view_xmlid in views_xmlids:
        full_xml_id = ".".join(["l10n_it_intrastat", view_xmlid])
        view = env.ref(full_xml_id)
        view.inherit_id = False

    restore_intrastat_codes(env.cr)
