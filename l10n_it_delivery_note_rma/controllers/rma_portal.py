# Copyright 2023 Nextev
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.rma.controllers.main import PortalRma


class PortalRma(PortalRma):
    def _get_filter_domain(self, kw):
        res = super()._get_filter_domain(kw)
        if "dn_id" in kw:
            res.append(("delivery_note_id", "=", int(kw["dn_id"])))
        return res
