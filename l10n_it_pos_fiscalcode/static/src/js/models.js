odoo.define("l10n_it_pos_fiscalcode.fiscalcode_field", function (require) {
    "use strict";

    var pos_models = require("point_of_sale.models");
    pos_models.load_fields("res.partner", "fiscalcode");
});
