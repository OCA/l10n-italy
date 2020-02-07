odoo.define("fiscal_epos_print_fiscalcode.models", function (require) {
    "use strict";

    var core = require('web.core');
    var _t = core._t;
    var fiscal_epos_print_models =
        require("fiscal_epos_print.epson_epos_print");

    fiscal_epos_print_models.eposDriver.include( {
        printFiscalReceiptHeader: function (receipt) {
            var fiscalcode_message = "";
            var current_client = this.sender.pos.get_client();
            var fiscalcode = current_client && current_client.fiscalcode;
            if (fiscalcode && current_client.epos_print_fiscalcode_receipt) {
                fiscalcode = fiscalcode.toUpperCase();
                fiscalcode_message = "\n" + _t("F.C.: ") + fiscalcode + "\n";
            }

            if (fiscalcode_message) {
                if (!receipt.header) {
                    receipt.header = "";
                }
                receipt.header += fiscalcode_message;
            }

            return this._super(receipt);
        },
    });
});
