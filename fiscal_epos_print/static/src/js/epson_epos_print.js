odoo.define("fiscal_epos_print.epson_epos_print", function (require) {
    "use strict";

    var core = require("web.core");
    var utils = require('web.utils');
    var PosDB = require('point_of_sale.DB');
    var rpc = require('web.rpc');
    var _t = core._t;
    var round_pr = utils.round_precision;

    function addPadding(str, padding=4) {
        var pad = new Array(padding).fill(0).join('') + str;
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
                //receipt = "Fiscale/Non fiscale chiuso";
                break;
            case "2":
                receipt = _t("Non fiscal open");
                break;
            case "3":
                receipt = _t("Payment in progress");
                break;
            case "4":
                receipt = _t("Error on last ESC/POS command with Fiscal/Non fiscal closed");
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

    function getStatusField(tag){
        return tag === 'printerStatus' || tag === 'fsStatus';
    }

    var eposDriver = core.Class.extend({
        init: function(options, sender) {
            var self = this;
            options = options || {};
            this.url = options.url || 'http://192.168.1.1/cgi-bin/fpmate.cgi';
            this.fiscalPrinter = new epson.fiscalPrint();
            this.sender = sender;
            this.order = options.order || null;
            this.fiscalPrinter.onreceive = function(res, tag_list_names, add_info) {
                sender.chrome.loading_hide();
                var tagStatus = (tag_list_names ? tag_list_names.filter(getStatusField) : []);
                var msgPrinter = "";

                if (tagStatus.length > 0 && res.success) {
                    var info = add_info[tagStatus[0]];
                    res.success = !isErrorStatus(info);
                }

                if (!res.success) {
                    if (self.order != null) {
                        var order = self.order;
                        order.fiscal_printer_debug_info = JSON.stringify(res) + '\n' + JSON.stringify(tag_list_names) + '\n' + JSON.stringify(add_info);
                        sender.pos.push_order(order);
                    }
                    if (tagStatus.length > 0) {
                        var info = add_info[tagStatus[0]];
                        var msgPrinter = decodeFpStatus(info);
                    }
                    sender.chrome.screens['receipt'].lock_screen(true);
                    sender.pos.gui.show_popup('error', {
                        'title': _t('Connection to the printer failed'),
                        'body': _t('An error happened while sending data to the printer. Error code: ') + (res.code || '') + '\n' + _t('Error Message: ') + msgPrinter,
                    });
                    return;
                }

                if (add_info.responseCommand == "1138") {
                    // coming from FiscalPrinterADEFilesButtonWidget
                    var to_be_sent = add_info.responseData[9] + add_info.responseData[10] + add_info.responseData[11] + add_info.responseData[12];
                    var old = add_info.responseData[13] + add_info.responseData[14] + add_info.responseData[15] + add_info.responseData[16];
                    var rejected = add_info.responseData[17] + add_info.responseData[18] + add_info.responseData[19] + add_info.responseData[20];
                    var msg = _t("Files waiting to be sent: ") + to_be_sent + "; " + _t("Old files: ") + old + "; " + _t("Rejected files: ") + rejected;
                    sender.pos.gui.show_popup('alert', {
                        'title': _t('IRA files'),
                        'body': msg,
                    });
                    return;
                }

                // is it a receipt data?
                if (add_info.fiscalReceiptNumber && add_info.fiscalReceiptAmount && add_info.fiscalReceiptDate && add_info.zRepNumber) {
                    sender.chrome.screens['receipt'].lock_screen(false);
                    var order = self.order;
                    order._printed = true;
                    if (!order.fiscal_receipt_number) {
                        order.fiscal_receipt_number = parseInt(add_info.fiscalReceiptNumber);
                        order.fiscal_receipt_amount = parseFloat(add_info.fiscalReceiptAmount.replace(',', '.'));
                        var fiscalReceiptDate = new Date(add_info.fiscalReceiptDate.replace(/(\d{1,2})\/(\d{1,2})\/(\d{4})/, '$3/$2/$1'));
                        order.fiscal_receipt_date = moment(fiscalReceiptDate).format('YYYY-MM-DD');
                        order.fiscal_z_rep_number = add_info.zRepNumber;
                        order.fiscal_printer_serial = sender.pos.config.fiscal_printer_serial;
                        sender.pos.db.add_order(order.export_as_JSON());
                        // try to save the order
                        sender.pos.push_order();
                    }
                    if(sender.pos.config.fiscal_cashdrawer)
                    {
                        self.printOpenCashDrawer();
                    }
                    if (!sender.pos.config.show_receipt_when_printing) {
                        sender.chrome.screens['receipt'].click_next();
                    }
                    return;
                }
            }
            this.fiscalPrinter.onerror = function() {
                sender.chrome.loading_hide();
                sender.chrome.screens['receipt'].lock_screen(true);
                sender.pos.gui.show_popup('error', {
                    'title': _t('Network error'),
                    'body': _t('Printer can not be reached')
                });
            }
        },

        encodeXml: function (string) {
            var xml_special_to_escaped_one_map = {
                '&': '&amp;',
                '"': '&quot;',
                '<': '&lt;',
                '>': '&gt;'
            };

            return string.replace(/([\&"<>])/g, function(str, item) {
                return xml_special_to_escaped_one_map[item];
            });
        },

        /*
          Prints a sale item line.
        */
        printRecItem: function(args) {
            var tag = '<printRecItem'
                + ' description="' + this.encodeXml(args.description || '') + '"'
                + ' quantity="' + (args.quantity || '1') + '"'
                + ' unitPrice="' + (args.unitPrice || '') + '"'
                + ' department="' + (args.department || '1') + '"'
                + ' justification="' + (args.justification || '1') + '"'
                + ' operator="' + (args.operator || '1') + '"'
                + ' />';
            return tag;
        },

        /*
          Prints a sale refund item line.
        */
        printFiscalRefundDetails: function(args) {
            var message = 'REFUND ' +
                addPadding(args.refund_report) + ' ' +
                addPadding(args.refund_doc_num) + ' ' +
                args.refund_date.substr(8, 2) + // day
                args.refund_date.substr(5, 2) + // month
                args.refund_date.substr(0, 4) + // year
                ' ' + args.refund_cash_fiscal_serial;

            var tag = '<printRecMessage'
                + ' messageType="4" message="' + this.encodeXml(message) + '" font="1" index="1"'
                + ' operator="' + (args.operator || '1') + '"'
                + ' />\n';
            return tag;
        },

        /*
          Prints a sale refund item line.
        */
        printRecRefund: function(args) {
            var tag = '<printRecRefund'
                + ' description="' + this.encodeXml(args.description || '') + '"'
                + ' quantity="' + (args.quantity || '1') + '"'
                + ' unitPrice="' + (args.unitPrice || '') + '"'
                + ' department="' + (args.department || '1') + '"'
                + ' justification="' + (args.justification || '1') + '"'
                + ' operator="' + (args.operator || '1') + '"'
                + ' />';
            return tag;
        },

        /*
          Adds a discount to the last line.
        */
        printRecItemAdjustment: function(args) {
            var tag = '<printRecItemAdjustment'
                + ' operator="' + (args.operator || '1') + '"'
                + ' adjustmentType="' + (args.adjustmentType || 0) + '"'
                + ' description="' + this.encodeXml(args.description || '' ) + '"'
                + ' amount="' + (args.amount || '') + '"'
                + ' department="' + (args.department || '') + '"'
                + ' justification="' + (args.justification || '2') + '"'
                + ' />';
            return tag;
        },

        /*
          Prints a payment.
        */
        printRecTotal: function(args) {
            var tag = '<printRecTotal'
                + ' operator="' + (args.operator || '1') + '"'
                + ' description="' + this.encodeXml(args.description || _t('Payment')) + '"'
                + ' payment="' + (args.payment || '') + '"'
                + ' paymentType="' + (args.paymentType || '0') + '"'
                + ' index="' + (args.paymentIndex || '0') + '"'
                + ' />';
            return tag;
        },

        printRecTotalRefund: function(args) {
            var tag = '<printRecTotal'
                + ' operator="' + (args.operator || '1') + '"'
                + ' />';
            return tag;
        },

        // Remember that the header goes after <printerFiscalReceipt>
        // but before <beginFiscalReceipt /> otherwise it will not be printed
        // as additional header messageType=1
        printFiscalReceiptHeader: function(receipt){
            var self = this;
            var msg = '';
            if (receipt.header != '' && receipt.header.length > 0) {
                var hdr = receipt.header.split(/\r\n|\r|\n/);
                _.each(hdr, function(m, i) {
                    msg += '<printRecMessage' + ' messageType="1" message="' + self.encodeXml(m)
                         + '" font="1" index="' + (i+1) + '"'
                         + ' operator="' + (receipt.operator || '1') + '" />'
                    });
            }
            return msg;
        },

        // Remember that the footer goes within <printerFiscalReceipt><beginFiscalReceipt />
        // as PROMO code messageType=3
        printFiscalReceiptFooter: function(receipt){
            var self = this;
            var msg = '';
            if (receipt.footer != '' && receipt.footer.length > 0) {
                var hdr = receipt.footer.split(/\r\n|\r|\n/);
                _.each(hdr, function(m, i) {
                    msg += '<printRecMessage' + ' messageType="3" message="' + self.encodeXml(m)
                         + '" font="1" index="' + (i+1) + '"'
                         + ' operator="' + (receipt.operator || '1') + '" />'
                    });
            }
            return msg;
        },

        printDisplayText: function(msg) {
            var xml = '<printerCommand>'
                + '<displayText '
                + ' operator="1" text="' + this.encodeXml(msg || '') + '"'
                + ' /></printerCommand>';
            this.fiscalPrinter.send(this.url, xml);
        },

        /*
          Prints a receipt
        */
        printFiscalReceipt: function(receipt) {
            var self = this;
            var has_refund = _.every(receipt.orderlines, function(line) {
                return line.quantity < 0;
            });
            var xml = '<printerFiscalReceipt>';
            // header must be printed before beginning a fiscal receipt
            xml += this.printFiscalReceiptHeader(receipt);
            if (!has_refund) {
                xml += '<beginFiscalReceipt/>';
            }
            if (has_refund)
            {
                xml += this.printFiscalRefundDetails({
                        refund_date: receipt.refund_date,
                        refund_report: receipt.refund_report,
                        refund_doc_num: receipt.refund_doc_num,
                        refund_cash_fiscal_serial: receipt.refund_cash_fiscal_serial});
            }
            _.each(receipt.orderlines, function(l, i, list) {
                if (l.price >= 0) {
                    if(l.quantity>=0) {
                        xml += self.printRecItem({
                            description: l.product_name,
                            quantity: l.quantity,
                            unitPrice: l.full_price,
                            department: l.tax_department.code
                        });
                        if (l.discount) {
                            xml += self.printRecItemAdjustment({
                                adjustmentType: 0,
                                description: _t('Discount') + ' ' + l.discount + '%',
                                amount: round_pr((l.quantity * l.full_price) - l.price_display, self.sender.pos.currency.rounding),
                            });
                        }
                    }
                    else
                    {
                        xml += self.printRecRefund({
                            description: _t('Refund >>> ') + l.product_name,
                            quantity: l.quantity * -1.0,
                            unitPrice: l.price,
                            department: l.tax_department.code
                        });
                    }
                }
                else {
                    xml += self.printRecItemAdjustment({
                        adjustmentType: 3,
                        description: l.product_name,
                        department: l.tax_department.code,
                        amount: -l.price,
                    });
                }
            });
            // footer can go only as promo code so within a fiscal receipt body
            xml += this.printFiscalReceiptFooter(receipt);
            if (receipt.lottery_code != null) {
                // TX
                // 1 135   OP   ID CODE   NU
                // Example: 113501ABCDEFGN        0000
                // Pad with spaces to make the code field always 16 characters.
                xml += '<directIO command="1135" data="01' + receipt.lottery_code.padEnd(16, ' ') + '0000" />';
            }
            if (has_refund) {
                xml += self.printRecTotalRefund({});
            }
            else {
                _.each(receipt.paymentlines, function(l, i, list) {
                    xml += self.printRecTotal({
                        payment: l.amount,
                        paymentType: l.type,
                        paymentIndex: l.type_index,
                        description: l.journal,
                    });
                });
            }
            xml += '<endFiscalReceipt /></printerFiscalReceipt>';
            this.fiscalPrinter.send(this.url, xml);
            console.log(xml);
        },

        printFiscalReport: function() {
            var xml = '<printerFiscalReport>';
            xml += '<printZReport operator="" />';
            xml += '</printerFiscalReport>';
            this.fiscalPrinter.send(this.url, xml);
        },

        printFiscalXReport: function() {
            var xml = '<printerFiscalReport>';
            xml += '<printXReport operator="" />';
            xml += '</printerFiscalReport>';
            this.fiscalPrinter.send(this.url, xml);
        },

        getStatusOfFilesForADE: function() {
            var xml = '<printerCommand>';
            xml += '<directIO command="1138" data="01" />';
            xml += '</printerCommand>';
            this.fiscalPrinter.send(this.url, xml);
        },

        printFiscalReprintLast: function() {
            var xml = '<printerCommand>';
            xml += '<printDuplicateReceipt operator="1" />';
            xml += '</printerCommand>';
            this.fiscalPrinter.send(this.url, xml);
        },

        printOpenCashDrawer: function() {
            var xml = '<printerCommand>';
            xml += '<openDrawer operator="1"/>';
            xml += '</printerCommand>';
            this.fiscalPrinter.send(this.url, xml);
        },

    });

    return {
        eposDriver: eposDriver
    }

});
