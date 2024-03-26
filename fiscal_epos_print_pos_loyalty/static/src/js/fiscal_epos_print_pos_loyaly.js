odoo.define("fiscal_epos_print_pos_loyaly.models", function (require) {
    "use strict";

    var core = require('web.core');
    var _t = core._t;
    var fiscal_epos_print_models =
        require("fiscal_epos_print.epson_epos_print");
    var loyalty_program = require("pos_loyalty.loyalty_program");

    fiscal_epos_print_models.eposDriver.include( {
        printFiscalReceiptFooter: function (receipt) {
            var loyalty_message = "";
            var current_client = this.order.get_client();
            if (current_client) {
                var loyalty_points = this.order.get_new_total_points();
                var new_points = this.order.get_new_points();
                if (current_client.barcode) {
                    loyalty_message += _t("Customer code: ") + current_client.barcode + "\n";
                }
                if (new_points) {
                    loyalty_message += _t("New loyalty points: ") + new_points + "\n";
                }
                if (loyalty_points) {
                    loyalty_message += _t("Total loyalty points: ") + loyalty_points + "\n";
                }
            }

            if (loyalty_message) {
                if (!receipt.footer) {
                    receipt.footer = "";
                }
                receipt.footer += loyalty_message;
            }

            return this._super(receipt);
        },
    });
});
