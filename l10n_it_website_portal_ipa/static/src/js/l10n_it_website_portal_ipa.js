odoo.define("l10n_it_website_portal_ipa", function (require) {
    "use strict";
    require("web.core");

    $(document).ready(function () {
        var details_div_selector = ".o_portal_details";
        var $details_div = $(details_div_selector);
        if ($details_div.length) {
            var $is_pa = $details_div.find("input[name='is_pa'][type='checkbox']");
            if (!$is_pa.length) {
                return;
            }

            var $ipa_code_div = $details_div
                .find("input[name='ipa_code'][type='text']")
                .parent();

            var compute_ipa_fields_visibility = function () {
                if ($is_pa[0].checked) {
                    $ipa_code_div.show();
                } else {
                    $ipa_code_div.hide();
                }
            };
            compute_ipa_fields_visibility();
            $is_pa.change(compute_ipa_fields_visibility);
        }
    });
});
