/** @odoo-module **/

import { Order, Orderline, Payment } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { roundPrecision as round_pr } from "@web/core/utils/numbers";

// vedi PosStore, forse
// class FiscalEposPrintPosGlobalState extends PosGlobalState {
//     set_refund_data(refund_date, refund_report, refund_doc_num, refund_cash_fiscal_serial, refund_full_refund) {
//         const selectedOrder = this.get_order();
//         selectedOrder.refund_date = refund_date;
//         selectedOrder.refund_report = refund_report;
//         selectedOrder.refund_doc_num = refund_doc_num;
//         selectedOrder.refund_cash_fiscal_serial = refund_cash_fiscal_serial;
//         selectedOrder.refund_full_refund = refund_full_refund;
//     }

//     set_lottery_code_data(lottery_code) {
//         const selectedOrder = this.get_order();
//         selectedOrder.lottery_code = lottery_code;
//     }

//     reset_cashier() {
//         this.cashier = {
//             name: null,
//             id: null,
//             barcode: null,
//             user_id: null,
//             pin: null,
//             role: null,
//             fiscal_operator_number: null,
//         };
//     }
// }

// Register the extended PosGlobalState class
//registry.category("models").add("PosGlobalState", FiscalEposPrintPosGlobalState);

patch(Order.prototype, {
    setup() {
        super.setup(...arguments);
        this.lottery_code = null;
        this.refund_report = null;
        this.refund_date = null;
        this.refund_doc_num = null;
        this.refund_cash_fiscal_serial = null;
        this.refund_full_refund = false;
        this.has_refund = false;
        this.fiscal_receipt_number = null;
        this.fiscal_receipt_amount = null;
        this.fiscal_receipt_date = null;
        this.fiscal_z_rep_number = null;
        this.fiscal_printer_serial = this.pos.config.fiscal_printer_serial || null;
        this.fiscal_printer_debug_info = null;

        try {
            if (this.pos.config.module_pos_hr) {
                this.fiscal_operator_number = this.pos.cashier.fiscal_operator_number || "1";
            } else {
                this.fiscal_operator_number = "1";
            }
        } catch (error) {
            this.fiscal_operator_number = "1";
        }
    },

    // serve?
    // add_product(product, options) {
    //     if (this._printed || this.finalized === true) {
    //         this.destroy();
    //         return this.pos.get_order().add_product(product, options);
    //     }
    //     return super.add_product(product, options);
    // },

    // funziona? a cosa serve scrivere refund_report etc?
    // check_order_has_refund() {
    //     const order = this.pos.get_order();
    //     if (order) {
    //         const lines = order.orderlines;
    //         order.has_refund = lines.some((line) => line.quantity < 0.0);
    //         if (order.has_refund) {
    //             order.refund_report = this.name.substr(-4);
    //             order.refund_doc_num = this.name.substr(-4);
    //             order.refund_date = new Date();
    //             order.refund_cash_fiscal_serial = this.pos.config.fiscal_printer_serial;
    //         }
    //     }
    // },

    export_as_JSON() {
        var json = super.export_as_JSON(...arguments);
        json.lottery_code = this.lottery_code;
        json.refund_date = this.refund_date;
        json.refund_report = this.refund_report;
        json.refund_doc_num = this.refund_doc_num;
        json.refund_cash_fiscal_serial = this.refund_cash_fiscal_serial;
        json.refund_full_refund = this.refund_full_refund;
        json.fiscal_receipt_number = this.fiscal_receipt_number;
        json.fiscal_receipt_amount = this.fiscal_receipt_amount;
        json.fiscal_receipt_date = this.fiscal_receipt_date;
        json.fiscal_z_rep_number = this.fiscal_z_rep_number;
        json.fiscal_printer_serial = this.fiscal_printer_serial;
        json.fiscal_printer_debug_info = this.fiscal_printer_debug_info;
        try {
            json.fiscal_operator_number =
                this.pos.cashier.fiscal_operator_number || null;
        } catch (error) {}
        return json;
    },

    getPrinterOptions() {
        var protocol = this.pos.config.use_https ? "https://" : "http://";
        var printer_url =
            protocol + this.pos.config.printer_ip + "/cgi-bin/fpmate.cgi";
        return {url: printer_url};
    },
});


patch(Orderline.prototype, {
    export_as_JSON() {
        const line = super.export_as_JSON();
        line.tax_department = this.get_tax_details_r();

        if (!line.tax_department) {
            this.popup.add(ErrorPopup, {
                title: _t("Network error"),
                body: _t("No tax found for the product"),
            });
        }
        if (line.tax_department) {
            if (line.tax_department.included_in_price === true) {
                line.price_unit_incl = this.price;
            } else {
                // This strategy was used because JavaScript's Math.round rounds to the nearest integer
                const rounding = this.pos.currency.rounding;
                line.price_unit_incl = round_pr(
                    this.price * (1 + line.tax_department.tax_amount / 100), rounding
                );
            }
        }
        return line;
    },

    get_tax_details_r() {
        const detail = this.get_all_prices().taxDetails;
        for (const i in detail) {
            return {
                code: this.pos.taxes_by_id[i].fpdeptax,
                taxname: this.pos.taxes_by_id[i].name,
                included_in_price: this.pos.taxes_by_id[i].price_include,
                tax_amount: this.pos.taxes_by_id[i].amount,
            };
        }

        this.popup.add(ErrorPopup, {
            title: _t("Error"),
            body: _t("No taxes found"),
        });
    },
});


patch(Payment.prototype, {
    setup() {
        super.setup(...arguments);
    },

    // serve?
    // export_as_JSON() {
    //     const json = super.export_as_JSON();
    //     json.type = this.payment_method.fiscalprinter_payment_type;
    //     json.type_index = this.payment_method.fiscalprinter_payment_index;
    //     return json;
    // }

    export_as_JSON() {
        const res = super.export_as_JSON();
        res.fiscalprinter_payment_type = this.payment_method.fiscalprinter_payment_type || null;
        res.fiscalprinter_payment_index = this.payment_method.fiscalprinter_payment_index || null;
        res.payment_method_name = this.payment_method.name || null;
        return res;
    },
});
