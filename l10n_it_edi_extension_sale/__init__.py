# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from . import models
from openupgradelib import openupgrade


def _recover_related_documents(env):
    """Recover the link between related documents and sale orders.

    The legacy ``l10n_it_fatturapa_sale`` module linked related documents to
    the invoices, so the document of a sale order kept its link to the
    order even when invoiced.
    ``l10n_it_edi_related_document`` copies the rows of the legacy table into
    ``account_move_related_document`` without the sale order link:

    - the documents not invoiced yet are the same rows, so they are linked
      back to their sale order;
    - the invoiced documents are copied to the sale order, because in this
      module the documents of an invoice are a copy of the documents of
      the sale order;
    - the documents whose data is related to different sale orders are
      left unlinked, because their sale order cannot be determined and
      linking them to the wrong order would copy them to the invoices of
      that order.
    """
    cr = env.cr
    if not openupgrade.table_exists(cr, "fatturapa_related_document_type"):
        return
    if not all(
        openupgrade.column_exists(cr, "fatturapa_related_document_type", field)
        for field in ("sale_order_id", "sale_order_line_id")
    ):
        return
    # Documents not invoiced yet: link them to their sale order
    openupgrade.logged_query(
        cr,
        """
        UPDATE account_move_related_document amrd
        SET
            sale_order_id = legacy.sale_order_id,
            sale_order_line_id = legacy.sale_order_line_id
        FROM (
            SELECT
                type,
                name,
                "lineRef",
                date,
                numitem,
                code,
                cig,
                cup,
                min(sale_order_id) AS sale_order_id,
                min(sale_order_line_id) AS sale_order_line_id,
                count(
                    DISTINCT (sale_order_id, sale_order_line_id)
                ) AS order_links
            FROM fatturapa_related_document_type
            WHERE
                (sale_order_id IS NOT NULL OR sale_order_line_id IS NOT NULL)
                AND invoice_id IS NULL
                AND invoice_line_id IS NULL
            GROUP BY
                type, name, "lineRef", date, numitem, code, cig, cup
        ) legacy
        WHERE
            legacy.order_links = 1
            AND amrd.sale_order_id IS NULL
            AND amrd.sale_order_line_id IS NULL
            AND amrd.invoice_id IS NULL
            AND amrd.invoice_line_id IS NULL
            AND amrd.type = legacy.type
            AND amrd.name = legacy.name
            AND amrd."lineRef" IS NOT DISTINCT FROM legacy."lineRef"
            AND amrd.date IS NOT DISTINCT FROM legacy.date
            AND amrd.numitem IS NOT DISTINCT FROM legacy.numitem
            AND amrd.code IS NOT DISTINCT FROM legacy.code
            AND amrd.cig IS NOT DISTINCT FROM legacy.cig
            AND amrd.cup IS NOT DISTINCT FROM legacy.cup
        """,
    )
    # Documents already invoiced: the sale order gets its own copy
    openupgrade.logged_query(
        cr,
        """
        INSERT INTO account_move_related_document (
            type,
            name,
            "lineRef",
            date,
            numitem,
            code,
            cig,
            cup,
            sale_order_id,
            sale_order_line_id
        )
        SELECT DISTINCT
            legacy.type,
            legacy.name,
            legacy."lineRef",
            legacy.date,
            legacy.numitem,
            legacy.code,
            legacy.cig,
            legacy.cup,
            legacy.sale_order_id,
            legacy.sale_order_line_id
        FROM fatturapa_related_document_type legacy
        WHERE
            (
                legacy.sale_order_id IS NOT NULL
                OR legacy.sale_order_line_id IS NOT NULL
            )
            AND (
                legacy.invoice_id IS NOT NULL
                OR legacy.invoice_line_id IS NOT NULL
            )
            AND NOT EXISTS (
                SELECT 1
                FROM account_move_related_document amrd
                WHERE
                    amrd.sale_order_id
                        IS NOT DISTINCT FROM legacy.sale_order_id
                    AND amrd.sale_order_line_id
                        IS NOT DISTINCT FROM legacy.sale_order_line_id
                    AND amrd.invoice_id IS NULL
                    AND amrd.invoice_line_id IS NULL
                    AND amrd.type = legacy.type
                    AND amrd.name = legacy.name
                    AND amrd."lineRef" IS NOT DISTINCT FROM legacy."lineRef"
                    AND amrd.date IS NOT DISTINCT FROM legacy.date
                    AND amrd.numitem IS NOT DISTINCT FROM legacy.numitem
                    AND amrd.code IS NOT DISTINCT FROM legacy.code
                    AND amrd.cig IS NOT DISTINCT FROM legacy.cig
                    AND amrd.cup IS NOT DISTINCT FROM legacy.cup
            )
        """,
    )


def _recover_admin_ref(env):
    """Recover the Admin. Ref. of the sale order lines.

    The legacy ``l10n_it_fatturapa_sale`` module stored the Admin. Ref. of
    the sale order lines in the ``admin_ref`` column, while
    ``l10n_it_edi_extension`` uses ``l10n_it_edi_admin_ref`` (and only
    renames it for the invoice lines).
    The new field is 20 characters wide (the EDI limit), so longer values
    are truncated.
    """
    cr = env.cr
    if not openupgrade.column_exists(cr, "sale_order_line", "admin_ref"):
        return
    openupgrade.logged_query(
        cr,
        """
        UPDATE sale_order_line
        SET l10n_it_edi_admin_ref = LEFT(admin_ref, 20)
        WHERE admin_ref IS NOT NULL AND l10n_it_edi_admin_ref IS NULL
        """,
    )


def _post_init_hook(env):
    _recover_related_documents(env)
    _recover_admin_ref(env)
