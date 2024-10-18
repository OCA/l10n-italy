from odoo.exceptions import AccessError, MissingError
from odoo.http import request, route
from odoo.osv.expression import OR

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager


class DNCustomerPortal(CustomerPortal):
    def _get_delivery_note_domain(self):
        domain = [("state", "in", ["confirm", "invoiced", "done"])]
        return domain

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        dn_count = (
            request.env["stock.delivery.note"].search_count(
                self._get_delivery_note_domain()
            )
            if request.env["stock.delivery.note"].has_access("read")
            else 0
        )
        values["dn_count"] = dn_count
        return values

    def _get_delivery_notes_searchbar_sortings(self):
        return {
            "date": {"label": self.env._("Delivery Note Date"), "order": "date desc"},
            "name": {"label": self.env._("Delivery Note #"), "order": "name"},
        }

    def _get_delivery_notes_searchbar_inputs(self):
        return {
            "name": {"input": "name", "label": self.env._("Search in Description")},
        }

    def _prepare_my_delivery_notes_values(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        search="",
        search_in="name",
        **kwargs,
    ):
        values = self._prepare_portal_layout_values()
        DeliveryNote = request.env["stock.delivery.note"]

        url = "/my/delivery-notes"
        _items_per_page = 100

        # default sortby order
        if not sortby:
            sortby = "date"

        searchbar_sortings = self._get_delivery_notes_searchbar_sortings()
        searchbar_inputs = self._get_delivery_notes_searchbar_inputs()

        sort_order = searchbar_sortings[sortby]["order"]
        domain = self._get_delivery_note_domain()

        if date_begin and date_end:
            domain += [("date", ">", date_begin), ("date", "<=", date_end)]

        if search and search_in:
            search_domain = []
            if search_in == "name":
                search_domain = OR([search_domain, [("name", "ilike", search)]])
            domain += search_domain

        pager_values = portal_pager(
            url=url,
            total=DeliveryNote.search_count(domain),
            page=page,
            step=_items_per_page,
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "search_in": search_in,
                "search": search,
            },
        )

        delivery_note = DeliveryNote.search(
            domain,
            order=sort_order,
            limit=_items_per_page,
            offset=pager_values["offset"],
        )

        values.update(
            {
                "date": date_begin,
                "delivery_notes": delivery_note,
                "page_name": "delivery_notes",
                "default_url": url,
                "pager": pager_values,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "search": search,
                "sortby": sortby,
            }
        )
        return values

    @route(
        ["/my/delivery-notes", "/my/delivery-notes/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_delivery_notes(self, **kwargs):
        values = self._prepare_my_delivery_notes_values(**kwargs)
        request.session["my_delivery_notes_history"] = values["delivery_notes"].ids[
            :100
        ]
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
        self, dn_id, access_token=None, report_type=None, download=False, **kwargs
    ):
        try:
            delivery_note_sudo = self._document_check_access(
                "stock.delivery.note", dn_id, access_token=access_token
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

        values = self._dn_get_page_view_values(
            delivery_note_sudo, access_token, **kwargs
        )

        return request.render("l10n_it_delivery_note.portal_delivery_note_page", values)
