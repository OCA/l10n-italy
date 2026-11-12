# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):
    # Codes loaded by previous versions of this module are ATECO 2007,
    # superseded by ATECO 2025 since 2025-04-01: archive them, so that
    # they stay linked to partners until these are reclassified.
    # Records created by users are left untouched.
    cr.execute(
        """
        UPDATE ateco_category
        SET ateco_version = COALESCE(ateco_version, '2007'),
            active = FALSE
        WHERE id IN (
            SELECT res_id
            FROM ir_model_data
            WHERE module = 'l10n_it_ateco'
                AND model = 'ateco.category'
                AND name NOT LIKE %s
        )
        """,
        ("ateco\\_category\\_2025\\_%",),
    )
