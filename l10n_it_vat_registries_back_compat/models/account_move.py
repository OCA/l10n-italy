# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMove(models.Model):
    """Re-declare v16 reverse charge fields so the ORM can read
    data that was written by l10n_it_reverse_charge in version 16.

    In a database migrated from 16 to 18, the columns
    ``rc_self_purchase_invoice_id`` and ``rc_purchase_invoice_id``
    still exist in the ``account_move`` table but no v18 module
    defines them.  This module re-exposes them as read-only fields
    for backward-compatible VAT-registry printing.
    """

    _inherit = "account.move"

    rc_self_purchase_invoice_id = fields.Many2one(
        comodel_name="account.move",
        string="RC Self Purchase Invoice",
        readonly=True,
        copy=False,
    )
    rc_purchase_invoice_id = fields.Many2one(
        comodel_name="account.move",
        string="RC Purchase Invoice",
        readonly=True,
        copy=False,
    )
    rc_original_purchase_invoice_ids = fields.One2many(
        comodel_name="account.move",
        inverse_name="rc_self_purchase_invoice_id",
        string="Original purchase invoices",
        readonly=True,
        copy=False,
    )
