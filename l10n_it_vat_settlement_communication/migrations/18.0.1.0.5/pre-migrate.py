#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Remove VP rows left orphan by past deletions of comunicazione.liquidazione
    # (before ondelete='cascade' was declared on comunicazione_id).
    # Such rows keep account.move records of monthly VAT settlements linked
    # through liquidazioni_move_id, preventing the wizard from picking those
    # months when a new comunicazione is generated.
    openupgrade.logged_query(
        env.cr,
        """
        DELETE FROM comunicazione_liquidazione_vp
        WHERE comunicazione_id IS NULL
        """,
    )
