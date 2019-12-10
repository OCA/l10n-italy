odoo.define("fiscal_epos_print.models", function (require) {
    "use strict";

    var models = require("point_of_sale.models");
    var core = require("web.core");
    var screens = require('point_of_sale.screens');
    var _t = core._t;
    var utils = require('web.utils');
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var chrome = require('point_of_sale.chrome');
    var round_pr = utils.round_precision;
    var pos_order_mgmt = require('pos_order_mgmt.widgets');
    var OrderListScreenWidget = pos_order_mgmt.OrderListScreenWidget;

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
                + ' description="' + (args.description || 'Pagamento') + '"'
                + ' payment="' + (args.payment || '') + '"'
                + ' paymentType="' + (args.paymentType || '0') + '"'
                + ' />';
            return tag;
        },

        /*
          Prints a receipt
        */
        printFiscalReceipt: function(receipt) {
            var self = this;
            var xml = '<printerFiscalReceipt><beginFiscalReceipt />';
            _.each(receipt.orderlines, function(l, i, list) {
                if (l.price >= 0) {
                    xml += self.printRecItem({
                        description: l.product_name,
                        quantity: l.quantity,
                        unitPrice: l.price,
                        department: l.tax_department.code
                    });
                    if (l.discount) {
                        xml += self.printRecItemAdjustment({
                            adjustmentType: 0,
                            description: 'Sconto ' + l.discount + '%',
                            amount: round_pr(l.quantity * l.price - l.price_display, self.sender.pos.currency.rounding),
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
                    description: l.journal,
                });
            });
            xml += '<endFiscalReceipt /></printerFiscalReceipt>';
            this.fiscalPrinter.send(this.url, xml);
            console.log(xml);
        },

        printFiscalReport: function() {
            var xml = '<printerFiscalReport>';
            xml += '<displayText operator="1" data="Chiusura fiscale" />';
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

    var _orderline_super = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        export_for_printing: function(){
            var res = _orderline_super.export_for_printing.call(this, arguments);
            res['tax_department'] = this.get_tax_details_r();
            return res;
        },
        get_tax_details_r: function(){
            var details =  this.get_all_prices();
            for (var i in details.taxDetails){
                return {
                    code: this.pos.taxes_by_id[i].fpdeptax,
                    taxname: this.pos.taxes_by_id[i].name,
                }
            }
            alert(_t("No taxes found"));
        },
        compute_all: function(taxes, price_unit, quantity, currency_rounding, no_map_tax) {
            var res = _orderline_super.compute_all.call(this, taxes, price_unit, quantity, currency_rounding, no_map_tax);
            var self = this;

            var total_excluded = round_pr(price_unit * quantity, currency_rounding);
            var total_included = total_excluded;
            var base = total_excluded;
            var list_taxes = res.taxes;
            // amount_type 'group' not handled (used only for purchases, in Italy)
            _(taxes).each(function(tax) {
                if (!no_map_tax){
                    tax = self._map_tax_fiscal_position(tax);
                }
                if (!tax){
                    return;
                }
                var tax_amount = self._compute_all(tax, base, quantity);
                tax_amount = round_pr(tax_amount, currency_rounding);
                if (!tax_amount){
                    // Intervene here: also add taxes with 0 amount
                    if (tax.price_include) {
                        total_excluded -= tax_amount;
                        base -= tax_amount;
                    }
                    else {
                        total_included += tax_amount;
                    }
                    if (tax.include_base_amount) {
                        base += tax_amount;
                    }
                    var data = {
                        id: tax.id,
                        amount: tax_amount,
                        name: tax.name,
                    };
                    list_taxes.push(data);
                }
            });
            res.taxes = list_taxes;

            return res;
        },
    });

    /*
      Overwrite Paymentline.export_for_printing() in order
      to make it export the payment type that must be passed
      to the fiscal printer.
    */
    var original = models.Paymentline.prototype.export_for_printing;
    models.Paymentline = models.Paymentline.extend({
        export_for_printing: function() {
            var res = original.apply(this, arguments);
            res.type = this.cashregister.journal.fiscalprinter_payment_type;
            return res;
        }
    });

    // when print order i validate call print receipt
    screens.PaymentScreenWidget.include({
        getPrinterOptions: function (){
            var protocol = ((this.pos.config.use_https) ? 'https://' : 'http://');
            var printer_url = protocol + this.pos.config.printer_ip + '/cgi-bin/fpmate.cgi';
            return {url: printer_url};
        },
        sendToPrinter: function(receipt, printer_options) {
            var fp90 = new eposDriver(printer_options, this);
            fp90.printFiscalReceipt(receipt);
        },
        finalize_validation: function() {
            this._super.apply(this, arguments);
            var currentOrder = this.pos.get('selectedOrder');
            if (!currentOrder.is_to_invoice()) {
                var printer_options = this.getPrinterOptions();
                var receipt = currentOrder.export_for_printing();
                this.sendToPrinter(receipt, printer_options);
                this.pos.get('selectedOrder')._printed = true;
            }
        }

    });

    var _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var tax_model = _.find(this.models, function(model){ return model.model === 'account.tax'; });
            tax_model.fields.push('fpdeptax');
            return _super_posmodel.initialize.call(this, session, attributes);
        },
    });

    OrderListScreenWidget.include({
        // copiato da screens.PaymentScreenWidget
        getPrinterOptions: function (){
            var protocol = ((this.pos.config.use_https) ? 'https://' : 'http://');
            var printer_url = protocol + this.pos.config.printer_ip + '/cgi-bin/fpmate.cgi';
            return [{url: printer_url}];
        },
        // copiato da screens.PaymentScreenWidget
        sendToPrinter: function(receipt, printer_options) {
            for (var i = 0; i < printer_options.length; i++){
                var printer_option = printer_options[i];
                var fp90 = new eposDriver(printer_option, this);
                fp90.printFiscalReceipt(receipt);
            }
        },
        action_print: function (order_data, order) {
            var receipt = order.export_for_printing();
            var printer_options = this.getPrinterOptions();
            this.sendToPrinter(receipt, printer_options);
            return this._super(order_data, order);
        },
    });

    var FiscalPrinterADEFilesButtonWidget = PosBaseWidget.extend({
        template: 'FiscalPrinterADEFilesButtonWidget',

        button_click: function () {
            this.chrome.loading_show();
            this.chrome.loading_message(_t('Connecting to the fiscal printer'));
            var protocol = ((this.pos.config.use_https) ? 'https://' : 'http://');
            var printer_url = protocol + this.pos.config.printer_ip + '/cgi-bin/fpmate.cgi';
            var printer_options = {url: printer_url};
            var fp90 = new eposDriver(printer_options, this);
            fp90.getStatusOfFilesForADE();
        },

        renderElement: function () {
            var self = this;
            this._super();
            this.$el.click(function () {
                self.button_click();
            });
        },

    });

    var widgets = chrome.Chrome.prototype.widgets;
    widgets.push({
        'name': 'ADE files status',
        'widget': FiscalPrinterADEFilesButtonWidget,
        'append': '.pos-rightheader',
        'args': {
            'label': 'ADE files status',
        },
    });

    return {
        eposDriver: eposDriver,
        FiscalPrinterADEFilesButtonWidget: FiscalPrinterADEFilesButtonWidget,
    };

});
