odoo.define("fiscal_epos_print.ReceiptScreen", function (require) {
    "use strict";

    var epson_epos_print = require("fiscal_epos_print.epson_epos_print");
    var eposDriver = epson_epos_print.eposDriver;
    const Registries = require("point_of_sale.Registries");
    const ReceiptScreen = require("point_of_sale.ReceiptScreen");

    // eslint-disable-next-line
    const MyReceiptScreen = (ReceiptScreen) =>
        class extends ReceiptScreen {
            lock_screen(locked) {
                super.lock_screen(...arguments);
                if (locked) {
                    this.$(".receipt-sent").hide();
                    this.$(".printing-error").show();
                    this.$(".printing-retry").show();
                } else {
                    this.$(".receipt-sent").show();
                    this.$(".printing-error").hide();
                    this.$(".printing-retry").hide();
                }
            }

            sendToFP90Printer(receipt, printer_options) {
                var fp90 = new eposDriver(printer_options, this);
                fp90.printFiscalReceipt(receipt);
            }

            render_receipt() {
                var self = this;
                this._super();
                this.$(".printing-retry").click(function () {
                    if (self._locked) {
                        var currentOrder = self.env.pos.get_order();
                        // TODO self.chrome does not exists
                        // self.chrome.loading_show();
                        // self.chrome.loading_message(_t('Connecting to the fiscal printer'));
                        var printer_options = currentOrder.getPrinterOptions();
                        printer_options.order = currentOrder;
                        var receipt = currentOrder.export_for_printing();
                        self.sendToFP90Printer(receipt, printer_options);
                    }
                });
            }
        };

    Registries.Component.extend(ReceiptScreen, MyReceiptScreen);

    return ReceiptScreen;
});
