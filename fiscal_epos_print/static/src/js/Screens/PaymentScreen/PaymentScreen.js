odoo.define("fiscal_epos_print.PaymentScreen", function (require) {
    "use strict";

    var core = require("web.core");
    var epson_epos_print = require("fiscal_epos_print.epson_epos_print");
    var _t = core._t;
    var eposDriver = epson_epos_print.eposDriver;
    const Registries = require("point_of_sale.Registries");
    const PaymentScreen = require("point_of_sale.PaymentScreen");

    // eslint-disable-next-line
    const MyPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            setup() {
                super.setup();
                if (this.env.pos.config.printer_ip) {
                    var currentOrder = this.env.pos.get_order();
                    var printer_options = currentOrder.getPrinterOptions();
                    var fp90 = new eposDriver(printer_options, this);
                    var amount = this.env.pos.format_currency(
                        currentOrder.get_total_with_tax()
                    );
                    fp90.printDisplayText(_t("SubTotal") + " " + amount);
                }
            }

            sendToFP90Printer(receipt, printer_options) {
                var fp90 = new eposDriver(printer_options, this);
                fp90.printFiscalReceipt(receipt);
                // This line causes problems on bill split. What's the sense of deleting the actual pos context?!
                // It regenerates orders wich are already partly paid using split function...
                // this.env.pos.context = {};
            }

            async _finalizeValidation() {
                // We need to get currentOrder before calling the _super()
                // otherwise we will likely get a empty order when we want to skip
                // the receipt preview
                var currentOrder = this.currentOrder;
                await super._finalizeValidation();
                if (this.env.pos.config.printer_ip && !currentOrder.is_to_invoice()) {
                    // TODO self.chrome does not exists
                    // this.chrome.loading_show();
                    // this.chrome.loading_message(_t('Connecting to the fiscal printer'));
                    if (
                        currentOrder.has_refund &&
                        this.env.pos.context &&
                        this.env.pos.context.refund_details
                    ) {
                        currentOrder.refund_date = this.env.pos.context.refund_date;
                        currentOrder.refund_report = this.env.pos.context.refund_report;
                        currentOrder.refund_doc_num =
                            this.env.pos.context.refund_doc_num;
                        currentOrder.refund_cash_fiscal_serial =
                            this.env.pos.context.refund_cash_fiscal_serial;
                    }

                    var printer_options = currentOrder.getPrinterOptions();
                    printer_options.order = currentOrder;
                    var receipt = currentOrder.export_for_printing();
                    this.sendToFP90Printer(receipt, printer_options);
                }
            }

            _isOrderValid(isForceValidate) {
                if (this.env.pos.config.iface_tax_included === "subtotal") {
                    this.showPopup("ErrorPopup", {
                        title: _t("Wrong tax configuration"),
                        body: _t(
                            "Product prices on receipts must be set to 'Tax-Included Price' in POS configuration"
                        ),
                    });
                    return false;
                }
                var receipt = this.env.pos.get_order();
                if (
                    receipt.has_refund &&
                    (receipt.refund_date === null ||
                        receipt.refund_date === "" ||
                        receipt.refund_doc_num === null ||
                        receipt.refund_doc_num === "" ||
                        receipt.refund_cash_fiscal_serial === null ||
                        receipt.refund_cash_fiscal_serial === "" ||
                        receipt.refund_report === null ||
                        receipt.refund_report === "")
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
