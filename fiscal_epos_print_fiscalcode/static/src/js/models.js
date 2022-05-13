odoo.define("fiscal_epos_print_fiscalcode.epos_print_fiscalcode_receipt_field", function (require) {
    "use strict";

    var pos_models = require("point_of_sale.models");
    pos_models.load_fields("res.partner", "epos_print_fiscalcode_receipt");
});
