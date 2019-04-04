odoo.define('l10n_it_website_portal_fatturapa', function(require) {
    'use strict';
    require('web.core');

    $(document).ready(function () {
        var $details_div = $('.o_portal_details');
        if (!$details_div.length) {
            return $.Deferred().reject(
                "DOM doesn't contain '.o_website_portal_details'");
        }
        var $electronic_invoice_subjected_input = $details_div.find("input[name='electronic_invoice_subjected'][type='checkbox']");
        var $div_codice_destinatario = $details_div.find(".div_codice_destinatario");
        var $div_pec_destinatario = $details_div.find(".div_pec_destinatario");

         var compute_e_inv_fields_visibility = function(){
            if ($electronic_invoice_subjected_input[0].checked) {
                $div_codice_destinatario.show();
                $div_pec_destinatario.show();
            } else {
                $div_codice_destinatario.hide();
                $div_pec_destinatario.hide();
            }
        };
        compute_e_inv_fields_visibility();
        $electronic_invoice_subjected_input.change(compute_e_inv_fields_visibility);

    });
});
