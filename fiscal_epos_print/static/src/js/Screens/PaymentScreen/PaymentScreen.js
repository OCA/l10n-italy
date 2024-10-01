/** @odoo-module **/

import { useState } from "@odoo/owl";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { patch } from "@web/core/utils/patch";
import { EpsonEposPrint } from "../../epson_epos_print";


patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.state = useState({
            order: this.pos.get_order(),
        });

        // Print Subtotal on screen if printer IP is configured
        if (this.pos.config.printer_ip) {
            const currentOrder = this.state.order;
            const printer_options = currentOrder.getPrinterOptions();
            this.fp90 = new EpsonEposPrint(printer_options, this);
            const amount = parseFloat(currentOrder.get_total_with_tax()) + " €";
            this.fp90.printDisplayText(_t("SubTotal") + " " + amount);
        }
    },

    async sendToFP90Printer(order) {
        // If there is a printer IP and it's not an invoice, send the order to the fiscal printer
        if (this.pos.config.printer_ip && !order.is_to_invoice()) {

            // TODO
            // if (order.has_refund && this.pos.context && this.pos.context.refund_details) {
            //     order.refund_date = this.pos.context.refund_date;
            //     order.refund_report = this.pos.context.refund_report;
            //     order.refund_doc_num = this.pos.context.refund_doc_num;
            //     order.refund_cash_fiscal_serial = this.pos.context.refund_cash_fiscal_serial;
            // }

            const receipt = order.export_as_JSON();
            this.fp90.order = order
            await this.fp90.printFiscalReceipt(receipt);

            // TODO loading screen
            await new Promise(resolve => setTimeout(resolve, 2000));
        }
    },

    async _finalizeValidation() {
        const currentOrder = this.state.order;
        await this.sendToFP90Printer(currentOrder);
        await super._finalizeValidation();
    },

    _isOrderValid(isForceValidate) {
        // Validate tax configuration
        if (this.pos.config.iface_tax_included === "subtotal") {
            this.popup.add(ErrorPopup, {
                title: _t("Wrong tax configuration"),
                body: _t("Product prices on receipts must be set to 'Tax-Included Price' in POS configuration"),
            });
            return false;
        }

        const receipt = this.state.order;

        // TODO
        // // Validate refund information
        // if (
        //     receipt.has_refund &&
        //     (!receipt.refund_date ||
        //         !receipt.refund_doc_num ||
        //         !receipt.refund_cash_fiscal_serial ||
        //         !receipt.refund_report)
        // ) {
        //     this.popup.add(ErrorPopup, {
        //         title: _t("Refund Information Not Present"),
        //         body: _t("The refund information isn't present. Please insert them before printing the receipt."),
        //     });
        //     return false;
        // }

        return super._isOrderValid(isForceValidate);
    },
});

