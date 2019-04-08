odoo.define('l10n_it_website_portal_fatturapa', function (require) {
    'use strict';
    require('web.core');

    $(document).ready(function () {

        var $details_div = $('.o_website_portal_details');
        if (!$details_div.length) {
            return $.Deferred().reject(
                "DOM doesn't contain '.o_website_portal_details'");
        }
        var $electronic_invoice_subjected_input = $details_div.find(
            "input[name='electronic_invoice_subjected'][type='checkbox']");
        var $div_codice_destinatario = $details_div.find(
            ".div_codice_destinatario");
        var $div_pec_destinatario = $details_div.find(".div_pec_destinatario");

        var compute_e_inv_fields_visibility = function () {
            if ($electronic_invoice_subjected_input[0].checked) {
                $div_codice_destinatario.removeClass("hidden");
                $div_pec_destinatario.removeClass("hidden");
            } else {
                $div_codice_destinatario.addClass("hidden");
                $div_pec_destinatario.addClass("hidden");
            }
        };
        compute_e_inv_fields_visibility();
        $electronic_invoice_subjected_input.change(
            compute_e_inv_fields_visibility);

    });
});
