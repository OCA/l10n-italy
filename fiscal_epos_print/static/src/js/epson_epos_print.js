odoo.define("fiscal_epos_print.epson_epos_print", function (require) {
    "use strict";

    var core = require("web.core");
    var utils = require("web.utils");
    // Var PosDB = require('point_of_sale.DB');
    // var rpc = require('web.rpc');
    var _t = core._t;
    var round_pr = utils.round_precision;

    const {Gui} = require("point_of_sale.Gui");

    function addPadding(str, padding = 4) {
        var pad = new Array(padding).fill(0).join("") + str;
        return pad.substr(pad.length - padding, padding);
    }

    function isErrorStatus(printerStatus) {
        var error = false;
        switch (printerStatus.substring(0, 2)) {
            case "00":
            case "01":
            case "20":
            case "21":
                error = false;
                break;
            default:
                error = true;
        }
        return error;
    }

    // eslint-disable-next-line
    function decodeFpStatus(printerStatus) {
        var printer = "";
        var ej = "";
        var receipt = "";

        switch (printerStatus.substring(0, 1)) {
            case "0":
                printer = false;
                break;
            case "2":
                printer = _t("Paper running low");
                break;
            case "3":
                printer = _t("Offline (end of paper or open cover)");
                break;
            default:
                printer = _t("Wrong answer");
        }

        switch (printerStatus.substring(1, 2)) {
            case "0":
                ej = false;
                break;
            case "1":
                ej = _t("Running low");
                break;
            case "2":
                ej = _t("To format");
                break;
            case "3":
                ej = _t("Previous");
                break;
            case "4":
                ej = _t("From other measurement device");
                break;
            case "5":
                ej = _t("Finished");
                break;
            default:
                ej = _t("Wrong answer");
        }

        switch (printerStatus.substring(3, 4)) {
            case "0":
                receipt = _t("Fiscal open");
                break;
            case "1":
                receipt = false;
                // Receipt = "Fiscale/Non fiscale chiuso";
                break;
            case "2":
                receipt = _t("Non fiscal open");
                break;
            case "3":
                receipt = _t("Payment in progress");
                break;
            case "4":
                receipt = _t(
                    "Error on last ESC/POS command with Fiscal/Non fiscal closed"
                );
                break;
            case "5":
                receipt = _t("Negative receipt");
                break;
            case "6":
                receipt = _t("Error on last ESC/POS command with Non fiscal open");
                break;
            case "7":
                receipt = _t("Waiting for receipt closing in JAVAPOS mode");
                break;
            case "8":
                receipt = _t("Fiscal document open");
                break;
            case "A":
                receipt = _t("Title open");
                break;
            case "B":
                receipt = _t("Title closed");
                break;
            default:
                receipt = _t("Wrong answer");
        }

        return printer || ej || receipt;
    }

    function getStatusField(tag) {
        return tag === "printerStatus" || tag === "fsStatus";
    }

    var eposDriver = core.Class.extend({
        init: function (options, sender) {
            var self = this;
            var opts = options || {};
            this.url = opts.url || "http://192.168.1.1/cgi-bin/fpmate.cgi";
            // eslint-disable-next-line
            this.fiscalPrinter = new epson.fiscalPrint();
            this.sender = sender;
            this.order = opts.order || null;
            // eslint-disable-next-line
            this.fiscalPrinter.onreceive = function (res, tag_list_names, add_info) {
                // TODO not exist
                // sender.chrome.loading_hide();
                var tagStatus = tag_list_names
                    ? tag_list_names.filter(getStatusField)
                    : [];
                var msgPrinter = "";
                var info = "";

                if (tagStatus.length > 0 && res.success) {
                    info = add_info[tagStatus[0]];
                    res.success = !isErrorStatus(info);
                }

                var order = "";
                if (!res.success) {
                    if (self.order !== null) {
                        order = self.order;
                        order.fiscal_printer_debug_info =
                            JSON.stringify(res) +
                            "\n" +
                            JSON.stringify(tag_list_names) +
                            "\n" +
                            JSON.stringify(add_info);
                        // Sender.env.pos.push_single_order(order);
                    }
                    if (tagStatus.length > 0) {
                        info = add_info[tagStatus[0]];
                        msgPrinter = decodeFpStatus(info);
                    }
                    // TODO
                    // sender.chrome.screens['receipt'].lock_screen(true);
                    // TODO is this correct?
                    Gui.showPopup("ErrorPopup", {
                        title: _t("Connection to the printer failed"),
                        body:
                            _t(
                                "An error happened while sending data to the printer. Error code: "
                            ) +
                            (res.code || "") +
                            "\n" +
                            _t("Error Message: ") +
                            msgPrinter,
                    });
                    return;
                }

                if (add_info.responseCommand === "1138") {
                    // Coming from FiscalPrinterADEFilesButtonWidget
                    var to_be_sent =
                        add_info.responseData[9] +
                        add_info.responseData[10] +
                        add_info.responseData[11] +
                        add_info.responseData[12];
                    var old =
                        add_info.responseData[13] +
                        add_info.responseData[14] +
                        add_info.responseData[15] +
                        add_info.responseData[16];
                    var rejected =
                        add_info.responseData[17] +
                        add_info.responseData[18] +
                        add_info.responseData[19] +
                        add_info.responseData[20];
                    var msg =
                        _t("Files waiting to be sent: ") +
                        to_be_sent +
                        "; " +
                        _t("Old files: ") +
                        old +
                        "; " +
                        _t("Rejected files: ") +
                        rejected;
                    // TODO is this correct?
                    Gui.showPopup("ErrorPopup", {
                        title: _t("IRA files"),
                        body: msg,
                    });
                    return;
                }

                // Is it a receipt data?
                if (
                    add_info.fiscalReceiptNumber &&
                    add_info.fiscalReceiptAmount &&
                    add_info.fiscalReceiptDate &&
                    add_info.zRepNumber
                ) {
                    // TODO
                    // sender.chrome.screens['receipt'].lock_screen(false);
                    order = self.order;
                    order._printed = true;
                    if (!order.fiscal_receipt_number) {
                        order.fiscal_receipt_number = parseInt(
                            add_info.fiscalReceiptNumber,
                            10
                        );
                        order.fiscal_receipt_amount = parseFloat(
                            add_info.fiscalReceiptAmount.replace(",", ".")
                        );
                        var fiscalReceiptDate = new Date(
                            add_info.fiscalReceiptDate.replace(
                                /(\d{1,2})\/(\d{1,2})\/(\d{4})/,
                                "$3/$2/$1"
                            )
                        );
                        order.fiscal_receipt_date =
                            moment(fiscalReceiptDate).format("YYYY-MM-DD");
                        order.fiscal_z_rep_number = add_info.zRepNumber;
                        order.fiscal_printer_serial =
                            sender.env.pos.config.fiscal_printer_serial;
                        // Sender.env.pos.db.add_order(order.export_as_JSON());
                        // Try to save the order
                        // sender.env.pos.push_single_order(order);
                    }
                    if (sender.env.pos.config.fiscal_cashdrawer) {
                        self.printOpenCashDrawer();
                        self.resetPrinter();
                    }
                    if (!sender.env.pos.config.show_receipt_when_printing) {
                        // TODO
                        // sender.chrome.screens['receipt'].click_next();
                    }
                    return;
                }
            };
            this.fiscalPrinter.onerror = function () {
                // TODO not exist
                // sender.chrome.loading_hide();
                // sender.chrome.screens['receipt'].lock_screen(true);
                // TODO is this correct?
                Gui.showPopup("ErrorPopup", {
                    title: _t("Network error"),
                    body: _t("Printer can not be reached"),
                });
            };
        },

        encodeXml: function (string) {
            var xml_special_to_escaped_one_map = {
                "&": "&amp;",
                '"': "&quot;",
                "<": "&lt;",
                ">": "&gt;",
            };

            // eslint-disable-next-line
            return string.replace(/([\&"<>])/g, function (str, item) {
                return xml_special_to_escaped_one_map[item];
            });
        },

        /*
          Prints a sale item line.
        */
        printRecItem: function (args) {
            var tag =
                "<printRecItem" +
                ' description="' +
                this.encodeXml(args.description || "") +
                '"' +
                ' quantity="' +
                (args.quantity || "1") +
                '"' +
                ' unitPrice="' +
                (args.unitPrice || "") +
                '"' +
                ' department="' +
                (args.department || "1") +
                '"' +
                ' justification="' +
                (args.justification || "1") +
                '"' +
                ' operator="' +
                (args.operator || "1") +
                '"' +
                " />";
            return tag;
        },

        /*
          Prints a sale refund item line.
        */
        printFiscalRefundDetails: function (args) {
            var message =
                "REFUND " +
                addPadding(args.refund_report) +
                " " +
                addPadding(args.refund_doc_num) +
                " " +
                // Day
                args.refund_date.substr(8, 2) +
                // Month
                args.refund_date.substr(5, 2) +
                // Year
                args.refund_date.substr(0, 4) +
                " " +
                args.refund_cash_fiscal_serial;

            var tag =
                "<printRecMessage" +
                ' messageType="4" message="' +
                this.encodeXml(message) +
                '" font="1" index="1"' +
                ' operator="' +
                (args.operator || "1") +
                '"' +
                " />";
            return tag;
        },

        printFiscalVoidDetails: function (args) {
            var message =
                "VOID " +
                addPadding(args.refund_report) +
                " " +
                addPadding(args.refund_doc_num) +
                " " +
                // Day
                args.refund_date.substr(8, 2) +
                // Month
                args.refund_date.substr(5, 2) +
                // Year
                args.refund_date.substr(0, 4) +
                " " +
                args.refund_cash_fiscal_serial;

            var tag =
                "<printRecMessage" +
                ' messageType="4" message="' +
                this.encodeXml(message) +
                '" font="1" index="1"' +
                ' operator="' +
                (args.operator || "1") +
                '"' +
                " />";
            return tag;
        },

        /*
          Prints a sale refund item line.
          Prints refund items on a commercial refund document if flag SET 14/58 = 1 (from display 3333 > 14 > 58 > X).
        */
        printRecRefund: function (args) {
            var tag =
                "<printRecRefund" +
                ' description="' +
                this.encodeXml(args.description || "") +
                '"' +
                ' quantity="' +
                (args.quantity || "1") +
                '"' +
                ' unitPrice="' +
                (args.unitPrice || "") +
                '"' +
                ' department="' +
                (args.department || "1") +
                '"' +
                ' justification="' +
                (args.justification || "1") +
                '"' +
                ' operator="' +
                (args.operator || "1") +
                '"' +
                " />";
            return tag;
        },

        /*
          Adds a discount to the last line.
        */
        printRecItemAdjustment: function (args) {
            var tag =
                "<printRecItemAdjustment" +
                ' operator="' +
                (args.operator || "1") +
                '"' +
                ' adjustmentType="' +
                (args.adjustmentType || 0) +
                '"' +
                ' description="' +
                this.encodeXml(args.description || "") +
                '"' +
                ' amount="' +
                (args.amount || "") +
                '"' +
                ' department="' +
                (args.department || "") +
                '"' +
                ' justification="' +
                (args.justification || "2") +
                '"' +
                " />";
            return tag;
        },

        /*
          Prints a payment.
        */
        printRecTotal: function (args) {
            var tag =
                "<printRecTotal" +
                ' operator="' +
                (args.operator || "1") +
                '"' +
                ' description="' +
                this.encodeXml(args.description || _t("Payment")) +
                '"' +
                ' payment="' +
                (args.payment || "") +
                '"' +
                ' paymentType="' +
                (args.paymentType || "0") +
                '"' +
                ' index="' +
                (args.paymentIndex || "0") +
                '"' +
                " />";
            return tag;
        },

        printRecTotalRefund: function (args) {
            var tag =
                "<printRecTotal" +
                ' operator="' +
                (args.operator || "1") +
                '"' +
                ' description="' +
                this.encodeXml(args.description || _t("Payment")) +
                '"' +
                ' payment="' +
                (args.payment || "") +
                '"' +
                ' paymentType="' +
                (args.paymentType || "0") +
                '"' +
                ' index="' +
                (args.paymentIndex || "1") +
                '"' +
                ' justification="' +
                (args.paymentJustification || "2") +
                '"' +
                " />";
            return tag;
        },

        /*
          Prints a rounding
        */
        printRounding: function (args) {
            var tag =
                "<printRecSubtotalAdjustment" +
                ' operator="' +
                (args.operator || "1") +
                '"' +
                ' adjustmentType="0"' +
                ' description="' +
                this.encodeXml(args.description || _t("Rounding")) +
                '"' +
                ' amount="' +
                (args.amount || "") +
                '"' +
                ' justification="2" />';
            return tag;
        },

        // Remember that the header goes after <printerFiscalReceipt>
        // but before <beginFiscalReceipt /> otherwise it will not be printed
        // as additional header messageType=1
        printFiscalReceiptHeader: function (receipt) {
            var self = this;
            var msg = "";
            if (receipt.header !== "" && receipt.header.length > 0) {
                var hdr = receipt.header.split(/\r\n|\r|\n/);
                _.each(hdr, function (m, i) {
                    msg +=
                        "<printRecMessage" +
                        ' messageType="1" message="' +
                        self.encodeXml(m) +
                        '" font="1" index="' +
                        (i + 1) +
                        '"' +
                        ' operator="' +
                        (receipt.fiscal_operator_number || "1") +
                        '" />';
                });
            }
            return msg;
        },

        // Remember that the footer goes within <printerFiscalReceipt><beginFiscalReceipt />
        // as PROMO code messageType=3
        printFiscalReceiptFooter: function (receipt) {
            var self = this;
            var msg = "";
            if (receipt.footer !== "" && receipt.footer.length > 0) {
                var hdr = receipt.footer.split(/\r\n|\r|\n/);
                _.each(hdr, function (m, i) {
                    msg +=
                        "<printRecMessage" +
                        ' messageType="3" message="' +
                        self.encodeXml(m) +
                        '" font="1" index="' +
                        (i + 1) +
                        '"' +
                        ' operator="' +
                        (receipt.fiscal_operator_number || "1") +
                        '" />';
                });
            }
            return msg;
        },

        printDisplayText: function (msg) {
            var xml =
                "<printerCommand>" +
                "<displayText " +
                ' operator="1" text="' +
                this.encodeXml(msg || "") +
                '"' +
                " /></printerCommand>";
            this.fiscalPrinter.send(this.url, xml);
        },

        /*
        Print the order.id into fiscal receipt for the refund
        */
        printOrderId: function (receipt) {
            var message = receipt.name;
            var tag =
                "<printRecMessage" +
                ' messageType="3" message="' +
                this.encodeXml(message) +
                '" font="1" index="4"' +
                ' operator="' +
                (receipt.fiscal_operator_number || "1") +
                '"' +
                " />";
            return tag;
        },

        /*
          Prints info payment customer
        */
        printInfoPaymentCustomer: function (receipt) {
            var tag =
                '<printRecMessage operator="' +
                (receipt.fiscal_operator_number || "1") +
                '" message="------------------" messageType="3" index="5" font="2" />';
            var index = 5;
            _.each(receipt.ticket.split("<br />"), function (msg) {
                index += 1;
                tag +=
                    "<printRecMessage " +
                    'operator="' +
                    (receipt.fiscal_operator_number || "1") +
                    '"' +
                    ' messageType="3" message="' +
                    msg +
                    '" font="1" index="' +
                    index.toString() +
                    '" />';
            });
            return tag;
        },

        /*
          Prints a receipt
        */
        printFiscalReceipt: function (receipt) {
            var self = this;
            var has_refund = _.every(receipt.orderlines, function (line) {
                return line.quantity < 0;
            });
            var xml = "<printerFiscalReceipt>";
            var fiscal_operator = receipt.fiscal_operator_number || "1";
            // Header must be printed before beginning a fiscal receipt
            if (!receipt.refund_full_refund) {
                xml += this.printFiscalReceiptHeader(receipt);
            }
            if (has_refund) {
                if (receipt.refund_full_refund) {
                    xml += this.printFiscalVoidDetails({
                        refund_date: receipt.refund_date,
                        refund_report: receipt.refund_report,
                        refund_doc_num: receipt.refund_doc_num,
                        refund_cash_fiscal_serial: receipt.refund_cash_fiscal_serial,
                        operator: fiscal_operator,
                    });
                } else {
                    xml += this.printFiscalRefundDetails({
                        refund_date: receipt.refund_date,
                        refund_report: receipt.refund_report,
                        refund_doc_num: receipt.refund_doc_num,
                        refund_cash_fiscal_serial: receipt.refund_cash_fiscal_serial,
                        operator: fiscal_operator,
                    });
                }
            }
            xml += '<beginFiscalReceipt operator="' + fiscal_operator + '" />';

            _.each(receipt.orderlines, function (l) {
                if (l.price >= 0) {
                    if (l.quantity >= 0) {
                        if (l.discount < 100) {
                            xml += self.printRecItem({
                                description: l.product_name,
                                quantity: l.quantity,
                                unitPrice: round_pr(
                                    l.full_price,
                                    self.sender.env.pos.currency.rounding
                                ),
                                department: l.tax_department.code,
                                operator: fiscal_operator,
                            });
                            if (l.discount) {
                                xml += self.printRecItemAdjustment({
                                    adjustmentType: 0,
                                    description:
                                        _t("Discount") + " " + l.discount + "%",
                                    amount: round_pr(
                                        l.quantity * l.full_price - l.price_display,
                                        self.sender.env.pos.currency.rounding
                                    ),
                                    operator: fiscal_operator,
                                });
                            }
                        }
                    } else {
                        xml += self.printRecRefund({
                            description: _t("Refund: ") + l.product_name,
                            quantity: l.quantity * -1.0,
                            unitPrice: round_pr(
                                l.price,
                                self.sender.env.pos.currency.rounding
                            ),
                            department: l.tax_department.code,
                            operator: fiscal_operator,
                        });

                        // TODO This line of code is added by us, check if it's right
                        // xml += self.printRecItem({
                        //     description: _t("Refund cash"),
                        //     quantity: l.quantity,
                        //     unitPrice: round_pr(
                        //         l.price,
                        //         self.sender.env.pos.currency.rounding
                        //     ),
                        //     department: l.tax_department.code,
                        //     operator: fiscal_operator,
                        // });
                    }
                } else {
                    xml += self.printRecItemAdjustment({
                        adjustmentType: 3,
                        description: l.product_name,
                        department: l.tax_department.code,
                        amount: -l.price,
                        operator: fiscal_operator,
                    });
                }
            });
            // Footer can go only as promo code so within a fiscal receipt body
            xml += this.printFiscalReceiptFooter(receipt);
            if (receipt.lottery_code) {
                // TX
                // 1 135   OP   ID CODE   NU
                // Example: 113501ABCDEFGN        0000
                // Pad with spaces to make the code field always 16 characters.
                xml +=
                    '<directIO command="1135" data="01' +
                    receipt.lottery_code.padEnd(16, " ") +
                    '0000" />';
            }
            if (receipt.rounding_applied !== 0 && !has_refund) {
                xml += self.printRounding({
                    amount: Math.abs(
                        round_pr(
                            receipt.rounding_applied,
                            self.sender.env.pos.currency.rounding
                        )
                    ),
                    operator: fiscal_operator,
                });
                xml +=
                    '<printRecSubtotal operator="' +
                    fiscal_operator +
                    '" option="1" />';
            }
            // TODO is always the same Total for refund and payments?
            receipt.ticket = "";
            _.each(receipt.paymentlines, function (l) {
                // Set ticket
                receipt.ticket += l.ticket;
                // Amount always positive because it's used for refund too
                if (has_refund) {
                    xml += self.printRecTotalRefund({
                        payment: Math.abs(l.amount),
                        paymentType: l.type,
                        paymentIndex: l.type_index,
                        description: l.journal,
                        operator: fiscal_operator,
                    });
                } else {
                    xml += self.printRecTotal({
                        payment: Math.abs(l.amount),
                        paymentType: l.type,
                        paymentIndex: l.type_index,
                        description: l.journal,
                        operator: fiscal_operator,
                    });
                }
            });
            xml += this.printOrderId(receipt);
            if (receipt.ticket) {
                xml += this.printInfoPaymentCustomer(receipt);
            }
            xml +=
                '<endFiscalReceipt operator="' +
                fiscal_operator +
                '" /></printerFiscalReceipt>';
            this.fiscalPrinter.send(this.url, xml);
            console.log(xml);
        },

        /*
        DON'T USE, this fiscal closure is forbid by Epson by default
        */
        printFiscalReport: function (f_op) {
            var xml = "<printerFiscalReport>";
            xml += '<printZReport operator="' + f_op + '" timeout="" />';
            xml += "</printerFiscalReport>";
            this.fiscalPrinter.send(this.url, xml);
        },

        /*
        It prints report and fiscal closure both
        */
        printFiscalXZReport: function (f_op) {
            var xml = "<printerFiscalReport>";
            xml +=
                '<displayText operator="' +
                f_op +
                '" data="Stampa chiusura giornaliera" />';
            xml += '<printXZReport operator="' + f_op + '" timeout="" />';
            xml += "</printerFiscalReport>";
            this.fiscalPrinter.send(this.url, xml);
        },

        printFiscalXReport: function (f_op) {
            var xml = "<printerFiscalReport>";
            xml += '<printXReport operator="' + f_op + '"/>';
            xml += "</printerFiscalReport>";
            this.fiscalPrinter.send(this.url, xml);
        },

        getStatusOfFilesForADE: function () {
            var xml = "<printerCommand>";
            xml += '<directIO command="1138" data="01" />';
            xml += "</printerCommand>";
            this.fiscalPrinter.send(this.url, xml);
        },

        /*
        It need to be logged in to print the duplicate, the pw in data is 0212345 plus 93 spaces, total 100 chars
        */
        printFiscalReprintLast: function (f_op) {
            var xml = "<printerCommand>";
            xml +=
                '<directIO command="4038" data="0212345" comment="Login password 0212345 followed by 93 spaces for a length of 100" />';
            xml += '<printDuplicateReceipt operator="' + f_op + '" />';
            xml += "</printerCommand>";
            this.fiscalPrinter.send(this.url, xml);
        },

        printOpenCashDrawer: function () {
            var xml = "<printerCommand>";
            xml += '<openDrawer operator="1"/>';
            xml += "</printerCommand>";
            this.fiscalPrinter.send(this.url, xml);
        },

        resetPrinter: function () {
            var xml = "<printerCommand>";
            xml += '<displayText operator="" data="Welcome" />';
            xml += '<resetPrinter operator="1" />';
            xml += "</printerCommand>";
            this.fiscalPrinter.send(this.url, xml);
        },
    });

    return {
        eposDriver: eposDriver,
    };
});
