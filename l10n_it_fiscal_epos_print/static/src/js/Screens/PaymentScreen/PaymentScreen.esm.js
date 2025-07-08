import {PaymentScreen} from "@point_of_sale/app/screens/payment_screen/payment_screen";
import {_t} from "@web/core/l10n/translation";
import {AlertDialog} from "@web/core/confirmation_dialog/confirmation_dialog";
import {patch} from "@web/core/utils/patch";
import {EpsonEposPrint} from "../../epson_epos_print.esm";

patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.dialog = this.env.services.dialog;

        // Print Subtotal on screen if printer IP is configured
        if (this.pos.config.printer_ip) {
            const currentOrder = this.pos.get_order();
            const printer_options = currentOrder.getPrinterOptions();
            this.fp90 = new EpsonEposPrint(printer_options, this);
            const amount = currentOrder.get_total_with_tax().toFixed(2) + " €";
            this.fp90.printDisplayText(_t("SubTotal") + " " + amount);
        }
    },

    async sendToFP90Printer(order) {
        order.recomputeOrderData();
        this.fp90.order = order;
        await this.fp90.printFiscalReceipt(order);
    },

    async _finalizeValidation() {
        const currentOrder = this.currentOrder;
        if (this.pos.config.printer_ip && !currentOrder.is_to_invoice()) {
            await this.sendToFP90Printer(currentOrder);
            if (currentOrder._printed) {
                await super._finalizeValidation();
            }
        } else {
            await super._finalizeValidation();
        }
    },

    _isOrderValid(isForceValidate) {
        // Validate tax configuration
        if (this.pos.config.iface_tax_included === "subtotal") {
            this.dialog.add(AlertDialog, {
                title: _t("Wrong tax configuration"),
                body: _t(
                    "Product prices on receipts must be set to 'Tax-Included Price' in POS configuration"
                ),
            });
            return false;
        }

        const receipt = this.pos.get_order();

        // Check if order has refund items
        receipt.check_order_has_refund();

        // Validate refund information - simplified like Odoo 12
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
            this.dialog.add(AlertDialog, {
                title: _t("Refund Information Not Present"),
                body: _t(
                    "The refund information isn't present. Please insert them before printing the receipt."
                ),
            });
            return false;
        }

        return super._isOrderValid(isForceValidate);
    },
});
