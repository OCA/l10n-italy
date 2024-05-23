odoo.define("fiscal_epos_print.models", function (require) {
    "use strict";

    var {PosGlobalState, Order, Orderline, Payment} = require("point_of_sale.models");
    const {Gui} = require("point_of_sale.Gui");
    var core = require("web.core");
    var _t = core._t;
    const Registries = require("point_of_sale.Registries");

    const FiscalEposPrintPosGlobalState = (PosGlobalState) =>
        class FiscalEposPrintPosGlobalState extends PosGlobalState {
            set_refund_data(
                refund_date,
                refund_report,
                refund_doc_num,
                refund_cash_fiscal_serial,
                refund_full_refund
            ) {
                const selectedOrder = this.get_order();
                selectedOrder.refund_date = refund_date;
                selectedOrder.refund_report = refund_report;
                selectedOrder.refund_doc_num = refund_doc_num;
                selectedOrder.refund_cash_fiscal_serial = refund_cash_fiscal_serial;
                selectedOrder.refund_full_refund = refund_full_refund;
            }

            set_lottery_code_data(lottery_code) {
                const selectedOrder = this.get_order();
                selectedOrder.lottery_code = lottery_code;
            }

            reset_cashier() {
                this.cashier = {
                    name: null,
                    id: null,
                    barcode: null,
                    user_id: null,
                    pin: null,
                    role: null,
                    fiscal_operator_number: null,
                };
            }
        };
    Registries.Model.extend(PosGlobalState, FiscalEposPrintPosGlobalState);

    const FiscalEposPrintOrder = (Order) =>
        class FiscalEposPrintOrder extends Order {
            constructor() {
                super(...arguments);
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
                this.fiscal_printer_serial =
                    this.pos.config.fiscal_printer_serial || null;
                this.fiscal_printer_debug_info = null;
                try {
                    if (this.pos.config.module_pos_hr) {
                        this.fiscal_operator_number =
                            this.pos.cashier.fiscal_operator_number || null;
                    } else {
                        this.fiscal_operator_number = "1";
                    }
                } catch (error) {
                    this.fiscal_operator_number = "1";
                }
            }

            // Manages the case in which after printing an invoice
            // you pass a barcode in the mask of the registered invoice
            add_product(product, options) {
                if (this._printed || this.finalized === true) {
                    this.destroy();
                    return this.pos.get_order().add_product(product, options);
                }
                return super.add_product(...arguments);
            }

            check_order_has_refund() {
                var order = this.pos.get_order();
                if (order) {
                    var lines = order.orderlines;
                    order.has_refund =
                        lines.find(function (line) {
                            return line.quantity < 0.0;
                        }) !== undefined;
                    if (order.has_refund) {
                        order.refund_report = this.name.substr(-4);
                        order.refund_doc_num = this.name.substr(-4);
                        order.refund_date = new Date();
                        order.refund_cash_fiscal_serial =
                            this.pos.config.fiscal_printer_serial;
                    }
                }
            }

            init_from_JSON(json) {
                super.init_from_JSON(...arguments);
                this.check_order_has_refund();
                this.lottery_code = json.lottery_code;
                this.refund_report = json.refund_report;
                this.refund_date = json.refund_date;
                this.refund_doc_num = json.refund_doc_num;
                this.refund_cash_fiscal_serial = json.refund_cash_fiscal_serial;
                this.refund_full_refund = json.refund_full_refund;
                this.fiscal_receipt_number = json.fiscal_receipt_number;
                this.fiscal_receipt_amount = json.fiscal_receipt_amount;
                this.fiscal_receipt_date = json.fiscal_receipt_date;
                this.fiscal_z_rep_number = json.fiscal_z_rep_number;
                this.fiscal_printer_serial = this.pos.config.fiscal_printer_serial;
                this.fiscal_printer_debug_info = json.fiscal_printer_debug_info;
                try {
                    if (this.pos.config.module_pos_hr && json.employee_id) {
                        this.fiscal_operator_number =
                            this.pos.employee_by_id[json.employee_id]
                                .fiscal_operator_number || null;
                    } else {
                        this.fiscal_operator_number = "1";
                    }
                } catch (error) {}
            }

            export_as_JSON() {
                const json = super.export_as_JSON(...arguments);
                this.check_order_has_refund();
                json.lottery_code = this.lottery_code || null;
                json.refund_report = this.refund_report || null;
                json.refund_date = this.refund_date || null;
                json.refund_doc_num = this.refund_doc_num || null;
                json.refund_cash_fiscal_serial = this.refund_cash_fiscal_serial || null;
                json.refund_full_refund = this.refund_full_refund || false;
                json.fiscal_receipt_number = this.fiscal_receipt_number || null;
                json.fiscal_receipt_amount = this.fiscal_receipt_amount || null;
                // Parsed by backend
                json.fiscal_receipt_date = this.fiscal_receipt_date || null;
                json.fiscal_z_rep_number = this.fiscal_z_rep_number || null;
                json.fiscal_printer_serial = this.fiscal_printer_serial || null;
                json.fiscal_printer_debug_info = this.fiscal_printer_debug_info || null;
                try {
                    if (this.pos.config.module_pos_hr) {
                        json.fiscal_operator_number =
                            this.pos.cashier.fiscal_operator_number || null;
                    } else {
                        json.fiscal_operator_number = "1";
                    }
                } catch (error) {}
                return json;
            }

            export_for_printing() {
                var json = super.export_for_printing(...arguments);
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
            }

            getPrinterOptions() {
                var protocol = this.pos.config.use_https ? "https://" : "http://";
                var printer_url =
                    protocol + this.pos.config.printer_ip + "/cgi-bin/fpmate.cgi";
                return {url: printer_url};
            }
        };
    Registries.Model.extend(Order, FiscalEposPrintOrder);

    const FiscalEposPrintOrderline = (Orderline) =>
        class FiscalEposPrintOrderline extends Orderline {
            export_for_printing() {
                var receipt = super.export_for_printing(...arguments);

                receipt.tax_department = this.get_tax_details_r();
                if (!receipt.tax_department) {
                    Gui.showPopup("ErrorPopup", {
                        title: _t("Network error"),
                        body: _t("Manca iva su prodotto"),
                    });
                }
                if (receipt.tax_department) {
                    if (receipt.tax_department.included_in_price === true) {
                        receipt.full_price = this.price;
                    } else {
                        // This strategy was used because JavaScript's Math.round rounds to the nearest integer
                        const dec_precision = this.pos.currency.decimal_places;
                        const full_price = Number(
                            (
                                this.price *
                                (1 + receipt.tax_department.tax_amount / 100)
                            ).toFixed(dec_precision)
                        );
                        const rounding_factor = Math.pow(10, dec_precision);
                        receipt.full_price =
                            Math.trunc(full_price * rounding_factor) / rounding_factor;
                    }
                }

                return receipt;
            }

            get_tax_details_r() {
                var detail = this.get_all_prices().taxDetails;
                for (var i in detail) {
                    return {
                        code: this.pos.taxes_by_id[i].fpdeptax,
                        taxname: this.pos.taxes_by_id[i].name,
                        included_in_price: this.pos.taxes_by_id[i].price_include,
                        tax_amount: this.pos.taxes_by_id[i].amount,
                    };
                }
                // TODO is this correct?
                Gui.showPopup("ErrorPopup", {
                    title: _t("Error"),
                    body: _t("No taxes found"),
                });
            }

            set_quantity(quantity) {
                if (quantity === "0") {
                    // Epson FP doesn't allow lines with quantity 0
                    quantity = "remove";
                }
                return super.set_quantity(...arguments);
            }
        };
    Registries.Model.extend(Orderline, FiscalEposPrintOrderline);

    /*
    Overwrite Payment.export_for_printing() in order
    to make it export the payment type that must be passed
    to the fiscal printer.
    */
    const FiscalEposPrintPayment = (Payment) =>
        class FiscalEposPrintPayment extends Payment {
            constructor() {
                super(...arguments);
                this.type = this.payment_method.fiscalprinter_payment_type || null;
                this.type_index =
                    this.payment_method.fiscalprinter_payment_index || null;
            }
            export_as_JSON() {
                const json = super.export_as_JSON(...arguments);
                json.type = this.payment_method.fiscalprinter_payment_type;
                json.type_index = this.payment_method.fiscalprinter_payment_index;
                return json;
            }
            init_from_JSON(json) {
                super.init_from_JSON(...arguments);
                this.type = json.type;
                this.type_index = json.type_index;
            }
            setFiscalprinterType(value) {
                this.type = value;
            }
            setFiscalprinterIdex(value) {
                this.type_index = value;
            }
            export_for_printing() {
                const res = super.export_for_printing(...arguments);
                res.type = this.type;
                res.type_index = this.type_index;
                return res;
            }
        };
    Registries.Model.extend(Payment, FiscalEposPrintPayment);
});
