odoo.define("fiscal_epos_print.PaymentScreen", function (require) {
    "use strict";

    var core = require("web.core");
    var epson_epos_print = require("fiscal_epos_print.epson_epos_print");
    var _t = core._t;
    var eposDriver = epson_epos_print.eposDriver;
    const Registries = require("point_of_sale.Registries");
    const PaymentScreen = require("point_of_sale.PaymentScreen");

    const MyPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            show() {
                _super.apply(this, arguments);
                if (this.pos.config.printer_ip) {
                    var currentOrder = this.env.pos.get_order();
                    var printer_options = currentOrder.getPrinterOptions();
                    var fp90 = new eposDriver(printer_options, this);
                    var amount = this.format_currency(
                        currentOrder.get_total_with_tax()
                    );
                    fp90.printDisplayText(_t("SubTotal") + " " + amount);
                }
            }

            sendToFP90Printer(receipt, printer_options) {
                var fp90 = new eposDriver(printer_options, this);
                fp90.printFiscalReceipt(receipt);
            }

            _finalizeValidation() {
                // We need to get currentOrder before calling the _super()
                // otherwise we will likely get a empty order when we want to skip
                // the receipt preview
                var currentOrder = this.env.pos.get("selectedOrder");
                super._finalizeValidation(...arguments);
                if (this.env.pos.config.printer_ip && !currentOrder.is_to_invoice()) {
                    // TODO self.chrome does not exists
                    // this.chrome.loading_show();
                    // this.chrome.loading_message(_t('Connecting to the fiscal printer'));
                    var printer_options = currentOrder.getPrinterOptions();
                    printer_options.order = currentOrder;
                    var receipt = currentOrder.export_for_printing();
                    this.sendToFP90Printer(receipt, printer_options);
                }
            }

            _isOrderValid(isForceValidate) {
                if (this.env.pos.config.iface_tax_included == "subtotal") {
                    this.showPopup("ErrorPopup", {
                        title: _t("Wrong tax configuration"),
                        body: _t(
                            "Product prices on receipts must be set to 'Tax-Included Price' in POS configuration"
                        ),
                    });
                    return false;
                }
                var self = this;
                var receipt = this.env.pos.get_order();
                if (
                    receipt.has_refund &&
                    (receipt.refund_date == null ||
                        receipt.refund_date === "" ||
                        receipt.refund_doc_num == null ||
                        receipt.refund_doc_num == "" ||
                        receipt.refund_cash_fiscal_serial == null ||
                        receipt.refund_cash_fiscal_serial == "" ||
                        receipt.refund_report == null ||
                        receipt.refund_report == "")
                ) {
                    this.showPopup("ErrorPopup", {
                        title: _t("Refund Information Not Present"),
                        body: _t(
                            "The refund information aren't present. Please insert them before printing the receipt"
                        ),
                    });
                    return false;
                }
                return super._isOrderValid(isForceValidate);
            }
        };

    Registries.Component.extend(PaymentScreen, MyPaymentScreen);

    return PaymentScreen;
});
