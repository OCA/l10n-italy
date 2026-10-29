import {_t} from "@web/core/l10n/translation";
import {AlertDialog} from "@web/core/confirmation_dialog/confirmation_dialog";
import {roundPrecision as round_pr} from "@web/core/utils/numbers";

export class EpsonEposPrint {
    constructor(...args) {
        this.setup(...args);
    }
    setup(options, sender) {
        this.url = "http://192.168.1.1/cgi-bin/fpmate.cgi"; // Default value, see options
        this.order = null;
        this.pos = sender.pos;
        this.sender = sender;

        // Initialize the fiscal printer
        // eslint-disable-next-line no-undef
        this.fiscalPrinter = new epson.fiscalPrint();
        this.fiscalPrinter.onreceive = this.onReceive.bind(this);
        this.fiscalPrinter.onerror = this.onError.bind(this);
        this.dialog = sender.dialog;

        if (options) {
            this.url = options.url || this.url;
            this.order = options.order || null;
        }
    }

    getStatusField(tag) {
        return tag === "printerStatus" || tag === "fsStatus";
    }

    addPadding(str, padding = 4) {
        var pad = new Array(padding).fill(0).join("") + str;
        return pad.substring(pad.length - padding);
    }

    // Method to handle successful receipt
    onReceive(res, tagListNames, addInfo) {
        const tagStatus = tagListNames ? tagListNames.filter(this.getStatusField) : [];
        let msgPrinter = "";
        let info = "";
        let body_msg = "";
        let order_lines_msg = "";
        let order_payment_msg = "";

        if (tagStatus.length > 0 && res.success) {
            info = addInfo[tagStatus[0]];
            res.success = !this.isErrorStatus(info);
        }

        let order = "";
        if (!res.success) {
            if (this.order !== null) {
                order = this.order;
                order.fiscal_printer_debug_info =
                    JSON.stringify(res) +
                    "\n" +
                    JSON.stringify(tagListNames) +
                    "\n" +
                    JSON.stringify(addInfo);
                order_lines_msg = order.lines
                    .map(
                        (l) =>
                            `\n${l.get_full_product_name() || ""}, Quantity: ${l.get_quantity() || ""}, Price: ${l.price || ""}, Discount: ${l.discount || ""}`
                    )
                    .join(",");
                order_payment_msg = order.payment_ids
                    .map(
                        (l) =>
                            `\nType: ${l.payment_method_id ? l.payment_method_id.name : ""}, Amount: ${l.amount || ""}`
                    )
                    .join(",");
                // Save the order
                // this.pos.push_single_order(order);
            }

            if (tagStatus.length > 0) {
                info = addInfo[tagStatus[0]];
                msgPrinter = this.decodeFpStatus(info);
            }

            body_msg =
                `${_t("An error happened while sending data to the printer.\nError code: ")}${res.code || ""}` +
                `${_t("\nStatus: ")}${res.status || ""}` +
                `${_t("\nPrinter Code: ")}${info || ""}\n${_t("Error Message: ")}${msgPrinter}`;
            if (order) {
                body_msg +=
                    `\n${_t("Order Details.\nOrder lines: {")}${order_lines_msg}` +
                    `${_t(" }\nPayment Lines: {")}${order_payment_msg}` +
                    `${_t(" }\nTechnical details: \nXML: ")}${order.fp_xml}`;
            }
            if (this.dialog) {
                this.dialog.add(AlertDialog, {
                    title: _t("Connection to the printer failed"),
                    body: body_msg,
                });
            } else {
                // Printer error: body_msg
            }
            return;
        }

        // Additional logic for handling responseCommand or receipt data
        if (addInfo.responseCommand === "1138") {
            const toBeSent = addInfo.responseData.slice(9, 13).join("");
            const old = addInfo.responseData.slice(13, 17).join("");
            const rejected = addInfo.responseData.slice(17, 21).join("");
            const msg = `${_t("Files waiting to be sent: ")}${toBeSent}; ${_t("Old files: ")}${old}; ${_t("Rejected files: ")}${rejected}`;

            if (this.dialog) {
                this.dialog.add(AlertDialog, {
                    title: _t("IRA files"),
                    body: msg,
                });
            } else {
                // IRA files status: msg
            }
            return;
        }

        if (
            addInfo.fiscalReceiptNumber &&
            addInfo.fiscalReceiptAmount &&
            addInfo.fiscalReceiptDate &&
            addInfo.zRepNumber
        ) {
            // Process fiscal receipt details
            order = this.order;
            order._printed = true;

            if (!order.fiscal_receipt_number) {
                // Parse fiscal receipt number, handle "null" string
                const receiptNum = addInfo.fiscalReceiptNumber;
                order.fiscal_receipt_number =
                    receiptNum && receiptNum !== "null"
                        ? parseInt(receiptNum, 10)
                        : null;

                // Parse amount
                order.fiscal_receipt_amount =
                    parseFloat(addInfo.fiscalReceiptAmount.replace(",", ".")) || 0;

                // Parse date
                order.fiscal_receipt_date = addInfo.fiscalReceiptDate.replace(
                    /(\d{1,2})\/(\d{1,2})\/(\d{4})/,
                    "$3-$2-$1"
                );

                // Parse z report number, handle "null" string
                const zRepNum = addInfo.zRepNumber;
                order.fiscal_z_rep_number =
                    zRepNum && zRepNum !== "null" ? parseInt(zRepNum, 10) : null;

                order.fiscal_printer_serial =
                    this.pos.config.fiscal_printer_serial || null;
            }

            if (this.pos.config.fiscal_cashdrawer) {
                this.printOpenCashDrawer();
                this.resetPrinter();
            }

            if (!this.pos.config.show_receipt_when_printing) {
                // Navigate to the next screen
                // document.querySelector("div[name='done']").click();
            }
            return;
        }
    }

    // Method to handle errors
    onError() {
        if (this.dialog) {
            this.dialog.add(AlertDialog, {
                title: _t("Network error"),
                body: _t("Printer can not be reached"),
            });
        }
    }

    // Additional helper methods like encodeXml, printRecItem, etc.
    encodeXml(string) {
        const xmlSpecialMap = {
            "&": "&amp;",
            '"': "&quot;",
            "<": "&lt;",
            ">": "&gt;",
        };

        return string.replace(/([&"<>])/g, (str, item) => xmlSpecialMap[item]);
    }

    printFiscalReceipt(receipt) {
        const lines = receipt.lines;
        receipt.check_order_has_refund();
        const hasRefund = receipt.has_refund;
        let xml = "<printerFiscalReceipt>";
        const fiscalOperator = receipt.fiscal_operator_number || "1";

        // Header should be printed before the fiscal receipt starts
        if (!receipt.refund_full_refund) {
            xml += this.printFiscalReceiptHeader(receipt);
        }

        // If the receipt has refund
        if (hasRefund) {
            xml += receipt.refund_full_refund
                ? this.printFiscalVoidDetails({
                      refund_date: receipt.refund_date,
                      refund_report: receipt.refund_report,
                      refund_doc_num: receipt.refund_doc_num,
                      refund_cash_fiscal_serial: receipt.refund_cash_fiscal_serial,
                      operator: fiscalOperator,
                  })
                : this.printFiscalRefundDetails({
                      refund_date: receipt.refund_date,
                      refund_report: receipt.refund_report,
                      refund_doc_num: receipt.refund_doc_num,
                      refund_cash_fiscal_serial: receipt.refund_cash_fiscal_serial,
                      operator: fiscalOperator,
                  });
        }

        xml += `<beginFiscalReceipt operator="${fiscalOperator}" />`;

        // Iterate through each order line
        lines.forEach((l) => {
            // Skip if no line data
            if (!l) return;

            l.set_fp_data();
            const quantity = l.qty;
            const discount = parseFloat(l.discount) || 0;
            const productName = l.full_product_name || "";

            if (l.price_unit_incl >= 0) {
                if (quantity >= 0) {
                    xml += this.printRecItem({
                        description: productName,
                        quantity: quantity,
                        unitPrice: l.price_unit_incl.toFixed(2),
                        department: l.tax_department.fpdeptax,
                        operator: fiscalOperator,
                    });

                    if (discount > 0 && discount < 100) {
                        xml += this.printRecItemAdjustment({
                            adjustmentType: 0,
                            description: `${_t("Discount")} ${discount}%`,
                            amount: (
                                ((quantity * l.price_unit_incl) / 100.0) *
                                discount
                            ).toFixed(2),
                            operator: fiscalOperator,
                        });
                    }
                } else {
                    xml += this.printRecRefund({
                        description: `${_t("Refund: ")} ${productName}`,
                        quantity: quantity * -1.0,
                        unitPrice: l.price_unit_incl.toFixed(2),
                        department: l.tax_department.fpdeptax,
                        operator: fiscalOperator,
                    });
                }
            } else {
                xml += this.printRecItemAdjustment({
                    adjustmentType: 3,
                    description: productName,
                    department: l.tax_department.fpdeptax,
                    amount: -l.price_unit_incl.toFixed(2),
                    operator: fiscalOperator,
                });
            }
        });

        // Append fiscal receipt footer
        xml += this.printFiscalReceiptFooter(receipt);

        // Handle lottery code if present
        if (receipt.lottery_code) {
            xml += `<directIO command="1135" data="01${receipt.lottery_code.padEnd(16, " ")}0000" />`;
        }

        // Process payment lines

        // Gestione arrotondamento pagamenti
        // Viene aggiunta una riga di pagamento con payment method type a 6
        // Use proper floating point comparison with 2 decimal precision
        const amountTotal = Math.round(receipt.amount_total * 100) / 100;
        const amountPaid = Math.round(receipt.amount_paid * 100) / 100;

        if (amountTotal !== amountPaid) {
            let payment_round = 0;
            if (amountPaid < amountTotal) {
                const rounding = this.pos.currency.rounding;
                payment_round = round_pr(amountTotal - amountPaid, rounding);
                xml += this.printRecTotal({
                    payment: Math.abs(payment_round),
                    paymentType: "6",
                    operator: fiscalOperator,
                    description: _t("Rounding Payment"),
                });
            }
        }

        if (hasRefund) {
            xml += this.printRecTotalRefund({});
        } else {
            receipt.payment_ids.forEach((l) => {
                // Skip if no payment data
                if (!l) return;

                xml += this.printRecTotal({
                    payment: l.amount.toFixed(2),
                    paymentType: l.payment_method_id.fiscalprinter_payment_type,
                    paymentIndex: l.payment_method_id.fiscalprinter_payment_index,
                    description: l.payment_method_id.name,
                    operator: fiscalOperator,
                });
            });
        }

        xml += this.printOrderId(receipt);

        xml += `<endFiscalReceipt operator="${fiscalOperator}" /></printerFiscalReceipt>`;

        this.order.fp_xml = xml;
        if (odoo.debug) {
            // eslint-disable-next-line no-undef
            console.log("Fiscal Printer XML:", xml);
        }
        this.fiscalPrinter.send(this.url, xml, 0, "sync");
        // Debug: xml
    }

    // Helper methods like printFiscalReceiptHeader, printFiscalVoidDetails, etc.
    printFiscalReceiptHeader(receipt) {
        let msg = "";

        // Check if the receipt header is not empty
        if (receipt.header && receipt.header.length > 0) {
            const hdr = receipt.header.split(/\r\n|\r|\n/);

            // Map each line of the header to the XML message string
            msg = hdr
                .map(
                    (m, i) =>
                        `<printRecMessage
                    messageType="1"
                    message="${this.encodeXml(m)}"
                    font="1"
                    index="${i + 1}"
                    operator="${receipt.fiscal_operator_number || "1"}" />`
                )
                .join(""); // Join the array of strings into one string
        }

        return msg;
    }

    printFiscalVoidDetails(args) {
        var message =
            "VOID " +
            this.addPadding(args.refund_report) +
            " " +
            this.addPadding(args.refund_doc_num) +
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
    }

    printFiscalRefundDetails(args) {
        const message =
            "REFUND " +
            this.addPadding(args.refund_report) +
            " " +
            this.addPadding(args.refund_doc_num) +
            " " +
            // Day
            args.refund_date.substr(8, 2) +
            // Month
            args.refund_date.substr(5, 2) +
            // Year
            args.refund_date.substr(0, 4) +
            " " +
            args.refund_cash_fiscal_serial;

        const tag = `<printRecMessage
                messageType="4"
                message="${this.encodeXml(message)}"
                font="1"
                index="1"
                operator="${args.operator || "1"}"
            />`;

        return tag;
    }

    printRecItem(args) {
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
    }

    printRecItemAdjustment(args) {
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
    }

    printRecTotal(args) {
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
    }

    printRecTotalRefund(args) {
        var tag =
            "<printRecTotal" + ' operator="' + (args.operator || "1") + '"' + " />";
        return tag;
    }

    /*
    Prints a sale refund item line.
    Prints refund items on a commercial refund document if flag SET 14/58 = 1 (from display 3333 > 14 > 58 > X).
    */
    printRecRefund(args) {
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
    }

    printFiscalReceiptFooter(receipt) {
        let msg = "";

        // Check if the receipt header is not empty
        if (receipt.footer && receipt.footer.length > 0) {
            const hdr = receipt.footer.split(/\r\n|\r|\n/);

            // Map each line of the header to the XML message string
            msg = hdr
                .map(
                    (m, i) =>
                        `<printRecMessage
                    messageType="3"
                    message="${this.encodeXml(m)}"
                    font="1"
                    index="${i + 1}"
                    operator="${receipt.fiscal_operator_number || "1"}" />`
                )
                .join(""); // Join the array of strings into one string
        }

        return msg;
    }

    printDisplayText(msg) {
        var xml =
            "<printerCommand>" +
            "<displayText " +
            ' operator="1" text="' +
            this.encodeXml(msg || "") +
            '"' +
            " /></printerCommand>";
        this.fiscalPrinter.send(this.url, xml);
    }

    printOrderId(receipt) {
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
    }

    /*
    It prints report and fiscal closure both
    */
    printFiscalZReport(fiscal_op) {
        var xml = "<printerFiscalReport>";
        xml +=
            '<displayText operator="' +
            fiscal_op +
            '" data="Stampa chiusura giornaliera" />';
        xml += '<printZReport operator="' + fiscal_op + '" timeout="" />';
        xml += "</printerFiscalReport>";
        this.fiscalPrinter.send(this.url, xml);
    }

    /*
    It prints financial report X without fiscal closure
    */
    printFiscalXReport(fiscal_op) {
        var xml = "<printerFiscalReport>";
        xml +=
            '<displayText operator="' +
            fiscal_op +
            '" data="Stampa rapporto finanziario" />';
        xml += '<printXReport operator="' + fiscal_op + '" timeout="" />';
        xml += "</printerFiscalReport>";
        this.fiscalPrinter.send(this.url, xml);
    }

    printOpenCashDrawer() {
        var xml = "<printerCommand>";
        xml += '<openDrawer operator="1"/>';
        xml += "</printerCommand>";
        this.fiscalPrinter.send(this.url, xml);
    }

    resetPrinter() {
        var xml = "<printerCommand>";
        xml += '<displayText operator="" data="Welcome" />';
        xml += '<resetPrinter operator="1" />';
        xml += "</printerCommand>";
        this.fiscalPrinter.send(this.url, xml);
    }

    decodeFpStatus(printerStatus) {
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

    isErrorStatus(printerStatus) {
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
}
