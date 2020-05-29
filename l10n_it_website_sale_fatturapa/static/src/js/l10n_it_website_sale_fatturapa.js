odoo.define('l10n_it_website_sale_fatturapa', function (require) {
    'use strict';
    require('web.core');

    $(document).ready(function () {
        var $container_div = $('.oe_website_sale');
        var $electronic_invoice_subjected_input =
            $container_div.find(
                "input[name='electronic_invoice_subjected'][type='checkbox']");
        var $div_codice_destinatario =
            $container_div.find(".div_codice_destinatario");
        var $div_pec_destinatario =
            $container_div.find(".div_pec_destinatario");

        var compute_e_inv_fields_visibility = function () {
            if ($electronic_invoice_subjected_input.length !== 0) {
                if ($electronic_invoice_subjected_input[0].checked) {
                    $div_codice_destinatario.show();
                    $div_pec_destinatario.show();
                } else {
                    $div_codice_destinatario.hide();
                    $div_pec_destinatario.hide();
                }
            }
        };
        compute_e_inv_fields_visibility();
        $electronic_invoice_subjected_input
            .change(compute_e_inv_fields_visibility);
    });
});
