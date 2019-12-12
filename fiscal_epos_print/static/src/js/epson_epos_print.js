odoo.define("fiscal_epos_print.epson_epos_print", function (require) {
    "use strict";

    var core = require("web.core");
    var utils = require('web.utils');
    var _t = core._t;
    var round_pr = utils.round_precision;

    function addPadding(str, padding=4) {
        var pad = new Array(padding).fill(0).join('') + str;
        return pad.substr(pad.length - padding, padding);
    }

    var eposDriver = core.Class.extend({
        init: function(options, sender) {
            options = options || {};
            this.url = options.url || 'http://192.168.1.1/cgi-bin/fpmate.cgi';
            this.fiscalPrinter = new epson.fiscalPrint();
            this.fpreponse = false;
            this.sender = sender;
            this.fiscalPrinter.onreceive = function(res, tag_list_names, add_info) {
                this.fpreponse = tag_list_names
                if (res['code'] == "EPTR_REC_EMPTY"){
                    sender.chrome.loading_hide();
                    alert(_t("Error missing paper."));
                }
                if (add_info.responseCommand == "1138") {
                    // coming from FiscalPrinterADEFilesButtonWidget
                    sender.chrome.loading_hide();
                    var to_be_sent = add_info.responseData[9] + add_info.responseData[10] + add_info.responseData[11] + add_info.responseData[12];
                    var old = add_info.responseData[13] + add_info.responseData[14] + add_info.responseData[15] + add_info.responseData[16];
                    var rejected = add_info.responseData[17] + add_info.responseData[18] + add_info.responseData[19] + add_info.responseData[20];
                    var msg = _t("Files waiting to be sent: ") + to_be_sent + _t("\nOld files: ") + old + _t("\nRejected files: ") + rejected
                    alert(msg);
                }
            }
            this.fiscalPrinter.onerror = function() {
                sender.chrome.loading_hide();
                alert(
                _t('Network error. Printer can not be reached')
                );
            }
        },

        /*
          Prints a sale item line.
        */
        printRecItem: function(args) {
            var tag = '<printRecItem'
                + ' description="' + (args.description || '') + '"'
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
        printRecRefund: function(args) {
            var message = 'REFUND ' +
                addPadding(args.refund_report) + ' ' +
                addPadding(args.refund_doc_num) + ' ' +
                args.refund_date + ' ' +
                args.refund_cash_fiscal_serial;

            var tag = '<printRecMessage'
                + ' messageType="4" message="' + message + '" font="1" index="1"'
                + ' operator="' + (args.operator || '1') + '"'
                + ' />\n'
                + '<printRecRefund'
                + ' description="' + (args.description || '') + '"'
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
                + ' description="' + (args.description || '' ) + '"'
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
                + ' description="' + (args.description || _t('Payment')) + '"'
                + ' payment="' + (args.payment || '') + '"'
                + ' paymentType="' + (args.paymentType || '0') + '"'
                + ' index="' + (args.paymentIndex || '0') + '"'
                + ' />';
            return tag;
        },

        // Remember that the header goes after <printerFiscalReceipt>
        // but before <beginFiscalReceipt /> otherwise it will not be printed
        // as additional header messageType=1
        printFiscalReceiptHeader: function(receipt){
            var msg = '';
            if (receipt.header != '' && receipt.header.length > 0) {
                var hdr = receipt.header.split(/\r\n|\r|\n/);
                _.each(hdr, function(m, i) {
                    msg += '<printRecMessage' + ' messageType="1" message="' + m
                         + '" font="1" index="' + (i+1) + '"'
                         + ' operator="' + (receipt.operator || '1') + '" />'
                    });
            }
            return msg;
        },

        // Remember that the footer goes within <printerFiscalReceipt><beginFiscalReceipt />
        // as PROMO code messageType=3
        printFiscalReceiptFooter: function(receipt){
            var msg = '';
            if (receipt.footer != '' && receipt.footer.length > 0) {
                var hdr = receipt.footer.split(/\r\n|\r|\n/);
                _.each(hdr, function(m, i) {
                    msg += '<printRecMessage' + ' messageType="3" message="' + m
                         + '" font="1" index="' + (i+1) + '"'
                         + ' operator="' + (receipt.operator || '1') + '" />'
                    });
            }
            return msg;
        },

        /*
          Prints a receipt
        */
        printFiscalReceipt: function(receipt) {
            var self = this;
            var xml = '<printerFiscalReceipt>';
            // header must be printed before beginning a fiscal receipt
            xml += this.printFiscalReceiptHeader(receipt);
            xml += '<beginFiscalReceipt />';
            // footer can go only as promo code so within a fiscal receipt body
            xml += this.printFiscalReceiptFooter(receipt);
            _.each(receipt.orderlines, function(l, i, list) {
                if (l.price >= 0) {
                    if(l.quantity>=0) {
                        var full_price = l.price;
                        if (l.discount) {
                            full_price = round_pr(l.price / (1 - (l.discount / 100)), self.sender.pos.currency.rounding);
                        }
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
                                amount: round_pr(l.quantity * full_price - l.price, self.sender.pos.currency.rounding),
                            });
                        }
                    }
                    else
                    {
                        xml += self.printRecRefund({
                            refund_date: receipt.refund_date,
                            refund_report: receipt.refund_report,
                            refund_doc_num: receipt.refund_doc_num,
                            refund_cash_fiscal_serial: receipt.refund_cash_fiscal_serial,
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
            _.each(receipt.paymentlines, function(l, i, list) {
                xml += self.printRecTotal({
                    payment: l.amount,
                    paymentType: l.type,
                    paymentIndex: l.type_index,
                    description: l.journal,
                });
            });
            xml += '<endFiscalReceipt /></printerFiscalReceipt>';
            this.fiscalPrinter.send(this.url, xml);
            console.log(xml);
        },

        printFiscalReport: function() {
            var xml = '<printerFiscalReport>';
            xml += '<displayText operator="1" data="' + _t('Fiscal Closing') + '" />';
            xml += '<printZReport operator="1" />';
            xml += '</printerFiscalReport>';
            this.fiscalPrinter.send(this.url, xml);
        },

        getStatusOfFilesForADE: function() {
            var xml = '<printerCommand>';
            xml += '<directIO command="1138" data="01" />';
            xml += '</printerCommand>';
            this.fiscalPrinter.send(this.url, xml);
        },

    });

    return {
        eposDriver: eposDriver
    }

});
