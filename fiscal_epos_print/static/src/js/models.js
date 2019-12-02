odoo.define('fiscal_epos_print.fiscalcode_field', function (require) {
    "use strict";

  var pos_models = require('point_of_sale.models');
  pos_models.load_fields("account.journal",
        ["fiscalprinter_payment_type", "fiscalprinter_payment_index"]);

});
