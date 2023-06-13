# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class DDTCustomerPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner_id = request.env.user.partner_id.id
        ddt_count = request.env["stock.delivery.note"].search_count(
            [("partner_id", "=", partner_id)]
        )
        values.update({"ddt_count": ddt_count})
        return values

    @http.route(
        ["/my/delivery-notes", "/my/delivery-notes/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_delivery_notes(
        self, page=1, date_begin=None, date_end=None, sortby=None, **kw
    ):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        DeliveryNote = request.env["stock.delivery.note"]

        domain = [("partner_id", "=", partner.id)]

        self._get_sale_searchbar_sortings()

        # default sortby order
        if not sortby:
            sortby = "date"
        # searchbar_sortings[sortby]

        # if date_begin and date_end:
        #     domain += [
        #         ("create_date", ">", date_begin),
        #         ("create_date", "<=", date_end),
        #     ]

        # count for pager
        ddt_count = DeliveryNote.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/delivery-notes",
            # url_args={"date_begin": date_begin, "date_end": date_end, "sortby": sortby},
            total=ddt_count,
            page=page,
            # step=self._items_per_page,
        )
        # search the count to display, according to the pager data
        ddt = DeliveryNote.search(domain)
        # request.session["my_quotations_history"] = quotations.ids[:100]

        values.update(
            {
                "date": date_begin,
                "delivery_notes": ddt.sudo(),
                "page_name": "ddt",
                "pager": pager,
                "default_url": "/my/delivery-notes",
                # "searchbar_sortings": searchbar_sortings,
                # "sortby": sortby,
            }
        )
        return request.render(
            "l10n_it_delivery_note_rma.portal_my_delivery_notes", values
        )
