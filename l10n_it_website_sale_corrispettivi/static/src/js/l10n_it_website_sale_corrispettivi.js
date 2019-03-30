odoo.define('l10n_it_website_sale_corrispettivi', function(require) {
    'use strict';
    require('web.core');

    $(document).ready(function () {
        var $container_div = $('.oe_website_sale');
        var $use_invoice_input = $container_div.find("input[name='use_invoice'][type='checkbox']");
        var $electronic_invoice_subjected_input = $container_div.find("input[name='electronic_invoice_subjected'][type='checkbox']");
        var $electronic_invoice_subjected_div = $container_div.find("div.div_electronic_invoice_subjected");
        var $div_codice_destinatario = $container_div.find("div.div_codice_destinatario");
        var $div_pec_destinatario = $container_div.find("div.div_pec_destinatario");

         var compute_invoice_subjected_fields_visibility = function(){
            if ($use_invoice_input[0] != null) {
                if ($use_invoice_input[0].checked) {
                    $electronic_invoice_subjected_div.show();
                } else {
                    $electronic_invoice_subjected_input.prop('checked', false);
                    $electronic_invoice_subjected_div.hide();
                    $div_codice_destinatario.hide();
                    $div_pec_destinatario.hide();
                }
            }
        };
        compute_invoice_subjected_fields_visibility();
        $use_invoice_input.change(compute_invoice_subjected_fields_visibility);

    });
});
