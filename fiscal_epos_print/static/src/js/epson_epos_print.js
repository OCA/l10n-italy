/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { roundPrecision as round_pr } from "@web/core/utils/numbers";

export class EpsonEposPrint {
    constructor(...args) {
        this.setup(...args);
    }
    setup(options, sender) {
        this.url = "http://192.168.1.1/cgi-bin/fpmate.cgi"; // default value, see options
        this.order = null;
        this.pos = sender.pos;
        this.sender = sender;

        // Initialize the fiscal printer
        this.fiscalPrinter = new epson.fiscalPrint();
        this.fiscalPrinter.onreceive = this.onReceive.bind(this);
        this.fiscalPrinter.onerror = this.onError.bind(this);
        this.popup = sender.popup;

        if (options) {
            this.url = options.url || this.url;
            this.order = options.order || null;
        }
    }

    // Method to handle successful receipt
    onReceive(res, tagListNames, addInfo) {
        let tagStatus = tagListNames ? tagListNames.filter(this.getStatusField) : [];
        let msgPrinter = "";
        let info = "";

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
                // Save the order
                // this.pos.push_single_order(order);
            }

            if (tagStatus.length > 0) {
                info = addInfo[tagStatus[0]];
                msgPrinter = this.decodeFpStatus(info);
            }

            this.popup.add(ErrorPopup, {
                title: _t("Connection to the printer failed"),
                body: `${_t("An error happened while sending data to the printer. Error code: ")} ${res.code || ""}\n${_t("Error Message: ")}${msgPrinter}`,
            });
            return;
        }

        // Additional logic for handling responseCommand or receipt data
        if (addInfo.responseCommand === "1138") {
            const toBeSent = addInfo.responseData.slice(9, 13).join("");
            const old = addInfo.responseData.slice(13, 17).join("");
            const rejected = addInfo.responseData.slice(17, 21).join("");
            const msg = `${_t("Files waiting to be sent: ")}${toBeSent}; ${_t("Old files: ")}${old}; ${_t("Rejected files: ")}${rejected}`;
            
            this.popup.add(ErrorPopup, {
                title: _t("IRA files"),
                body: msg,
            });
            return;
        }

        if (addInfo.fiscalReceiptNumber && addInfo.fiscalReceiptAmount && addInfo.fiscalReceiptDate && addInfo.zRepNumber) {
            // Process fiscal receipt details
            order = this.order;
            order._printed = true;

            if (!order.fiscal_receipt_number) {
                order.fiscal_receipt_number = parseInt(addInfo.fiscalReceiptNumber, 10);
                order.fiscal_receipt_amount = parseFloat(addInfo.fiscalReceiptAmount.replace(",", "."));
                const fiscalReceiptDate = new Date(addInfo.fiscalReceiptDate.replace(/(\d{1,2})\/(\d{1,2})\/(\d{4})/, "$3/$2/$1"));
                order.fiscal_receipt_date = moment(fiscalReceiptDate).format("YYYY-MM-DD");
                order.fiscal_z_rep_number = addInfo.zRepNumber;
                order.fiscal_printer_serial = this.pos.config.fiscal_printer_serial;

                // Save the order
                // this.pos.push_single_order(order);
            }

            if (this.pos.config.fiscal_cashdrawer) {
                this.printOpenCashDrawer();
                this.resetPrinter();
            }

            if (!this.pos.config.show_receipt_when_printing) {
                // Navigate to the next screen
                // this.env.chrome.screens['receipt'].click_next();
            }
            return;
        }
    }

    // Method to handle errors
    onError() {
        this.popup.add(ErrorPopup, {
            title: _t("Network error"),
            body: _t("Printer can not be reached"),
        });
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

    printRecItem(args) {
        const tag = `<printRecItem description="${this.encodeXml(args.description || "")}" quantity="${args.quantity || "1"}" unitPrice="${args.unitPrice || ""}" department="${args.department || "1"}" justification="${args.justification || "1"}" operator="${args.operator || "1"}" />`;
        return tag;
    }

    printFiscalReceipt(receipt) {
        //const hasRefund = receipt.orderlines.every((line) => line.quantity < 0);
        let xml = "<printerFiscalReceipt>";
        const fiscalOperator = receipt.fiscal_operator_number || "1";

        // Header should be printed before the fiscal receipt starts
        if (!receipt.refund_full_refund) {
            xml += this.printFiscalReceiptHeader(receipt);
        }

        // TODO
        // If the receipt has refund
        // if (hasRefund) {
        //     xml += receipt.refund_full_refund
        //         ? this.printFiscalVoidDetails({
        //               refund_date: receipt.refund_date,
        //               refund_report: receipt.refund_report,
        //               refund_doc_num: receipt.refund_doc_num,
        //               refund_cash_fiscal_serial: receipt.refund_cash_fiscal_serial,
        //               operator: fiscalOperator,
        //           })
        //         : this.printFiscalRefundDetails({
        //               refund_date: receipt.refund_date,
        //               refund_report: receipt.refund_report,
        //               refund_doc_num: receipt.refund_doc_num,
        //               refund_cash_fiscal_serial: receipt.refund_cash_fiscal_serial,
        //               operator: fiscalOperator,
        //           });
        // }

        xml += `<beginFiscalReceipt operator="${fiscalOperator}" />`;

        // Iterate through each order line
        receipt.lines.forEach((l_tup) => {
            let l = l_tup[2];
            if (l.price_unit_incl >= 0) {
                if (l.qty >= 0 && l.discount < 100) {
                    xml += this.printRecItem({
                        description: l.product_name,
                        quantity: l.qty,
                        unitPrice: round_pr(l.price_unit_incl, this.pos.currency.rounding),
                        department: l.tax_department.code,
                        operator: fiscalOperator,
                    });

                    if (l.discount) {
                        xml += this.printRecItemAdjustment({
                            adjustmentType: 0,
                            description: `${_t("Discount")} ${l.discount}%`,
                            amount: round_pr(
                                l.qty * l.price_unit_incl - l.price_display,
                                this.pos.currency.rounding
                            ),
                            operator: fiscalOperator,
                        });
                    }
                }
                // TODO
                // else {
                //     xml += this.printRecRefund({
                //         description: `${_t("Refund: ")} ${l.product_name}`,
                //         quantity: l.quantity * -1.0,
                //         unitPrice: round_pr(l.price, this.pos.currency.rounding),
                //         department: l.tax_department.code,
                //         operator: fiscalOperator,
                //     });
                // }
            } else {
                xml += this.printRecItemAdjustment({
                    adjustmentType: 3,
                    description: l.product_name,
                    department: l.tax_department.code,
                    amount: -l.price_subtotal_incl,
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

        // TODO
        // // Handle rounding
        // if (receipt.rounding_applied !== 0 && !hasRefund) {
        //     xml += this.printRounding({
        //         amount: Math.abs(
        //             round_pr(receipt.rounding_applied, this.pos.currency.rounding)
        //         ),
        //         operator: fiscalOperator,
        //     });
        //     xml += `<printRecSubtotal operator="${fiscalOperator}" option="1" />`; // funziona?
        // }

        // Process payment lines
        //receipt.ticket = "";
        receipt.statement_ids.forEach((st) => {
            let l = st[2];
            // vedi modulo fiscal_epos_print_meal_voucher
            //receipt.ticket += l.ticket;  // Append ticket to receipt

            // TODO
            //const method = hasRefund ? "printRecTotalRefund" : "printRecTotal";
            xml += this.printRecTotal({
                payment: Math.abs(l.amount),
                paymentType: l.fiscalprinter_payment_type,
                paymentIndex: l.fiscalprinter_payment_index,
                description: l.payment_method_name,
                operator: fiscalOperator,
            });
        });

        // ?
        //xml += this.printOrderId(receipt);

        // if (receipt.ticket) {
        //     xml += this.printInfoPaymentCustomer(receipt);
        // }

        xml += `<endFiscalReceipt operator="${fiscalOperator}" /></printerFiscalReceipt>`;

        this.fiscalPrinter.send(this.url, xml);
        console.log(xml);
    }

    // Helper methods like printFiscalReceiptHeader, printFiscalVoidDetails, etc.
    printFiscalReceiptHeader(receipt) {
        let msg = "";
    
        // Check if the receipt header is not empty
        if (receipt.header && receipt.header.length > 0) {
            const hdr = receipt.header.split(/\r\n|\r|\n/);
            
            // Map each line of the header to the XML message string
            msg = hdr.map((m, i) => 
                `<printRecMessage 
                    messageType="1" 
                    message="${this.encodeXml(m)}" 
                    font="1" 
                    index="${i + 1}" 
                    operator="${receipt.fiscal_operator_number || "1"}" />`
            ).join("");  // Join the array of strings into one string
        }
        
        return msg;
    }

    printFiscalVoidDetails(details) {
        // Implement the logic for printing void details
    }

    printFiscalRefundDetails(args) {
        const message = 
            "REFUND " +
            this.addPadding(args.refund_report) + " " +
            this.addPadding(args.refund_doc_num) + " " +
            // Day
            args.refund_date.substr(8, 2) + 
            // Month
            args.refund_date.substr(5, 2) + 
            // Year
            args.refund_date.substr(0, 4) + " " +
            args.refund_cash_fiscal_serial;
    
        const tag =
            `<printRecMessage 
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
        // Implement the logic for printing a receipt item adjustment
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

    printRecRefund(args) {
        // Implement the logic for printing refund receipt items
    }

    printRounding(args) {
        // Implement rounding print logic
    }

    printFiscalReceiptFooter(receipt) {
        let msg = "";
    
        // Check if the receipt header is not empty
        if (receipt.footer && receipt.footer.length > 0) {
            const hdr = receipt.footer.split(/\r\n|\r|\n/);
            
            // Map each line of the header to the XML message string
            msg = hdr.map((m, i) => 
                `<printRecMessage 
                    messageType="3" 
                    message="${this.encodeXml(m)}" 
                    font="1" 
                    index="${i + 1}" 
                    operator="${receipt.fiscal_operator_number || "1"}" />`
            ).join("");  // Join the array of strings into one string
        }
        
        return msg;
    }

    printDisplayText(msg) {
        var xml = '<printerCommand>'
            + '<displayText '
            + ' operator="1" text="' + this.encodeXml(msg || '') + '"'
            + ' /></printerCommand>';
        this.fiscalPrinter.send(this.url, xml);
    }

    printOrderId(receipt) {
        // Implement the logic for printing the order ID
    }

    printInfoPaymentCustomer(receipt) {
        // Implement the logic for printing payment info for customer
    }

}
