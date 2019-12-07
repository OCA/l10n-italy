odoo.define('l10n_it_website_portal_fatturapa_sale.portal', function (require) {
    "use strict";

    var check_e_inv_data = function (self, el_selector, super_event, self_args) {
        var electronic_invoice_subjected = $(el_selector);
        if (electronic_invoice_subjected.length) {
            var complete = electronic_invoice_subjected.data('e-inv-data-complete');
            var inv_subj = electronic_invoice_subjected[0].checked;
            if (inv_subj && !complete) {
                var redirect_url = "/my/account";
                var params = {
                    redirect: window.location.pathname,
                };
                params.electronic_invoice_subjected = 'on';
                window.location = redirect_url + "?" + $.param(params);
            }
            else {
                return super_event.apply(self, self_args);
            }
        }
        else {
            return super_event.apply(self, self_args);
        }
    };
    return {
        check_e_inv_data: check_e_inv_data,
    };
});
