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

            async sendToFP90Printer(order) {
                if (this.env.pos.config.printer_ip && !order.is_to_invoice()) {
                    // TODO self.chrome does not exists
                    // this.chrome.loading_show();
                    // this.chrome.loading_message(_t('Connecting to the fiscal printer'));
                    if (
                        order.has_refund &&
                        this.env.pos.context &&
                        this.env.pos.context.refund_details
                    ) {
                        order.refund_date = this.env.pos.context.refund_date;
                        order.refund_report = this.env.pos.context.refund_report;
                        order.refund_doc_num = this.env.pos.context.refund_doc_num;
                        order.refund_cash_fiscal_serial =
                            this.env.pos.context.refund_cash_fiscal_serial;
                    }

                    var printer_options = order.getPrinterOptions();
                    printer_options.order = order;
                    var receipt = order.export_for_printing();
                    var fp90 = new eposDriver(printer_options, this);
                    await fp90.printFiscalReceipt(receipt);
                    await new Promise((resolve) => setTimeout(resolve, 2000));
                    // This line causes problems on bill split. What's the sense of deleting the actual pos context?!
                    // It regenerates orders which are already partly paid using split function...
                    // this.env.pos.context = {};
                }
            }

            async _finalizeValidation() {
                var currentOrder = this.currentOrder;
                await this.sendToFP90Printer(currentOrder);
                await super._finalizeValidation();
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
