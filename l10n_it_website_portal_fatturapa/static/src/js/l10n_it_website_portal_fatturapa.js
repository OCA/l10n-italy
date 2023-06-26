odoo.define("l10n_it_website_portal_fatturapa", function (require) {
    "use strict";
    require("web.core");

    $(document).ready(function () {
        var details_div_selector = ".o_portal_details";
        var $details_div = $(details_div_selector);
        if ($details_div.length) {
            var $electronic_invoice_subjected_input = $details_div.find(
                "input[name='electronic_invoice_subjected'][type='checkbox']"
            );
            var $div_electronic_invoice_subjected_fields = $details_div.find(
                ".div_electronic_invoice_subjected_fields"
            );

            var compute_e_inv_fields_visibility = function () {
                if ($electronic_invoice_subjected_input[0].checked) {
                    $div_electronic_invoice_subjected_fields.show();
                } else {
                    $div_electronic_invoice_subjected_fields.hide();
                }
            };
            compute_e_inv_fields_visibility();
            $electronic_invoice_subjected_input.change(compute_e_inv_fields_visibility);

            var $is_pa = $details_div.find("input[name='is_pa'][type='checkbox']");
            if (!$is_pa.length) {
                return;
            }
            var $codice_destinatario_div = $details_div
                .find("input[name='codice_destinatario'][type='text']")
                .parent();
            var $pec_destinatario_div = $details_div
                .find("input[name='pec_destinatario'][type='text']")
                .parent();

            var compute_destinatario_fields_visibility = function () {
                if ($is_pa[0].checked) {
                    $codice_destinatario_div.hide();
                    $pec_destinatario_div.hide();
                } else {
                    $codice_destinatario_div.show();
                    $pec_destinatario_div.show();
                }
            };
            compute_destinatario_fields_visibility();
            $is_pa.change(compute_destinatario_fields_visibility);
        }
    });
});
