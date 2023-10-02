# Copyright 2023 Nextev
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):
    @http.route(
        ["/my/delivery-notes/<int:dn>/requestrma"],
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def request_delivery_rma(self, dn, access_token=None, **post):
        try:
            dn_sudo = self._document_check_access(
                "stock.delivery.note", dn, access_token=access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")
        dn_obj = request.env["stock.delivery.note"]
        wizard_obj = request.env["stock.delivery.note.rma.wizard"].sudo()
        wizard_line_field_types = {
            f: d["type"] for f, d in wizard_obj.line_ids.fields_get().items()
        }
        # Set wizard line vals
        mapped_vals = {}
        custom_vals = {}
        partner_shipping_id = post.pop("partner_shipping_id", False)
        for name, value in post.items():
            try:
                row, field_name = name.split("-", 1)
                if wizard_line_field_types.get(field_name) == "many2one":
                    value = int(value) if value else False
                mapped_vals.setdefault(row, {}).update({field_name: value})
            # Catch possible form custom fields to add them to the RMA
            # description values
            except ValueError:
                custom_vals.update({name: value})
        # If no operation is filled, no RMA will be created
        line_vals = [
            (0, 0, vals) for vals in mapped_vals.values() if vals.get("operation_id")
        ]
        # Create wizard an generate rmas
        dn = dn_obj.browse(dn).sudo()
        location_id = dn.warehouse_id.rma_loc_id.id
        # Add custom fields text
        custom_description = ""
        if custom_vals:
            custom_description = r"<br \>---<br \>"
            custom_description += r"<br \>".join(
                ["{}: {}".format(x, y) for x, y in custom_vals.items()]
            )
        wizard = wizard_obj.with_context(active_id=dn).create(
            {
                "line_ids": line_vals,
                "location_id": location_id,
                "partner_shipping_id": partner_shipping_id,
                "custom_description": custom_description,
            }
        )
        user_has_group_portal = request.env.user.has_group(
            "base.group_portal"
        ) or request.env.user.has_group("base.group_public")
        rma = wizard.sudo().create_rma()
        for rec in rma:
            rec.origin += _(" (Portal)")
        # Add the user as follower of the created RMAs so they can later view them.
        rma.message_subscribe([request.env.user.partner_id.id])
        # Subscribe the user to the notification subtype so he receives the confirmation
        # note.
        rma.message_follower_ids.filtered(
            lambda x: x.partner_id == request.env.user.partner_id
        ).subtype_ids += request.env.ref("rma.mt_rma_notification")
        if len(rma) == 0:
            route = dn_sudo.get_portal_url()
        elif len(rma) == 1:
            route = rma._get_share_url() if user_has_group_portal else rma.access_url
        else:
            route = "/my/rmas?dn_id=%d" % dn.id
        return request.redirect(route)
