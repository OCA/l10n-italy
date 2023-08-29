from odoo import _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request, route

from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class DNCustomerPortal(CustomerPortal):
    def _get_delivery_note_domain(self, search_in=False):
        domain = [("state", "in", ["confirm", "invoiced", "done"])]
        if search_in:
            domain += search_in
        return domain

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        dn_count = (
            request.env["stock.delivery.note"].search_count(
                self._get_delivery_note_domain()
            )
            if request.env["stock.delivery.note"].check_access_rights(
                "read", raise_exception=False
            )
            else 0
        )
        values["dn_count"] = dn_count
        return values

    @route(
        ["/my/delivery-notes", "/my/delivery-notes/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_delivery_notes(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        search="",
        search_in="name",
        **kw
    ):
        values = self._prepare_portal_layout_values()
        DeliveryNote = request.env["stock.delivery.note"]

        searchbar_sortings = {
            "date": {"label": _("Delivery Note Date"), "order": "date desc"},
            "name": {"label": _("Delivery Note #"), "order": "name"},
        }
        searchbar_inputs = {
            "name": {
                "input": "name",
                "label": _('Search <span class="nolabel"> Name</span>'),
                "domain": [("name", "ilike", search)],
            },
        }

        search_domain = searchbar_inputs[search_in]["domain"] if search_in else []
        # default sortby order
        if not sortby:
            sortby = "date"
        sort_order = searchbar_sortings[sortby]["order"]

        # count for pager
        dn_count = DeliveryNote.search_count(
            self._get_delivery_note_domain(search_domain)
        )
        # make pager
        pager = portal_pager(
            url="/my/delivery-notes",
            url_args={"sortby": sortby, "search_in": search_in, "search": "search"},
            total=dn_count,
            page=page,
            step=self._items_per_page,
        )
        # search the count to display, according to the pager data
        delivery_note = DeliveryNote.search(
            self._get_delivery_note_domain(search_domain),
            order=sort_order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )

        values.update(
            {
                "date": date_begin,
                "delivery_notes": delivery_note,
                "page_name": "delivery_notes",
                "pager": pager,
                "default_url": "/my/delivery-notes",
                "searchbar_sortings": searchbar_sortings,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "search": search,
                "sortby": sortby,
            }
        )
        return request.render("l10n_it_delivery_note.portal_my_delivery_notes", values)

    def _dn_get_page_view_values(self, dn, access_token, **kwargs):
        values = {
            "page_name": "delivery_note",
            "dn": dn,
        }
        return self._get_page_view_values(
            dn, access_token, values, "my_dn_history", False, **kwargs
        )

    @route(["/my/delivery-notes/<int:dn_id>"], type="http", auth="user", website=True)
    def portal_my_delivery_note_detail(
        self, dn_id, access_token=None, report_type=None, download=False, **kw
    ):
        try:
            delivery_note_sudo = self._document_check_access(
                "stock.delivery.note", dn_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        if report_type in ("html", "pdf", "text"):
            return self._show_report(
                model=delivery_note_sudo,
                report_type=report_type,
                report_ref="l10n_it_delivery_note.delivery_note_report_action",
                download=download,
            )

        values = self._dn_get_page_view_values(delivery_note_sudo, access_token, **kw)

        return request.render("l10n_it_delivery_note.portal_delivery_note_page", values)
